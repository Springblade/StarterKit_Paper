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
  if (userId===session.user.id && role==='user') return Response.json({error:'Self demotion denied'}, {status:403});
  const upstream=await auth.handler(new Request(new URL('/api/auth/admin/set-role',request.url),{method:'POST',headers:{'Content-Type':'application/json',Origin:new URL(request.url).origin,Cookie:request.headers.get('cookie')??''},body:JSON.stringify({userId,role})}));
  if (!upstream.ok) return Response.json({error:'Role change rejected'},{status:upstream.status});
  return Response.redirect(new URL('/dashboard/admin/users',request.url),303);
}
