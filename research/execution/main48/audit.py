"""Fail-closed readiness audit. freeze is permitted only after every recorded gate passes."""
from pathlib import Path
import argparse,json,re,time
from prepare import HERE,EX,PRE,TASKS,CELLS,MOVES,digest,save
import runtime

def qualification_binding(task,layout,variant,visible_rounds,hidden_rounds,basic=True):
 cell='S1V1' if layout=='feature' else 'S0V1';p=HERE/'packages'/task/cell
 hidden=HERE/('hidden-profile.cjs' if task=='A01' else 'hidden-auth.cjs' if task=='A04' else 'hidden-billing.cjs' if task in ['B05','B06'] else 'hidden-admin.cjs')
 value={'image_id':json.loads(runtime.docker('image','inspect',runtime.IMAGE).stdout)[0]['Id'],'package':digest(p.with_name(cell+'-manifest.json')),'hidden':digest(hidden),'visible':digest(p/'scripts/check-preservation.cjs'),'runtime':digest(HERE/'runtime.py'),'mock':digest(HERE/'mock-sepay.cjs'),'solution':digest((HERE/'solutions'/layout/task/variant).with_name(variant+'-manifest.json')) if variant!='baseline' else None,'visible_rounds':visible_rounds,'hidden_rounds':hidden_rounds,'basic':basic}
 if variant!='baseline':value['candidate_setup']='pre-overlaid-start-v1'
 return value

def paired_packages():
 count=0
 for task in TASKS:
  for layout in ['feature','layered']:
   for variant in ['reference','alternative','fault']:
    source=HERE/'solutions'/layout/task/variant
    expected=json.loads(source.with_name(variant+'-manifest.json').read_text(encoding='utf-8'))
    assert {p.relative_to(source).as_posix():digest(p) for p in source.rglob('*') if p.is_file()}==expected,('candidate manifest mismatch',task,layout,variant)
  for cell in CELLS:
   p=HERE/'packages'/task/cell;manifest=json.loads(p.with_name(cell+'-manifest.json').read_text(encoding='utf-8'))
   files={f.relative_to(p).as_posix():digest(f) for f in p.rglob('*') if f.is_file()};assert files==manifest['files'],(task,cell,'manifest mismatch')
   assert not any(x.startswith(('.git/','.codex/','solutions/','qualification/')) or 'hidden-' in x for x in files),(task,cell,'exposure')
   assert 'CHECK_TASK' not in (p/'TASK.md').read_text() # no hidden harness instructions
   original=PRE/'packages'/'DP03'/('S1V0' if cell[1]=='1' else 'S0V0')
   original_manifest=json.loads(original.with_name(original.name+'-manifest.json').read_text(encoding='utf-8'))['files']
   for rel,expected in original_manifest.items():
    assert digest(original/rel)==expected,('changed historical baseline package',rel)
    if rel not in {'.env','TASK.md','package.json'}:assert digest(p/rel)==expected,('changed starting source/check',task,cell,rel)
   count+=1
  for s in [0,1]:
   a=HERE/'packages'/task/f'S{s}V0';b=HERE/'packages'/task/f'S{s}V1'
   af={p.relative_to(a).as_posix() for p in a.rglob('*') if p.is_file()};bf={p.relative_to(b).as_posix() for p in b.rglob('*') if p.is_file()}
   assert bf-af=={'scripts/check-preservation.cjs'} and not af-bf
   changed={rel for rel in af if (a/rel).read_bytes()!=(b/rel).read_bytes()};assert changed=={'TASK.md','package.json'},changed
   pa=json.loads((a/'package.json').read_text());pb=json.loads((b/'package.json').read_text());pb['scripts'].pop('test:preservation');assert pa==pb
   assert (b/'TASK.md').read_text().replace('Additional visible preservation command: pnpm test:preservation.\n','').strip()==(a/'TASK.md').read_text().strip()
 # Layout transform is independently checked against the source manifest; existing unsolved
 # package snapshots are used without modifying their logic or removing supplied tests.
 baseline=json.loads((EX/'layout-manifest.json').read_text(encoding='utf-8'))
 for row in baseline['files']:assert digest(EX/'layouts'/row['layout']/row['path'])==row['sha256']
 for task in TASKS:
  for v in [0,1]:
   layered=HERE/'packages'/task/f'S0V{v}';feature=HERE/'packages'/task/f'S1V{v}'
   import posixpath
   inventories={root:{p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()} for root in [feature,layered]}
   def canonical(root,rel):
    available=inventories[root]
    inverse={v:k for k,v in MOVES.items()}
    def replace(match):
     text=match[2]
     candidate='src/'+text[2:] if text.startswith('@/') else posixpath.normpath(posixpath.join(posixpath.dirname(rel),text)) if text.startswith('.') else None
     if candidate is None:return match[0]
     options=[candidate]+[candidate+x for x in ['.ts','.tsx','.js','.mjs','.json']]+[candidate+'/index'+x for x in ['.ts','.tsx','.js']]
     target=next((x for x in options if x in available),None)
     return match[1]+'<module:'+inverse.get(target,target)+'>'+match[1] if target else match[0]
    return re.sub(r"(['\"])([^'\"\r\n]+)\1",replace,(root/rel).read_text(encoding='utf-8'))
   for src in inventories[feature]:
    if Path(src).suffix not in ['.ts','.tsx','.js','.mjs','.json','.css']:continue
    dst=MOVES.get(src,src)
    assert dst in inventories[layered],(task,src,'missing paired code file')
    assert canonical(feature,src)==canonical(layered,dst),(task,src,dst,'unintended source-layout difference')
 return count

