"""Common isolated runtime, using Next's documented Turbopack dev-server option.

No model client or account credentials. Source/auth/dependency behavior unchanged.
https://nextjs.org/docs/app/api-reference/cli/next#next-dev-options
"""
from pathlib import Path
import json
import os
import subprocess
import time

IMAGE = 'smartkit-main48:20261115'
DEV_BUNDLER = 'turbopack'


def call(args, *, check=True, timeout=240):
    p = subprocess.run([str(a) for a in args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    if check and p.returncode:
        raise RuntimeError(f'Command failed ({p.returncode}): {args[:3]}\n' + p.stdout.decode(errors='replace')[-1200:])
    return p


def docker(*args, **kwargs):
    return call(['docker', *args], **kwargs)


def stamp():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def env_text():
    return '''DATABASE_URL="postgresql://postgres:local-pilot-only@pilot-db:5432/smartkit_pilot"
BETTER_AUTH_SECRET="local-development-pilot-secret-at-least-32-characters"
BETTER_AUTH_URL="http://localhost:3107"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3107"
NEXT_PUBLIC_APP_URL="http://localhost:3107"
NEXT_PUBLIC_GOOGLE_ENABLED="false"
RESEND_FROM_EMAIL="onboarding@resend.dev"
SEPAY_API_KEY="synthetic-study-only"
SEPAY_WEBHOOK_SECRET="local-development-pilot-only"
CRON_SECRET="local-development-pilot-only"
NODE_ENV="development"
'''


def start(name, package, logdir):
    net, db = name + '-net', name + '-db'
    logdir.mkdir(parents=True, exist_ok=True)
    docker('network', 'create', net)
    docker('run', '-d', '--name', db, '--network', net, '--network-alias', 'pilot-db',
           '-e', 'POSTGRES_PASSWORD=local-pilot-only', '-e', 'POSTGRES_DB=smartkit_pilot', 'postgres:16-alpine')
    docker('run', '-d', '--name', name, '--network', net, IMAGE)
    docker('cp', str(package) + os.sep + '.', name + ':/workspace/')
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if docker('exec', db, 'pg_isready', '-h', '127.0.0.1', '-p', '5432', '-U', 'postgres', '-d', 'smartkit_pilot', check=False).returncode == 0:
            break
        time.sleep(.25)
    else:
        raise RuntimeError('PostgreSQL TCP readiness failed')
    for command, filename in [('pnpm db:migrate', 'migrate.log'), ('pnpm db:seed', 'seed.log')]:
        p = docker('exec', name, 'sh', '-c', command, check=False)
        (logdir / filename).write_bytes(p.stdout)
        if p.returncode:
            raise RuntimeError(filename + ' failed')
    docker('exec', name, 'mkdir', '-p', '/opt/study')
    docker('cp', Path(__file__).with_name('mock-sepay.cjs'), name + ':/opt/study/mock-sepay.cjs')
    command = 'NODE_OPTIONS=--require=/opt/study/mock-sepay.cjs pnpm exec next dev --turbopack -p 3107 > /tmp/app.log 2>&1'
    docker('exec', '-d', name, 'sh', '-c', command)
    probe = "fetch('http://localhost:3107/',{signal:AbortSignal.timeout(10000)}).then(r=>process.exit(r.status===200?0:1)).catch(()=>process.exit(1))"
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        if docker('exec', name, 'node', '-e', probe, check=False, timeout=15).returncode == 0:
            break
        time.sleep(.3)
    else:
        raise RuntimeError('Application readiness failed')
    warm = "(async()=>{for(const p of ['/api/auth/get-session','/auth/sign-in','/auth/sign-up','/auth/reset-password','/dashboard','/dashboard/settings','/dashboard/admin/users','/dashboard/billing']){const r=await fetch('http://localhost:3107'+p,{signal:AbortSignal.timeout(90000)});if(r.status>=500)throw Error(p+':'+r.status);console.log(p+' '+r.status)}})().catch(e=>{console.error(e);process.exit(1)})"
    warmed = docker('exec', name, 'node', '-e', warm, timeout=240)
    (logdir / 'warmup.log').write_bytes(warmed.stdout)
    docker('exec', name, 'sh', '-c', 'git init -q && git config user.name Pilot && git config user.email pilot@local.invalid && git add . && git commit -qm baseline')
    info = json.loads(docker('inspect', name).stdout)[0]
    assert not info['Mounts'] and not info['HostConfig']['Privileged']
    assert info['HostConfig']['PidMode'] != 'host'
    probe = "const f=require('fs');for(const p of ['/research','/var/run/docker.sock','/workspace/.git/objects/info/alternates'])if(f.existsSync(p))process.exit(1);"
    docker('exec', name, 'node', '-e', probe)
    (logdir / 'isolation.json').write_text(json.dumps({'no_host_mounts': True, 'no_docker_socket': True,
        'private_pid_namespace': True, 'fresh_single_commit': True, 'image_id': info['Image'],
        'network': net, 'dev_bundler': DEV_BUNDLER}, indent=2) + '\n', encoding='utf-8')
    return docker('exec', name, 'git', 'rev-parse', 'HEAD').stdout.decode().strip()


def stop(name, logdir):
    app_log = docker('exec', name, 'cat', '/tmp/app.log', check=False)
    if app_log.returncode == 0:
        (logdir / 'app.log').write_bytes(app_log.stdout)
    db_log = docker('logs', name + '-db', check=False)
    if db_log.returncode == 0:
        (logdir / 'postgres.log').write_bytes(db_log.stdout)
    docker('rm', '-f', '-v', name, name + '-db', check=False)
    docker('network', 'rm', name + '-net', check=False)
