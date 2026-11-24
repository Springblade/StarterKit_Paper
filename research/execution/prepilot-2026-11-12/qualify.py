"""Container-only qualification runner. Deliberately has no model-run command."""
import argparse
import json
import time
from pathlib import Path
from prepare import HERE, runtime, save, digest


def read_result(process, path, visible_suite=False):
    value = json.loads(path.read_text(encoding='utf-8'))
    lines = process.stdout.decode(errors='replace').splitlines()
    emitted = json.loads(next(line for line in reversed(lines) if line.startswith('{')))
    assert emitted == value, 'Checker output file is stale or inconsistent with this invocation'
    expected_exit = 1 if visible_suite and value.get('completed') and not value.get('pass') else 0
    if value.get('completed'):
        assert process.returncode == expected_exit, 'Unexpected checker process exit'
    return value


def start(task, layout, folder):
    cell = 'S1V1' if layout == 'feature' else 'S0V1'
    name = 'smartkit-pre-' + task.lower() + '-' + layout
    runtime.start(name, HERE / 'packages' / task / cell, folder)
    runtime.docker('exec', name, 'mkdir', '-p', '/evaluator')
    return name


def visible(name, folder, number=0):
    output = folder / f'visible-{number:02}.json'
    p = runtime.docker('exec', '-e', 'CHECK_OUTPUT=/evaluator/visible.json', name,
                       'node', 'scripts/check-preservation.cjs', check=False, timeout=300)
    (folder / f'visible-{number:02}.log').write_bytes(p.stdout)
    runtime.docker('cp', name + ':/evaluator/visible.json', output)
    value = read_result(p, output, visible_suite=True)
    value['check_sha256'] = runtime.docker('exec', name, 'sha256sum', 'scripts/check-preservation.cjs').stdout.decode().split()[0]
    save(output, value)
    return value


def final(name, task, folder, number=0):
    evaluator_digest = digest(HERE / 'final-check.cjs')
    runtime.docker('cp', HERE / 'final-check.cjs', name + ':/evaluator/final-check.cjs')
    p = runtime.docker('exec', '-e', 'CHECK_TASK=' + task, name, 'node', '/evaluator/final-check.cjs', check=False, timeout=300)
    (folder / f'final-{number:02}.log').write_bytes(p.stdout)
    output = folder / f'final-{number:02}.json'
    runtime.docker('cp', name + ':/evaluator/final.json', output)
    runtime.docker('cp', name + ':/evaluator/profile-form.png', folder / 'profile-form.png', check=False)
    value = read_result(p, output)
    value['check_sha256'] = evaluator_digest
    save(output, value)
    return value


def apply_solution(name, task, layout, variant):
    folder = HERE / 'solutions' / task / layout / variant
    for filename in json.loads((folder / 'files.json').read_text(encoding='utf-8')):
        runtime.docker('exec', name, 'mkdir', '-p', str(Path('/workspace') / Path(filename).parent).replace('\\', '/'))
        runtime.docker('cp', folder / filename, name + ':/workspace/' + filename)


def qualify(task, layout, variant, visible_rounds, final_rounds, basic):
    folder = HERE / 'qualification' / f'{task}-{layout}-{variant}'
    if folder.exists():
        folder = folder.with_name(folder.name + '-' + str(time.time_ns()))
    folder.mkdir(parents=True)
    name = None
    summary = {'task': task, 'layout': layout, 'variant': variant, 'visible': [], 'final': [], 'basic': {},
               'instrument_version': 'prepilot-v1', 'started': runtime.stamp()}
    if variant != 'baseline':
        source_manifest = HERE / 'solutions' / task / layout / variant / 'files.json'
        summary['declared_solution_files'] = json.loads(source_manifest.read_text(encoding='utf-8'))
    try:
        name = 'smartkit-pre-' + task.lower() + '-' + layout
        start(task, layout, folder)
        if variant != 'baseline':
            apply_solution(name, task, layout, variant)
        if basic:
            for command in ['check-types', 'test:run', 'build', 'test:billing', 'test:sepay-qr-url']:
                p = runtime.docker('exec', '-e', 'TEST_BASE_URL=http://localhost:3107',
                    '-e', 'SEPAY_BANK_ACCOUNT=0010000000000', '-e', 'SEPAY_BANK_NAME=Vietcombank',
                    name, 'pnpm', command, check=False, timeout=240)
                (folder / (command.replace(':', '-') + '.log')).write_bytes(p.stdout)
                summary['basic'][command] = p.returncode
                print(json.dumps({'task': task, 'layout': layout, 'variant': variant, 'basic': command, 'exit': p.returncode}), flush=True)
        for i in range(visible_rounds):
            row = visible(name, folder, i)
            summary['visible'].append(row)
            save(folder / 'summary.json', summary)
            print(json.dumps({'task': task, 'layout': layout, 'variant': variant, 'suite': 'visible', 'round': i + 1, 'pass': row.get('pass'), 'failed': [r['id'] for r in row.get('results', []) if not r['pass']]}), flush=True)
            if variant in ['baseline', 'reference', 'alternative']:
                assert row.get('completed') and row.get('pass'), 'Unexpected visible feedback; retained logs require diagnosis'
        for i in range(final_rounds):
            row = final(name, task, folder, i)
            summary['final'].append(row)
            save(folder / 'summary.json', summary)
            print(json.dumps({'task': task, 'layout': layout, 'variant': variant, 'suite': 'final', 'round': i + 1, 'completed': row.get('completed'), 'acceptance': row.get('acceptance'), 'preservation': row.get('preservation'), 'failed': [r['id'] for r in row.get('results', []) if not r['pass']]}), flush=True)
            if variant in ['baseline', 'reference', 'alternative']:
                assert row.get('completed') and row.get('preservation') and row.get('acceptance') == (variant != 'baseline'), 'Unexpected final evaluation; retained logs require diagnosis'
        return summary
    finally:
        save(folder / 'summary.json', summary)
        if name:
            runtime.stop(name, folder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', choices=['DP02', 'DP03'], required=True)
    parser.add_argument('--layout', choices=['feature', 'layered'], required=True)
    parser.add_argument('--variant', default='baseline')
    parser.add_argument('--visible-rounds', type=int, default=1)
    parser.add_argument('--final-rounds', type=int, default=1)
    parser.add_argument('--basic', action='store_true')
    args = parser.parse_args()
    qualify(args.task, args.layout, args.variant, args.visible_rounds, args.final_rounds, args.basic)
