"""Fixed 48-slot descriptive analysis. Missing outcomes yield bounds, never replacements."""
from pathlib import Path
import argparse,json,math
from prepare import HERE,TASKS,CELLS,save

def sharp_p(pairs):
 # Conditional randomization within each held-fixed factor level and task/repetition block.
 discordant=[a-b for a,b in pairs if a!=b];n=len(discordant);observed=abs(sum(discordant))
 return sum(math.comb(n,k) for k in range(n+1) if abs(2*k-n)>=observed)/(2**n)

def analyze(rows):
 assert len(rows)==48 and len({r['slot'] for r in rows})==48
 cells=[]
 for task in TASKS:
  for cell in CELLS:
   selected=[r for r in rows if r['task']==task and r['cell']==cell];assert len(selected)==2
   cells.append({'task':task,'cell':cell,'planned':2,'invoked':sum(bool(r.get('invoked')) for r in selected),'assessable':sum(r.get('joint') is not None for r in selected),'success':sum(r.get('joint') is True for r in selected)})
 contrasts={}
 for factor,index in [('S',1),('V',3)]:
  plus=[r for r in rows if r['cell'][index]=='1'];minus=[r for r in rows if r['cell'][index]=='0']
  observed=sum(r.get('joint') is True for r in plus)/24-sum(r.get('joint') is True for r in minus)/24
  missing_plus=sum(r.get('joint') is None for r in plus);missing_minus=sum(r.get('joint') is None for r in minus)
  bounds=[observed-missing_minus/24,observed+missing_plus/24]
  value={'risk_difference':observed if not missing_plus+missing_minus else None,'all-planned-outcome_bounds':bounds,'missing_high':missing_plus,'missing_low':missing_minus}
  if not missing_plus+missing_minus:
   h=math.sqrt(2*math.log(4/.05)/48);value['simultaneous95_Hoeffding_independent_slots']=[max(-1,observed-h),min(1,observed+h)]
   pairs=[]
   for task in TASKS:
    for rep in [1,2]:
     for other in [0,1]:
      a=f'S1V{other}' if factor=='S' else f'S{other}V1';b=f'S0V{other}' if factor=='S' else f'S{other}V0'
      pair=[next(r for r in rows if r['task']==task and r['repetition']==rep and r['cell']==c)['joint'] for c in [a,b]];pairs.append(pair)
   value['sharp_no_factor_effect_randomization_p']=sharp_p(pairs)
  contrasts[factor]=value
 if all('sharp_no_factor_effect_randomization_p' in v for v in contrasts.values()):
  order=sorted(contrasts,key=lambda k:contrasts[k]['sharp_no_factor_effect_randomization_p']);prev=0
  for i,k in enumerate(order):prev=max(prev,min(1,(2-i)*contrasts[k]['sharp_no_factor_effect_randomization_p']));contrasts[k]['Holm_adjusted_sharp_p']=prev
 sensitivity=[]
 groups=[('omit-task-'+t,{t}) for t in TASKS]+[('omit-auth',{'A01','A04'}),('omit-billing',{'B05','B06'}),('omit-admin',{'U02','U03'})]
 for label,excluded in groups:
  subset=[r for r in rows if r['task'] not in excluded];values={}
  for factor,index in [('S',1),('V',3)]:
   high=[r for r in subset if r['cell'][index]=='1'];low=[r for r in subset if r['cell'][index]=='0'];n=len(high);assert n==len(low)
   point=(sum(r.get('joint') is True for r in high)-sum(r.get('joint') is True for r in low))/n;mh=sum(r.get('joint') is None for r in high);ml=sum(r.get('joint') is None for r in low)
   values[factor]={'risk_difference':point if not mh+ml else None,'bounds':[point-ml/n,point+mh/n]}
  sensitivity.append({'analysis':label,'remaining_tasks':len(set(r['task'] for r in subset)),'contrasts':values})
 times=[r['elapsed_seconds'] for r in rows if r.get('invoked') and r.get('elapsed_seconds') is not None]
 usages=[u for r in rows for u in r.get('usage_events',[])];token_totals={key:sum(u[key] for u in usages if isinstance(u.get(key),int)) for key in ['input_tokens','cached_input_tokens','output_tokens']}
 def check_audit(subset):
  counts={f'B1-{b}-EP-{e}':0 for b in ['pass','fail'] for e in ['pass','fail']};missing=0
  for r in subset:
   if r.get('B1') is None or r.get('EP') is None:missing+=1
   else:counts[f"B1-{'pass' if r['B1'] else 'fail'}-EP-{'pass' if r['EP'] else 'fail'}"]+=1
  return {'jointly_assessable':len(subset)-missing,'missing':missing,'counts':counts}
 audit={'overall':check_audit(rows),'by_condition':{c:check_audit([r for r in rows if r['cell']==c]) for c in CELLS},'by_task':{t:check_audit([r for r in rows if r['task']==t]) for t in TASKS}}
 examples={}
 for task in TASKS:
  candidates=[r for r in rows if r['task']==task and r.get('joint') is not None];chosen=next((r for r in candidates if r['joint'] is False),candidates[0] if candidates else None);examples[task]=chosen['slot'] if chosen else None
 secondary=None
 if all(r.get('joint') is not None for r in rows):
  means={c:sum(r['joint'] for r in rows if r['cell']==c)/12 for c in CELLS}
  secondary={'condition_means':means,'S_at_V0':means['S1V0']-means['S0V0'],'S_at_V1':means['S1V1']-means['S0V1'],'V_at_S0':means['S0V1']-means['S0V0'],'V_at_S1':means['S1V1']-means['S1V0'],'interaction':means['S1V1']-means['S1V0']-means['S0V1']+means['S0V0']}
 return {'planned':48,'invoked':sum(bool(r.get('invoked')) for r in rows),'assessable':sum(r.get('joint') is not None for r in rows),'cells':cells,'contrasts':contrasts,'secondary':secondary,'sensitivity':sensitivity,'preservation_audit':audit,'rule_selected_examples':examples,'cost':{'recorded_invocation_times':len(times),'total_seconds':sum(times),'recorded_usage_events':len(usages),'reported_token_totals':token_totals if usages else None,'scope':'all invoked slots including timeouts/errors; preparation and offline grading excluded; unavailable token usage remains missing'},'scope':'six fixed constructed tasks; task-cell counts precede exploratory contrasts; sharp p-values are not tests of average-effect nulls'}

