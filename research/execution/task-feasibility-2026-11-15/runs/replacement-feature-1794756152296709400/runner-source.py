"""Bounded replacement-task probes; no model calls or frozen-source writes."""
from pathlib import Path
import importlib.util,json,hashlib,os,time,sys
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verify',HERE/'verify.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
r=v.runtime
moves=json.loads((HERE.parent/'layout-manifest.json').read_text(encoding='utf-8'))['moved_files']

def main():
 results=[]
 run_id=str(time.time_ns())
 report=HERE/('replacement-results-'+run_id+'.json')
 for layout in ['feature','layered']:
  name='smartkit-replacement-'+layout
  assert not r.docker('ps','-aq','--filter','name=^/'+name+'$',check=False).stdout.strip()
  log=HERE/'runs'/('replacement-'+layout+'-'+str(time.time_ns()));log.mkdir(parents=True)
  def path(p):return moves.get(p,p) if layout=='layered' else p
  def put(p,s):
   local=log/'overlay'/task/variant/p;local.parent.mkdir(parents=True,exist_ok=True);local.write_text(s,encoding='utf-8')
   r.docker('cp',local,name+':/workspace/'+p)
  def original(p):return (v.package(layout)/path(p)).read_text(encoding='utf-8')
  try:
   (log/'runner-source.py').write_bytes(Path(__file__).read_bytes())
   r.start(name,v.package(layout),log)
   r.docker('exec',name,'pnpm','exec','tsx','scripts/ensure-server-only-shim.ts')
   for probe in ['replacement-billing.ts','replacement-auth.cjs']:
    target='scripts/'+probe
    r.docker('cp',HERE/probe,name+':/workspace/'+target)
   # All changed application files remain in this disposable container and its archived overlay.
   for task in (sys.argv[1:] or ['A04','B05','B06']):
    for variant in ['baseline','reference','alternative','fault']:
     if task=='A04':
      config=original('src/features/auth/auth.config.ts')
      if variant!='baseline':config=config.replace('minPasswordLength: 8','minPasswordLength: 12')
      if variant=='alternative':config=config.replace('minPasswordLength: 12','minPasswordLength: 3 * 4')
      if variant=='fault':config=config.replace('maxPasswordLength: 128','maxPasswordLength: 127')
      put(path('src/features/auth/auth.config.ts'),config)
      for page in ['sign-up','reset-password']:
       p=f'src/app/(auth)/auth/{page}/page.tsx';s=original(p)
       if variant!='baseline':s=s.replace('8 characters','12 characters').replace('minLength={8}','minLength={12}').replace('password.length < 8','password.length < 12')
       put(path(p),s)
     if task=='B05':
      p='src/features/billing/payment-content.ts';s=original(p)
      if variant!='baseline':
       start=s.index('  const trimmed');end=s.index('\n}',start)
       body="  const tokens = content.trim().split(/\\s+/);\n  const markers = tokens.flatMap((t,i) => t === OrderCodePrefix ? [i] : []);\n  if (markers.length !== 1) return null;\n  const code = tokens[markers[0]! + 1];\n  return code && /^[A-Za-z0-9_-]{5,50}$/.test(code) ? code : null;"
       if variant=='alternative':body="  const tokens = content.trim().split(/\\s+/);\n  if (tokens.filter(t => t === OrderCodePrefix).length !== 1) return null;\n  const code = tokens[tokens.indexOf(OrderCodePrefix)+1];\n  return code && /^[A-Za-z0-9_-]{5,50}$/.test(code) ? code : null;"
       if variant=='fault':body=body.replace('? code : null','? code.toLowerCase() : null')
       s=s[:start]+body+s[end:]
      put(path(p),s)
     if task=='B06':
      p='src/features/billing/process-order-completion.ts';s=original(p)
      if variant!='baseline':
       s=s.replace("  const orderRows = await db.select().from(orders).where(eq(orders.code, orderCode)).limit(1);","  return db.transaction(async (tx) => {\n  const orderRows = await tx.select().from(orders).where(eq(orders.code, orderCode)).limit(1).for('update');")
       s=s.replace('await db\n','await tx\n')
       needle='  await db.transaction(async (tx) => {'
       expiry="  const decisionTime = new Date();\n  if (order.expiresAt.getTime() <= decisionTime.getTime()) {\n    await tx.update(orders).set({status: 'expired'}).where(eq(orders.id, order.id));\n    await tx.update(paymentTransactions).set({orderId: order.id}).where(eq(paymentTransactions.sepayTransactionId, String(sepayTransactionId)));\n    return {status: 'ignored', reason: 'order_not_pending'} as const;\n  }\n"
       if variant=='alternative':expiry=expiry.replace('order.expiresAt.getTime() <= decisionTime.getTime()','!(order.expiresAt > decisionTime)')
       if variant=='fault':expiry=expiry.replace('order.expiresAt.getTime() <= decisionTime.getTime()','decisionTime.getTime() > 0')
       s=s.replace(needle,expiry)
       s=s.replace("  });\n\n  return { status: 'completed'", "\n  return { status: 'completed'")
       s=s.replace("userId: order.userId };\n}","userId: order.userId } as const;\n  });\n}")
      put(path(p),s)
     # Probe files use canonical feature imports, transformed for the layered layout.
     probe=HERE/('replacement-auth.cjs' if task=='A04' else 'replacement-billing.ts')
     text=probe.read_text(encoding='utf-8')
     if layout=='layered':
      for src,dst in moves.items():text=text.replace('@/ '+src,'@/ '+dst).replace('@/'+src[4:-3],'@/'+dst[4:-3])
     put('scripts/'+probe.name,text)
     cmd=['node','scripts/'+probe.name] if task=='A04' else ['node','--conditions=react-server','--import','tsx','scripts/'+probe.name]
     proc=r.docker('exec','-e','TASK='+task,'-e','VARIANT='+variant,name,*cmd,check=False,timeout=180)
     (log/f'{task}-{variant}.log').write_bytes(proc.stdout)
     # V0 is the unchanged basic suite; preservation probe is reported separately.
     basic=r.docker('exec',name,'pnpm','test:run',check=False,timeout=180)
     (log/f'{task}-{variant}-basic.log').write_bytes(basic.stdout)
     tc=r.docker('exec',name,'pnpm','check-types',check=False,timeout=180)
     (log/f'{task}-{variant}-types.log').write_bytes(tc.stdout)
     row={'probe_sha256':hashlib.sha256(text.encode()).hexdigest(),'layout':layout,'task':task,'variant':variant,'probe_exit':proc.returncode,'basic_exit':basic.returncode,'type_exit':tc.returncode,'log':str(log/f'{task}-{variant}.log'),'model_calls':0}
     results.append(row);print(json.dumps(row),flush=True)
     report.write_text(json.dumps(results,indent=2),encoding='utf-8')
    # Reset this task before moving to the next task.
    paths={'A04':['src/features/auth/auth.config.ts','src/app/(auth)/auth/sign-up/page.tsx','src/app/(auth)/auth/reset-password/page.tsx'],'B05':['src/features/billing/payment-content.ts'],'B06':['src/features/billing/process-order-completion.ts']}[task]
    for p in paths:put(path(p),original(p))
  finally:r.stop(name,log)
 # The suite is a bounded qualification experiment, never an automatic release signal.
 assert len(results)==8*len(sys.argv[1:] or ['A04','B05','B06'])

if __name__=='__main__':main()
