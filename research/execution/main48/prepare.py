"""Construct unsolved packages and qualification candidates. Never invokes models."""
from pathlib import Path
import hashlib,json,shutil,random
import runtime
HERE=Path(__file__).resolve().parent;EX=HERE.parent;PRE=EX/'prepilot-2026-11-12';FEAS=EX/'task-feasibility-2026-11-15'
TASKS=['A01','A04','B05','B06','U02','U03'];CELLS=['S0V0','S0V1','S1V0','S1V1']
MOVES=json.loads((EX/'layout-manifest.json').read_text(encoding='utf-8'))['moved_files']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def write(root,rel,text):p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def copy_source(src,dst):
 for p in src.rglob('*'):
  if p.is_file() and p.relative_to(src).parts[0]=='src':target=dst/p.relative_to(src);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
def visible(task):
 if task=='A04':return (HERE/'visible-auth.cjs').read_text(encoding='utf-8')
 if task in ['B05','B06']:return (HERE/'visible-billing.cjs').read_text(encoding='utf-8')
 return (PRE/'visible-check.cjs').read_text(encoding='utf-8').replace('__TASK__','DP03' if task=='A01' else 'DP02').replace('const page = await context.newPage();','const page = await context.newPage(); page.setDefaultNavigationTimeout(60000);')
