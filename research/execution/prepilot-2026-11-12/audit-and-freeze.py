"""Audit qualification, paired sources, packages and no-model rehearsal; freeze artifacts."""
import json
import platform
import posixpath
import random
import re
from pathlib import Path, PurePosixPath
from prepare import HERE, EXEC, runtime, digest, save


def destination(name):
    parts = PurePosixPath(name).parts
    if parts[:2] != ('src', 'features'):
        return name
    domain, tail = parts[2], parts[3:]
    if tail[0] in {'components', 'hooks', 'actions', 'types', 'emails', 'lib'}:
        return '/'.join(('src', tail[0], domain, *tail[1:]))
    if tail == ('types.ts',):
        return f'src/types/{domain}.ts'
    if tail == ('client.ts',):
        return f'src/lib/{domain}/client.ts'
    return '/'.join(('src', 'services', domain, *tail))


def canonical(name, body, available, identities):
    def replace(match):
        spec = match[2]
        if spec.startswith('@/'):
            candidate = 'src/' + spec[2:]
        elif spec.startswith('.'):
            candidate = posixpath.normpath(posixpath.join(posixpath.dirname(name), spec))
        else:
            return match[0]
        options = [candidate, *(candidate + ext for ext in ['.ts', '.tsx', '.js', '.mjs', '.json']),
                   *(candidate + '/index' + ext for ext in ['.ts', '.tsx', '.js'])]
        for target in options:
            if target in available:
                return match[1] + '<module:' + identities[target] + '>' + match[1]
        return match[0]
    return re.sub(r"(['\"])([^'\"\r\n]+)\1", replace, body)


def audit_qualification():
    reliability = json.loads((HERE / 'sweep-reliability.json').read_text(encoding='utf-8'))
    faults = json.loads((HERE / 'sweep-faults.json').read_text(encoding='utf-8'))
    expected = {'visible': digest(HERE / 'visible-check.cjs'), 'final': digest(HERE / 'final-check.cjs'),
                'runtime': digest(HERE / 'local-runtime.py')}
    for ledger in [reliability, faults]:
        assert ledger['status'] == 'passed' and ledger['versions'] == expected
        assert all(job['validated'] for job in ledger['jobs'].values())
        for job in ledger['jobs'].values():
            assert len(job['basic']) == 5 and all(code == 0 for code in job['basic'].values())
            visible = digest(HERE / 'packages' / job['task'] / ('S1V1' if job['layout'] == 'feature' else 'S0V1') / 'scripts/check-preservation.cjs')
            assert all(row.get('completed') and row['check_sha256'] == visible for row in job['visible'])
            assert all(row.get('completed') and row['check_sha256'] == expected['final'] for row in job['final'])
    for task in ['DP02', 'DP03']:
        for layout in ['feature', 'layered']:
            for variant, vr, fr in [('baseline', 20, 3), ('reference', 20, 20), ('alternative', 3, 3)]:
                if task == 'DP03' and variant in ['baseline', 'reference']:
                    vr = 30
                    if variant == 'reference':
                        fr = 30
                job = reliability['jobs']['/'.join([task, layout, variant])]
                assert len(job['visible']) == vr and len(job['final']) == fr
                assert all(row['pass'] for row in job['visible'])
                assert all(row['preservation'] and row['acceptance'] == (variant != 'baseline') for row in job['final'])
    assert len(reliability['jobs']) == 12 and len(faults['jobs']) == 26
    expected_fault_checks = {
        'fault-ignore-filter': 'U-A-role-user', 'fault-hardcode-role': 'U-A-role-admin',
        'fault-total': 'U-P2-unfiltered-session-aggregates-and-date-order',
        'fault-admin-access': 'U-P1-direct-route-non-admin-and-anonymous',
        'fault-session-count': 'U-P2-unfiltered-session-aggregates-and-date-order',
        'fault-no-server-validation': 'A-A3-server-rejects-empty',
        'fault-no-persistence': 'A-A1-labelled-form-submission-trim-and-refresh',
        'fault-no-ui-refresh': 'A-A1-labelled-form-submission-trim-and-refresh',
        'fault-utf16': 'A-A2-boundary-eighty-unicode',
        'fault-no-trim': 'A-A1-labelled-form-submission-trim-and-refresh',
        'fault-unsafe-name': 'A-P3-stored-name-safe-on-existing-settings',
        'fault-foreign-write': 'A-A4-own-target-and-protected-fields-through-actual-write',
        'fault-protected-field': 'A-A4-own-target-and-protected-fields-through-actual-write',
    }
    for job in faults['jobs'].values():
        expected = expected_fault_checks[job['variant']]
        assert all(any(check['id'] == expected and not check['pass'] for check in row['results'])
                   for row in job['final']), ('Fault failed for the wrong reason', job['task'], job['layout'], job['variant'])
    return reliability, faults


