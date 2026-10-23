"""v2: graph-generated Gestalten, bidirectional pressure, non-provability."""
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from endogenous import make_graph,relation_signature,group_from_edges,proposals,equal_angle_witness,run,experiment,side,angle

class EndogenousGestaltTests(unittest.TestCase):
    def test_graph_is_built_from_cycles_not_target_groups(self):
        original=make_graph("isosceles",include_bridge=False)
        after=make_graph("isosceles")
        self.assertEqual(len(original["triangles"]),1)
        self.assertEqual(len(after["triangles"]),3)
        self.assertGreater(len(after["nodes"]),len(original["nodes"]))
        self.assertGreater(len(after["edges"]),len(original["edges"]))
        self.assertEqual(after["certified_metric_equalities"],[])
        self.assertIn(side("A","D"),after["nodes"])
        self.assertIn(side("B","D"),after["nodes"])

    def test_oppositions_are_generated_per_triangle(self):
        graph=make_graph("isosceles")
        pairs=[e["nodes"] for e in graph["edges"].values() if e["kind"]=="opposite"]
        self.assertIn(sorted([angle("A","C","D"),side("A","D")]),pairs)
        self.assertIn(sorted([angle("B","C","D"),side("B","D")]),pairs)
        self.assertTrue(any(e["kind"]=="equal_given" and
            set(e["nodes"])=={angle("A","C","D"),angle("B","C","D")}
            for e in graph["edges"].values()))

    def test_graph_grammar_produces_non_enumerated_generic_alignments(self):
        graph=make_graph("isosceles")
        opposites=[e for e in graph["edges"].values() if e["kind"]=="opposite" and
                   angle("A","C","D") in e["nodes"] and side("A","D") in e["nodes"]]
        self.assertEqual(len(opposites),1)
        chosen=group_from_edges(graph,[opposites[0]["id"]],"SEED")
        frontier=proposals(graph,{chosen["id"]:chosen},{chosen["id"]})
        candidates=[g for g in frontier.values() if g["operator"]=="ALIGN" and equal_angle_witness(graph,g)]
        self.assertEqual(len(candidates),1)
        self.assertEqual(len(candidates[0]["relations"]),2)
        self.assertTrue(candidates[0]["cross_domain"])

    def test_graph_grammar_expands_groups_and_keeps_origins(self):
        graph=make_graph("isosceles")
        edge_id=next(e["id"] for e in graph["edges"].values() if e["kind"]=="opposite")
        chosen=group_from_edges(graph,(edge_id,),"SEED")
        expansions=proposals(graph,{chosen["id"]:chosen},{chosen["id"]})
        self.assertTrue(any(g["operator"]=="EXTEND" for g in expansions.values()))
        self.assertTrue(all(chosen["id"] in g["parents"] for g in expansions.values()
                            if g["operator"]=="EXTEND"))
        self.assertTrue(all(e in graph["edges"] for g in expansions.values() for e in g["relations"]))

    def test_transfers_are_only_hypotheses_not_metric_certificates(self):
        for mode in ("isosceles","scalene"):
            graph=make_graph(mode)
            self.assertFalse(graph["certified_metric_equalities"])
            r=run("reciprocal",mode,seed=4,budget=20)
            self.assertEqual(r["metrics"]["false_certified_metric_equalities"],0)
            for h in r["analogical_hypotheses"]:
                self.assertEqual(h["epistemic_status"],"HYPOTHESIS_ONLY")
                self.assertEqual(h["license"],"none")
            for e in r["timeline"]:
                self.assertFalse(e.get("certified_metric_equalities"))
        scalene=make_graph("scalene")["geometry"]
        self.assertFalse(scalene["observations"]["base_halves_equal_by_coordinates"])
        self.assertTrue(scalene["construction_given"])

    def test_same_seed_deterministic(self):
        self.assertEqual(run("reciprocal","isosceles",1,12),run("reciprocal","isosceles",1,12))

    def test_topdown_and_feedback_are_distinct(self):
        baseline=run("bottom_up","isosceles",0,12)
        one_way=run("feedforward","isosceles",0,12)
        two_way=run("reciprocal","isosceles",0,12)
        no_opp=run("reciprocal_without_opposition","isosceles",0,12)
        self.assertEqual(baseline["timeline"][0]["activation_after"]["opposition"],0)
        self.assertGreater(one_way["timeline"][0]["activation_after"]["opposition"],0)
        self.assertEqual(no_opp["timeline"][-1]["activation_after"]["opposition"],0)
        self.assertTrue(all(e["activation_after"]==e["activation_before"] for e in one_way["timeline"]))
        self.assertTrue(any(e["feedback"] for e in two_way["timeline"] if e.get("operation")!="CONSTRUCT_CD"))
        self.assertEqual({c["kind"] for c in baseline["graph"]["nodes"].values()},
                         {c["kind"] for c in two_way["graph"]["nodes"].values()})
        self.assertEqual(baseline["graph"],two_way["graph"])

    def test_multi_seed_ablation_bookkeeping(self):
        out=experiment(range(3),budget=9)
        self.assertEqual(len(out["runs"]),24)
        self.assertTrue(out["no_proof"])
        self.assertTrue(out["no_llm_or_jev"])
        for mode in out["modes"]:
            self.assertEqual(set(out["aggregate"][mode]),set(out["conditions"]))
            for c in out["conditions"]:
                self.assertEqual(out["aggregate"][mode][c]["n"],3)
                self.assertEqual(out["aggregate"][mode][c]["false_metric_assertions"],0)

if __name__=="__main__":
    unittest.main()
