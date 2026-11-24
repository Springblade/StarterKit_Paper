"""Seeded-fault detection checks; no model and no baseline changes."""
from pathlib import Path
import argparse,subprocess,sys
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--layout',required=True,choices=['feature','layered']);a=p.parse_args()
cases=[('A03','fault-confirmation'),('B03','fault-foreign-resume'),('B04','fault-foreign-receipt'),('U02','fault-no-admin-guard'),('U03','fault-cached-role'),('U03','fault-self-demotion')]
for task,variant in cases:
 print('Checking seeded fault '+a.layout+'/'+task+'/'+variant,flush=True)
 r=subprocess.run([sys.executable,str(HERE/'verify.py'),'--layout',a.layout,'--task',task,'--phase',variant])
 if r.returncode:sys.exit(r.returncode)
