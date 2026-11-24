"""Exercise OLD directory obligations with retained task solutions and a shared-guard fault."""
from pathlib import Path
import importlib.util,json,time,os
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verify',HERE/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
r=v.runtime
moves=json.loads((HERE.parent/'layout-manifest.json').read_text(encoding='utf-8'))['moved_files']

def main():
 rows=[];runid=str(time.time_ns());out=HERE/('admin-preservation-results-'+runid+'.json')
 for layout in ['feature','layered']:
  name='smartkit-admin-preserve-'+layout+'-'+runid[-6:]
  log=HERE/'runs'/('admin-preservation-'+layout+'-'+runid);log.mkdir(parents=True)
  original={}
  try:
   r.start(name,v.package(layout),log)
   r.docker('exec',name,'mkdir','-p','/evaluator')
   checker=(v.PRE/'visible-check.cjs').read_text(encoding='utf-8').replace('__TASK__','DP02')
   p=log/'visible-source.cjs';p.write_text(checker,encoding='utf-8');r.docker('cp',p,name+':/workspace/scripts/admin-preservation.cjs')
   guard='src/features/auth/lib/auth.ts';guard=moves.get(guard,guard) if layout=='layered' else guard
   saved=(v.package(layout)/guard).read_text(encoding='utf-8')
   for task,variant in [('baseline','baseline'),('U02','reference'),('U02','fault'),('U03','reference'),('U03','fault')]:
    # Restore prior task's overlay before applying the next independent task.
    for rel,data in original.items():
     p=log/'restore'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);r.docker('cp',p,name+':/workspace/'+rel)
    original={}
    if task!='baseline':
     source=HERE/'solutions'/layout/task/'reference'
     for p in source.rglob('*'):
      if p.is_file():
       rel=p.relative_to(source).as_posix();base=v.package(layout)/rel
       # New routes may remain between probes, but the OLD directory and guard are restored.
       if base.exists():original[rel]=base.read_bytes()
     r.docker('cp',str(source)+os.sep+'.',name+':/workspace/')
    text=saved if variant!='fault' else saved.replace("if (!isAdmin(session.user as { role?: string | null }))",'if (session.user.id.length === 0)')
    assert variant!='fault' or text!=saved
    p=log/f'{task}-{variant}-guard.ts';p.write_text(text,encoding='utf-8');r.docker('cp',p,name+':/workspace/'+guard)
    probe=r.docker('exec',name,'node','scripts/admin-preservation.cjs',check=False,timeout=180);(log/f'{task}-{variant}.log').write_bytes(probe.stdout)
    basic=r.docker('exec',name,'pnpm','test:run',check=False,timeout=180);(log/f'{task}-{variant}-basic.log').write_bytes(basic.stdout)
    tc=r.docker('exec',name,'pnpm','check-types',check=False,timeout=180);(log/f'{task}-{variant}-types.log').write_bytes(tc.stdout)
    row={'layout':layout,'task':task,'variant':variant,'preservation_exit':probe.returncode,'basic_exit':basic.returncode,'type_exit':tc.returncode,'log':str(log),'model_calls':0};rows.append(row);out.write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(row),flush=True)
  finally:r.stop(name,log)
 assert len(rows)==10

if __name__=='__main__':main()
