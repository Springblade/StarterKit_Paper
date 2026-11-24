"""Verify unchanged baseline sources and characterize reference exposure, not agent behavior."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent;EX=HERE.parent;PRE=EX/'prepilot-2026-11-12'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((EX/'layout-manifest.json').read_text(encoding='utf-8'));moves=manifest['moved_files'];inverse={v:k for k,v in moves.items()}
new_correspondence={'src/actions/auth/update-display-name.ts':'src/features/auth/actions/update-display-name.ts','src/types/auth/profile.ts':'src/features/auth/types/profile.ts','src/components/auth/display-name-form.tsx':'src/features/auth/components/display-name-form.tsx'}
for row in manifest['files']:
 p=EX/'layouts'/row['layout']/row['path'];assert digest(p)==row['sha256'],str(p)
rows=[]
for task in ['A01','A03','B03','B04','U02','U03']:
 for variant in ['reference','alternative']:
  sets={}
  for layout in ['feature','layered']:
   folder=PRE/'solutions'/'DP03'/layout/variant if task=='A01' else HERE/'solutions'/layout/task/variant
   files=[p for p in folder.rglob('*') if p.is_file() and p.suffix in ['.tsx','.ts']]
   changed=[];imported=[]
   for p in files:
    rel=p.relative_to(folder).as_posix();canonical=inverse.get(rel,new_correspondence.get(rel,rel));old=EX/'layouts'/layout/rel
    if not old.exists() or p.read_bytes()!=old.read_bytes():changed.append({'path':rel,'logical':canonical,'existing':old.exists(),'relocated_existing':old.exists() and (rel in moves or rel in inverse),'framework_route':rel.startswith('src/app/')})
    for spec in re.findall(r"from ['\"](@/[^'\"]+)['\"]",p.read_text(encoding='utf-8')):
     path='src/'+spec[2:]
     targets=[path+'.ts',path+'.tsx',path+'/index.ts',path+'/index.tsx']
     for t in targets:
      if (EX/'layouts'/layout/t).exists():
       if t in moves or t in inverse:imported.append({'specifier':spec,'logical':inverse.get(t,t)})
       break
   sets[layout]={'changed_files':changed,'relocated_existing_edit_count':sum(x['relocated_existing'] for x in changed),'unchanged_path_route_edit_count':sum(x['framework_route'] for x in changed),'direct_imports_of_relocated_modules':sorted({x['logical'] for x in imported})}
  assert {x['logical'] for x in sets['feature']['changed_files']}=={x['logical'] for x in sets['layered']['changed_files']},(task,variant)
  rows.append({'task':task,'implementation':variant,**sets})
# Old freeze mismatch is localized; do not rewrite the frozen record.
freeze=json.loads((PRE/'freeze.json').read_text(encoding='utf-8'))
old_digest=''
for key in ['files','assets']:
 if isinstance(freeze.get(key),dict):
  for k,v in freeze[key].items():
   if k.endswith('local-runtime.py'):old_digest=v
current=(PRE/'local-runtime.py').read_bytes()
normalized=current.replace(b"docker('rm', '-f', '-v', name, name + '-db', check=False)",b"docker('rm', '-f', name, name + '-db', check=False)")
summary={'baseline_manifest_records_checked':len(manifest['files']),'all_baseline_files_unchanged':True,'reference_exposure':rows,'limits':['Static references only; not actual agent reads','Zero relocated existing edits does not imply zero layout effect','Five new task reference candidates use same framework routes; imports still differ','No main task admitted; feasibility probes do not replace final evaluator or V-gate qualification'],'runtime_check':{'current_sha256':hashlib.sha256(current).hexdigest(),'without_volume_flag_sha256':hashlib.sha256(normalized).hexdigest(),'old_manifest_runtime_entry':old_digest}}
(HERE/'source-evidence.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'baseline_records':len(manifest['files']),'unchanged':True,'cases':len(rows),'existing_relocated_edits_by_task':{r['task']:r['feature']['relocated_existing_edit_count'] for r in rows if r['implementation']=='reference'},'relocated_imports_by_task':{r['task']:len(r['feature']['direct_imports_of_relocated_modules']) for r in rows if r['implementation']=='reference'}},indent=2))