def audit_packages():
    original = json.loads((EXEC / 'layout-manifest.json').read_text(encoding='utf-8'))
    source_records = {layout: {r['path']: r['sha256'] for r in original['files'] if r['layout'] == layout}
                      for layout in ['feature', 'layered']}
    inventories = {}
    for task in ['DP02', 'DP03']:
        for s in [0, 1]:
            layout = ['layered', 'feature'][s]
            for v in [0, 1]:
                cell = f'S{s}V{v}'
                folder = HERE / 'packages' / task / cell
                inventory = json.loads(folder.parent.joinpath(cell + '-manifest.json').read_text(encoding='utf-8'))['files']
                actual = {p.relative_to(folder).as_posix(): digest(p) for p in folder.rglob('*') if p.is_file()}
                assert actual == inventory, 'Package inventory mismatch'
                assert not any(part in {'.git', 'auth.json', 'final-check.cjs', 'task-cards.md', 'files.json'} for path in actual for part in Path(path).parts)
                for filename, value in source_records[layout].items():
                    if filename in {'scripts/check-order-baseline.integration.ts', 'vitest.orders.config.ts', 'AGENTS.md', 'package.json'}:
                        continue
                    assert actual[filename] == value, filename
                assert b'STATUS_OPTIONS' not in (folder / 'src/app/dashboard/billing/history/page.tsx').read_bytes()
                inventories[(task, s, v)] = inventory
            a, b = inventories[(task, s, 0)], inventories[(task, s, 1)]
            changes = {path for path in a.keys() | b.keys() if a.get(path) != b.get(path)}
            assert changes == {'TASK.md', 'package.json', 'scripts/check-preservation.cjs'}, changes
            p0 = json.loads((HERE / 'packages' / task / f'S{s}V0' / 'package.json').read_text(encoding='utf-8'))
            p1 = json.loads((HERE / 'packages' / task / f'S{s}V1' / 'package.json').read_text(encoding='utf-8'))
            assert p1['scripts'].pop('test:preservation') == 'node scripts/check-preservation.cjs'
            assert p0 == p1
        assert inventories[(task, 0, 1)]['scripts/check-preservation.cjs'] == inventories[(task, 1, 1)]['scripts/check-preservation.cjs']
        prompts = [(HERE / 'packages' / task / cell / 'TASK.md').read_text(encoding='utf-8') for cell in ['S0V0', 'S0V1', 'S1V0', 'S1V1']]
        assert len({p.replace(' Additional preservation command: pnpm test:preservation.', '') for p in prompts}) == 1
    return {'packages': 8, 'baseline_source_files_unchanged': True, 'V_changes_only_declared_files': True,
            'task_requirements_equal_across_cells': True, 'checks_path_independent': True}


def reference_metrics():
    baseline = json.loads((EXEC / 'layout-manifest.json').read_text(encoding='utf-8'))
    source_names = {r['path'] for r in baseline['files'] if r['layout'] == 'feature'}
    active = json.loads((HERE / 'solution-inventory.json').read_text(encoding='utf-8'))
    metrics = {}
    for task in ['DP02', 'DP03']:
        metrics[task] = {}
        for variant in active[task]:
            a = HERE / 'solutions' / task / 'feature' / variant
            b = HERE / 'solutions' / task / 'layered' / variant
            af = json.loads((a / 'files.json').read_text(encoding='utf-8'))
            bf = json.loads((b / 'files.json').read_text(encoding='utf-8'))
            assert all(digest(a / name) == value for name, value in af.items())
            assert all(digest(b / name) == value for name, value in bf.items())
            available = source_names | set(af)
            moved = {name: destination(name) for name in available}
            reverse = {new: old for old, new in moved.items()}
            assert {moved[name] for name in af} == set(bf)
            for name in af:
                assert canonical(name, (a / name).read_text(encoding='utf-8'), available, {n: n for n in available}) == canonical(
                    moved[name], (b / moved[name]).read_text(encoding='utf-8'), set(reverse), reverse), (task, variant, name)
            if variant in ['reference', 'alternative']:
                paths = list(af)
                metrics[task][variant] = {
                    'source_files_S0': len(bf), 'source_files_S1': len(af),
                    'parent_directories_S0': len({str(PurePosixPath(p).parent) for p in bf}),
                    'parent_directories_S1': len({str(PurePosixPath(p).parent) for p in af}),
                    'different_path_logical_modules': sum(moved[p] != p for p in paths),
                    'relocated_existing_logical_modules': sum(moved[p] != p and p in source_names for p in paths),
                    'new_layout_specific_modules': sum(moved[p] != p and p not in source_names for p in paths),
                    'changed_framework_routes_at_identical_paths': sum(p.startswith('src/app/') and p.endswith(('page.tsx', 'route.ts')) for p in paths),
                    'root': 'src', 'mapping': {p: moved[p] for p in paths}}
    save(HERE / 'reference-metrics.json', metrics)
    return metrics


