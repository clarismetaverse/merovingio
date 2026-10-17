"""Tests exclude API calls. Exact control of support and time ablation."""
import json
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import causal_ablation_v13 as p

class CausalTests(unittest.TestCase):
    def test_all_geometry_controls(self):
        for shape in p.SHAPES:
            oracle=p.geometric_oracle(shape)
            self.assertEqual(oracle['shared_carrier'],shape.startswith('iso_'))
            self.assertFalse(oracle['cross_pair_metric_equality'])

    def test_support_dag_same_across_histories(self):
        for shape in p.SHAPES:
            u=p.graph(shape,'upper_first',False)
            l=p.graph(shape,'lower_first',False)
            self.assertEqual(u,l)
            self.assertEqual(p.canonical_signature(u),p.canonical_signature(l))
            ua=p.graph(shape,'upper_first',True)
            la=p.graph(shape,'lower_first',True)
            self.assertNotEqual(p.canonical_signature(ua),p.canonical_signature(la))
            unode={v['id']:{k:v[k] for k in v if k!='step'} for v in ua['nodes']}
            lnode={v['id']:{k:v[k] for k in v if k!='step'} for v in la['nodes']}
            self.assertEqual(unode,lnode)
            common=lambda g:{tuple(sorted(x.items())) for x in g['edges'] if x['relation']!='happens_before'}
            self.assertEqual(common(ua),common(la))

    def test_serialization_invariance_and_matched_shuffle(self):
        for shape in p.SHAPES:
            for hist in p.HISTORIES:
                for treatment in (False,True):
                    signatures={p.canonical_signature(p.permute_graph(p.graph(shape,hist,treatment),mode,shape,hist,'chronology' if treatment else 'supports')) for mode in p.PRESENTATIONS}
                    self.assertEqual(len(signatures),1)
            u=p.permute_graph(p.graph(shape,'upper_first',False),'shuffled',shape,'upper_first','supports')
            l=p.permute_graph(p.graph(shape,'lower_first',False),'shuffled',shape,'lower_first','supports')
            self.assertEqual(u,l)

    def test_payload_identical_without_time(self):
        for shape in p.SHAPES:
            for pr in p.PRESENTATIONS:
                u=p.make_payload(shape,'supports','upper_first',pr)
                l=p.make_payload(shape,'supports','lower_first',pr)
                self.assertEqual(u,l)
                self.assertNotIn('step',json.dumps(u))
                self.assertNotIn('happens_before',json.dumps(u))
                t=p.make_payload(shape,'chronology','upper_first',pr)
                self.assertEqual(u['questions']['exploratory_focus'],t['questions']['exploratory_focus'])
                self.assertIn('last_emergence',t['questions'])
            f=p.make_payload(shape,'final')
            self.assertNotIn('support_graph',f['state'])

    def test_no_answer_key_and_api_secret_leak(self):
        for shape in p.SHAPES:
            for cond in p.CONDITIONS:
                content=json.dumps(p.make_payload(shape,cond,'lower_first','reversed')).lower()
                for bad in ('api_key','bearer ','oracle_shared','later_expected','correct_answer','proof of euclid'):
                    self.assertNotIn(bad,content)
                self.assertNotIn('assets',content)

    def test_schedule(self):
        runs=p.schedule()
        self.assertEqual(len(runs),56)
        self.assertEqual(sum(r['condition']=='final' for r in runs),8)
        self.assertEqual(sum(r['condition']=='supports' for r in runs),24)
        self.assertEqual(sum(r['condition']=='chronology' for r in runs),24)
        self.assertEqual(len({(r['shape'],r.get('history'),r.get('presentation'),r.get('condition'),r.get('repeat')) for r in runs}),56)

if __name__=='__main__':unittest.main()