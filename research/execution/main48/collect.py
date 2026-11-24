"""Collection entry point: audit/rehearsal by default; run needs a frozen author release."""
from pathlib import Path
import argparse,json,os,subprocess,tarfile,time,tempfile,shutil,queue,threading
from prepare import HERE,TASKS,CELLS,digest,save
import runtime

def read_quota():
 # Account status RPCs create no model thread or turn.
 process=subprocess.Popen([shutil.which('codex'),'app-server','--stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
 messages=queue.Queue()
 def receive():
  for line in process.stdout:
   try:messages.put(json.loads(line))
   except json.JSONDecodeError:pass
 threading.Thread(target=receive,daemon=True).start()
 def request(method,ident,params=None):
  value={'method':method,'id':ident}
  if params is not None:value['params']=params
  process.stdin.write(json.dumps(value)+'\n');process.stdin.flush();deadline=time.monotonic()+25
  while time.monotonic()<deadline:
   try:message=messages.get(timeout=max(.01,deadline-time.monotonic()))
   except queue.Empty:break
   if message.get('id')==ident:
    if 'error' in message:raise RuntimeError('Account quota preflight RPC failed; no slot invoked')
    return message['result']
  raise RuntimeError('Account quota preflight timed out; no slot invoked')
 try:
  request('initialize',1,{'clientInfo':{'name':'main48-quota-preflight','version':'1.0'}})
  process.stdin.write('{"method":"initialized"}\n');process.stdin.flush()
  result=request('account/rateLimits/read',2)
  buckets=result.get('rateLimitsByLimitId') or {'default':result.get('rateLimits')}
  return {'checked':runtime.stamp(),'buckets':{k:{field:v.get(field) for field in ['limitId','normalModelSlug','primary','secondary','rateLimitReachedType','spendControlReached']} for k,v in buckets.items() if v},'model_calls':0}
 finally:
  process.terminate()
  try:process.wait(timeout=5)
  except subprocess.TimeoutExpired:process.kill();process.wait()

def require_quota(snapshot,model):
 buckets=[b for b in snapshot['buckets'].values() if b.get('normalModelSlug') in [None,model]]
 if not buckets:raise RuntimeError('Target quota unavailable; no slot invoked')
 for bucket in buckets:
  if not any(isinstance((bucket.get(w) or {}).get('usedPercent'),(int,float)) for w in ['primary','secondary']) and not bucket.get('rateLimitReachedType') and not bucket.get('spendControlReached'):
   raise RuntimeError('Target quota measurement unavailable; no slot invoked')
  if bucket.get('rateLimitReachedType') or bucket.get('spendControlReached') or any((bucket.get(w) or {}).get('usedPercent',0)>=100 for w in ['primary','secondary']):
   raise RuntimeError('Account quota exhausted; wait for reset, then resume unstarted slots only')

def audit():
 frozen=json.loads((HERE/'freeze.json').read_text(encoding='utf-8'))
 assert frozen.get('technical_ready') is True
 for rel,expected in frozen['files'].items():assert digest(HERE/rel)==expected,'Changed frozen file: '+rel
 assert json.loads(runtime.docker('image','inspect',runtime.IMAGE).stdout)[0]['Id']==frozen['image_id']
 allocation=json.loads((HERE/'allocation.json').read_text(encoding='utf-8'));assert len(allocation['slots'])==48
 return frozen,allocation

def capture(name,folder,head):
 # Quiesce every process in this disposable app container before capturing code;
 # a model's background shell must not keep editing after its session ends.
 quiesce="const f=require('fs');for(const p of f.readdirSync('/proc'))if(/^\\d+$/.test(p)&&+p>1&&+p!==process.pid){try{process.kill(+p,'SIGKILL')}catch{}}"
 runtime.docker('exec',name,'node','-e',quiesce)
 runtime.docker('exec',name,'git','add','-N','.')
 (folder/'patch.diff').write_bytes(runtime.docker('exec',name,'git','diff','--binary',head).stdout)
 runtime.docker('exec',name,'tar','-czf','/tmp/final-workspace.tgz','--exclude=./node_modules','--exclude=./.next','--exclude=./.git','--exclude=./.env','--exclude=./tsconfig.tsbuildinfo','-C','/workspace','.')
 runtime.docker('cp',name+':/tmp/final-workspace.tgz',folder/'final-workspace.tgz')
 output=folder/'final-workspace';output.mkdir()
 with tarfile.open(folder/'final-workspace.tgz') as archive:archive.extractall(output,filter='data')
 return output

def rehearsal_binding(task,cell):
 hidden=HERE/('hidden-profile.cjs' if task=='A01' else 'hidden-auth.cjs' if task=='A04' else 'hidden-billing.cjs' if task in ['B05','B06'] else 'hidden-admin.cjs')
 layout='feature' if cell[1]=='1' else 'layered'
 return {'collector':digest(HERE/'collect.py'),'runtime':digest(HERE/'runtime.py'),'mock':digest(HERE/'mock-sepay.cjs'),'hidden':digest(hidden),'package':digest((HERE/'packages'/task/cell).with_name(cell+'-manifest.json')),'solution':digest((HERE/'solutions'/layout/task/'reference').with_name('reference-manifest.json')),'image':json.loads(runtime.docker('image','inspect',runtime.IMAGE).stdout)[0]['Id']}

def qualified_reference_v0(workspace,task,cell):
 # Rehearsals may reuse full V0 only when capture exactly equals a previously
 # qualified reference. Arbitrary model output always executes V0 afresh.
 layout='feature' if cell[1]=='1' else 'layered';source=HERE/'solutions'/layout/task/'reference'
 required={'image_id':json.loads(runtime.docker('image','inspect',runtime.IMAGE).stdout)[0]['Id'],'runtime':digest(HERE/'runtime.py'),'mock':digest(HERE/'mock-sepay.cjs'),'solution':digest(source.with_name('reference-manifest.json')),'candidate_setup':'pre-overlaid-start-v1'}
 row=None;p=None
 for candidate in (HERE/'qualification').glob(f'ledger-{task}-{layout}-reference-*.json'):
  value=json.loads(candidate.read_text())
  if value.get('passed') and value.get('cleanup_volumes_removed') and all(value.get('binding',{}).get(k)==v for k,v in required.items()) and all(value.get('basic',{}).get(c)==0 for c in ['check-types','test:run','test:billing','test:sepay-qr-url','build']):row=value;p=candidate;break
 if row is None:return None
 original=HERE/'packages'/task/cell
 excluded={'.env','TASK.md','scripts/check-preservation.cjs'}
 expected={p.relative_to(original).as_posix():digest(p) for p in original.rglob('*') if p.is_file() and p.relative_to(original).as_posix() not in excluded}
 expected.update({p.relative_to(source).as_posix():digest(p) for p in source.rglob('*') if p.is_file()})
 actual={p.relative_to(workspace).as_posix():digest(p) for p in workspace.rglob('*') if p.is_file() and p.relative_to(workspace).as_posix() not in excluded}
 generated=workspace/'next-env.d.ts'
 if generated.exists() and generated.read_text(encoding='utf-8').replace('.next/dev/types/','.next/types/')==(original/'next-env.d.ts').read_text(encoding='utf-8'):actual['next-env.d.ts']=expected['next-env.d.ts']
 if actual!=expected:return None
 commands=['check-types','test:run','test:billing','test:sepay-qr-url','build']
 return {'ledger':str(p),'commands':row['basic']} if all(row.get('basic',{}).get(c)==0 for c in commands) else None

def score(workspace,task,cell,folder,rehearsal=False):
 from qualify import read_result
 name='smartkit-score-'+str(time.time_ns())[-12:];folder.mkdir(parents=True)
 result={'task':task,'cell':cell,'completed':False,'model_calls':0}
 try:
  # Trusted starting checks and runtime are reconstructed outside the model workspace.
  with tempfile.TemporaryDirectory(prefix='smartkit-score-') as tmp:
   assert Path(tmp).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve())
   package=Path(tmp)/'workspace';shutil.copytree(HERE/'packages'/task/cell,package)
   immutable={'package.json','pnpm-lock.yaml','.env','AGENTS.md','TASK.md','vitest.config.ts','scripts/check-preservation.cjs'}
   immutable.update(p.relative_to(package).as_posix() for p in (package/'src/tests').rglob('*') if p.is_file())
   immutable.update(p.relative_to(package).as_posix() for p in (package/'scripts').rglob('*') if p.is_file() and (p.name.startswith(('test-','check-','ensure-server-only')) or 'server-only-shim' in p.parts))
   for p in workspace.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(workspace)
    # Restore trusted checks while retaining arbitrary new helpers and application files.
    if rel.as_posix() not in immutable and rel.parts[0] not in {'.git','.next','node_modules'}:
     target=package/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
   original=HERE/'packages'/task/cell
   for p in (original/'src').rglob('*'):
    if p.is_file() and p.relative_to(original).parts[1]!='tests' and not (workspace/p.relative_to(original)).exists():(package/p.relative_to(original)).unlink(missing_ok=True)
   expected=json.loads((original/'package.json').read_text());actual=json.loads((workspace/'package.json').read_text())
   result['forbidden_dependency_changes']=[key for key in ['dependencies','devDependencies','optionalDependencies','overrides','packageManager'] if actual.get(key)!=expected.get(key)]
   result['lockfile_changed']=(workspace/'pnpm-lock.yaml').exists() and (workspace/'pnpm-lock.yaml').read_bytes()!=(original/'pnpm-lock.yaml').read_bytes()
   runtime.start(name,package,folder)
  runtime.docker('exec',name,'mkdir','-p','/evaluator')
  hidden=HERE/('hidden-profile.cjs' if task=='A01' else 'hidden-auth.cjs' if task=='A04' else 'hidden-billing.cjs' if task in ['B05','B06'] else 'hidden-admin.cjs')
  runtime.docker('cp',hidden,name+':/evaluator/hidden.cjs')
  from prepare import visible
  check=folder/'visible-source.cjs';check.write_text(visible(task),encoding='utf-8');runtime.docker('cp',check,name+':/evaluator/visible.cjs')
  for suite,cmd in [('V1',['node','/evaluator/visible.cjs']),('E',['node','/evaluator/hidden.cjs'])]:
   target=folder/(suite+'.json');p=runtime.docker('exec','-e','CHECK_TASK='+('DP03' if task=='A01' and suite=='E' else task),'-e','CHECK_OUTPUT=/evaluator/'+suite+'.json',name,*cmd,check=False,timeout=300)
   (folder/(suite+'.log')).write_bytes(p.stdout)
   runtime.docker('cp',name+':/evaluator/'+suite+'.json',target);result[suite]=read_result(p,target)
  reused=qualified_reference_v0(workspace,task,cell) if rehearsal else None
  result['V0']=reused['commands'] if reused else {}
  if reused:result['V0_reused_from']=reused['ledger']
  for command in ([] if reused else ['test:billing','test:sepay-qr-url','check-types','test:run','build']):
   if command=='check-types':
    stop="const f=require('fs');for(const p of f.readdirSync('/proc'))if(/^\\d+$/.test(p)&&+p!==process.pid){try{if(f.readFileSync('/proc/'+p+'/comm','utf8').startsWith('next-server'))process.kill(+p,'SIGTERM')}catch{}}"
    runtime.docker('exec',name,'node','-e',stop)
   p=runtime.docker('exec','-e','TEST_BASE_URL=http://localhost:3107','-e','SEPAY_BANK_ACCOUNT=0010000000000','-e','SEPAY_BANK_NAME=Vietcombank',name,'pnpm',command,check=False,timeout=300)
   (folder/('V0-'+command.replace(':','-')+'.log')).write_bytes(p.stdout);result['V0'][command]=p.returncode
  result['completed']=True;result['assessable']=result['E'].get('assessable',True) and not result['lockfile_changed']
  result['jointSuccess']=result['E'].get('jointSuccess',False) and all(x==0 for x in result['V0'].values()) and not result['forbidden_dependency_changes']
  return result
 finally:runtime.stop(name,folder);save(folder/'outcome.json',result)

def rehearse(layout=None):
 # One complete capture/reset/score case for each of the 24 treatment packages.
 ledger=HERE/('rehearsal-'+layout+'.json' if layout else 'rehearsal.json');results=json.loads(ledger.read_text(encoding='utf-8')) if ledger.exists() else {}
 for task in TASKS:
  for cell in CELLS:
   if layout and (cell[1]=='1')!=(layout=='feature'):continue
   key=task+'/'+cell
   binding=rehearsal_binding(task,cell)
   if results.get(key,{}).get('passed') and results[key].get('binding')==binding:continue
   folder=HERE/'rehearsal'/(task+'-'+cell+'-'+str(time.time_ns()));folder.mkdir(parents=True);name='smartkit-rehearse-'+str(time.time_ns())[-12:]
   try:
    head=runtime.start(name,HERE/'packages'/task/cell,folder)
    probe="const f=require('fs');for(const p of ['/opt/codex-home/auth.json','/root/.codex/auth.json','/evaluator','/research','/workspace/solutions'])if(f.existsSync(p))process.exit(1)"
    runtime.docker('exec',name,'node','-e',probe)
    source=HERE/'solutions'/('feature' if cell[1]=='1' else 'layered')/task/'reference';runtime.docker('cp',str(source)+os.sep+'.',name+':/workspace/')
    workspace=capture(name,folder,head)
   finally:runtime.stop(name,folder)
   outcome=score(workspace,task,cell,folder/'score',rehearsal=True);assert outcome['jointSuccess'],outcome
   results[key]={'passed':True,'binding':binding,'kind':'no-model-reference-capture-reset-score','folder':str(folder),'model_calls':0};save(ledger,results);print('Rehearsal passed '+key,flush=True)

def next_slot(root,slot):
 path=root/slot/'attempt.json'
 if path.exists() and json.loads(path.read_text(encoding='utf-8')).get('invoked'):return None
 return path

def rescore(slot):
 allocation=json.loads((HERE/'allocation.json').read_text(encoding='utf-8'))['slots'];assigned=next(x for x in allocation if x['slot']==slot)
 folder=HERE/'runs'/slot;record=folder/'attempt.json';attempt=json.loads(record.read_text(encoding='utf-8'))
 assert attempt.get('invoked') and (folder/'final-workspace').is_dir(),'Only an existing saved attempt can be rescored'
 output=folder/('scoring-'+str(time.time_ns()));outcome=score(folder/'final-workspace',assigned['task'],assigned['cell'],output)
 if attempt.get('outcome'):attempt.setdefault('score_history',[]).append(attempt['outcome'])
 if attempt.get('generation_requires_adjudication'):outcome['assessable']=False;outcome['generation_requires_adjudication']=True
 outcome['scoring_folder']=str(output);attempt.update(outcome=outcome,status='scored' if outcome.get('assessable',True) else 'scored-needs-adjudication');save(record,attempt)
 print('Replayed the saved patch only; no model invocation.')

def run():
 frozen,allocation=audit()
 release=json.loads((HERE/'author-release.json').read_text(encoding='utf-8'))
 assert release.get('approved') is True and release.get('freeze_sha256')==digest(HERE/'freeze.json'),'Author release is absent or stale'
 assert release.get('scope')=='one-48-slot-collection-no-replacements'
 auth=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'auth.json'
 account=json.loads(auth.read_text(encoding='utf-8'));assert account.get('auth_mode')=='chatgpt' and not account.get('OPENAI_API_KEY'),'Existing ChatGPT allowance only'
 for slot in allocation['slots']:
  record=next_slot(HERE/'runs',slot['slot'])
  if record is None:continue
  audit()
  quota=read_quota();require_quota(quota,allocation['model'])
  folder=record.parent;folder.mkdir(parents=True,exist_ok=True);name='smartkit-main-'+slot['slot'].lower();attempt={'slot':slot,'invoked':False,'status':'preparing','configuration':frozen['configuration'],'quota_preflight':quota};save(record,attempt)
  workspace=None
  try:
   head=runtime.start(name,HERE/'packages'/slot['task']/slot['cell'],folder)
   runtime.docker('exec',name,'mkdir','-p','/opt/codex-home');runtime.docker('cp',auth,name+':/opt/codex-home/auth.json')
   command=['docker','exec','-e','CODEX_HOME=/opt/codex-home',name,'codex','exec','--ignore-user-config','--ignore-rules','--ephemeral','--dangerously-bypass-approvals-and-sandbox','-m',allocation['model'],'-c','model_reasoning_effort="high"','--disable','multi_agent','--disable','apps','--disable','plugins','--disable','memories','--json','--output-last-message','/tmp/final-message.txt','Read TASK.md and implement its requirement. Use available checks as appropriate. Do not invoke another model or launch a nested coding-agent session.']
   attempt.update(invoked=True,status='running',started=runtime.stamp());save(record,attempt);began=time.monotonic()
   with (folder/'events.jsonl').open('wb') as stream:
    process=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    while process.poll() is None:
     if time.monotonic()-began>=900:
      runtime.docker('exec',name,'pkill','-f','codex exec',check=False);process.kill();process.wait();attempt['timeout']=True;break
     time.sleep(.5)
   attempt.update(elapsed_seconds=time.monotonic()-began,returncode=process.returncode,status='awaiting-scoring')
   events=[]
   for line in (folder/'events.jsonl').read_text(encoding='utf-8',errors='replace').splitlines():
    try:events.append(json.loads(line))
    except json.JSONDecodeError:pass
   attempt['completed_turns']=sum(e.get('type')=='turn.completed' for e in events)
   attempt['usage_events']=[e['usage'] for e in events if e.get('type')=='turn.completed' and isinstance(e.get('usage'),dict)]
   attempt['generation_requires_adjudication']=not(attempt.get('timeout') or (attempt['completed_turns']>0 and process.returncode==0))
   # No authentication files are included in capture or scoring.
   runtime.docker('exec',name,'rm','-f','/opt/codex-home/auth.json')
   runtime.docker('cp',name+':/tmp/final-message.txt',folder/'final-message.txt',check=False);workspace=capture(name,folder,head);save(record,attempt)
  except Exception as e:attempt.update(status='infrastructure-or-execution-error',errorClass=type(e).__name__);save(record,attempt)
  finally:runtime.stop(name,folder)
  if workspace:
   try:
    outcome=score(workspace,slot['task'],slot['cell'],folder/('scoring-'+str(time.time_ns())))
    if attempt.get('generation_requires_adjudication'):outcome['assessable']=False;outcome['generation_requires_adjudication']=True
    attempt.update(status='scored' if outcome.get('assessable',True) else 'scored-needs-adjudication',outcome=outcome)
   except Exception as e:attempt.update(status='scoring-error-retry-same-patch-only',errorClass=type(e).__name__)
   save(record,attempt)
  if attempt['status']!='scored':raise RuntimeError('Stopped for recorded infrastructure adjudication; never repeat an invoked slot')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['audit','rehearse','rescore','run']);ap.add_argument('--layout',choices=['feature','layered']);ap.add_argument('--slot');a=ap.parse_args()
 if a.action=='audit':audit();print('Frozen audit passed; no model calls')
 elif a.action=='rehearse':rehearse(a.layout)
 elif a.action=='rescore':assert a.slot;rescore(a.slot)
 else:run()
if __name__=='__main__':main()
