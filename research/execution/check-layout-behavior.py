"""Sequential local qualification; keeps gold solutions outside task snapshots."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time
import urllib.request

execution = Path(__file__).resolve().parent
results = []
for layout in ('feature', 'layered'):
    root = execution / 'layouts' / layout
    page = root / 'src/app/dashboard/billing/history/page.tsx'
    baseline = page.read_bytes()
    manifest = json.loads((execution / 'layout-manifest.json').read_text())
    expected = next(row['sha256'] for row in manifest['files']
                    if row['layout'] == layout and row['path'] == 'src/app/dashboard/billing/history/page.tsx')
    assert hashlib.sha256(baseline).hexdigest() == expected, 'Baseline changed since snapshot generation'
    reference = (execution / f'history-reference-{layout}.tsx.txt').read_bytes()
    server_log = (execution / 'logs' / f'layout-{layout}-server.log').open('wb')
    server = subprocess.Popen(['pnpm.cmd', 'exec', 'next', 'dev', '-p', '3107'], cwd=root,
                              stdout=server_log, stderr=subprocess.STDOUT,
                              creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    try:
        deadline = time.monotonic() + 45
        while True:
            if server.poll() is not None:
                raise RuntimeError('Development server exited; inspect server log')
            try:
                urllib.request.urlopen('http://localhost:3107/', timeout=3).close()
                break
            except Exception:
                if time.monotonic() > deadline:
                    raise
                time.sleep(0.3)
        for stage in ('baseline', 'reference', 'restored-baseline'):
            page.write_bytes(reference if stage == 'reference' else baseline)
            command = ['pnpm.cmd', 'exec', 'vitest', 'run', '--config', 'vitest.orders.config.ts']
            if stage != 'reference':
                command += ['-t', 'real HTTP ownership checks|actual server actions']
            result = subprocess.run(command, cwd=root, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=120)
            (execution / 'logs' / f'layout-{layout}-{stage}.log').write_bytes(result.stdout)
            record = {'layout': layout, 'stage': stage, 'exit_code': result.returncode}
            results.append(record)
            print(json.dumps(record), flush=True)
            if result.returncode:
                raise RuntimeError(f'{layout}/{stage} failed')
    finally:
        page.write_bytes(baseline)
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(server.pid), '/T', '/F'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            server.terminate()
        server_log.close()
        assert page.read_bytes() == baseline
        (execution / 'layout-behavior-results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