def main():
    assert not (HERE / 'freeze.json').exists(), 'Retain existing freeze; revisions need a separate reviewed version'
    reliability, faults = audit_qualification()
    packages = audit_packages()
    metrics = reference_metrics()
    rehearsals = json.loads((HERE / 'rehearsal/ledger.json').read_text(encoding='utf-8'))
    for task in ['DP02', 'DP03']:
        for cell in ['S0V0', 'S0V1', 'S1V0', 'S1V1']:
            row = rehearsals[task + '/' + cell]
            assert row['passed'] and not row['account_credentials_supplied']
            assert row['final_check_sha256'] == digest(HERE / 'final-check.cjs')
            assert row['package_manifest_sha256'] == digest(HERE / 'packages' / task / (cell + '-manifest.json'))
    assert not (HERE / 'runs').exists(), 'Unexpected pilot records before release'
    rng = random.Random(2026111102)
    slots = []
    for task, repetitions in [('DP02', 1), ('DP03', 3)]:
        for repetition in range(1, repetitions + 1):
            cells = ['S0V0', 'S0V1', 'S1V0', 'S1V1']; rng.shuffle(cells)
            for cell in cells:
                slots.append({'slot': f'{task}-R{repetition:02}-{cell}', 'task': task, 'repetition': repetition, 'cell': cell})
    save(HERE / 'allocation.json', {'seed': 2026111102, 'python': platform.python_version(), 'slots': slots,
         'scheduled_trials': len(slots), 'model_attempt_replacements_cap': 6, 'automatic_model_retries': False,
         'wall_seconds_per_trial': 900, 'scheduled_wall_hours_cap': len(slots) / 4})
    image = json.loads(runtime.docker('image', 'inspect', runtime.IMAGE).stdout)[0]
    files = {}
    for name in ['task-cards.md', 'solution-inventory.json', 'visible-check.cjs', 'final-check.cjs', 'pilot.py', 'prepare.py',
                 'qualify.py', 'sweep.py', 'build-solutions.py', 'audit-and-freeze.py', 'local-runtime.py', 'preflight-selfcheck.py', 'Dockerfile',
                 'allocation.json', 'reference-metrics.json', 'sweep-reliability.json', 'sweep-faults.json', 'rehearsal/ledger.json']:
        files[name] = digest(HERE / name)
    for p in (HERE / 'packages').rglob('*'):
        if p.is_file():
            files[p.relative_to(HERE).as_posix()] = digest(p)
    for p in (HERE / 'solutions').rglob('*'):
        if p.is_file():
            files[p.relative_to(HERE).as_posix()] = digest(p)
    save(HERE / 'freeze.json', {
        'status': 'technical-artifact-freeze-awaiting-author-pilot-release', 'time': runtime.stamp(),
        'image_id': image['Id'], 'files': files, 'package_audit': packages,
        'configuration': {'requested_model': 'gpt-6-luna', 'reasoning': 'high', 'speed': 'standard-default',
                          'wall_seconds': 900, 'token_cap': None, 'funding': 'existing-ChatGPT-allowance-only'},
        'reuse': {'DP02': 'development-only', 'DP03': 'evaluation-ready-after-author-release-with-outcome-independent-main-eligibility'},
        'main_protocol_frozen': False, 'new_model_invocations': 0,
        'next_author_decision': 'Approve the concrete task cards, qualification scope and 16-slot development pilot release.'})
    print('Technical freeze created; pilot remains gated by missing author-pilot-release.json', flush=True)


if __name__ == '__main__':
    main()
