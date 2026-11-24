"""Development-only evaluator probes. Restores the reference page in finally.

Requires the local orders test database and Next development server from the task
report. Run while nobody else is editing the history page.
"""
from pathlib import Path
import difflib
import json
import subprocess

research = Path(__file__).resolve().parents[1]
repo = research / 'SmartKit'
page = repo / 'src/app/dashboard/billing/history/page.tsx'
log_dir = research / 'execution/logs'
original = page.read_bytes()
reference = original.decode('utf-8')
predicate = 'where: and(eq(orders.userId, userId), status ? eq(orders.status, status) : undefined),'
assert reference.count(predicate) == 1, 'Unexpected reference; refusing to overwrite'

variants = {
    'ignore-filter': (reference.replace(predicate, 'where: eq(orders.userId, userId),'), False),
    'remove-owner': (reference.replace(predicate, 'where: status ? eq(orders.status, status) : undefined,'), False),
    'wrong-status': (reference.replace('eq(orders.status, status)', "eq(orders.status, 'pending')"), False),
    'correct-in-memory-filter': (
        reference.replace('const userOrders = await', 'const queriedOrders = await')
        .replace(predicate, 'where: eq(orders.userId, userId),')
        .replace('  return (', '  const userOrders = queriedOrders.filter(order => !status || order.status === status);\n\n  return (', 1),
        True,
    ),
}
results = []
try:
    for name, (source, should_pass) in variants.items():
        page.write_text(source, encoding='utf-8', newline='\n')
        patch = ''.join(difflib.unified_diff(reference.splitlines(True), source.splitlines(True),
                                            fromfile='reference/page.tsx', tofile=f'{name}/page.tsx'))
        (log_dir / f'history-filter-{name}.patch').write_text(patch, encoding='utf-8')
        result = subprocess.run(['pnpm.cmd', 'exec', 'vitest', 'run', '--config', 'vitest.orders.config.ts'],
                                cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        output = result.stdout.decode('utf-8', errors='replace')
        (log_dir / f'history-filter-{name}.log').write_text(output, encoding='utf-8')
        # Compile/server crashes are not evidence of detecting a behavioral defect.
        assertion_failure = 'AssertionError' in output
        matched = result.returncode == 0 if should_pass else result.returncode != 0 and assertion_failure
        results.append({'variant': name, 'exit_code': result.returncode,
                        'expected_pass': should_pass, 'assertion_failure': assertion_failure,
                        'expected_result_observed': matched})
        print(json.dumps(results[-1]), flush=True)
finally:
    page.write_bytes(original)
    (log_dir / 'history-filter-mutation-results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')

assert len(results) == len(variants) and all(row['expected_result_observed'] for row in results)