def readiness():
 blockers=[];evidence=[]
 running=runtime.docker('ps','--format','{{.Names}}').stdout.decode().splitlines()
 if any(name.startswith(('smartkit-mainqual-','smartkit-rehearse-','smartkit-score-','smartkit-main-')) for name in running):blockers.append('study runtimes still active; wait for clean completion before freeze')
 try:packages=paired_packages()
 except (AssertionError,FileNotFoundError) as e:blockers.append('package/source audit: '+str(e));packages=0
 for task in TASKS:
  for layout in ['feature','layered']:
   for variant in ['baseline','reference','alternative','fault']:
    rounds=30 if task=='A01' else 20;vr=rounds if variant in ['baseline','reference'] else 3 if variant=='alternative' else 1;hr=rounds if variant=='reference' else 3 if variant in ['baseline','alternative'] else 1
    required=qualification_binding(task,layout,variant,vr,hr)
    candidates=list((HERE/'qualification').glob(f'ledger-{task}-{layout}-{variant}-*.json'));found=None
    for path in candidates:
     row=json.loads(path.read_text(encoding='utf-8'))
     if row.get('passed') and row.get('cleanup_volumes_removed') and row.get('binding')==required and all(row.get('basic',{}).get(cmd)==0 for cmd in ['check-types','test:run','test:billing','test:sepay-qr-url','build']):found=path;break
    if found:evidence.append(found.relative_to(HERE).as_posix())
    else:blockers.append(f'qualification/reliability missing or stale: {task}/{layout}/{variant} V{vr}/E{hr}/all V0')
    if found and variant=='fault':
     expected={
      'A01':('VP-A4-existing-display-name-is-text','A-P3-stored-name-safe-on-existing-settings'),
      'A04':('preservation-reset-maximum128','EA-old-expired-reset-max-identity'),
      'B05':('VP-existing-checkout-transfer-format','E-old-checkout-preserves-standard-transfer-content'),
      'B06':('VP-standard-QR-payment-case-live-audit-retry','E-old-standard-webhook-retry'),
      'U02':('VP-U1-admin-only-direct-route','EU-old-directory-access-no-token'),
      'U03':('VP-U1-admin-only-direct-route','EU-old-directory-access-no-token'),
     }[task]
     row=json.loads(found.read_text(encoding='utf-8'))
     for suite,check in zip(['visible','hidden'],expected):
      if not any(x.get('id')==check and x.get('pass') is False for invocation in row[suite] for x in invocation.get('results',[])):blockers.append(f'fault missed named old obligation: {task}/{layout}/{check}')
 from collect import rehearsal_binding
 rehearsed={}
 for rehearsal in [HERE/'rehearsal.json',HERE/'rehearsal-feature.json',HERE/'rehearsal-layered.json']:
  if rehearsal.exists():rehearsed.update(json.loads(rehearsal.read_text()))
 if not all(rehearsed.get(t+'/'+c,{}).get('passed') and rehearsed[t+'/'+c].get('binding')==rehearsal_binding(t,c) for t in TASKS for c in CELLS):blockers.append('24 current no-model capture/reset/score rehearsals incomplete')
 selfcheck=HERE/'selfcheck.json'
 checked=json.loads(selfcheck.read_text()) if selfcheck.exists() else {}
 if not checked.get('pass') or not all((HERE/rel).exists() and digest(HERE/rel)==expected for rel,expected in checked.get('files',{}).items()):blockers.append('runner self-check missing or stale')
 review=HERE/'review.json'
 reviewed=json.loads(review.read_text()) if review.exists() else {}
 if not reviewed.get('pass') or not reviewed.get('files') or not all((HERE/rel).exists() and digest(HERE/rel)==expected for rel,expected in reviewed.get('files',{}).items()):blockers.append('documented instrument review missing or stale')
 for rel in ['protocol.md','analysis.py','model-preflight.json']:
  if not (HERE/rel).exists():blockers.append('missing '+rel)
 if (HERE/'model-preflight.json').exists():
  models=json.loads((HERE/'model-preflight.json').read_text()).get('matched_models',[])
  if not any(m.get('model')=='gpt-6-luna' and any(e.get('reasoningEffort')=='high' for e in m.get('supportedReasoningEfforts',[])) for m in models):blockers.append('requested model/high reasoning not in model-list preflight')
 allocation=json.loads((HERE/'allocation.json').read_text());slots=allocation['slots']
 assert len(slots)==48 and len({x['slot'] for x in slots})==48
 assert all(sum(x['task']==t and x['cell']==c for x in slots)==2 for t in TASKS for c in CELLS)
 assert allocation['cap_seconds']==900 and allocation['model']=='gpt-6-luna' and allocation['reasoning_effort']=='high' and allocation['replacement_attempts']==0
 for i in range(0,48,4):
  block=slots[i:i+4];assert len({(x['task'],x['repetition']) for x in block})==1 and {x['cell'] for x in block}==set(CELLS)
 result={'technical_ready':not blockers,'model_calls':0,'packages_checked':packages,'qualified_case_ledgers':evidence,'blockers':blockers,'checked':runtime.stamp(),'allocation_slots':48,'author_start_release_present':(HERE/'author-release.json').exists()}
 save(HERE/'readiness.json',result);return result

