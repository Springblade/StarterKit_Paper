"""Small checks of result provenance and the no-authorization/no-model boundary."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir
from types import SimpleNamespace
from unittest.mock import patch
import pilot
from qualify import read_result


def rejects(fn):
    try:
        fn()
    except (AssertionError, FileNotFoundError, StopIteration):
        return
    raise AssertionError('Invalid operation was accepted')


def main():
    with TemporaryDirectory(prefix='smartkit-preflight-') as name:
        folder = Path(name).resolve()
        assert folder.is_relative_to(Path(gettempdir()).resolve())
        path = folder / 'result.json'
        value = {'completed': True, 'pass': True}
        path.write_text(json.dumps(value), encoding='utf-8')
        process = SimpleNamespace(stdout=(json.dumps(value) + '\n').encode(), returncode=0)
        assert read_result(process, path, visible_suite=True) == value
        rejects(lambda: read_result(SimpleNamespace(stdout=b'', returncode=1), path, True))
        rejects(lambda: read_result(SimpleNamespace(stdout=b'{"completed":false}\n', returncode=0), path, True))
        rejects(lambda: read_result(SimpleNamespace(stdout=process.stdout, returncode=1), path, True))
        value['pass'] = False
        path.write_text(json.dumps(value), encoding='utf-8')
        assert read_result(SimpleNamespace(stdout=json.dumps(value).encode(), returncode=1), path, True) == value
        runs = folder / 'runs'
        assert pilot.next_attempt(runs, 'test-slot').name == 'attempt-01'
        record = runs / 'test-slot/attempt-01/attempt.json'
        record.parent.mkdir(parents=True)
        record.write_text(json.dumps({'status': 'complete'}), encoding='utf-8')
        assert pilot.next_attempt(runs, 'test-slot') is None
        record.write_text(json.dumps({'status': 'infrastructure-interrupted-needs-adjudication'}), encoding='utf-8')
        rejects(lambda: pilot.next_attempt(runs, 'test-slot'))
        (record.parents[1] / 'adjudication.json').write_text(json.dumps({'parent_attempt': 'attempt-01',
            'category': 'infrastructure-only', 'allow_model_replacement': True,
            'reason': 'Synthetic test outage', 'evidence': 'synthetic fixture only'}), encoding='utf-8')
        assert pilot.next_attempt(runs, 'test-slot').name == 'attempt-02'
        for i in range(6):
            (runs / f'other-{i}/attempt-02').mkdir(parents=True)
        rejects(lambda: pilot.next_attempt(runs, 'test-slot'))
    # audit is stubbed so this checks the release guard independently of readiness.
    # Popen and docker must remain unreachable when the author release is absent.
    with patch.object(pilot, 'audit', return_value=({}, {})), \
         patch.object(Path, 'read_text', side_effect=FileNotFoundError('author release missing')), \
         patch.object(pilot.subprocess, 'Popen') as launch, \
         patch.object(pilot.runtime, 'docker') as docker:
        rejects(pilot.run)
        launch.assert_not_called()
        docker.assert_not_called()
    print('Preflight self-check passed: stale results rejected; missing author release cannot invoke model/tools')


if __name__ == '__main__':
    main()
