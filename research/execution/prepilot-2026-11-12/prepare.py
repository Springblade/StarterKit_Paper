"""Prepare/qualify local research artifacts. This program never invokes a model."""
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil

HERE = Path(__file__).resolve().parent
EXEC = HERE.parent
spec = importlib.util.spec_from_file_location('local_runtime', HERE / 'local-runtime.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def packages():
    manifest = json.loads((EXEC / 'layout-manifest.json').read_text())
    for task in ['DP02', 'DP03']:
        for s in [0, 1]:
            layout = ['layered', 'feature'][s]
            for v in [0, 1]:
                target = HERE / 'packages' / task / f'S{s}V{v}'
                if target.exists() and (HERE / 'freeze.json').exists():
                    raise RuntimeError(f'Refusing to overwrite package {target}')
                target.mkdir(parents=True, exist_ok=True)
                for row in manifest['files']:
                    if row['layout'] != layout or row['path'] in {'scripts/check-order-baseline.integration.ts', 'vitest.orders.config.ts'}:
                        continue
                    source = EXEC / 'layouts' / layout / row['path']
                    assert digest(source) == row['sha256'], row['path']
                    dest = target / row['path']
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, dest)
                shutil.copyfile(EXEC / 'layouts' / layout / 'AGENTS.md', target / 'AGENTS.md')
                (target / '.env').write_text(runtime.env_text(), encoding='utf-8')
                cards = (HERE / 'task-cards.md').read_text(encoding='utf-8')
                if task == 'DP02':
                    requirement = cards.split('## DP-02 —', 1)[1].split('## DP-03 —', 1)[0]
                    requirement = 'Add ' + requirement.split('\n\nAdd ', 1)[1].split('\n\n| Requirement', 1)[0]
                else:
                    requirement = cards.split('## DP-03 —', 1)[1].split('\n\n| Requirement', 1)[0]
                    requirement = 'Add ' + requirement.split('\n\nAdd ', 1)[1]
                task_text = ('# Assigned task: ' + task + '\n\n' + requirement + '\n\n'
                    'Preserve the supplied layout and behavior outside this task. Do not change dependencies, '
                    'globally disable cookie caching, or modify auth-library internals. You may add appropriate '
                    'source files and use any correct implementation. No fixed file list is required.\n\n'
                    '## Local environment and tools\n\n'
                    'Dependencies are installed. A fresh PostgreSQL database is migrated/seeded and a Next.js '
                    'development server is running at http://localhost:3107. Synthetic test accounts are listed '
                    'in scripts/seed.ts; no real payment/email credentials are configured. Playwright 1.58.2 '
                    'and Chromium are available in every condition. A Node check can load '
                    "require('/opt/behavior/node_modules/playwright') and launch chromium with args: ['--no-sandbox']. "
                    'You may write/run your own checks and use the browser.\n\n'
                    'Supplied checks: pnpm check-types; pnpm test:run; pnpm build; existing project scripts.'
                    + (' Additional preservation command: pnpm test:preservation.' if v else '')
                    + '\n\nThe wall-time limit is 900 seconds from CLI invocation, including check execution. '
                    'Keep all work in this workspace and do not commit it. Finish with a brief account of changes and checks.\n')
                (target / 'TASK.md').write_text(task_text, encoding='utf-8')
                package = json.loads((target / 'package.json').read_text())
                if v:
                    (target / 'scripts/check-preservation.cjs').write_text(
                        (HERE / 'visible-check.cjs').read_text(encoding='utf-8').replace('__TASK__', task), encoding='utf-8')
                    package['scripts']['test:preservation'] = 'node scripts/check-preservation.cjs'
                (target / 'package.json').write_text(json.dumps(package, indent=2) + '\n', encoding='utf-8')
                assert b'STATUS_OPTIONS' not in (target / 'src/app/dashboard/billing/history/page.tsx').read_bytes()
                save(target.parent / (target.name + '-manifest.json'), {
                    'task': task, 'cell': f'S{s}V{v}', 'files': {p.relative_to(target).as_posix(): digest(p) for p in target.rglob('*') if p.is_file()}})
    print('Prepared eight unsolved packages; no model invocation', flush=True)


if __name__ == '__main__':
    packages()
