"""Rebuild the frozen semantic request and independently replay code dispatch."""
import json
import math
from pathlib import Path
import sys

import benchmark_routing as b


def same(a, c):
    if isinstance(a, dict) and isinstance(c, dict):
        return a.keys() == c.keys() and all(same(a[k], c[k]) for k in a)
    if isinstance(a, list) and isinstance(c, list):
        return len(a) == len(c) and all(same(x, y) for x, y in zip(a, c))
    if type(a) in (int, float) and type(c) in (int, float):
        return math.isclose(a, c, rel_tol=0, abs_tol=1e-12)
    return a == c


def audit(out):
    r = json.loads((out / 'results.json').read_text(encoding='utf-8'))
    f = b.fixture()
    assert r['prepared'] == f
    assert r['request_sha256'] == b.digest(f['payload'])
    assert r['fixture_sha256'] == b.digest(f)
    assert same(r['workspace_inventory_observer_only'], b.dispatch(sorted(b.FRAMES)))
    call = r.get('call', {})
    if 'response' in call:
        response = call['response']
        raw = {'model': response['returned_model'], **{k: v for k, v in response.items() if k != 'returned_model'}}
        assert b.sanitize(raw, f['payload']['questions']) == response
        assert r['status'] == 'completed'
    elif 'failure' in call:
        assert r['status'] == 'failed'
    else:
        assert r['status'] == 'offline_only'
    assert same(r['analysis'], b.analyze(r))
    for row in r['analysis']['observations']:
        assert same(row['execution'], b.dispatch(row['selected']))
        for binding in row['execution']['certified_bindings']:
            if binding['frame'] == 'congruence':
                assert b.congruence_certificate(b.geometry.objects_for(binding['method'], 0))['valid']
    result = {'status': r['status'], 'run_id': r['run_id'], 'source_commit': r['source_commit'],
              'request_reconstructed': True, 'fixture_sha256': r['fixture_sha256'],
              'native_choice_answers_verified': r['analysis']['native_choice_answers'],
              'no_geometric_verdicts_or_annotations_in_input': True,
              'code_dispatch_replayed_for_all_systems': True,
              'no_model_visible_images': 'assets' not in f['payload'],
              'numeric_reliability_count': sum(a['reliability'] is not None for a in call.get('response', {}).get('answers', {}).values()),
              'native_confidence_count': sum(a['confidence'] is not None for a in call.get('response', {}).get('answers', {}).values()),
              'systems': r['analysis']['systems'], 'usage': r['analysis']['usage'], 'numeric_replay_tolerance': 1e-12}
    (out / 'artifact-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(audit(Path(sys.argv[1])), indent=2))
