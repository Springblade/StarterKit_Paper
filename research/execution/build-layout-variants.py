"""Build paired, unsolved qualification snapshots without editing SmartKit.

Python stdlib only. Output directories must not already exist. Import rewrites
are checked by resolving their targets back to original module identities.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import posixpath
import re
import subprocess

research = Path(__file__).resolve().parents[1]
source = research / 'SmartKit'
execution = research / 'execution'
output = execution / 'layouts'
assert not output.exists(), 'Refusing to overwrite existing layout snapshots'
saved_baseline = (execution / 'history-page-before-filter.tsx.txt').read_bytes()
history = 'src/app/dashboard/billing/history/page.tsx'
code_suffixes = {'.ts', '.tsx', '.js', '.mjs', '.json'}
root_names = {
    '.env.example', '.gitignore', 'biome.json', 'docker-compose.yml',
    'drizzle.config.ts', 'next-env.d.ts', 'next.config.ts', 'package.json',
    'pnpm-lock.yaml', 'pnpm-workspace.yaml', 'postcss.config.mjs', 'tsconfig.json',
    'vercel.json', 'vitest.config.ts', 'vitest.orders.config.ts', 'README.md',
}
inputs = {}
for root_name in ('src', 'scripts', 'public'):
    for path in (source / root_name).rglob('*'):
        if path.is_file() and not any(part in {'node_modules', '__pycache__'} for part in path.parts):
            inputs[path.relative_to(source).as_posix()] = path.read_bytes()
for name in root_names:
    inputs[name] = (source / name).read_bytes()
inputs[history] = saved_baseline

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

mapping = {name: destination(name) for name in inputs}
assert len(set(mapping.values())) == len(mapping), 'Destination collision'
reverse = {new: old for old, new in mapping.items()}
# Quoted path literals include imports/exports, dynamic imports and vi.mock.
# Only strings resolving to an actual local input are rewritten.
quoted = re.compile(r"(['\"])([^'\"\r\n]+)\1")

def resolve(name, specifier, available):
    if specifier.startswith('@/'):
        candidate = 'src/' + specifier[2:]
    elif specifier.startswith('.'):
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(name), specifier))
    else:
        return None
    for target in [candidate, *(candidate + ext for ext in ('.ts', '.tsx', '.js', '.mjs', '.json')),
                   *(candidate + '/index' + ext for ext in ('.ts', '.tsx', '.js'))]:
        if target in available:
            return target
    return None

def specifier_for(name, target):
    if target.startswith('src/'):
        specifier = '@/' + target[4:]
    else:
        specifier = posixpath.relpath(target, posixpath.dirname(name) or '.')
        if not specifier.startswith('.'):
            specifier = './' + specifier
    if PurePosixPath(target).suffix in {'.ts', '.tsx'}:
        specifier = specifier.rsplit('.', 1)[0]
    return specifier

def rewrite(name, body):
    def replace(match):
        target = resolve(name, match[2], inputs)
        if target is None or (mapping[name] == name and mapping[target] == target):
            return match[0]
        return match[1] + specifier_for(mapping[name], mapping[target]) + match[1]
    return quoted.sub(replace, body)

def canonical(name, body, available, identities):
    def replace(match):
        target = resolve(name, match[2], available)
        return match[1] + '<module:' + identities[target] + '>' + match[1] if target else match[0]
    return quoted.sub(replace, body)

common_instructions = '''# SmartKit qualification snapshot

Next.js App Router paths remain under src/app. Keep existing authentication,
ownership predicates, billing state semantics, and server/client boundaries.
Client components use 'use client'; server-only modules retain server-only imports.
Share validation schemas between callers. Revalidate affected routes after writes.
Keep the supplied layout when extending code. Resolve imports through @/.
Tests remain centralized under src/tests with the same test cases in both layouts.
Run pnpm check-types, pnpm test:run and pnpm build for relevant changes.

## Layout
{layout}
'''
feature_layout = ('Application domain modules live under src/features/{domain}. '
                  'Within each domain, use components, hooks, actions, types, lib and emails as appropriate. '
                  'Domain entry points and processing modules remain at the domain root.')
layered_layout = ('Application modules are grouped by technical role under src/components, src/hooks, '
                  'src/actions, src/types, src/lib, src/emails and src/services. '
                  'Within each role, use domain subdirectories; domain entry points and processing modules live under services.')

manifest = {
    'source_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip(),
    'source_state': 'working tree with recorded baseline repairs; history reference excluded',
    'history_baseline_sha256': hashlib.sha256(saved_baseline).hexdigest(),
    'moved_files': {old: new for old, new in mapping.items() if old != new},
    'files': [],
    'canonical_module_check': 'all code/config module bodies equal after resolving local import targets',
    'instructions': 'same common text, layout paragraph varies; original AGENTS replaced in both',
    'instruction_sha256': {},
    'qualification_only': True,
}
for layout in ('feature', 'layered'):
    root = output / layout
    root.mkdir(parents=True)
    for name, data in inputs.items():
        target = name if layout == 'feature' else mapping[name]
        result = data
        if layout == 'layered' and PurePosixPath(name).suffix in code_suffixes:
            body = data.decode('utf-8')
            transformed = rewrite(name, body)
            assert canonical(name, body, inputs, {key: key for key in inputs}) == canonical(
                target, transformed, reverse, reverse), f'Non-import change in {name}'
            result = transformed.encode('utf-8')
        dest = root / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(result)
        manifest['files'].append({'layout': layout, 'original': name, 'path': target,
                                  'sha256': hashlib.sha256(result).hexdigest()})
    (root / 'AGENTS.md').write_text(common_instructions.format(
        layout=feature_layout if layout == 'feature' else layered_layout), encoding='utf-8')
    manifest['instruction_sha256'][layout] = hashlib.sha256((root / 'AGENTS.md').read_bytes()).hexdigest()

# Gold patches are outside both snapshots. They are applied only for evaluator
# qualification, and must be removed from an agent's starting snapshot.
reference = (source / history).read_text(encoding='utf-8')
assert reference.encode('utf-8') != saved_baseline, 'Reference solution missing'
for layout in ('feature', 'layered'):
    if layout == 'layered':
        assert canonical(history, reference, inputs, {key: key for key in inputs}) == canonical(
            history, rewrite(history, reference), reverse, reverse)
    (execution / f'history-reference-{layout}.tsx.txt').write_text(
        reference if layout == 'feature' else rewrite(history, reference), encoding='utf-8')
(execution / 'layout-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(f'Created {len(inputs)} files per snapshot; moved {len(manifest["moved_files"])} modules; canonical check passed')
