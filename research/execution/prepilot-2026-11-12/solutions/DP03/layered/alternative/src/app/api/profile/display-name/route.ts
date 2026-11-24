import { auth } from '@/lib/auth/auth';
import { displayNameSchema } from '@/types/auth/profile';

export async function POST(request: Request) {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 });
  let body;
  try { body = await request.json(); } catch { return Response.json({ error: 'Invalid JSON' }, { status: 400 }); }
  const parsed = displayNameSchema.safeParse(body?.name);
  if (!parsed.success) return Response.json({ error: 'Invalid display name' }, { status: 400 });
  // Return the original auth response, including Set-Cookie, to this browser.
  return auth.api.updateUser({ headers: request.headers, body: { name: parsed.data }, asResponse: true });
}
