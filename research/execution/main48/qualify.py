"""Real-transport qualification, with resumable evidence; never invokes models."""
import argparse,json,time,os,shutil,tempfile
from pathlib import Path
import runtime
from prepare import HERE,PRE,TASKS,digest,save

def read_result(p,path):
 value=json.loads(path.read_text(encoding='utf-8'));assert value.get('completed'),value
 emitted=json.loads(next(line for line in reversed(p.stdout.decode(errors='replace').splitlines()) if line.startswith('{')))
 assert emitted==value,'Stale or inconsistent evaluator output'
 assert p.returncode in [0,1],p.returncode
 return value
def qualify(task,layout,variant,visible_rounds,hidden_rounds,basic):
 cell='S1V1' if layout=='feature' else 'S0V1';package=HERE/'packages'/task/cell
 src=HERE/'solutions'/layout/task/variant
 hidden=HERE/'hidden-profile.cjs' if task=='A01' else HERE/('hidden-auth.cjs' if task=='A04' else 'hidden-billing.cjs' if task in ['B05','B06'] else 'hidden-admin.cjs')
 binding={'image_id':json.loads(runtime.docker('image','inspect',runtime.IMAGE).stdout)[0]['Id'],'package':digest(package.with_name(cell+'-manifest.json')),'hidden':digest(hidden),'visible':digest(package/'scripts/check-preservation.cjs'),'runtime':digest(HERE/'runtime.py'),'mock':digest(HERE/'mock-sepay.cjs'),'solution':digest(src.with_name(variant+'-manifest.json')) if variant!='baseline' else None,'visible_rounds':visible_rounds,'hidden_rounds':hidden_rounds,'basic':basic}
 if variant!='baseline':binding['candidate_setup']='pre-overlaid-start-v1'
 key=f'{task}-{layout}-{variant}-V{visible_rounds}-E{hidden_rounds}-B{int(basic)}';ledger=HERE/'qualification'/('ledger-'+key+'.json')
 if ledger.exists():
  prior=json.loads(ledger.read_text(encoding='utf-8'))
  if prior.get('binding')==binding and prior.get('passed') and prior.get('cleanup_volumes_removed'):print('Already qualified: '+key,flush=True);return prior
 folder=HERE/'qualification'/(key+'-'+str(time.time_ns()));folder.mkdir(parents=True);name='smartkit-mainqual-'+str(time.time_ns())[-12:]
 result={'task':task,'layout':layout,'variant':variant,'binding':binding,'folder':str(folder),'visible':[],'hidden':[],'basic':{},'model_calls':0,'passed':False}
 shutil.copyfile(hidden,folder/'hidden-source.cjs');shutil.copyfile(package/'scripts/check-preservation.cjs',folder/'visible-source.cjs')
 assert digest(folder/'hidden-source.cjs')==binding['hidden'] and digest(folder/'visible-source.cjs')==binding['visible']
 volumes=[]
 try:
  if variant=='baseline':runtime.start(name,package,folder)
  else:
   shutil.copytree(src,folder/'solution')
   with tempfile.TemporaryDirectory(prefix='smartkit-qualified-source-') as tmp:
    assert Path(tmp).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve())
    staged=Path(tmp)/'workspace';shutil.copytree(package,staged);shutil.copytree(src,staged,dirs_exist_ok=True)
    runtime.start(name,staged,folder)
  volumes=[x['Name'] for x in json.loads(runtime.docker('inspect',name+'-db').stdout)[0]['Mounts'] if x['Type']=='volume']
  runtime.docker('exec',name,'mkdir','-p','/evaluator');runtime.docker('cp',folder/'hidden-source.cjs',name+':/evaluator/final.cjs');runtime.docker('cp',folder/'visible-source.cjs',name+':/evaluator/visible.cjs')
  for suite,count,cmd in [('visible',visible_rounds,['node','/evaluator/visible.cjs']),('hidden',hidden_rounds,['node','/evaluator/final.cjs'])]:
   for i in range(count):
    output=f'/evaluator/{suite}-{i:02}.json';p=runtime.docker('exec','-e','CHECK_TASK='+('DP03' if task=='A01' and suite=='hidden' else task),'-e','CHECK_OUTPUT='+output,name,*cmd,check=False,timeout=300)
    (folder/f'{suite}-{i:02}.log').write_bytes(p.stdout);target=folder/f'{suite}-{i:02}.json';runtime.docker('cp',name+':'+output,target)
    value=read_result(p,target);result[suite].append(value)
    if variant in ['baseline','reference','alternative']:
     assert (value.get('pass') if suite=='visible' else value.get('preservation')),value
     if suite=='hidden':assert value.get('acceptance')==(variant!='baseline'),value
    elif suite=='visible':assert value.get('pass') is False,'Shared regression escaped visible suite'
    else:assert value.get('preservation') is False,'Shared regression escaped hidden old-behavior checks'
    save(folder/'summary.json',result)
    print(json.dumps({'task':task,'layout':layout,'variant':variant,'suite':suite,'round':i+1,'expected_outcome_observed':True}),flush=True)
  if basic:
   # Reuse a completed full-V0 execution only for the identical image, runtime,
   # starting package and candidate. Reliability repetitions do not need new builds.
   prior_basic=None
   for path in (HERE/'qualification').glob(f'ledger-{task}-{layout}-{variant}-*.json'):
    prior=json.loads(path.read_text(encoding='utf-8'))
    comparable={k:v for k,v in binding.items() if k in ['image_id','package','runtime','mock','solution','candidate_setup']}
    if prior.get('passed') and all(prior.get('binding',{}).get(k)==v for k,v in comparable.items()) and all(prior.get('basic',{}).get(c)==0 for c in ['check-types','test:run','test:billing','test:sepay-qr-url','build']):
     # A mutable ledger can be replaced by this same case; retain its immutable run summary.
     prior_basic=Path(prior['folder'])/'summary.json';break
   if prior_basic:
    result['basic']=json.loads(prior_basic.read_text(encoding='utf-8'))['basic'];result['basic_reused_from']=str(prior_basic)
   else:
    for command in ['test:billing','test:sepay-qr-url','check-types','test:run','build']:
     if command=='check-types':
      # HTTP checks are finished; stop dev writes before reading generated types and building.
      stop="const f=require('fs');for(const p of f.readdirSync('/proc'))if(/^\\d+$/.test(p)&&+p!==process.pid){try{if(f.readFileSync('/proc/'+p+'/comm','utf8').startsWith('next-server'))process.kill(+p,'SIGTERM')}catch{}}"
      runtime.docker('exec',name,'node','-e',stop)
     p=runtime.docker('exec','-e','TEST_BASE_URL=http://localhost:3107','-e','SEPAY_BANK_ACCOUNT=0010000000000','-e','SEPAY_BANK_NAME=Vietcombank',name,'pnpm',command,check=False,timeout=300)
     (folder/(command.replace(':','-')+'.log')).write_bytes(p.stdout);result['basic'][command]=p.returncode;save(folder/'summary.json',result)
     assert p.returncode==0,(task,layout,variant,command)
  result['passed']=True;save(ledger,result);return result
 finally:
  runtime.stop(name,folder);result['cleanup_volumes_removed']=all(runtime.docker('volume','inspect',x,check=False).returncode!=0 for x in volumes)
  assert result['cleanup_volumes_removed'];save(folder/'summary.json',result)
  if result['passed']:save(ledger,result)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--task',choices=TASKS);ap.add_argument('--layout',choices=['feature','layered'],required=True);ap.add_argument('--variant',choices=['baseline','reference','alternative','fault']);ap.add_argument('--basic',action='store_true');ap.add_argument('--all-smoke',action='store_true');ap.add_argument('--reliability',action='store_true');a=ap.parse_args()
 tasks=TASKS if a.all_smoke or a.reliability else [a.task];assert all(tasks)
 for task in tasks:
  variants=['baseline','reference','alternative'] if a.reliability else ['baseline','reference','alternative','fault'] if a.all_smoke else [a.variant or 'reference']
  for variant in variants:
   rounds=30 if task=='A01' else 20
   vr=rounds if a.reliability and variant in ['baseline','reference'] else 3 if a.reliability else 1
   hr=rounds if a.reliability and variant=='reference' else 3 if a.reliability else 1
   qualify(task,a.layout,variant,vr,hr,a.basic or a.all_smoke)
if __name__=='__main__':main()
