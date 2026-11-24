"""Continue only no-model preparation after reliability has finished successfully."""
import json
import subprocess
import sys
import time
from prepare import HERE, save


def main():
    reliability = HERE / 'sweep-reliability.json'
    deadline = time.monotonic() + 7200
    while time.monotonic() < deadline:
        if not reliability.exists():
            time.sleep(10)
            continue
        try:
            data = json.loads(reliability.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            time.sleep(1)
            continue
        if data.get('status') == 'passed':
            break
        time.sleep(10)
    else:
        raise RuntimeError('Reliability has not passed; no downstream work launched')
    commands = [['sweep.py', '--phase', 'faults'], ['pilot.py', 'rehearse'],
                ['preflight-selfcheck.py'], ['audit-and-freeze.py'], ['pilot.py', 'audit']]
    ledger = {'kind': 'no-model-preparation', 'stages': [], 'status': 'running'}
    for command in commands:
        path = HERE / ('finish-' + command[0].replace('.py', '') + '.log')
        with path.open('wb') as output:
            result = subprocess.run([sys.executable, str(HERE / command[0]), *command[1:]], stdout=output, stderr=subprocess.STDOUT)
        ledger['stages'].append({'command': command, 'returncode': result.returncode, 'log': path.name})
        save(HERE / 'preparation-pipeline.json', ledger)
        if result.returncode:
            raise RuntimeError('Preparation stopped; retained log: ' + path.name)
    ledger['status'] = 'passed-awaiting-author-pilot-release'
    save(HERE / 'preparation-pipeline.json', ledger)
    print(ledger['status'], flush=True)


if __name__ == '__main__':
    main()