def load_records():
 allocation=json.loads((HERE/'allocation.json').read_text())['slots'];rows=[]
 for slot in allocation:
  path=HERE/'runs'/slot['slot']/'attempt.json';record=json.loads(path.read_text()) if path.exists() else {};out=record.get('outcome',{});assessable=out.get('completed') and out.get('assessable',out.get('E',{}).get('assessable',True))
  rows.append({**slot,'invoked':record.get('invoked',False),'joint':bool(out.get('jointSuccess')) if assessable else None,'B1':out.get('V1',{}).get('pass') if out.get('V1',{}).get('completed') else None,'EP':out.get('E',{}).get('preservation') if out.get('E',{}).get('completed') and out.get('E',{}).get('assessable',True) else None,'status':record.get('status','unstarted'),'elapsed_seconds':record.get('elapsed_seconds'),'usage_events':record.get('usage_events',[])})
 return rows

def selfcheck():
 slots=json.loads((HERE/'allocation.json').read_text())['slots']
 rows=[{**r,'invoked':True,'joint':r['cell'][1]=='1'} for r in slots];value=analyze(rows);assert value['contrasts']['S']['risk_difference']==1 and value['contrasts']['V']['risk_difference']==0
 rows[0]['joint']=None;assert analyze(rows)['contrasts']['S']['risk_difference'] is None
 assert sharp_p([(True,False)]*24)==2/(2**24)
 assert sharp_p([(True,True)]*24)==1
 print('Analysis self-check passed (synthetic only, never an agent result).')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--selfcheck',action='store_true');a=ap.parse_args()
 if a.selfcheck:selfcheck()
 else:save(HERE/'analysis-results.json',analyze(load_records()))
