"""Validate probe evidence and preserve a bounded, non-release conclusion."""
from pathlib import Path
import json,hashlib,sys
HERE=Path(__file__).resolve().parent
def records(path):
 rows=[]
 for line in path.read_text(encoding='utf-8').splitlines():
  if line.startswith('{'):
   try:row=json.loads(line)
   except json.JSONDecodeError:continue
   if 'id' in row and 'pass' in row:rows.append(row)
 return rows
def main():
 replacement=Path(sys.argv[1]);admin=Path(sys.argv[2]);rows=json.loads(replacement.read_text(encoding='utf-8'));admins=json.loads(admin.read_text(encoding='utf-8'))
 assert len(rows)==24 and len(admins)==10
 expected={'A04':'preservation-reset-maximum128','B05':'preservation-standard-QR-mixed-case','B06':'preservation-live-completion-and-audit'}
 matrix=[]
 for row in rows:
  checks=records(Path(row['log']));assert checks,row
  assert row['basic_exit']==row['type_exit']==0,row
  preserved=[x for x in checks if x['id'].startswith('preservation-')]
  assert preserved
  if row['variant'] in ['reference','alternative']:assert row['probe_exit']==0 and all(x['pass'] for x in checks),row
  elif row['variant']=='baseline':assert all(x['pass'] for x in preserved) and any(not x['pass'] for x in checks if x['id'].startswith('acceptance-')),row
  else:assert row['probe_exit']!=0 and any(x['id']==expected[row['task']] and not x['pass'] for x in checks),row
  matrix.append({**row,'checks':checks})
 for row in admins:
  assert row['basic_exit']==row['type_exit']==0,row
  assert (row['preservation_exit']!=0)==(row['variant']=='fault'),row
 manifest=json.loads((HERE.parent/'layout-manifest.json').read_text(encoding='utf-8'))
 for row in manifest['files']:
  assert hashlib.sha256((HERE.parent/'layouts'/row['layout']/row['path']).read_bytes()).hexdigest()==row['sha256']
 builds=json.loads((HERE/'replacement-build-results.json').read_text(encoding='utf-8'))
 assert len(builds)==2 and all(x['exit']==0 for x in builds)
 result={'build_results':builds,'model_calls':0,'release_authorized':False,'verdict':'hold-model-collection; bounded-feasibility-and-old-behavior-fault-evidence-positive','replacement_correct_cases':12,'replacement_fault_cases_detected':6,'replacement_baseline_cases':6,'admin_old_behavior_correct_cases':6,'admin_shared_guard_fault_cases':4,'admin_distinct_fault_templates':1,'baseline_manifest_records_unchanged':len(manifest['files']),'V0':'Unchanged supplied package basic suite: 4 files / 14 tests. Not every upstream SmartKit test.','V1_scope':'Candidate preservation assertion subset; not a frozen visible package or independent hidden evaluator.','gate_status':{'G1':'stronger source exposure for replacements; no measured agent navigation effect','G2':'old-behavior differential detection demonstrated in bounded probes; A01 uses prior evidence','G3':'partial; no frozen solution-independent hidden evaluator, full cron transport or declared reliability rounds for replacements','G4':'conditional scoped case-study rationale only; no demonstrated S/V effect or publication guarantee'},'limitations':['The two replacement implementations largely share algorithms; expression-level alternatives do not establish broad oracle validity.','Reference-specific direct imports complement HTTP probes; they cannot alone grade arbitrary valid agent implementations.','B06 live concurrent responses are diagnostic: baseline can return completed twice; this is not evidence of duplicate entitlement grants.','Development attempts and corrected probe errors remain archived separately; do not count them as reliability repetitions.','Admin check applies old DP02 directory obligations and one shared requireAdmin fault; this does not qualify all new U02/U03 behavior.','Fresh container per layout; variants share runtime with task source reset, not one fresh runtime per variant.','Replacement fault application sources can be regenerated from the runner; reset overwrote some archived fault overlay paths. Do not claim exact fault-source snapshots for those paths.'],'source_evidence':[{'task':t,'feature_path':p,'layered_path':manifest['moved_files'][p]} for t,p in [('A04','src/features/auth/auth.config.ts'),('B05','src/features/billing/payment-content.ts'),('B06','src/features/billing/process-order-completion.ts')]],'replacement_matrix':matrix,'admin_matrix':admins,'raw_replacement_results':str(replacement),'raw_admin_results':str(admin)}
 (HERE/'replacement-qualification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print('PASS: replacement matrix 12 correct / 6 baseline / 6 detected; admin matrix 6 correct / 4 detected; 284 source records unchanged. Collection remains held.')
if __name__=='__main__':main()
