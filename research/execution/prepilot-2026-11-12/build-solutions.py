"""Explicit development references/alternatives/probes; never copied into packages."""
from pathlib import Path
import json
from prepare import HERE, EXEC, save, digest


def write_variant(task, layout, variant, files):
    folder = HERE / 'solutions' / task / layout / variant
    folder.mkdir(parents=True, exist_ok=True)
    for name, source in files.items():
        dest = folder / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(source, encoding='utf-8')
    save(folder / 'files.json', {name: digest(folder / name) for name in files})


def main():
    active = {'DP02': ['reference', 'alternative', 'fault-ignore-filter', 'fault-hardcode-role',
                       'fault-total', 'fault-admin-access', 'fault-session-count'],
              'DP03': ['reference', 'alternative', 'fault-no-server-validation', 'fault-no-persistence',
                       'fault-no-ui-refresh', 'fault-utf16', 'fault-no-trim', 'fault-unsafe-name',
                       'fault-foreign-write', 'fault-protected-field']}
    for layout in ['feature', 'layered']:
        feature = layout == 'feature'
        root = EXEC / 'layouts' / layout
        page_path = 'src/app/dashboard/admin/users/page.tsx'
        original = (root / page_path).read_text(encoding='utf-8')
        page = original.replace("import { desc, sql }", "import { desc, eq, sql }")
        page = page.replace('export default async function AdminUsersPage() {', '''export default async function AdminUsersPage({ searchParams }: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const requestedRole = (await searchParams).role;
  const role = requestedRole === 'user' || requestedRole === 'admin' ? requestedRole : undefined;''')
        page = page.replace('orderBy: [desc(user.createdAt)],', 'where: role ? eq(user.role, role) : undefined,\n    orderBy: [desc(user.createdAt)],')
        controls = '''      <form action="/dashboard/admin/users" method="get">
        <label htmlFor="role-filter">Role</label>
        <select id="role-filter" name="role" defaultValue={role ?? ''}>
          <option value="">All</option><option value="user">User</option><option value="admin">Admin</option>
        </select>
        <button type="submit">Apply role</button>
      </form>
'''
        page = page.replace('      <div className="rounded-lg border">', controls + '      <div className="rounded-lg border">')
        write_variant('DP02', layout, 'reference', {page_path: page})
        alternative = page.replace('where: role ? eq(user.role, role) : undefined,\n    ', '').replace('const allUsers = await db.query.user.findMany({', 'const directory = await db.query.user.findMany({')
        alternative = alternative.replace('  // Get session counts', "  const allUsers = directory.filter(account => !role || account.role === role);\n\n  // Get session counts").replace('desc, eq, sql', 'desc, sql')
        write_variant('DP02', layout, 'alternative', {page_path: alternative})
        variants = {
            'fault-ignore-filter': page.replace('where: role ? eq(user.role, role) : undefined,', 'where: undefined,'),
            'fault-hardcode-role': page.replace('eq(user.role, role)', "eq(user.role, 'user')"),
            'fault-total': page.replace('STRINGS.totalUsers(allUsers.length)', 'STRINGS.totalUsers(allUsers.length + 1)'),
            'fault-admin-access': page.replace('requireAdmin', 'requireAuth'),
            'fault-session-count': page.replace('sessionCountMap.get(u.id) ?? 0', '0'),
        }
        for name, faulty in variants.items():
            write_variant('DP02', layout, name, {page_path: faulty})

        auth_import = '@/features/auth/lib/auth' if feature else '@/lib/auth/auth'
        # Resolve exact relocated auth module from the transformation manifest.
        manifest = json.loads((EXEC / 'layout-manifest.json').read_text(encoding='utf-8'))
        if not feature:
            auth_import = '@/' + manifest['moved_files']['src/features/auth/lib/auth.ts'][4:-3]
        schema_path = 'src/features/auth/types/profile.ts' if feature else 'src/types/auth/profile.ts'
        schema_import = '@/' + schema_path[4:-3]
        action_path = 'src/features/auth/actions/update-display-name.ts' if feature else 'src/actions/auth/update-display-name.ts'
        schema = '''import { z } from 'zod';

export const displayNameSchema = z.string().transform(value => value.trim()).refine(
  value => [...value].length >= 1 && [...value].length <= 80,
  'Display name must contain 1 to 80 Unicode code points after trimming.',
);
'''
        action = f'''\'use server\';

import {{ headers }} from 'next/headers';
import {{ revalidatePath }} from 'next/cache';
import {{ redirect }} from 'next/navigation';
import {{ auth, requireAuth }} from '{auth_import}';
import {{ displayNameSchema }} from '{schema_import}';

// Better Auth v1.6 nextCookies handles response cookies for Server Actions.
// https://www.better-auth.com/docs/integrations/next
export async function updateDisplayName(form: FormData) {{
  await requireAuth();
  const parsed = displayNameSchema.safeParse(form.get('name'));
  if (!parsed.success) redirect('/dashboard/settings?profile=invalid');
  await auth.api.updateUser({{ headers: await headers(), body: {{ name: parsed.data }} }});
  revalidatePath('/dashboard', 'layout');
  redirect('/dashboard/settings?profile=saved');
}}
'''
        settings_path = 'src/app/dashboard/settings/page.tsx'
        settings = (root / settings_path).read_text(encoding='utf-8')
        settings = f"import {{ updateDisplayName }} from '@/{action_path[4:-3]}';\n" + settings
        form = '''          <form action={updateDisplayName}>
            <label htmlFor="display-name">Display name</label>
            <input id="display-name" name="name" type="text" defaultValue={user.name ?? ''} />
            <button type="submit">Save name</button>
          </form>
'''
        settings = settings.replace('          <dl className="mt-4 space-y-4">', form + '          <dl className="mt-4 space-y-4">')
        ref = {settings_path: settings, action_path: action, schema_path: schema}
        write_variant('DP03', layout, 'reference', ref)

        component_path = 'src/features/auth/components/display-name-form.tsx' if feature else 'src/components/auth/display-name-form.tsx'
        component = f'''\'use client\';
import {{ useState }} from 'react';
import {{ useRouter }} from 'next/navigation';
import {{ displayNameSchema }} from '{schema_import}';

export function DisplayNameForm({{ initialName }}: {{ initialName: string }}) {{
  const [name, setName] = useState(initialName);
  const [message, setMessage] = useState('');
  const router = useRouter();
  return <form onSubmit={{async event => {{
    event.preventDefault();
    if (!displayNameSchema.safeParse(name).success) {{ setMessage('Invalid display name'); return; }}
    const response = await fetch('/api/profile/display-name', {{
      method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ name }}),
    }});
    if (response.ok) {{ setName(name.trim()); setMessage('Saved'); router.refresh(); }}
    else setMessage('Invalid display name');
  }}}}>
    <label htmlFor="display-name">Display name</label>
    <input id="display-name" name="name" value={{name}} onChange={{e => setName(e.target.value)}} />
    <button type="submit">Save name</button><p role="status">{{message}}</p>
  </form>;
}}
'''
        route = f'''import {{ auth }} from '{auth_import}';
import {{ displayNameSchema }} from '{schema_import}';

export async function POST(request: Request) {{
  const session = await auth.api.getSession({{ headers: request.headers }});
  if (!session) return Response.json({{ error: 'Unauthorized' }}, {{ status: 401 }});
  let body;
  try {{ body = await request.json(); }} catch {{ return Response.json({{ error: 'Invalid JSON' }}, {{ status: 400 }}); }}
  const parsed = displayNameSchema.safeParse(body?.name);
  if (!parsed.success) return Response.json({{ error: 'Invalid display name' }}, {{ status: 400 }});
  // Return the original auth response, including Set-Cookie, to this browser.
  return auth.api.updateUser({{ headers: request.headers, body: {{ name: parsed.data }}, asResponse: true }});
}}
'''
        alt_settings = (root / settings_path).read_text(encoding='utf-8')
        alt_settings = f"import {{ DisplayNameForm }} from '@/{component_path[4:-4]}';\n" + alt_settings
        alt_settings = alt_settings.replace('          <dl className="mt-4 space-y-4">', '          <DisplayNameForm initialName={user.name ?? \'\'} />\n          <dl className="mt-4 space-y-4">')
        route_path = 'src/app/api/profile/display-name/route.ts'
        alt = {settings_path: alt_settings, component_path: component, route_path: route, schema_path: schema}
        write_variant('DP03', layout, 'alternative', alt)
        # Faults correspond to declared validation/identity/rendering requirements.
        faults = {
          'fault-no-server-validation': {**ref, action_path: action.replace("displayNameSchema.safeParse(form.get('name'))", "{ success: true, data: String(form.get('name')) }")},
          'fault-no-persistence': {**ref, action_path: action.replace("  await auth.api.updateUser({ headers: await headers(), body: { name: parsed.data } });", "  // Missing persistence: form submits without saving.")},
          'fault-no-ui-refresh': {**alt, component_path: component.replace('router.refresh();', '')},
          'fault-utf16': {**ref, schema_path: schema.replace('[...value].length', 'value.length')},
          'fault-no-trim': {**ref, schema_path: schema.replace('.transform(value => value.trim())', '')},
          'fault-unsafe-name': {**ref, settings_path: settings.replace("<dd className=\"mt-1 rounded-md border px-3 py-2\">{user.name ?? 'Not set'}</dd>", "<dd className=\"mt-1 rounded-md border px-3 py-2\" dangerouslySetInnerHTML={{ __html: user.name ?? 'Not set' }} />")},
        }
        db_imports = "import { db } from '@/database/db';\nimport { user } from '@/database/schema';\nimport { eq } from 'drizzle-orm';\n"
        foreign_write = "  if (typeof body.userId === 'string') await db.update(user).set({ name: parsed.data }).where(eq(user.id, body.userId));\n"
        privileged_write = "  if (typeof body.role === 'string') await db.update(user).set({ role: body.role === 'admin' ? 'admin' : 'user' }).where(eq(user.id, session.user.id));\n"
        marker = '  // Return the original auth response'
        faults['fault-foreign-write'] = {**alt, route_path: db_imports + route.replace(marker, foreign_write + marker)}
        faults['fault-protected-field'] = {**alt, route_path: db_imports + route.replace(marker, privileged_write + marker)}
        assert faults['fault-unsafe-name'][settings_path] != settings
        for variant, files in faults.items():
            write_variant('DP03', layout, variant, files)
    save(HERE / 'solution-inventory.json', active)
    print('References, different valid alternatives, and named faults generated outside agent packages', flush=True)


if __name__ == '__main__':
    main()
