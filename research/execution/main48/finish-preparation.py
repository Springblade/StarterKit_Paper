"""Complete the required matrix and rehearsals serially; never invokes models."""
import argparse,subprocess,sys
from pathlib import Path
from prepare import TASKS
HERE=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--layout',choices=['feature','layered'],required=True);a=ap.parse_args()
 commands=[['qualify.py','--layout',a.layout,'--reliability','--basic']]
 commands += [['qualify.py','--layout',a.layout,'--task',task,'--variant','fault','--basic'] for task in TASKS]
 commands += [['collect.py','rehearse','--layout',a.layout]]
 for command in commands:
  print('Preparation phase: '+' '.join(command),flush=True)
  result=subprocess.run([sys.executable,'-X','utf8',str(HERE/command[0]),*command[1:]])
  if result.returncode:raise SystemExit(result.returncode)
 print('Required qualification, reliability and rehearsals completed for '+a.layout+'; no model calls.',flush=True)
if __name__=='__main__':main()
