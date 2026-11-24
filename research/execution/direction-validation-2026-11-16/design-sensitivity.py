"""Exact hypothetical sensitivity only; no agent outcomes or allocation changes."""
import math,json,hashlib,sys
from pathlib import Path
from functools import lru_cache
HERE=Path(__file__).resolve().parent
@lru_cache(None)
def sharp_p(positive,negative):
 n=positive+negative;observed=abs(positive-negative)
 return sum(math.comb(n,k) for k in range(n+1) if abs(2*k-n)>=observed)/(2**n)
def rejection_probability(pairs,alpha=.05):
 distribution={(0,0):1.}
 for p0,p1,rho in pairs:
  both=p0*p1+rho*math.sqrt(p0*(1-p0)*p1*(1-p1))
  assert max(0,p0+p1-1)-1e-12<=both<=min(p0,p1)+1e-12
  plus=p1-both;minus=p0-both;same=1-plus-minus
  updated={}
  for (a,b),mass in distribution.items():
   for key,chance in [((a+1,b),plus),((a,b+1),minus),((a,b),same)]:updated[key]=updated.get(key,0)+mass*chance
  distribution=updated
 assert abs(sum(distribution.values())-1)<1e-10
 return sum(mass for (a,b),mass in distribution.items() if sharp_p(a,b)<=alpha+1e-12)
def main():
 assert sharp_p(0,0)==1 and sharp_p(24,0)==2/(2**24)
 for p in [.2,.5,.8]:
  assert rejection_probability([(p,p,0)]*24)<=.05+1e-12
 assert abs(rejection_probability([(.3,.5,0)]*24)-rejection_probability([(.5,.3,0)]*24))<1e-12
 rows=[]
 for p0 in [.2,.5]:
  for delta in [0,.1,.2,.3,.4]:
   p1=round(p0+delta,10)
   for rho in [0,.3]:
    both=p0*p1+rho*math.sqrt(p0*(1-p0)*p1*(1-p1))
    if both>min(p0,p1)+1e-12:continue
    rows.append({'p_V0':p0,'p_V1':p1,'risk_difference':delta,'within_pair_binary_correlation':rho,'rejection_probability':rejection_probability([(p0,p1,rho)]*24)})
 heterogeneous=[]
 for delta in [0,.1,.2,.3]:
  rates=[.1,.2,.3,.4,.5,.6]
  heterogeneous.append({'baseline_task_rates':rates,'common_difference':delta,'pairs_per_task':4,'within_pair_binary_correlation':0,'rejection_probability':rejection_probability([(p,p+delta,0) for p in rates for rep in range(4)])})
 output={'scope':'Illustrative exact sensitivity for two-sided paired sharp-null randomization test, alpha .05,24 pairs. Hypothetical joint-success probabilities, not estimates, guarantees or test of zero average effect. No sampling of task/kit populations.','new_proposal':{'kits':2,'tasks_per_kit':3,'V_arms':2,'repetitions':4,'slots':48,'per_V':24,'per_kit_per_V':12,'per_task_per_V':4},'old_factorial':{'kits':1,'tasks':6,'S_arms':2,'V_arms':2,'repetitions':2,'slots':48,'per_V':24,'per_task_per_V':4},'conditional_independent_slot_Hoeffding95_halfwidth':math.sqrt(2*math.log(2/.05)/48),'old_two_contrast_simultaneous95_halfwidth':math.sqrt(2*math.log(4/.05)/48),'scenarios':rows,'heterogeneous_scenarios':heterogeneous,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'model_calls':0,'selfcheck':'probability mass, null calibration, swap symmetry, exact sharp p boundaries passed'}
 (HERE/'design-sensitivity.json').write_text(json.dumps(output,indent=2)+'\n')
 for row in rows:
  if row['within_pair_binary_correlation']==0:print(json.dumps(row))
 print('Conditional single-contrast Hoeffding halfwidth',output['conditional_independent_slot_Hoeffding95_halfwidth'])
 print('Synthetic exact sensitivity checks passed; no model calls.')
if __name__=='__main__':main()
