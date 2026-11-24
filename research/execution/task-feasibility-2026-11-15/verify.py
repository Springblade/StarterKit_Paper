"""No-model feasibility runner; isolates DB/app and never modifies frozen packages."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,shutil,sys,time
HERE=Path(__file__).resolve().parent
PRE=HERE.parent/'prepilot-2026-11-12'
spec=importlib.util.spec_from_file_location('runtime',PRE/'local-runtime.py')
runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
runtime.IMAGE='smartkit-feasibility:20261115'

def save(p,value):p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def package(layout):
    cell='S1V1' if layout=='feature' else 'S0V1'
    path=PRE/'packages'/'DP03'/cell
    manifest=json.loads(path.with_name(cell+'-manifest.json').read_text(encoding='utf-8'))
    for rel,expected in manifest['files'].items():assert digest(path/rel)==expected,rel
    return path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--layout',choices=['feature','layered'],required=True);ap.add_argument('--phase',default='baseline');ap.add_argument('--task',choices=['A01','A03','B03','B04','U02','U03']);args=ap.parse_args()
    if args.phase!='baseline' and not args.task:ap.error('--task is required outside baseline')
    assert args.phase in ['baseline','reference','alternative','fault-confirmation','fault-cached-role','fault-self-demotion','fault-foreign-receipt','fault-no-admin-guard','fault-foreign-resume','basic']
    log=HERE/'runs'/(args.layout+'-'+str(args.task or 'all')+'-'+args.phase+'-'+str(time.time_ns()));log.mkdir(parents=True)
    name='smartkit-verify-'+args.layout
    assert runtime.docker('ps','-aq','--filter','name=^/'+name+'$',check=False).stdout.strip()==b'', 'Existing container; do not overwrite'
    result={'layout':args.layout,'phase':args.phase,'task':args.task,'model_calls':0,'started':runtime.stamp(),'runner_sha256':digest(Path(__file__)),'runtime_sha256':digest(PRE/'local-runtime.py'),'status':'started'}
    save(log/'record.json',result)
    try:
        runtime.start(name,package(args.layout),log)
        info=json.loads(runtime.docker('inspect',name+'-db').stdout)[0]
        result['db_volumes']=[m['Name'] for m in info['Mounts'] if m['Type']=='volume']
        result['versions']=[runtime.docker('exec',name,*cmd).stdout.decode().strip() for cmd in [('node','--version'),('pnpm','--version'),('pnpm','exec','next','--version')]]
        if args.phase!='baseline':
            source=(PRE/'solutions'/'DP03'/args.layout/('reference' if args.phase=='basic' else args.phase)) if args.task=='A01' else HERE/'solutions'/args.layout/args.task/('reference' if args.phase=='basic' else args.phase)
            assert source.exists(),source
            shutil.copytree(source,log/'source')
            result['solution_files']={str(p.relative_to(source)).replace('\\','/'):digest(p) for p in source.rglob('*') if p.is_file()}
            runtime.docker('cp',str(source)+os.sep+'.',name+':/workspace/')
        runtime.docker('exec',name,'mkdir','-p','/evaluator')
        probe=(PRE/'final-check.cjs') if args.task=='A01' and args.phase!='baseline' else HERE/('probe.cjs' if args.phase=='baseline' else 'task-probe.cjs')
        runtime.docker('cp',probe,name+':/evaluator/probe.cjs')
        result['probe_sha256']=digest(probe)
        shutil.copyfile(probe,log/'probe-source.cjs')
        p=runtime.docker('exec',name,'node','--version') if args.phase=='basic' else runtime.docker('exec','-e','PHASE='+args.phase,'-e','TASK='+str(args.task or ''),'-e','CHECK_TASK=DP03',name,'node','/evaluator/probe.cjs',check=False,timeout=600)
        (log/'probe.log').write_bytes(p.stdout)
        runtime.docker('cp',name+':/evaluator/browser.png',log/'browser.png',check=False)
        if args.phase!='baseline':
            t=runtime.docker('exec',name,'pnpm','check-types',check=False,timeout=180)
            (log/'check-types.log').write_bytes(t.stdout)
            result['typecheck_exit']=t.returncode
            if args.phase in ['reference','alternative','basic']:
                for command in ['test:run','build']:
                    b=runtime.docker('exec',name,'pnpm',command,check=False,timeout=240)
                    (log/(command.replace(':','-')+'.log')).write_bytes(b.stdout)
                    result[command+'_exit']=b.returncode
        remote='/evaluator/final.json' if args.task=='A01' and args.phase!='baseline' else '/evaluator/result.json'
        runtime.docker('cp',name+':'+remote,log/'result.json',check=False)
        if args.task=='A01' and args.phase!='basic':
            scored=json.loads((log/'result.json').read_text(encoding='utf-8'))
            result['A01_joint_success']=scored.get('jointSuccess')
            v=runtime.docker('exec',name,'pnpm','test:preservation',check=False,timeout=240)
            (log/'visible.log').write_bytes(v.stdout)
            result['visible_exit']=v.returncode
        result['probe_exit']=p.returncode
        result['status']='passed' if p.returncode==0 and result.get('typecheck_exit',0)==0 and result.get('test:run_exit',0)==0 and result.get('build_exit',0)==0 and result.get('A01_joint_success',True) and result.get('visible_exit',0)==0 else 'failed'
        if args.phase.startswith('fault-'):
            scored=json.loads((log/'result.json').read_text(encoding='utf-8'))
            expected={'fault-confirmation':'A03-server-invalid-input-preserves-credential','fault-cached-role':'U03-current-server-role-and-fresh-target-permissions','fault-self-demotion':'U03-server-boundaries','fault-foreign-receipt':'B04-ownership-and-status','fault-no-admin-guard':'U02-direct-access-and-missing-account','fault-foreign-resume':'B03-foreign-expired-and-terminal-denial'}[args.phase]
            result['expected_failure']=expected
            result['status']='detected' if scored.get('completed') and any(row['id']==expected and not row['pass'] for row in scored['results']) and result.get('typecheck_exit')==0 else 'fault-not-qualified'
        print(json.dumps({'layout':args.layout,'phase':args.phase,'status':result['status'],'log':str(log)},ensure_ascii=False),flush=True)
    except Exception as e:
        result['status']='infrastructure-error';result['errorClass']=type(e).__name__;print(str(e)[:1000],flush=True)
    finally:
        runtime.stop(name,log)
        remaining=[]
        for vol in result.get('db_volumes',[]):
            if runtime.docker('volume','inspect',vol,check=False).returncode==0:remaining.append(vol)
        result['cleanup_volumes_removed']=not remaining
        result['finished']=runtime.stamp();save(log/'record.json',result)
    if result['status'] not in ['passed','detected'] or not result['cleanup_volumes_removed']:sys.exit(1)

if __name__=='__main__':main()
