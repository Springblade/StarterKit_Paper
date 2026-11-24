"""Expanded development pilot entry point. Default commands never invoke a model.

`run` is gated by a separate author-release record tied to the frozen artifacts.
Rehearsal uses explicit reference patches, no account credentials and no model.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time
from prepare import HERE, runtime, save, digest
from qualify import apply_solution, final

MODEL = 'gpt-6-luna'
CAP = 900


def next_attempt(runs, slot):
    root = runs / slot
    previous = sorted(root.glob('attempt-*/attempt.json')) if root.exists() else []
    if not previous:
        return root / 'attempt-01'
    prior = json.loads(previous[-1].read_text(encoding='utf-8'))
    if prior.get('status') == 'complete':
        return None
    assert previous[-1].parent.name == 'attempt-01', 'At most one replacement per slot'
    assert prior.get('status') in {'infrastructure-interrupted-needs-adjudication', 'execution-error-needs-adjudication'}, 'Scoring must be retried on the same patch without another model call'
    adjudication = json.loads((root / 'adjudication.json').read_text(encoding='utf-8'))
    assert adjudication.get('parent_attempt') == 'attempt-01'
    assert adjudication.get('category') == 'infrastructure-only' and adjudication.get('allow_model_replacement') is True
    assert adjudication.get('reason') and adjudication.get('evidence'), 'A reason and evidence are required'
    assert len(list(runs.glob('*/attempt-02'))) < 6, 'Global six-replacement cap reached'
    assert not (root / 'attempt-02').exists(), 'Retain and adjudicate existing replacement'
    return root / 'attempt-02'


def audit():
    frozen = json.loads((HERE / 'freeze.json').read_text(encoding='utf-8'))
    for filename, value in frozen['files'].items():
        assert digest(HERE / filename) == value, 'Frozen artifact changed: ' + filename
    image = json.loads(runtime.docker('image', 'inspect', runtime.IMAGE).stdout)[0]
    assert image['Id'] == frozen['image_id'], 'Common runtime image changed'
    allocation = json.loads((HERE / 'allocation.json').read_text(encoding='utf-8'))
    assert len(allocation['slots']) <= 28
    assert len({s['slot'] for s in allocation['slots']}) == len(allocation['slots'])
    assert all(s['task'] in ['DP02', 'DP03'] for s in allocation['slots'])
    return frozen, allocation


def capture(name, folder, commit):
    runtime.docker('exec', name, 'git', 'add', '-N', '.')
    (folder / 'patch.diff').write_bytes(runtime.docker('exec', name, 'git', 'diff', '--binary', commit).stdout)
    runtime.docker('exec', name, 'tar', '-czf', '/tmp/final-workspace.tgz',
                   '--exclude=./node_modules', '--exclude=./.next', '--exclude=./.git', '--exclude=./.env',
                   '--exclude=./tsconfig.tsbuildinfo', '-C', '/workspace', '.')
    runtime.docker('cp', name + ':/tmp/final-workspace.tgz', folder / 'final-workspace.tgz')
    output = folder / 'final-workspace'
    output.mkdir()
    with tarfile.open(folder / 'final-workspace.tgz') as archive:
        archive.extractall(output, filter='data')
    (output / '.env').write_text(runtime.env_text(), encoding='utf-8')
    return output


def score(package, task, name, folder):
    folder.mkdir(parents=True)
    started = time.monotonic()
    try:
        runtime.start(name, package, folder)
        runtime.docker('exec', name, 'mkdir', '-p', '/evaluator')
        # No account-auth material is ever copied into this scoring container.
        result = final(name, task, folder)
        result['scoring_seconds_including_setup'] = time.monotonic() - started
        save(folder / 'outcome.json', result)
        return result
    finally:
        runtime.stop(name, folder)


def rehearse():
    # Qualification artifact, never a pilot observation.
    ledger_path = HERE / 'rehearsal' / 'ledger.json'
    ledger_path.parent.mkdir(exist_ok=True)
    ledger = json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else {}
    for task in ['DP02', 'DP03']:
        for cell in ['S0V0', 'S0V1', 'S1V0', 'S1V1']:
            key = task + '/' + cell
            binding = {'final_check_sha256': digest(HERE / 'final-check.cjs'),
                       'package_manifest_sha256': digest(HERE / 'packages' / task / (cell + '-manifest.json'))}
            if ledger.get(key, {}).get('passed') and all(ledger[key].get(k) == v for k, v in binding.items()):
                continue
            folder = HERE / 'rehearsal' / task / cell
            if folder.exists():
                folder = folder.with_name(folder.name + '-' + str(time.time_ns()))
            folder.mkdir(parents=True)
            name = 'smartkit-dry-' + task.lower() + '-' + cell.lower()
            try:
                head = runtime.start(name, HERE / 'packages' / task / cell, folder)
                probe = "const f=require('fs');for(const p of ['/opt/codex-home/auth.json','/root/.codex/auth.json','/evaluator','/research','/workspace/solutions'])if(f.existsSync(p))process.exit(1);"
                runtime.docker('exec', name, 'node', '-e', probe)
                apply_solution(name, task, 'feature' if cell[1] == '1' else 'layered', 'reference')
                package = capture(name, folder, head)
            finally:
                runtime.stop(name, folder)
            result = score(package, task, name + '-score', folder / 'evaluation')
            assert result.get('completed') and result.get('jointSuccess'), result
            summary = {'passed': True, 'task': task, 'cell': cell,
                 'kind': 'reference-pipeline-rehearsal-no-model', 'account_credentials_supplied': False, **binding}
            save(folder / 'summary.json', summary)
            ledger[key] = {**summary, 'folder': folder.relative_to(HERE).as_posix()}
            save(ledger_path, ledger)
            print('Rehearsal passed: ' + task + '/' + cell, flush=True)


def run():
    frozen, allocation = audit()
    release = json.loads((HERE / 'author-pilot-release.json').read_text(encoding='utf-8'))
    assert release.get('approved') is True and release.get('freeze_sha256') == digest(HERE / 'freeze.json'), 'Author pilot release missing or stale'
    auth_path = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'auth.json'
    account = json.loads(auth_path.read_text(encoding='utf-8'))
    assert account.get('auth_mode') == 'chatgpt' and not account.get('OPENAI_API_KEY'), 'Existing ChatGPT allowance only'
    runs = HERE / 'runs'
    for slot in allocation['slots']:
        task, cell = slot['task'], slot['cell']
        folder = next_attempt(runs, slot['slot'])
        if folder is None:
            continue
        folder.mkdir(parents=True)
        name = 'smartkit-trial-' + slot['slot'].lower()
        attempt = {'slot': slot, 'attempt_id': folder.name, 'parent_attempt_id': 'attempt-01' if folder.name == 'attempt-02' else None,
                   'configuration': frozen['configuration'], 'status': 'preparing', 'started': runtime.stamp()}
        save(folder / 'attempt.json', attempt)
        try:
            head = runtime.start(name, HERE / 'packages' / task / cell, folder)
            runtime.docker('exec', name, 'mkdir', '-p', '/opt/codex-home')
            runtime.docker('cp', auth_path, name + ':/opt/codex-home/auth.json')
            status = runtime.docker('exec', name, 'codex', 'login', 'status').stdout.decode()
            assert 'ChatGPT' in status, 'ChatGPT authentication unavailable'
            command = ['docker', 'exec', name, 'codex', 'exec', '--ignore-user-config', '--ignore-rules',
                       '--ephemeral', '--dangerously-bypass-approvals-and-sandbox', '-m', MODEL,
                       '-c', 'model_reasoning_effort="high"', '--json', '--output-last-message', '/tmp/final-message.txt',
                       'Read TASK.md and implement its requirement. Use available checks as appropriate.']
            attempt.update(status='running', model_started=runtime.stamp())
            save(folder / 'attempt.json', attempt)
            began = time.monotonic()
            timeout = False
            with (folder / 'events.jsonl').open('wb') as stream:
                process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                while process.poll() is None:
                    if time.monotonic() - began >= CAP:
                        timeout = True
                        runtime.docker('exec', name, 'pkill', '-f', 'codex', check=False)
                        process.kill(); process.wait(); break
                    time.sleep(.5)
            events = []
            for line in (folder / 'events.jsonl').read_text(encoding='utf-8', errors='replace').splitlines():
                try:
                    events.append(json.loads(line))
                except ValueError:
                    pass
            completed = [e for e in events if e.get('type') == 'turn.completed']
            attempt.update(elapsed_seconds=time.monotonic() - began, timeout=timeout,
                           returncode=process.returncode, model_finished=runtime.stamp(),
                           completed_turns=len(completed), usage_events=[e.get('usage') for e in completed])
            runtime.docker('cp', name + ':/tmp/final-message.txt', folder / 'final-message.txt', check=False)
            package = capture(name, folder, head)
            attempt['status'] = 'awaiting-scoring' if timeout or (completed and process.returncode == 0) else 'infrastructure-interrupted-needs-adjudication'
            save(folder / 'attempt.json', attempt)
        except Exception as error:
            attempt.update(status='execution-error-needs-adjudication', error_class=type(error).__name__)
            save(folder / 'attempt.json', attempt)
            raise
        finally:
            runtime.stop(name, folder)
        if attempt['status'] != 'awaiting-scoring':
            raise RuntimeError('Preserved interrupted model attempt; adjudication required')
        try:
            result = score(package, task, name + '-score', folder / 'evaluation')
        except Exception as error:
            attempt.update(status='scoring-error-needs-adjudication', error_class=type(error).__name__)
            save(folder / 'attempt.json', attempt)
            raise
        attempt.update(status='complete' if result.get('completed') else 'scorer-error-needs-adjudication', outcome=result)
        save(folder / 'attempt.json', attempt)
        if attempt['status'] != 'complete':
            raise RuntimeError('Preserved unassessable outcome; distinguish patch failure from infrastructure before continuing')
        print(json.dumps({'slot': slot['slot'], 'status': attempt['status']}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['audit', 'rehearse', 'run'])
    args = parser.parse_args()
    if args.command == 'audit':
        frozen, allocation = audit()
        print(json.dumps({'technical_freeze_valid': True, 'slots': len(allocation['slots']),
                          'author_pilot_release_present': (HERE / 'author-pilot-release.json').exists()}))
    elif args.command == 'rehearse':
        rehearse()
    else:
        run()