def freeze():
 result=readiness();assert result['technical_ready'],result['blockers']
 assert not (HERE/'freeze.json').exists(),'Preserve existing freeze'
 assert not any(json.loads(p.read_text()).get('invoked') for p in (HERE/'runs').glob('*/attempt.json')),'Do not freeze prospectively after a main invocation'
 files={}
 roots=['packages','solutions','qualification','rehearsal']
 for root in roots:
  for p in (HERE/root).rglob('*'):
   if p.is_file():files[p.relative_to(HERE).as_posix()]=digest(p)
 for p in HERE.iterdir():
  if p.is_file() and p.suffix in ['.py','.cjs','.md','.json'] and p.name not in ['freeze.json','author-release.json','readiness.json']:files[p.name]=digest(p)
 for rel in ['../../paper-proposal/main-revised.tex','../../paper-proposal/main-revised.pdf']:
  files[rel]=digest(HERE/rel)
 image=json.loads(runtime.docker('image','inspect',runtime.IMAGE).stdout)[0]['Id']
 save(HERE/'freeze.json',{'technical_ready':True,'author_start_release':False,'frozen':runtime.stamp(),'image_id':image,'files':files,'configuration':json.loads((HERE/'allocation.json').read_text()),'model_calls':0})
 print('Technical freeze complete; model invocation remains gated by an explicit start release.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--freeze',action='store_true');a=ap.parse_args()
 if a.freeze:freeze()
 else:r=readiness();print(json.dumps({'technical_ready':r['technical_ready'],'remaining_blockers':len(r['blockers']),'blockers':r['blockers']},indent=2))
