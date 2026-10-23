"""Reconstruct eight requests, verify frozen PNGs and replay independent trackers."""
import base64
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import benchmark_segment as b
from audit_routing import same


def audit(out):
    r = json.loads((out / 'results.json').read_text(encoding='utf-8'))
    assert r['fixture_manifest_sha256'] == b.digest(b.manifest())
    assert r['model'] == b.MODEL and r['limits'] == b.LIMITS
    assert [[c['history'], c['condition']] for c in r['calls']] == b.manifest()['event_order'][:len(r['calls'])]
    seen, controls, answers = set(), [], []
    with tempfile.TemporaryDirectory() as t:
        for c in r['calls']:
            key = (c['history'], c['condition'])
            assert key not in seen
            seen.add(key)
            p, observer, assets = b.build_payload(Path(t), *key)
            assert c['model_input'] == {k: v for k, v in p.items() if k != 'assets'}
            assert c['request_sha256'] == b.digest(p)
            assert c['asset_audit'] == assets
            assert all(same(c[k], v) for k, v in observer.items())
            for a in assets:
                data = (out / a['file']).read_bytes()
                assert hashlib.sha256(data).hexdigest() == a['sha256']
                assert data == base64.b64decode(p['assets'][a['asset']]['data_base64'])
            pixel = b.tracker(p, out, 'raster')
            text = b.tracker(p, out, 'coordinates')
            assert c['baseline_predictions'] == {'raster': pixel, 'coordinates': text,
                                                  'matched': text if c['condition'] == 'text_history' else pixel}
            if c['condition'] == 'final_only':
                assert c['reference_next_action'] is None and not c['identifiable']
                controls.append(c['request_sha256'])
            if c.get('response'):
                response = c['response']
                raw = {'model': response['returned_model'], **{k: v for k, v in response.items() if k != 'returned_model'}}
                assert b.native.sanitize(raw, p['questions']) == response
                answers.extend(response['answers'].values())
    assert len(set(controls)) <= 1
    if r['status'] in ('completed', 'completed_with_failures', 'offline_only'):
        assert seen == {(h, c) for h in b.HISTORIES for c in b.CONDITIONS}
    if r['status'] == 'completed':
        assert len(answers) == 8
    assert same(r['analysis'], b.analyze(r['calls']))
    assert r['analysis']['by_condition']['final_only']['next_step_accuracy'] is None
    m = b.manifest()
    assert m['scene_asset_refs']['move_A_2'] == m['scene_asset_refs']['move_B_2'] == m['scene_asset_refs']['current']
    result = {'status': r['status'], 'run_id': r['run_id'], 'source_commit': r['source_commit'],
              'requests_reconstructed': len(seen), 'native_choice_answers_verified': len(answers),
              'same_final_png_bytes': True, 'final_control_request_hashes_identical': len(set(controls)) <= 1,
              'candidate_options_identical_across_conditions_and_histories': True,
              'trackers_replayed_from_actual_pngs_and_supplied_coordinates': True,
              'final_only_next_step_accuracy': None, 'by_condition': r['analysis']['by_condition'],
              'usage_totals': r['analysis']['usage_totals'],
              'native_confidence_count': sum(a['confidence'] is not None for a in answers),
              'numeric_reliability_count': sum(a['reliability'] is not None for a in answers),
              'numeric_replay_tolerance': 1e-12}
    (out / 'artifact-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(audit(Path(sys.argv[1])), indent=2))
