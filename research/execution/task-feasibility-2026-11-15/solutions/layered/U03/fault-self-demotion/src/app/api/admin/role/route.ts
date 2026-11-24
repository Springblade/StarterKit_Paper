import { db } from '@/database/db';
import { user } from '@/database/schema';
import { eq } from 'drizzle-orm';
import { auth } from '@/lib/auth/auth';
export async function POST(request: Request) {
  if (request.headers.get('origin') !== new URL(request.url).origin) return Response.json({error:'Forbidden'}, {status:403});
  const session=await auth.api.getSession({headers:request.headers,query:{disableCookieCache:true}});
  if (!session || !('role' in session.user) || session.user.role!=='admin') return Response.json({error:'Forbidden'}, {status:403});
  const data=await request.formData();const userId=data.get('userId'), role=data.get('role');
  if (typeof userId!=='string' || (role!=='user' && role!=='admin')) return Response.json({error:'Invalid role'}, {status:400});
  const changed=await db.update(user).set({role}).where(eq(user.id,userId)).returning({id:user.id});
  if (!changed.length) return Response.json({error:'Not found'}, {status:404});
  return Response.redirect(new URL('/dashboard/admin/users',request.url),303);
}