def prepare():
 assert not (HERE/'freeze.json').exists(),'Do not rewrite a frozen study'
 cards=json.loads((HERE/'task-cards.json').read_text(encoding='utf-8'))
 for task in TASKS:
  for cell in CELLS:
   layout='feature' if cell[1]=='1' else 'layered';base=PRE/'packages'/'DP03'/('S1V0' if cell[1]=='1' else 'S0V0');target=HERE/'packages'/task/cell
   shutil.copytree(base,target,dirs_exist_ok=True)
   write(target,'.env',runtime.env_text());write(target,'TASK.md',cards[task]+'\n\n'+cards['common']+('\nAdditional visible preservation command: pnpm test:preservation.\n' if cell[-1]=='1' else '\n'))
   package=json.loads((target/'package.json').read_text(encoding='utf-8'))
   if cell[-1]=='1':write(target,'scripts/check-preservation.cjs',visible(task));package['scripts']['test:preservation']=f'CHECK_TASK={task} node scripts/check-preservation.cjs'
   write(target,'package.json',json.dumps(package,indent=2)+'\n');save(target.with_name(cell+'-manifest.json'),{'task':task,'cell':cell,'files':{p.relative_to(target).as_posix():digest(p) for p in target.rglob('*') if p.is_file()}})
 for layout in ['feature','layered']:
  for task in TASKS:
   ref=HERE/'solutions'/layout/task/'reference';alt=ref.with_name('alternative');fault=ref.with_name('fault')
   if task in ['A04','B05','B06']:
    rows=json.loads((FEAS/'replacement-results-1794756305953791300.json').read_text(encoding='utf-8'));row=next(r for r in rows if r['layout']==layout and r['task']==task and r['variant']=='reference');copy_source(Path(row['log']).parent/'overlay'/task/'reference',ref)
   else:copy_source(PRE/'solutions'/'DP03'/layout/'reference' if task=='A01' else FEAS/'solutions'/layout/task/'reference',ref)
   if task in ['A01','U02','U03']:copy_source(PRE/'solutions'/'DP03'/layout/'alternative' if task=='A01' else FEAS/'solutions'/layout/task/'alternative',alt)
   else:copy_source(ref,alt)
   def path(p):return MOVES.get(p,p) if layout=='layered' else p
   if task=='A04':
    p=alt/path('src/features/auth/auth.config.ts');s=p.read_text(encoding='utf-8').replace('minPasswordLength: 12','minPasswordLength: 8')
    s="import { createAuthMiddleware, APIError } from 'better-auth/api';\n"+s
    s=s.replace('  emailAndPassword: {',"  hooks: {before: createAuthMiddleware(async (ctx) => {\n    const password = ctx.path === '/sign-up/email' ? ctx.body?.password : ctx.path === '/reset-password' ? ctx.body?.newPassword : undefined;\n    if (typeof password === 'string' && password.length < 12) throw new APIError('BAD_REQUEST', {message:'Password must be at least 12 characters'});\n  })},\n  emailAndPassword: {");p.write_text(s,encoding='utf-8')
   if task=='B05':
    p=alt/path('src/features/billing/payment-content.ts');s=p.read_text(encoding='utf-8');start=s.index('  const tokens');end=s.index('\n}',start)
    s=s[:start]+"  if ([...content.matchAll(/(?:^|\\s)SK(?=\\s|$)/g)].length !== 1) return null;\n  return /(?:^|\\s)SK\\s+([A-Za-z0-9_-]{5,50})(?=\\s|$)/.exec(content)?.[1] ?? null;"+s[end:];p.write_text(s,encoding='utf-8')
   if task=='B06':
    p=alt/path('src/features/billing/process-order-completion.ts');s=p.read_text(encoding='utf-8');start=s.index('  return db.transaction');s=s[:start]+'''  return db.transaction(async (tx) => {
    await tx.select({id:orders.id}).from(orders).where(eq(orders.code,orderCode)).for('update');
    const clock = await tx.execute<{now:Date}>(sql`SELECT clock_timestamp() AS now`);
    const decisionTime = new Date(clock.rows[0]!.now);
    const updated = await tx.update(orders).set({
      status: sql`CASE WHEN ${orders.expiresAt} <= ${decisionTime} THEN 'expired'::order_status ELSE 'completed'::order_status END`,
      completedAt: sql`CASE WHEN ${orders.expiresAt} <= ${decisionTime} THEN NULL ELSE ${decisionTime}::timestamp END`,
    }).where(and(eq(orders.code,orderCode),eq(orders.status,'pending'),eq(orders.amountVnd,String(transferAmount)))).returning();
    const order = updated[0] ?? (await tx.select().from(orders).where(eq(orders.code,orderCode)).limit(1))[0];
    if (!order) return {status:'ignored',reason:'order_not_found'} as const;
    if (!updated.length && order.status==='pending') return {status:'ignored',reason:'amount_mismatch'} as const;
    await tx.update(paymentTransactions).set({orderId:order.id}).where(eq(paymentTransactions.sepayTransactionId,String(sepayTransactionId)));
    if (updated.length && order.status==='completed') return {status:'completed',orderId:order.id,planId:order.planId,userId:order.userId} as const;
    return {status:'ignored',reason:'order_not_pending'} as const;
  });
}
''';s=s.replace("import { and, eq }","import { and, eq, sql }");p.write_text(s,encoding='utf-8')
   copy_source(ref,fault)
   if task=='A01':copy_source(PRE/'solutions'/'DP03'/layout/'fault-unsafe-name',fault)
   elif task=='A04':p=fault/path('src/features/auth/auth.config.ts');p.write_text(p.read_text(encoding='utf-8').replace('maxPasswordLength: 128','maxPasswordLength: 127'),encoding='utf-8')
   elif task=='B05':p=fault/path('src/features/billing/payment-content.ts');p.write_text(p.read_text(encoding='utf-8').replace('${OrderCodePrefix} ${orderCode}','${OrderCodePrefix} ${orderCode.toLowerCase()}'),encoding='utf-8')
   elif task=='B06':p=fault/path('src/features/billing/process-order-completion.ts');p.write_text(p.read_text(encoding='utf-8').replace('order.expiresAt.getTime() <= decisionTime.getTime()','decisionTime.getTime() > 0'),encoding='utf-8')
   else:
    rel=path('src/features/auth/lib/auth.ts');s=(EX/'layouts'/layout/rel).read_text(encoding='utf-8').replace("if (!isAdmin(session.user as { role?: string | null }))",'if (session.user.id.length === 0)');write(fault,rel,s)
   for variant in ['reference','alternative','fault']:
    root=ref.with_name(variant);save(root.with_name(variant+'-manifest.json'),{p.relative_to(root).as_posix():digest(p) for p in root.rglob('*') if p.is_file()})
 rng=random.Random(20261115);slots=[]
 blocks=[(t,r) for t in TASKS for r in [1,2]];rng.shuffle(blocks)
 for task,rep in blocks:
  cells=CELLS.copy();rng.shuffle(cells)
  for cell in cells:slots.append({'slot':f'{task}-R{rep}-{cell}','task':task,'repetition':rep,'cell':cell})
 save(HERE/'allocation.json',{'seed':20261115,'cap_seconds':900,'model':'gpt-6-luna','reasoning_effort':'high','service_tier':'standard/default (no priority override)','cli_version':'0.166.0','features_disabled':['multi_agent','apps','plugins','memories'],'replacement_attempts':0,'slots':slots})
 print('Prepared 24 unsolved packages, 36 qualification candidates and 48 held slots; no model calls.')
if __name__=='__main__':prepare()
