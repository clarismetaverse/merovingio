import copy
import json
import math
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
import benchmark_segment as b
from audit_segment import audit


class SegmentTests(unittest.TestCase):
    def test_two_histories_converge_to_exactly_same_final_pixels(self):
        self.assertEqual(b.observations('move_A')[-1], b.observations('move_B')[-1])
        self.assertEqual(b.render(b.observations('move_A')[-1]).tobytes(), b.render(b.observations('move_B')[-1]).tobytes())
        for i in range(2):
            self.assertNotEqual(b.observations('move_A')[i], b.observations('move_B')[i])
            self.assertEqual(math.dist(*b.observations('move_A')[i].values()), math.dist(*b.observations('move_B')[i].values()))

    def test_endpoint_identity_and_fixed_equal_step_rule(self):
        for history, fixed, moving in [('move_A', 'B', 'A'), ('move_B', 'A', 'B')]:
            scenes = b.observations(history)
            self.assertEqual(len({tuple(s[fixed]) for s in scenes}), 1)
            self.assertEqual([math.dist(scenes[i][moving], scenes[i - 1][moving]) for i in (1, 2)], [25, 25])
            self.assertEqual(b.next_prediction(scenes), b.candidates()['extend_' + moving])

    def test_candidates_are_valid_but_only_two_are_prolongations(self):
        certs = {k: b.geometry_certificate(v) for k, v in b.candidates().items()}
        self.assertTrue(all(c['nondegenerate'] and c['collinear_with_current'] and c['equal_step_size_if_changed'] for c in certs.values()))
        self.assertEqual({k for k, v in certs.items() if v['strict_extension']}, {'extend_A', 'extend_B'})
        self.assertEqual(certs['hold']['changed_endpoints'], [])

    def test_final_only_requests_are_exactly_identical_and_nonidentifiable(self):
        with tempfile.TemporaryDirectory() as t:
            a, ma, _ = b.build_payload(Path(t), 'move_A', 'final_only')
            c, mc, _ = b.build_payload(Path(t), 'move_B', 'final_only')
            self.assertEqual(a, c)
            self.assertEqual(b.digest(a), b.digest(c))
            self.assertIsNone(ma['reference_next_action'])
            self.assertIsNone(mc['reference_next_action'])
            self.assertNotEqual(ma['history'], mc['history'])

    def test_budget_fixed_order_and_visual_option_mapping(self):
        m = b.manifest()
        self.assertEqual(len(m['event_order']), 8)
        self.assertEqual(len(set(map(tuple, m['event_order']))), 8)
        common = None
        with tempfile.TemporaryDirectory() as t:
            for h, c in m['event_order']:
                p, _, assets = b.build_payload(Path(t), h, c)
                self.assertEqual(len(p['questions']), 1)
                self.assertEqual(p['questions']['next']['type'], 'choice')
                criteria = p['questions']['next']['criteria']
                self.assertEqual(len(criteria), 6)
                self.assertEqual(sum('next_view' in v for v in criteria.values()), 5)
                if common is None:
                    common = criteria
                self.assertEqual(criteria, common)
                self.assertTrue(all(a['asset'] in p['assets'] for a in assets))

    def test_modalities_differ_only_in_available_observations(self):
        with tempfile.TemporaryDirectory() as t:
            for history in b.HISTORIES:
                images = b.build_payload(Path(t), history, 'images')[0]
                text = b.build_payload(Path(t), history, 'text_history')[0]
                both = b.build_payload(Path(t), history, 'combined')[0]
                self.assertEqual(images['assets'], both['assets'])
                for i, frame in enumerate(both['state']['observations']):
                    self.assertEqual({k: v for k, v in frame.items() if k != 'endpoint_coordinates'}, images['state']['observations'][i])
                    self.assertEqual({k: v for k, v in frame.items() if k != 'image'}, text['state']['observations'][i])
                self.assertNotEqual(images['assets'], text['assets'])
                self.assertTrue(text['assets'])  # Candidate images remain present.

    def test_no_gold_or_history_label_in_model_visible_input(self):
        forbidden = {'history', 'condition', 'reference', 'reference_response', 'reference_next_action', 'identifiable',
                     'baseline_predictions', 'candidate_certificates_observer_only', 'strict_extension', 'option_mapping', 'correct'}
        def walk(v):
            if isinstance(v, dict):
                self.assertFalse(forbidden & set(v))
                for x in v.values():
                    walk(x)
            elif isinstance(v, list):
                for x in v:
                    walk(x)
        with tempfile.TemporaryDirectory() as t:
            for h, c in b.manifest()['event_order']:
                p, _, _ = b.build_payload(Path(t), h, c)
                walk(p)
                self.assertFalse(any(k in json.dumps(p['questions']['next']['instructions']) for k in b.manifest()['option_mapping']))
                self.assertNotIn('move_A', json.dumps(p))
                self.assertNotIn('extend_A', json.dumps(p))

    def test_frozen_rasters_have_no_metadata_and_palette_centers_match(self):
        m = b.manifest()
        files = {a['asset']: b.HERE / 'fixtures' / a['file'] for a in m['assets']}
        for history in b.HISTORIES:
            for i, scene in enumerate(b.observations(history)):
                path = files[m['scene_asset_refs'][history + '_' + str(i)]]
                self.assertEqual(b.raster_endpoints(path), scene)
                with Image.open(path) as image:
                    self.assertEqual(image.size, (384, 384))
                    self.assertFalse(image.info)

    def test_raster_tracking_does_not_read_renderer_or_oracle_coordinates(self):
        with tempfile.TemporaryDirectory() as t:
            for history in b.HISTORIES:
                p = b.build_payload(Path(t), history, 'images')[0]
                with patch.object(b, 'observations', side_effect=AssertionError('oracle consulted')), patch.object(b, 'candidates', side_effect=AssertionError('oracle consulted')):
                    self.assertEqual(b.tracker(p, Path(t), 'raster'), 'extend_' + history[-1])

    def test_all_matched_trackers_and_combined_agreement(self):
        with tempfile.TemporaryDirectory() as t:
            for h, c in b.manifest()['event_order']:
                p, meta, _ = b.build_payload(Path(t), h, c)
                raster = b.tracker(p, Path(t), 'raster')
                text = b.tracker(p, Path(t), 'coordinates')
                chosen = text if c == 'text_history' else raster
                self.assertEqual(chosen, meta['reference_response'])
                if c == 'combined':
                    self.assertEqual(raster, text)

    def test_tracker_abstains_on_absent_or_conflicting_motion(self):
        scene = b.observations('move_A')[-1]
        self.assertIsNone(b.next_prediction([scene]))
        self.assertIsNone(b.next_prediction([scene, scene]))
        bad = copy.deepcopy(b.observations('move_A'))
        bad[-1]['B'][0] += 10
        self.assertIsNone(b.next_prediction(bad))
        bad = copy.deepcopy(b.observations('move_A'))
        bad[-1]['A'][0] += 10
        self.assertIsNone(b.next_prediction(bad))

    def test_continuation_covaries_with_rigid_transform(self):
        for angle in (0, 37, 90, 181):
            for sign in (-1, 1):
                r = math.radians(angle)
                def transform(s):
                    return {k: [sign * p[0] * math.cos(r) - p[1] * math.sin(r), sign * p[0] * math.sin(r) + p[1] * math.cos(r)] for k, p in s.items()}
                for history in b.HISTORIES:
                    actual = b.next_prediction([transform(s) for s in b.observations(history)])
                    expected = transform(b.candidates()['extend_' + history[-1]])
                    for k in actual:
                        self.assertLess(math.dist(actual[k], expected[k]), 1e-9)

    def test_local_live_guard(self):
        with tempfile.TemporaryDirectory() as t, patch.dict(os.environ, {}, clear=True), patch.object(b.native, 'transport') as transport:
            with self.assertRaises(SystemExit):
                b.main(Path(t), True)
            transport.assert_not_called()

    def test_rejection_saves_partial_and_never_retries(self):
        with tempfile.TemporaryDirectory() as t, patch.dict(os.environ, {'GITHUB_ACTIONS': 'true', 'TYPESAFE_API_KEY': 'test-only'}, clear=True), patch.object(b.native, 'transport', return_value={'failure': 'HTTP_403'}) as transport:
            with self.assertRaises(SystemExit):
                b.main(Path(t), True)
            self.assertEqual(transport.call_count, 1)
            self.assertEqual(audit(Path(t))['status'], 'request_rejected')

    def test_offline_audit_and_nonidentifiable_accuracy_null(self):
        with tempfile.TemporaryDirectory() as t:
            b.main(Path(t))
            result = audit(Path(t))
            self.assertEqual(result['native_choice_answers_verified'], 0)
            self.assertIsNone(result['final_only_next_step_accuracy'])

    def test_synthetic_live_answers_preserve_all_eight_and_detect_tamper(self):
        # Synthetic responses exercise plumbing only; never enter live artifacts.
        def answer(p):
            frames = p['state']['observations']
            if len(frames) == 1:
                action = 'insufficient'
            elif 'endpoint_coordinates' in frames[0]:
                action = 'extend_A' if frames[0]['endpoint_coordinates']['A'] != frames[-1]['endpoint_coordinates']['A'] else 'extend_B'
            else:
                # A fixed arbitrary answer is enough to test sanitization/audit plumbing.
                action = 'extend_A'
            choice = next(k for k, v in b.manifest()['option_mapping'].items() if v == action)
            raw = {'model': b.MODEL, 'answers': {'next': {'type': 'choice', 'choice': choice, 'confidence': .5,
                   'probabilities': {k: float(k == choice) for k in p['questions']['next']['criteria']}}}, 'usage': {'input_tokens': 1, 'output_tokens': 1}}
            return {'response': b.native.sanitize(raw, p['questions'])}
        with tempfile.TemporaryDirectory() as t, patch.dict(os.environ, {'GITHUB_ACTIONS': 'true', 'TYPESAFE_API_KEY': 'test-only'}, clear=True), patch.object(b.native, 'transport', side_effect=answer) as transport:
            b.main(Path(t), True)
            self.assertEqual(transport.call_count, 8)
            self.assertEqual(audit(Path(t))['native_choice_answers_verified'], 8)
            file = Path(t) / 'results.json'
            report = json.loads(file.read_text(encoding='utf-8'))
            report['analysis']['by_condition']['final_only']['next_step_accuracy'] = 1
            file.write_text(json.dumps(report), encoding='utf-8')
            with self.assertRaises(AssertionError):
                audit(Path(t))


if __name__ == '__main__':
    unittest.main()
