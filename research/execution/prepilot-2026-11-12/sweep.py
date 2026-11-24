"""Serial, resumable qualification. No model access or pilot-run functionality."""
import argparse
import json
from prepare import HERE, save, digest
from qualify import qualify


def validate(task, variant, result):
    assert all(value == 0 for value in result['basic'].values()), ('Basic check failure', result['basic'])
    assert all(r.get('completed') for r in result['visible'] + result['final']), 'Incomplete checker execution'
    assert all(all(c['pass'] for c in r['results'] if c['id'] == 'fixture-cleanup') for r in result['visible'] + result['final'])
    if variant in ['baseline', 'reference', 'alternative']:
        assert all(r['pass'] for r in result['visible']), 'False visible feedback'
        assert all(r['preservation'] for r in result['final']), 'Unexpected preservation failure'
        assert all(r['acceptance'] == (variant != 'baseline') for r in result['final']), 'Wrong acceptance discrimination'
    else:
        assert all(not r['jointSuccess'] for r in result['final']), 'Fault missed by final checker'
        if variant in ['fault-admin-access', 'fault-session-count', 'fault-total', 'fault-unsafe-name']:
            assert all(not r['pass'] for r in result['visible']), 'Expected additional visible feedback was absent'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['smoke', 'reliability', 'faults'], required=True)
    args = parser.parse_args()
    inventory = json.loads((HERE / 'solution-inventory.json').read_text(encoding='utf-8'))
    ledger_path = HERE / ('sweep-' + args.phase + '.json')
    ledger = json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else {'jobs': {}, 'status': 'running'}
    # Resume only across exactly the same checker versions.
    versions = {'visible': digest(HERE / 'visible-check.cjs'), 'final': digest(HERE / 'final-check.cjs'),
                'runtime': digest(HERE / 'local-runtime.py')}
    if 'versions' in ledger:
        assert ledger['versions'] == versions, 'Instruments changed; retain the old ledger and use a new version'
    ledger['versions'] = versions
    for task in ['DP02', 'DP03']:
        for layout in ['feature', 'layered']:
            variants = inventory[task][2:] if args.phase == 'faults' else ['baseline', 'reference', 'alternative']
            for variant in variants:
                key = '/'.join([task, layout, variant])
                if ledger['jobs'].get(key, {}).get('validated'):
                    continue
                vr, fr = (1, 1)
                if args.phase == 'reliability':
                    vr, fr = {'baseline': (20, 3), 'reference': (20, 20), 'alternative': (3, 3)}[variant]
                    if task == 'DP03' and variant in ['baseline', 'reference']:
                        vr = 30
                        if variant == 'reference':
                            fr = 30
                result = qualify(task, layout, variant, vr, fr, True)
                ledger['jobs'][key] = result
                save(ledger_path, ledger)
                validate(task, variant, result)
                ledger['jobs'][key]['validated'] = True
                save(ledger_path, ledger)
    ledger['status'] = 'passed'
    save(ledger_path, ledger)
    print('Qualification sweep passed: ' + args.phase, flush=True)


if __name__ == '__main__':
    main()
