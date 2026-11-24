"""Summarize saved no-model evidence and assert the claimed coverage."""
from pathlib import Path
import collections,hashlib,json
HERE=Path(__file__).resolve().parent
rows=[]
for p in sorted((HERE/'runs').glob('*/record.json')):
 r=json.loads(p.read_text(encoding='utf-8'));r['artifact_dir']=p.parent.relative_to(HERE).as_posix();rows.append(r)
assert all(r.get('model_calls')==0 for r in rows)
assert all(r['status']!='started' for r in rows),'An invocation is unfinished'
assert all(r.get('cleanup_volumes_removed') for r in rows),'Cleanup incomplete'
tasks=['A01','A03','B03','B04','U02','U03'];passed=[];failures=[]
for t in tasks:
 for layout in ['feature','layered']:
  for variant in ['reference','alternative']:
   matches=[r for r in rows if r.get('task')==t and r['layout']==layout and r['phase']==variant and r['status']=='passed']
   assert matches,(t,layout,variant)
   r=matches[-1];run=HERE/r['artifact_dir'];score=json.loads((run/'result.json').read_text(encoding='utf-8'))
   assert score.get('completed') and (score.get('jointSuccess') if t=='A01' else score.get('pass')),(t,layout,variant)
   assert r.get('typecheck_exit')==0
   basics=[b for b in rows if b.get('task')==t and b['layout']==layout and b['phase'] in ([variant,'basic'] if variant=='reference' else [variant]) and b['status']=='passed' and b.get('test:run_exit')==0 and b.get('build_exit')==0]
   assert basics,('Missing unit/build',t,layout,variant)
   # Supplemental basic run must have used the exact reference source.
   b=basics[-1]
   if r.get('solution_files') and b.get('solution_files'):assert r['solution_files']==b['solution_files'],('Different candidate used for build',t,layout,variant)
   passed.append({'task':t,'layout':layout,'implementation':variant,'runtime_log':r['artifact_dir'],'build_log':b['artifact_dir'],'check_count':len(score['results']),'source_archived':(run/'source').exists()})
for r in rows:
 if r['phase'].startswith('fault-'):
  assert r['status']=='detected',r['artifact_dir'];score=json.loads((HERE/r['artifact_dir']/'result.json').read_text(encoding='utf-8'))
  failed=[x['id'] for x in score['results'] if not x['pass']]
  assert r['expected_failure'] in failed and r['typecheck_exit']==0
  failures.append({'task':r['task'],'layout':r['layout'],'fault':r['phase'],'expected_assertion':r['expected_failure'],'failed_assertions':failed,'artifact_dir':r['artifact_dir'],'kind':'constructed new-feature fault; not observed agent outcome'})
assert len(failures)==12
base=[]
for layout in ['feature','layered']:
 r=[x for x in rows if x['layout']==layout and x['phase']=='baseline' and x['status']=='passed'][-1]
 score=json.loads((HERE/r['artifact_dir']/'result.json').read_text(encoding='utf-8'));assert score['pass']
 base.append({'layout':layout,'artifact_dir':r['artifact_dir'],'results':score['results']})
source=json.loads((HERE/'source-evidence.json').read_text(encoding='utf-8'))
assert source['all_baseline_files_unchanged']
summary={'kind':'non-model-feasibility-verification-not-main-qualification','date':'2026-11-15','model_invocations':0,'valid_implementation_layout_cases':passed,'constructed_fault_layout_cases':failures,'baseline_probes':base,'all_invocation_status_counts':dict(collections.Counter(r['status'] for r in rows)),'all_invocations':[{k:r[k] for k in ['layout','phase','task','status','artifact_dir','started','finished','cleanup_volumes_removed'] if k in r} for r in rows],'source_manifest_records_verified':source['baseline_manifest_records_checked'],'research_assessment':{'feasibility':'all six tasks have two scoped runnable candidates on both layouts','organization_exposure':'all twelve task-implementation pairs edit zero existing relocated modules; imports differ, no claim S effect equals0','verification_treatment':'new fault cases test new-feature semantics; V1 preservation benefit/gate not established by these tests','main_ready':False,'release':False},'limitations':['Feasibility probes have candidate-specific routes/labels, not frozen hidden evaluator accepting arbitrary implementations','Five new tasks lack full V0/V1 preservation-gate and reliability qualification','Reference/alternative variants are author-assistant constructs, not independent human validation','B03 concurrent completion/cancel races and expiry transition while open not comprehensively verified','No actual agent performance or effect measurement','Baseline feature absence checked through declared UI and chosen routes; not exhaustive search of all possible endpoints','Rebuilt feasibility image differs from old missing image; app lock/runtime/browser pinned, no Codex CLI or account credentials installed','Some early failed source versions were not archived; failed logs retained; latest successful candidates have hashes or archived source'],'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('*') if p.is_file() and p.name not in ['summary.json','report.md']}}
(HERE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'valid_candidate_cases':len(passed),'fault_cases_detected':len(failures),'baseline_layouts':len(base),'all_invocations':len(rows),'status_counts':summary['all_invocation_status_counts'],'model_runs':0,'baseline_manifest_records':source['baseline_manifest_records_checked'],'main_ready':False},indent=2))
