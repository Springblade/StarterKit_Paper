"""Alternative implementations and seeded faulty candidates for measurement checks."""
from pathlib import Path
import json,hashlib,shutil
HERE=Path(__file__).resolve().parent
for layout in ['feature','layered']:
 for task in ['A03','B03','B04','U02','U03']:
  reference=HERE/'solutions'/layout/task/'reference'
  alt=reference.with_name('alternative');alt.mkdir(parents=True,exist_ok=True)
  for p in reference.rglob('*'):
   if p.is_file():
    target=alt/p.relative_to(reference);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
  if task=='U03':
   path='src/app/api/admin/role/route.ts';p=alt/path;s=p.read_text()
   start=s.index('  const changed=');end=s.index("  return Response.redirect",start)
   s=s[:start]+'''  const upstream=await auth.handler(new Request(new URL('/api/auth/admin/set-role',request.url),{method:'POST',headers:{'Content-Type':'application/json',Origin:new URL(request.url).origin,Cookie:request.headers.get('cookie')??''},body:JSON.stringify({userId,role})}));
  if (!upstream.ok) return Response.json({error:'Role change rejected'},{status:upstream.status});
'''+s[end:];p.write_text(s)
   faults=[('fault-cached-role',path,"query:{disableCookieCache:true}","query:{disableCookieCache:false}"),('fault-self-demotion',path,"  if (userId===session.user.id && role==='user') return Response.json({error:'Self demotion denied'}, {status:403});\n",'')]
  elif task=='A03':
   path='src/app/api/profile/password/route.ts';p=alt/path;s=p.read_text()
   s=s.replace("const result=await auth.api.changePassword({headers:request.headers,body:{currentPassword,newPassword,revokeOtherSessions:false},asResponse:true});", "const result=await auth.handler(new Request(new URL('/api/auth/change-password',request.url),{method:'POST',headers:{'Content-Type':'application/json',Origin:new URL(request.url).origin,Cookie:request.headers.get('cookie')??''},body:JSON.stringify({currentPassword,newPassword,revokeOtherSessions:false})}));")
   p.write_text(s);faults=[('fault-confirmation',path,'newPassword!==confirmation || ','')]
  elif task=='B04':
   path='src/app/api/orders/[orderId]/receipt/route.ts';p=alt/path;s=p.read_text().replace('import { orders }','import { orders,plans }')
   old="const order=await db.query.orders.findFirst({where:and(eq(orders.id,orderId),eq(orders.userId,session.user.id),eq(orders.status,'completed')),with:{plan:true}});"
   new="const rows=await db.select({order:orders,plan:plans}).from(orders).innerJoin(plans,eq(orders.planId,plans.id)).where(and(eq(orders.id,orderId),eq(orders.userId,session.user.id),eq(orders.status,'completed'))).limit(1);\n const order=rows[0]?{...rows[0].order,plan:rows[0].plan}:undefined;"
   assert old in s;s=s.replace(old,new);p.write_text(s)
   faults=[('fault-foreign-receipt',path,'eq(orders.userId,session.user.id),','')]
  elif task=='U02':
   path='src/app/dashboard/admin/users/[userId]/page.tsx';p=alt/path;s=p.read_text().replace("where:eq(user.id,userId)}","where:eq(user.id,userId),with:{sessions:{columns:{id:true}}}}")
   old='const [count]=await db.select({n:sql<number>`count(*)::int`}).from(session).where(eq(session.userId,userId));';assert old in s;s=s.replace(old,'const count={n:record.sessions.length};');p.write_text(s)
   faults=[('fault-no-admin-guard',path,'requireAdmin','requireAuth')]
  else:
   path='src/app/dashboard/billing/page.tsx';p=alt/path;s=p.read_text()
   old="const resume=await db.query.orders.findFirst({where:and(eq(orders.id,params.order),eq(orders.userId,userId)),with:{plan:true}});"
   new="const rows=await db.select({order:orders,plan:plans}).from(orders).innerJoin(plans,eq(orders.planId,plans.id)).where(and(eq(orders.id,params.order),eq(orders.userId,userId))).limit(1);\n    const resume=rows[0]?{...rows[0].order,plan:rows[0].plan}:undefined;"
   assert old in s;s=s.replace(old,new);p.write_text(s)
   faults=[('fault-foreign-resume',path,'eq(orders.userId,userId)','eq(orders.userId,orders.userId)')]
  for name,path,before,after in faults:
   dest=reference.with_name(name);dest.mkdir(parents=True,exist_ok=True)
   for p in reference.rglob('*'):
    if p.is_file():
     target=dest/p.relative_to(reference);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
   p=dest/path;s=p.read_text();assert before in s;(p).write_text(s.replace(before,after))
  for folder in [alt]+[reference.with_name(x[0]) for x in faults]:
   manifest={p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()};folder.with_name(folder.name+'-files.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Five alternatives and six named fault variants per layout; independent fixtures required.')
