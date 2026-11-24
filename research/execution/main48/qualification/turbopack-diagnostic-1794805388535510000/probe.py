from pathlib import Path
import sys,shutil,tempfile,json
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import runtime
from prepare import HERE
root=Path(__file__).resolve().parent
original=runtime.docker
def traced(*args,**kwargs):
 if len(args)>3 and args[:2]==('exec','-d'):
  args=(*args[:-1],args[-1].replace('--webpack','--turbopack'))
 return original(*args,**kwargs)
runtime.docker=traced
runtime.DEV_BUNDLER='turbopack-diagnostic'
name='smartkit-mainqual-turbopack-probe'
try:
 with tempfile.TemporaryDirectory(prefix='smartkit-manifest-probe-') as tmp:
  stage=Path(tmp)/'workspace';shutil.copytree(HERE/'packages/B05/S1V1',stage);shutil.copytree(HERE/'solutions/feature/B05/reference',stage,dirs_exist_ok=True)
  runtime.start(name,stage,root)
 original('exec',name,'mkdir','-p','/evaluator');original('cp',HERE/'visible-billing.cjs',name+':/evaluator/visible.cjs')
 for i in range(60):
  p=original('exec','-e','CHECK_TASK=B05','-e','CHECK_OUTPUT=/evaluator/result.json',name,'node','/evaluator/visible.cjs',check=False,timeout=300)
  (root/f'round-{i:02}.log').write_bytes(p.stdout);print('Diagnostic round',i+1,p.returncode,flush=True)
  if p.returncode:break
finally:runtime.stop(name,root)
