"""Small negative tests for the collection boundary; no model credentials or calls."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from types import SimpleNamespace
import json
import collect,qualify,analysis
from prepare import HERE,digest,save

def rejects(fn):
 try:fn()
 except (AssertionError,FileNotFoundError,ValueError,StopIteration,RuntimeError):return
 raise AssertionError('Expected fail-closed rejection')
def main():
 with TemporaryDirectory(prefix='smartkit-selfcheck-') as tmp:
  root=Path(tmp);p=root/'x.json';x={'completed':True,'pass':True};p.write_text(json.dumps(x));process=SimpleNamespace(stdout=json.dumps(x).encode(),returncode=0)
  assert qualify.read_result(process,p)==x
  rejects(lambda:qualify.read_result(SimpleNamespace(stdout=b'{"completed":false}',returncode=0),p))
  rejects(lambda:qualify.read_result(SimpleNamespace(stdout=process.stdout,returncode=2),p))
  assert collect.next_slot(root,'slot')==root/'slot'/'attempt.json'
  save(root/'slot'/'attempt.json',{'invoked':True,'status':'infrastructure-error'})
  assert collect.next_slot(root,'slot') is None
 collect.require_quota({'buckets':{'codex':{'primary':{'usedPercent':99}}}},'gpt-6-luna')
 rejects(lambda:collect.require_quota({'buckets':{'codex':{'secondary':{'usedPercent':100}}}},'gpt-6-luna'))
 rejects(lambda:collect.require_quota({'buckets':{'codex':{'rateLimitReachedType':'usageLimit'}}},'gpt-6-luna'))
 rejects(lambda:collect.require_quota({'buckets':{}},'gpt-6-luna'))
 rejects(lambda:collect.require_quota({'buckets':{'codex':{'primary':None,'secondary':None}}},'gpt-6-luna'))
 release={'approved':True,'freeze_sha256':'current','scope':'one-48-slot-collection-no-replacements'}
 with patch.object(collect,'audit',return_value=({'configuration':{}},{'model':'gpt-6-luna','slots':[{'slot':'unstarted'}]})),patch.object(Path,'read_text',side_effect=[json.dumps(release),json.dumps({'auth_mode':'chatgpt'})]),patch.object(collect,'digest',return_value='current'),patch.object(collect,'next_slot',return_value=Path('never-created/attempt.json')),patch.object(collect,'read_quota',return_value={'buckets':{'codex':{'secondary':{'usedPercent':100}}}}),patch.object(collect.subprocess,'Popen') as process,patch.object(collect.runtime,'docker') as docker:
  rejects(collect.run);process.assert_not_called();docker.assert_not_called()
 with patch.object(collect,'audit',return_value=({},{})),patch.object(Path,'read_text',side_effect=FileNotFoundError('No start release')),patch.object(collect.subprocess,'Popen') as process,patch.object(collect.runtime,'docker') as docker:
  rejects(collect.run);process.assert_not_called();docker.assert_not_called()
 with patch.object(collect,'audit',return_value=({},{})),patch.object(Path,'read_text',return_value=json.dumps({'approved':True,'freeze_sha256':'wrong','scope':'one-48-slot-collection-no-replacements'})),patch.object(collect,'digest',return_value='current'),patch.object(collect.subprocess,'Popen') as process,patch.object(collect.runtime,'docker') as docker:
  rejects(collect.run);process.assert_not_called();docker.assert_not_called()
 analysis.selfcheck()
 save(HERE/'selfcheck.json',{'pass':True,'model_calls':0,'checks':['stale-result-rejection','checker-error-rejection','invoked-slot-never-replaced','missing-or-stale-author-start-release-cannot-launch-anything','known-exhausted-or-unavailable-quota-rejected-before-invocation','synthetic-analysis-boundaries'],'files':{p.name:digest(p) for p in [HERE/'collect.py',HERE/'qualify.py',HERE/'analysis.py',Path(__file__)]}})
 print('Collection self-check passed; no model calls.')
if __name__=='__main__':main()
