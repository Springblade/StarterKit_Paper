"""Production compile of the combined replacement reference overlay; no model calls."""
from pathlib import Path
import importlib.util,json,sys,time,os
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verify',HERE/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def main():
 rows=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'));out=[]
 for layout in ['feature','layered']:
  name='smartkit-replacement-build-'+layout;log=HERE/'runs'/('replacement-build-'+layout+'-'+str(time.time_ns()));log.mkdir(parents=True)
  try:
   v.runtime.start(name,v.package(layout),log)
   # Stop only this disposable container's dev server before using its build output directory.
   stop="const f=require('fs');for(const p of f.readdirSync('/proc'))if(/^\\d+$/.test(p)&&+p!==process.pid){try{const c=f.readFileSync('/proc/'+p+'/comm','utf8');if(c.startsWith('next-server'))process.kill(+p,'SIGTERM');}catch{}}"
   v.runtime.docker('exec',name,'node','-e',stop)
   for task in ['A04','B05','B06']:
    row=next(x for x in rows if x['layout']==layout and x['task']==task and x['variant']=='reference')
    overlay=Path(row['log']).parent/'overlay'/task/'reference'
    assert overlay.exists();v.runtime.docker('cp',str(overlay)+os.sep+'.',name+':/workspace/')
   p=v.runtime.docker('exec',name,'pnpm','build',check=False,timeout=300);(log/'build.log').write_bytes(p.stdout)
   row={'layout':layout,'scope':'combined A04/B05/B06 reference overlay, not individual independent-task builds','exit':p.returncode,'log':str(log),'model_calls':0};out.append(row);print(json.dumps(row),flush=True)
  finally:v.runtime.stop(name,log)
 (HERE/'replacement-build-results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 assert all(x['exit']==0 for x in out)
if __name__=='__main__':main()
