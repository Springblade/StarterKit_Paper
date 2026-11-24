"""Four-cell development pilot. Container-only agent; no host research mounts.

Preparation/qualification does not invoke a model. `run` consumes the author's
ChatGPT-authenticated Codex allowance. All cases are serial and separately logged.
"""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import os
import random
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
EXEC = HERE.parent
IMAGE = 'smartkit-pilot:20261111'
MODEL = 'gpt-6-luna'
LIMIT = 900

def call(args, *, check=True, timeout=240):
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    if check and p.returncode:
        raise RuntimeError(f'Command failed ({p.returncode}): {args[:3]}\n'+p.stdout.decode(errors='replace')[-1800:])
    return p

def docker(*args, **kw): return call(['docker', *map(str,args)], **kw)
def stamp(): return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
def save(path, value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def env_text():
    return '''DATABASE_URL="postgresql://postgres:local-pilot-only@pilot-db:5432/smartkit_pilot"
BETTER_AUTH_SECRET="local-development-pilot-secret-at-least-32-characters"
BETTER_AUTH_URL="http://localhost:3107"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3107"
NEXT_PUBLIC_APP_URL="http://localhost:3107"
NEXT_PUBLIC_GOOGLE_ENABLED="false"
RESEND_FROM_EMAIL="onboarding@resend.dev"
SEPAY_WEBHOOK_SECRET="local-development-pilot-only"
CRON_SECRET="local-development-pilot-only"
NODE_ENV="development"
'''

def prepare():
    manifest=json.loads((EXEC/'layout-manifest.json').read_text())
    task=(EXEC/'history-filter-task-card.md').read_text(encoding='utf-8').split('## Requirement supplied to the implementer\n\n',1)[1].split('\n## Qualification',1)[0]
    task=task.replace('Add a labelled status filter','Add a labelled native dropdown status filter')
    for s in (0,1):
        layout='layered' if s==0 else 'feature'
        for v in (0,1):
            cell=f'S{s}V{v}'; target=HERE/'packages'/cell
            if target.exists(): raise RuntimeError('Refusing to overwrite '+str(target))
            target.mkdir(parents=True)
            for row in manifest['files']:
                if row['layout']!=layout:continue
                if row['path'] in {'scripts/check-order-baseline.integration.ts','vitest.orders.config.ts'}:continue
                source=EXEC/'layouts'/layout/row['path']
                assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'],row['path']
                dest=target/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
            shutil.copyfile(EXEC/'layouts'/layout/'AGENTS.md',target/'AGENTS.md')
            with (target/'AGENTS.md').open('a',encoding='utf-8') as f:
                f.write('\n## Development pilot\nRead TASK.md for the assigned requirement and available check commands. Preserve application behavior outside the requested change.\n')
            commands='pnpm check-types; pnpm test:run; pnpm build'
            if v:
                visible=(EXEC/'layouts'/layout/'scripts/check-order-baseline.integration.ts').read_text(encoding='utf-8')
                start=visible.index("describe('history filter development-task evaluator'")
                end=visible.index("describe('actual server actions",start)
                visible=visible[:start]+visible[end:]
                visible=visible.replace("['localhost', '127.0.0.1'].includes(database.hostname)","['pilot-db'].includes(database.hostname)")
                visible=visible.replace('/smartkit_orders_test','/smartkit_pilot')
                visible=visible.replace('Use the dedicated local smartkit_orders_test database only','Use the dedicated smartkit_pilot database only')
                assert 'history filter development-task evaluator' not in visible
                (target/'scripts/check-order-baseline.integration.ts').write_text(visible,encoding='utf-8')
                shutil.copyfile(EXEC/'layouts'/layout/'vitest.orders.config.ts',target/'vitest.orders.config.ts')
                p=json.loads((target/'package.json').read_text());p['scripts']['test:behavior']='vitest run --config vitest.orders.config.ts'
                (target/'package.json').write_text(json.dumps(p,indent=2)+'\n')
                commands+='; pnpm test:behavior'
            (target/'.env').write_text(env_text())
            (target/'TASK.md').write_text('# Assigned development task\n\n'+task+'\n\n## Local environment\nDependencies are installed. A fresh local test database is migrated and seeded. A Next development server is running at http://localhost:3107. Test accounts are listed by scripts/seed.ts. No real payment or email service is configured.\n\nAvailable supplied checks: '+commands+'. You may write and run your own checks. Keep changes in this workspace and do not commit them. The same 15-minute wall-time limit applies to every condition. Finish with a short account of your changes and checks.\n',encoding='utf-8')
            assert b'STATUS_OPTIONS' not in (target/'src/app/dashboard/billing/history/page.tsx').read_bytes()
            inventory={p.relative_to(target).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in target.rglob('*') if p.is_file()}
            save(HERE/f'{cell}-manifest.json',{'cell':cell,'layout':layout,'V':v,'model':MODEL,'reasoning':'high','speed':'standard-default','wall_seconds':LIMIT,'files':inventory})
    order=['S0V0','S0V1','S1V0','S1V1'];random.Random(20261111).shuffle(order)
    save(HERE/'allocation.json',{'seed':20261111,'order':order,'purpose':'development smoke pilot, one session per cell; no inferential effect estimate'})
    print('Prepared four packages. Allocation '+str(order),flush=True)

def start(name, package, logdir):
    net=name+'-net'; db=name+'-db'
    logdir.mkdir(parents=True,exist_ok=True)
    docker('network','create',net)
    docker('run','-d','--name',db,'--network',net,'--network-alias','pilot-db',
           '-e','POSTGRES_PASSWORD=local-pilot-only','-e','POSTGRES_DB=smartkit_pilot','postgres:16-alpine')
    docker('run','-d','--name',name,'--network',net,IMAGE)
    docker('cp',str(package)+os.sep+'.',name+':/workspace/')
    for _ in range(40):
        # The entrypoint's temporary init server accepts Unix sockets before
        # the network server exists. Agent containers need TCP readiness.
        if docker('exec',db,'pg_isready','-h','127.0.0.1','-p','5432','-U','postgres','-d','smartkit_pilot',check=False).returncode==0:break
        time.sleep(.25)
    else:raise RuntimeError('PostgreSQL TCP readiness failed')
    for command,filename in [('pnpm db:migrate','migrate.log'),('pnpm db:seed','seed.log')]:
        p=docker('exec',name,'sh','-c',command,check=False)
        (logdir/filename).write_bytes(p.stdout)
        if p.returncode:raise RuntimeError(filename+' failed')
    docker('exec','-d',name,'sh','-c','pnpm exec next dev -p 3107 > /tmp/app.log 2>&1')
    probe="fetch('http://localhost:3107/').then(r=>process.exit(r.status===200?0:1)).catch(()=>process.exit(1))"
    for _ in range(30):
        if docker('exec',name,'node','-e',probe,check=False,timeout=25).returncode==0:break
        time.sleep(.3)
    else:raise RuntimeError('App did not become ready')
    # A fresh single-commit repo has no reachable solution history.
    docker('exec',name,'sh','-c','git init -q && git config user.name Pilot && git config user.email pilot@local.invalid && git add . && git commit -qm baseline')
    inspect=json.loads(docker('inspect',name).stdout)[0]
    assert not inspect['Mounts'] and not inspect['HostConfig']['Privileged']
    assert inspect['HostConfig']['PidMode']!='host'
    probe="const f=require('fs');for(const p of ['/research','/var/run/docker.sock','/workspace/.git/objects/info/alternates'])if(f.existsSync(p))process.exit(1);"
    docker('exec',name,'node','-e',probe)
    save(logdir/'isolation.json',{'no_host_mounts':True,'no_docker_socket':True,'private_pid_namespace':True,'fresh_single_commit':True,'image_id':inspect['Image'],'network':net})
    return docker('exec',name,'git','rev-parse','HEAD').stdout.decode().strip()

def stop(name, logdir):
    for filename,remote in [('app.log','/tmp/app.log')]:
        p=docker('exec',name,'cat',remote,check=False)
        if p.returncode==0:(logdir/filename).write_bytes(p.stdout)
    p=docker('logs',name+'-db',check=False)
    if p.returncode==0:(logdir/'postgres.log').write_bytes(p.stdout)
    docker('rm','-f','-v',name,name+'-db',check=False)
    docker('network','rm',name+'-net',check=False)

def score(package, name, logdir, reference=None):
    try:
        start(name,package,logdir)
        if reference:
            docker('cp',reference,name+':/workspace/src/app/dashboard/billing/history/page.tsx')
        docker('exec',name,'mkdir','-p','/evaluator')
        docker('cp',HERE/'final-check.cjs',name+':/evaluator/final-check.cjs')
        p=docker('exec',name,'node','/evaluator/final-check.cjs',check=False)
        (logdir/'scoring.log').write_bytes(p.stdout)
        docker('cp',name+':/evaluator/result.json',logdir/'result.json')
        return json.loads((logdir/'result.json').read_text())
    finally:stop(name,logdir)

def qualify():
    results=[]
    for layout,cell in [('feature','S1V1'),('layered','S0V1')]:
        package=HERE/'packages'/cell
        for stage in ('baseline','reference'):
            logdir=HERE/'qualification'/f'{layout}-{stage}'
            reference=EXEC/f'history-reference-{layout}.tsx.txt' if stage=='reference' else None
            r=score(package,'smartkit-q-'+layout+'-'+stage,logdir,reference)
            assert r['evaluator_completed'],r
            assert r['preservation'],r
            assert r['acceptance']==(stage=='reference'),r
            results.append({'layout':layout,'stage':stage,'acceptance':r['acceptance'],'preservation':r['preservation'],'checks':len(r['results'])})
            save(HERE/'qualification-results.json',results)
            print(json.dumps(results[-1]),flush=True)
    for cell in ('S0V1','S1V1'):
        name='smartkit-visible-'+cell.lower();logdir=HERE/'qualification'/('visible-'+cell)
        start(name,HERE/'packages'/cell,logdir)
        try:
            p=docker('exec',name,'pnpm','test:behavior',check=False)
            (logdir/'visible.log').write_bytes(p.stdout)
            assert p.returncode==0,p.stdout.decode(errors='replace')[-1500:]
        finally:stop(name,logdir)
    save(HERE/'qualification-complete.json',{'time':stamp(),'status':'passed','hidden_evaluator_sha256':hashlib.sha256((HERE/'final-check.cjs').read_bytes()).hexdigest()})

def run():
    assert (HERE/'qualification-complete.json').exists(),'Qualify first'
    qualification=json.loads((HERE/'qualification-complete.json').read_text())
    assert qualification['hidden_evaluator_sha256']==hashlib.sha256((HERE/'final-check.cjs').read_bytes()).hexdigest(),'Evaluator changed since qualification'
    auth=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'auth.json'
    account=json.loads(auth.read_text())
    assert account.get('auth_mode')=='chatgpt' and not account.get('OPENAI_API_KEY'),'ChatGPT auth required; no paid API'
    ledger=HERE/'runs';ledger.mkdir(exist_ok=True)
    order=json.loads((HERE/'allocation.json').read_text())['order']
    for cell in order:
        logdir=ledger/cell
        if (logdir/'attempt.json').exists():
            prior=json.loads((logdir/'attempt.json').read_text())
            if prior['status']=='complete':continue
            raise RuntimeError('An incomplete attempt exists; adjudicate rather than silently retry '+cell)
        package=HERE/'packages'/cell
        manifest=json.loads((HERE/f'{cell}-manifest.json').read_text())
        for filename,digest in manifest['files'].items():
            assert hashlib.sha256((package/filename).read_bytes()).hexdigest()==digest,filename
        name='smartkit-agent-'+cell.lower()
        attempt={'cell':cell,'model':MODEL,'reasoning':'high','speed':'standard-default','status':'preparing','started':stamp(),'limit_seconds':LIMIT}
        logdir.mkdir(parents=True,exist_ok=True);save(logdir/'attempt.json',attempt)
        try:
            commit=start(name,package,logdir)
            docker('exec',name,'mkdir','-p','/opt/codex-home')
            docker('cp',auth,name+':/opt/codex-home/auth.json')
            status=docker('exec',name,'codex','login','status').stdout.decode()
            assert 'ChatGPT' in status,status
            command=['docker','exec',name,'codex','exec','--ignore-user-config','--ignore-rules','--ephemeral',
                '--dangerously-bypass-approvals-and-sandbox','-m',MODEL,'-c','model_reasoning_effort="high"',
                '--json','--output-last-message','/tmp/final-message.txt',
                'Read TASK.md and implement its requirement in this repository. Use available checks as appropriate.']
            # Only the externally isolated container bypasses the inner sandbox.
            attempt['status']='running';attempt['model_started']=stamp();save(logdir/'attempt.json',attempt)
            began=time.monotonic();timed_out=False
            with (logdir/'events.jsonl').open('wb') as out:
                proc=subprocess.Popen(command,stdout=out,stderr=subprocess.STDOUT,
                                      creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
                while proc.poll() is None:
                    if time.monotonic()-began>=LIMIT:
                        timed_out=True;docker('exec',name,'pkill','-f','codex',check=False)
                        proc.kill();proc.wait();break
                    time.sleep(.5)
            attempt.update({'elapsed_seconds':round(time.monotonic()-began,2),'returncode':proc.returncode,'timeout':timed_out,'model_finished':stamp()})
            text=(logdir/'events.jsonl').read_text(errors='replace')
            events=[]
            for line in text.splitlines():
                try:events.append(json.loads(line))
                except (ValueError,TypeError):pass
            attempt['completed_turns']=sum(event.get('type')=='turn.completed' for event in events)
            attempt['usage_events']=[event.get('usage') for event in events if event.get('type')=='turn.completed']
            attempt['cli_version']=docker('exec',name,'codex','--version').stdout.decode().strip()
            # Preserve all events; never print authentication data or full traces.
            docker('cp',name+':/tmp/final-message.txt',logdir/'final-message.txt',check=False)
            interrupted=(not timed_out and not attempt['completed_turns']) or (proc.returncode and any(term in text.lower() for term in ['usage limit','rate limit','quota exceeded','unsupported model','not supported','authentication','unauthorized']))
            docker('exec',name,'git','add','-N','.')
            patch=docker('exec',name,'git','diff','--binary',commit)
            (logdir/'patch.diff').write_bytes(patch.stdout)
            docker('exec',name,'tar','-czf','/tmp/final-workspace.tgz','--exclude=./node_modules','--exclude=./.next','--exclude=./.git','--exclude=./.env','--exclude=./tsconfig.tsbuildinfo','-C','/workspace','.')
            docker('cp',name+':/tmp/final-workspace.tgz',logdir/'final-workspace.tgz')
            attempt['status']='infrastructure_interrupted' if interrupted else 'awaiting_scoring';save(logdir/'attempt.json',attempt)
        except Exception as error:
            attempt['status']='infrastructure_error';attempt['error']=str(error)[:2000];save(logdir/'attempt.json',attempt)
            raise
        finally:stop(name,logdir)
        if attempt['status']=='infrastructure_interrupted':
            print(json.dumps({'cell':cell,'status':attempt['status'],'returncode':attempt['returncode']}),flush=True)
            break
        # Scoring starts from a fresh container without ChatGPT credentials.
        final=logdir/'final-workspace';final.mkdir(exist_ok=True)
        # Archive is our own container output; validate members before extraction.
        import tarfile
        with tarfile.open(logdir/'final-workspace.tgz') as archive:
            archive.extractall(final,filter='data')
        (final/'.env').write_text(env_text())
        r=score(final,'smartkit-score-'+cell.lower(),logdir/'evaluation')
        attempt.update({'status':'complete' if r['evaluator_completed'] else 'scoring_error',
                        'acceptance':r['acceptance'],'preservation':r['preservation'],'joint_success':r['joint_success'],'finished':stamp()})
        save(logdir/'attempt.json',attempt)
        print(json.dumps({key:attempt[key] for key in ['cell','status','elapsed_seconds','acceptance','preservation','joint_success']}),flush=True)
        if not r['evaluator_completed']:break

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['prepare','qualify','run']);args=parser.parse_args()
    {'prepare':prepare,'qualify':qualify,'run':run}[args.mode]()
