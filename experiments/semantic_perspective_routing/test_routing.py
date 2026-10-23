import copy
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import benchmark_routing as b
from audit_routing import audit


def fake_response(payload):
    answers = {}
    for q, m in b.fixture()['observer']['question_metadata'].items():
        option = next(k for k, v in m['option_mapping'].items() if b.decision_key(v) == b.decision_key(m['acceptable'][0]))
        answers[q] = {'type': 'choice', 'choice': option, 'confidence': .8,
                      'probabilities': {k: float(k == option) for k in payload['questions'][q]['criteria']}}
    return {'model': b.MODEL, 'answers': answers, 'usage': {'input_tokens': 1, 'output_tokens': 1}}


class RoutingTests(unittest.TestCase):
    def test_frozen_budget_mapping_and_all_subsets(self):
        f = b.fixture()
        self.assertEqual(len(f['payload']['questions']), 6)
        self.assertEqual(set(f['observer']['frame_aliases']), set(b.FRAMES))
        self.assertNotEqual(list(f['payload']['state']['intents'].values()), [c['text'] for c in b.CASES])
        for q, m in f['observer']['question_metadata'].items():
            self.assertEqual(len(f['payload']['questions'][q]['criteria']), 9)
            self.assertEqual(set(map(b.decision_key, m['option_mapping'].values())),
                             {'none', 'clarify', 'triangles', 'polyrole', 'congruence', 'polyrole+triangles',
                              'congruence+triangles', 'congruence+polyrole', 'congruence+polyrole+triangles'})

    def test_payload_excludes_gold_instances_geometry_and_availability(self):
        p = b.fixture()['payload']
        self.assertNotIn('assets', p)
        forbidden = {'acceptable', 'reference', 'correct', 'annotation_reason', 'option_mapping', 'frame_aliases',
                     'coordinates', 'xy', 'valid', 'certificate', 'certified_bindings', 'unavailable_frames', 'method', 'checks'}
        def walk(v):
            if isinstance(v, dict):
                self.assertFalse(forbidden & set(v))
                for item in v.values():
                    walk(item)
            elif isinstance(v, list):
                for item in v:
                    walk(item)
        walk(p)
        for q in p['questions'].values():
            self.assertNotIn('K', json.dumps(q['instructions']))

    def test_semantic_input_never_calls_geometry_or_reference(self):
        with patch.object(b, 'dispatch', side_effect=AssertionError('geometry consulted')), patch.object(b.geometry, 'objects_for', side_effect=AssertionError('geometry consulted')):
            self.assertEqual(b.make_fixture(), b.fixture())

    def test_historical_contracts_and_proposal_are_distinct(self):
        inventory = b.dispatch(sorted(b.FRAMES))
        self.assertEqual(inventory['check_work_units'], 9)
        self.assertEqual(len(inventory['certified_bindings']), 6)
        self.assertEqual(inventory['unavailable_frames'], ['congruence'])
        for name in ('triangles', 'polyrole'):
            self.assertIn(b.FRAMES[name]['source'], b.geometry.native.ENTRIES)
            self.assertEqual(len(b.dispatch([name])['certified_bindings']), 3)
        self.assertNotIn(b.FRAMES['congruence']['source'], b.geometry.native.ENTRIES)

    def test_numeric_sss_matches_reflection_and_rejects_scale(self):
        objects = {'A': {'xy': [0, 0]}, 'B': {'xy': [3, 0]}, 'C': {'xy': [0, 4]},
                   'D': {'xy': [10, 10]}, 'E': {'xy': [10, 7]}, 'F': {'xy': [6, 10]},
                   'REGION_0': {'vertices': ['A', 'B', 'C']}, 'REGION_1': {'vertices': ['F', 'E', 'D']}}
        self.assertTrue(b.congruence_certificate(objects)['valid'])
        objects['F']['xy'] = [5, 10]
        self.assertFalse(b.congruence_certificate(objects)['valid'])

    def test_relevant_unavailable_frame_is_not_replaced_or_accepted(self):
        execution = b.dispatch(['congruence'])
        self.assertEqual(execution['certified_bindings'], [])
        self.assertEqual(execution['check_work_units'], 3)
        self.assertEqual(execution['unavailable_frames'], ['congruence'])
        self.assertEqual(b.dispatch([])['check_work_units'], 0)
        self.assertEqual(b.dispatch('clarify')['check_work_units'], 0)
        with self.assertRaises(ValueError):
            b.dispatch(['invented'])

    def test_multi_frame_and_nonunique_reference_do_not_force_a_winner(self):
        cases = {c['id']: c for c in b.CASES}
        self.assertEqual(cases['two_perspectives']['acceptable'], [['polyrole', 'triangles']])
        self.assertEqual(len(cases['underspecified']['acceptable']), 2)
        payload = b.fixture()['payload']
        report = {'call': {'response': b.sanitize(fake_response(payload), payload['questions'])}}
        result = b.analyze(report)
        self.assertEqual(result['systems']['jev']['acceptable'], 6)
        self.assertEqual(result['systems']['jev']['check_work_units'], 15)
        self.assertEqual(result['systems']['jev']['unavailable_frame_selections'], 1)
        self.assertEqual(result['systems']['explore_all']['check_work_units'], 54)

    def test_sanitizer_retains_only_native_typed_values(self):
        p = b.fixture()['payload']
        raw = fake_response(p)
        raw['error_text'] = 'sensitive free text'
        raw['usage']['server_text'] = 'sensitive free text'
        for a in raw['answers'].values():
            a['explanation'] = 'sensitive free text'
        clean = b.sanitize(raw, p['questions'])
        self.assertNotIn('sensitive', json.dumps(clean))
        self.assertIsNone(clean['reliability'])
        self.assertIsNone(clean['usage']['total_tokens'])
        for mutate in ('choice', 'probabilities', 'confidence'):
            bad = copy.deepcopy(raw)
            first = next(iter(bad['answers'].values()))
            first[mutate] = {'choice': 'unknown', 'probabilities': {}, 'confidence': float('nan')}[mutate]
            # NaN/missing confidence remains null by the same numerical allowlist policy;
            # invalid choices or probability shape must fail closed.
            if mutate == 'confidence':
                self.assertIsNone(next(iter(b.sanitize(bad, p['questions'])['answers'].values()))['confidence'])
            else:
                with self.assertRaises(ValueError):
                    b.sanitize(bad, p['questions'])

    def test_local_live_and_transport_guards(self):
        with tempfile.TemporaryDirectory() as t, patch.dict(os.environ, {}, clear=True), patch.object(b, 'transport') as transport:
            with self.assertRaises(SystemExit):
                b.main(Path(t), True)
            transport.assert_not_called()
            with self.assertRaises(RuntimeError):
                # Call original function: guard is inside transport too.
                transport.side_effect = None
                transport.reset_mock()
                b_transport(b.fixture()['payload'])

    def test_single_call_failure_saved_without_retry(self):
        with tempfile.TemporaryDirectory() as t, patch.dict(os.environ, {'GITHUB_ACTIONS': 'true', 'TYPESAFE_API_KEY': 'test-only'}, clear=True), patch.object(b, 'transport', return_value={'failure': 'HTTP_403'}) as transport:
            with self.assertRaises(SystemExit):
                b.main(Path(t), True)
            self.assertEqual(transport.call_count, 1)
            self.assertEqual(audit(Path(t))['status'], 'failed')

    def test_transport_header_timeout_and_error_body_allowlist(self):
        class Rejected:
            status_code = 429
            @property
            def text(self):
                raise AssertionError('Do not read free-form error text')
        post = Mock(return_value=Rejected())
        with patch.dict(os.environ, {'GITHUB_ACTIONS': 'true', 'TYPESAFE_API_KEY': 'test-only'}, clear=True), patch.dict(b.sys.modules, {'requests': SimpleNamespace(post=post)}):
            result = b.transport(b.fixture()['payload'])
            self.assertEqual(result['failure'], 'HTTP_429')
            self.assertEqual(post.call_count, 1)
            self.assertEqual(post.call_args.kwargs['headers']['TypeSafe-Danger-Zone-Images'], 'true')
            self.assertEqual(post.call_args.kwargs['timeout'], 180)
            self.assertNotIn('test-only', json.dumps(result))

    def test_offline_and_synthetic_live_audit_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as t:
            b.main(Path(t))
            self.assertEqual(audit(Path(t))['native_choice_answers_verified'], 0)
            report = json.loads((Path(t) / 'results.json').read_text(encoding='utf-8'))
            self.assertEqual(report['status'], 'offline_only')
            self.assertEqual(report['analysis']['api_calls_attempted'], 0)
        def response(p):
            return {'response': b.sanitize(fake_response(p), p['questions'])}
        with tempfile.TemporaryDirectory() as t, patch.dict(os.environ, {'GITHUB_ACTIONS': 'true', 'TYPESAFE_API_KEY': 'test-only'}, clear=True), patch.object(b, 'transport', side_effect=response) as transport:
            b.main(Path(t), True)
            self.assertEqual(transport.call_count, 1)
            self.assertEqual(audit(Path(t))['native_choice_answers_verified'], 6)
            file = Path(t) / 'results.json'
            report = json.loads(file.read_text(encoding='utf-8'))
            report['analysis']['systems']['jev']['acceptable'] = 0
            file.write_text(json.dumps(report), encoding='utf-8')
            with self.assertRaises(AssertionError):
                audit(Path(t))


b_transport = b.transport

if __name__ == '__main__':
    unittest.main()
