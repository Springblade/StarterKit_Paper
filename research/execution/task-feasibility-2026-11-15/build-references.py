"""Generate small per-task reference candidates; no application baseline changes."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;EX=HERE.parent
moves=json.loads((EX/'layout-manifest.json').read_text(encoding='utf-8'))['moved_files']
base=EX/'layouts'/'feature'
def read(p):return (base/p).read_text(encoding='utf-8')
solutions={}
password_route='''import { auth } from '@/features/auth/lib/auth';
export async function POST(request: Request) {
  if (request.headers.get('origin') !== new URL(request.url).origin) return Response.json({error:'Forbidden'}, {status:403});
  const data = await request.formData();
  const currentPassword=data.get('currentPassword'), newPassword=data.get('newPassword'), confirmation=data.get('confirmation');
  if (typeof currentPassword!=='string' || typeof newPassword!=='string' || newPassword!==confirmation || newPassword.length<8 || newPassword.length>128) return Response.json({error:'Invalid password input'}, {status:400});
  const session=await auth.api.getSession({headers:request.headers,query:{disableCookieCache:true}});
  if (!session) return Response.json({error:'Unauthorized'}, {status:401});
  try {
    const result=await auth.api.changePassword({headers:request.headers,body:{currentPassword,newPassword,revokeOtherSessions:false},asResponse:true});
    if (!result.ok) return Response.json({error:'Password change rejected'}, {status:400});
    const response=Response.redirect(new URL('/dashboard/settings?password=saved',request.url),303);
    const headers=new Headers(response.headers);
    for (const cookie of result.headers.getSetCookie()) headers.append('set-cookie',cookie);
    return new Response(null,{status:303,headers});
  } catch { return Response.json({error:'Password change rejected'}, {status:400}); }
}
'''
settings=read('src/app/dashboard/settings/page.tsx')
start=settings.index('            <a\n');end=settings.index('            </a>',start)+len('            </a>')
settings=settings[:start]+'''            <form action="/api/profile/password" method="post" aria-label="Change password">
              <label htmlFor="current-password">Current password</label>
              <input id="current-password" name="currentPassword" type="password" autoComplete="current-password" required />
              <label htmlFor="new-password">New password</label>
              <input id="new-password" name="newPassword" type="password" autoComplete="new-password" minLength={8} maxLength={128} required />
              <label htmlFor="confirm-password">Confirm password</label>
              <input id="confirm-password" name="confirmation" type="password" autoComplete="new-password" required />
              <button type="submit">Change password</button>
            </form>'''+settings[end:]
solutions['A03']={'src/app/dashboard/settings/page.tsx':settings,'src/app/api/profile/password/route.ts':password_route}

role_route='''import { db } from '@/database/db';
import { user } from '@/database/schema';
import { eq } from 'drizzle-orm';
import { auth } from '@/features/auth/lib/auth';
export async function POST(request: Request) {
  if (request.headers.get('origin') !== new URL(request.url).origin) return Response.json({error:'Forbidden'}, {status:403});
  const session=await auth.api.getSession({headers:request.headers,query:{disableCookieCache:true}});
  if (!session || !('role' in session.user) || session.user.role!=='admin') return Response.json({error:'Forbidden'}, {status:403});
  const data=await request.formData();const userId=data.get('userId'), role=data.get('role');
  if (typeof userId!=='string' || (role!=='user' && role!=='admin')) return Response.json({error:'Invalid role'}, {status:400});
  if (userId===session.user.id && role==='user') return Response.json({error:'Self demotion denied'}, {status:403});
  const changed=await db.update(user).set({role}).where(eq(user.id,userId)).returning({id:user.id});
  if (!changed.length) return Response.json({error:'Not found'}, {status:404});
  return Response.redirect(new URL('/dashboard/admin/users',request.url),303);
}
'''
directory=read('src/app/dashboard/admin/users/page.tsx')
directory=directory.replace('<th className="px-4 py-3 text-left text-sm font-medium">Created</th>','<th className="px-4 py-3 text-left text-sm font-medium">Created</th><th>Change role</th>')
needle='<td className="px-4 py-3 text-sm">{new Date(u.createdAt).toLocaleDateString(\'vi-VN\')}</td>'
assert needle in directory
directory=directory.replace(needle,needle+'''
                <td><form action="/api/admin/role" method="post" aria-label={`Role for ${u.email}`}>
                  <input type="hidden" name="userId" value={u.id} />
                  <label htmlFor={`role-${u.id}`}>Role for {u.email}</label>
                  <select id={`role-${u.id}`} name="role" defaultValue={u.role ?? 'user'}><option value="user">User</option><option value="admin">Admin</option></select>
                  <button type="submit">Save role</button>
                </form></td>''')
solutions['U03']={'src/app/dashboard/admin/users/page.tsx':directory,'src/app/api/admin/role/route.ts':role_route}

detail='''import { eq,sql } from 'drizzle-orm';
import { notFound } from 'next/navigation';
import { db } from '@/database/db';
import { user,session } from '@/database/schema';
import { requireAdmin } from '@/features/auth/lib/auth';
export default async function AccountDetail({params}:{params:Promise<{userId:string}>}) {
 await requireAdmin();const {userId}=await params;
 const record=await db.query.user.findFirst({where:eq(user.id,userId)});if(!record)notFound();
 const [count]=await db.select({n:sql<number>`count(*)::int`}).from(session).where(eq(session.userId,userId));
 if(!count)throw new Error('Missing session count');
 return <section><h2>Account detail</h2><dl>
 <dt>Name</dt><dd>{record.name}</dd><dt>Email</dt><dd>{record.email}</dd><dt>Role</dt><dd>{record.role}</dd>
 <dt>Verified</dt><dd>{record.emailVerified?'Yes':'No'}</dd><dt>Sessions</dt><dd>{count.n}</dd><dt>Created</dt><dd>{record.createdAt.toISOString()}</dd>
 </dl></section>;
}
'''
directory=read('src/app/dashboard/admin/users/page.tsx').replace("import { desc, sql }", "import Link from 'next/link';\nimport { desc, sql }")
directory=directory.replace('{u.email}</td>','<Link href={`/dashboard/admin/users/${u.id}`}>{u.email}</Link></td>')
solutions['U02']={'src/app/dashboard/admin/users/page.tsx':directory,'src/app/dashboard/admin/users/[userId]/page.tsx':detail}

receipt='''import { and,eq } from 'drizzle-orm';
import { db } from '@/database/db';
import { orders } from '@/database/schema';
import { auth } from '@/features/auth/lib/auth';
export async function GET(request:Request,{params}:{params:Promise<{orderId:string}>}) {
 const session=await auth.api.getSession({headers:request.headers});if(!session)return Response.json({error:'Unauthorized'},{status:401});
 const {orderId}=await params;
 const order=await db.query.orders.findFirst({where:and(eq(orders.id,orderId),eq(orders.userId,session.user.id),eq(orders.status,'completed')),with:{plan:true}});
 if(!order || !order.completedAt)return Response.json({error:'Not found'},{status:404});
 return Response.json({code:order.code,plan:{id:order.planId,name:order.plan.name},amountVnd:order.amountVnd,completedAt:order.completedAt.toISOString()},{headers:{'Content-Disposition':'attachment; filename="receipt.json"','Cache-Control':'no-store'}});
}
'''
history=read('src/app/dashboard/billing/history/page.tsx')
history=history.replace('<OrderStatusBadge status={order.status} />','<OrderStatusBadge status={order.status} />{order.status===\'completed\' && <a href={`/api/orders/${order.id}/receipt`} download>Download receipt</a>}')
solutions['B04']={'src/app/dashboard/billing/history/page.tsx':history,'src/app/api/orders/[orderId]/receipt/route.ts':receipt}

billing=read('src/app/dashboard/billing/page.tsx').replace("import { eq }", "import { and, eq }")
billing="import { generatePaymentContent } from '@/features/billing/payment-content';\n"+billing
billing=billing.replace('Promise<{ plan?: string }>','Promise<{ plan?: string; order?:string }>')
billing=billing.replace('  if (selectedPlanId) {','''  if (params.order) {
    const resume=await db.query.orders.findFirst({where:and(eq(orders.id,params.order),eq(orders.userId,userId)),with:{plan:true}});
    if(!resume || resume.status!=='pending' || resume.expiresAt.getTime()<=Date.now()) {
      orderError='This pending order cannot be resumed.';
    } else {
      selectedPlan=resume.plan;
      pendingOrder={orderId:resume.id,code:resume.code,content:generatePaymentContent(resume.code),amountVnd:Number(resume.amountVnd),expiresAt:resume.expiresAt};
    }
  } else if (selectedPlanId) {''')
history=read('src/app/dashboard/billing/history/page.tsx').replace('<OrderStatusBadge status={order.status} />','<OrderStatusBadge status={order.status} />{order.status===\'pending\' && order.expiresAt.getTime()>Date.now() && <Link href={`/dashboard/billing?order=${order.id}`}>Resume payment</Link>}')
solutions['B03']={'src/app/dashboard/billing/page.tsx':billing,'src/app/dashboard/billing/history/page.tsx':history}

for layout in ['feature','layered']:
 for task,files in solutions.items():
  dest=HERE/'solutions'/layout/task/'reference';dest.mkdir(parents=True,exist_ok=True)
  for path,text in files.items():
   if layout=='layered':
    for before,after in sorted(moves.items(),key=lambda kv:-len(kv[0])):
     b='@/'+before.removeprefix('src/').rsplit('.',1)[0];a='@/'+after.removeprefix('src/').rsplit('.',1)[0];text=text.replace("'"+b+"'","'"+a+"'")
   target=dest/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
  manifest={p.relative_to(dest).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.rglob('*') if p.is_file()}
  (dest.parent/'reference-files.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
assert len(solutions)==5
print('Five independent reference candidates per layout; frozen sources untouched.')
