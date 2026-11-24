"""Run independent no-model cases serially; stop on a failed candidate."""
from pathlib import Path
import argparse,subprocess,sys
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--layout',required=True,choices=['feature','layered']);p.add_argument('--tasks',nargs='+',default=['A01','A03','B03','B04','U02','U03']);p.add_argument('--phase',default='reference');a=p.parse_args()
for task in a.tasks:
    print('Starting reference '+a.layout+'/'+task,flush=True)
    r=subprocess.run([sys.executable,str(HERE/'verify.py'),'--layout',a.layout,'--task',task,'--phase',a.phase])
    if r.returncode:sys.exit(r.returncode)
