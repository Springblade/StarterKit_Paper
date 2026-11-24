"""Run the HTTP/session spike with the existing container harness, without a model."""
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parent
PILOT = ROOT / 'pilot-2026-11-11'
spec = importlib.util.spec_from_file_location('session_spike_runner', PILOT / 'pilot.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def main():
    # Refuse to overwrite an earlier observation or its diagnostic logs.
    output = ROOT / 'dp04-spike-2026-11-11'
    output.mkdir(exist_ok=False)
    records = []
    script = ROOT / 'dp04-session-spike.cjs'
    for layout, cell in [('feature', 'S1V0'), ('layered', 'S0V0')]:
        name = 'smartkit-dp04-spike-' + layout
        folder = output / layout
        folder.mkdir()
        try:
            head = runner.start(name, PILOT / 'packages' / cell, folder)
            runner.docker('exec', name, 'mkdir', '-p', '/evaluator')
            runner.docker('cp', script, name + ':/evaluator/spike.cjs')
            process = runner.docker('exec', name, 'node', '/evaluator/spike.cjs', check=False, timeout=180)
            (folder / 'spike.log').write_bytes(process.stdout)
            runner.docker('cp', name + ':/evaluator/result.json', folder / 'result.json', check=False)
            if process.returncode:
                runner.docker('cp', name + ':/evaluator/error.json', folder / 'error.json', check=False)
                raise RuntimeError('Spike failed; inspect safe error class and logs')
            result = json.loads((folder / 'result.json').read_text())
            assert result['completed'] and not result['baselineModified']
            assert all(item['pass'] for item in result['observations'] if 'pass' in item)
            records.append({'layout': layout, 'cell_source': cell, 'head': head, 'result': result})
            print(json.dumps({'layout': layout, 'immediateInvalidationPass': result['immediateInvalidationPass']}), flush=True)
        finally:
            runner.stop(name, folder)
    summary = {
        'purpose': 'DP04 feasibility spike; no coding-agent invocation',
        'script_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
        'baseline_changed': False, 'records': records,
    }
    (output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
