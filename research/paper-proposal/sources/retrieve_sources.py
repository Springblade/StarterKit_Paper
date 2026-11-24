"""Archive primary full texts for a claim-scoped review; retrieval is not review."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, subprocess, urllib.request
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
ARXIV = {
 'gloaguen2026agents':'2602.11988v3', 'zhu2026precedent':'2610.38244v1',
 'dente2026constraint':'2605.06445v2', 'patel2026codethread':'2606.21804v2',
 'zhao2026coverage':'2607.22880v1', 'jimenez2024swebench':'2310.06770v3',
 'yang2024sweagent':'2405.15793v3', 'xia2024agentless':'2407.01489v2',
 'deng2025swepro':'2509.16941v2', 'liu2023evalplus':'2305.01210v3',
 'shinn2023reflexion':'2303.11366v4', 'wang2026featurearc':'2610.37434v1',
 'mehta2026verification':'2608.28795v2'}
EXTRA = {
 'borg2026echoes':'https://link.springer.com/article/10.1007/s10664-026-10889-1',
 'parnas1972modules':'https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html',
 'barr2015oracle':'https://discovery.ucl.ac.uk/id/eprint/1471263/1/06963470.pdf',
 'inozemtseva2014coverage':'https://cs.uwaterloo.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf',
 'just2014mutants':'https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014.pdf',
 'arcuri2014statistics':'https://onlinelibrary.wiley.com/doi/10.1002/stvr.1486',
 'liu2024lost':'https://aclanthology.org/2024.tacl-1.9.pdf'}
def get(item):
 key, urls = item
 errors=[]
 for url in urls:
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=25) as r: data=r.read()
   pdf=data.startswith(b'%PDF')
   path=ROOT/(key+('.pdf' if pdf else '.html')); path.write_bytes(data)
   out=ROOT/(key+'.txt')
   if pdf: subprocess.run(['pdftotext','-layout',str(path),str(out)],check=True,capture_output=True)
   else:
    soup=BeautifulSoup(data,'html.parser')
    for tag in soup(['script','style','nav']): tag.decompose()
    out.write_text(soup.get_text(' ',strip=True),encoding='utf8')
   text=out.read_text(encoding='utf8')
   if len(text)<3000: raise ValueError('Content too short for full-text review')
   return {'key':key,'url':url,'characters':len(text),'file':out.name,'status':'retrieved','review_status':'not automatically reviewed'}
  except Exception as e: errors.append(str(e))
 return {'key':key,'status':'failed','errors':errors}
items=[(k,[f'https://arxiv.org/html/{v}',f'https://arxiv.org/pdf/{v}']) for k,v in ARXIV.items()]
items += [(k,[v]) for k,v in EXTRA.items()]
with ThreadPoolExecutor(max_workers=6) as pool: records=list(pool.map(get,items))
(ROOT/'retrieval-ledger.json').write_text(json.dumps(records,indent=2),encoding='utf8')
for r in records: print(r['key'],r['status'],r.get('characters',''),r.get('errors',''))
