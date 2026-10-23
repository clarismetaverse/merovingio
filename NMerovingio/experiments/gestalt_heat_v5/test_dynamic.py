"""Dynamic next-opposition selection and anti-proof safety."""
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from dynamic import (build_material,opposite_roles,coorigin_ledger,initialize,
                     candidate_score,propagate,pair_generic,question_if_given,
                     simulate,experiment,CONDITIONS,MODES)

class DynamicOppositionTests(unittest.TestCase):
    def test_all_candidates_derived_from_actual_graph_oppositions(self):
        for mode in MODES:
            graph=build_material(mode)
            mappings=opposite_roles(graph)
            self.assertGreaterEqual(len(mappings),5)
            self.assertTrue(all(graph["edges"][m["id"]]["kind"]=="opposite" for m in mappings))
            self.assertTrue(all(graph["nodes"][m["angle"]]["kind"]=="angle" for m in mappings))
            self.assertTrue(all(graph["nodes"][m["side"]]["kind"]=="side" for m in mappings))
            self.assertEqual(len(mappings),len({m["id"] for m in mappings}))

    def test_new_group_changes_candidate_scores_and_node_salience(self):
        graph=build_material("isosceles")
        packets,ledger=coorigin_ledger(graph)
        nodes,macro,origins=initialize(graph,packets,"coupled")
        mappings=opposite_roles(graph)
        before={m["id"]:candidate_score(m,"SIDE",nodes,macro,ledger,"coupled",set())["score"]
                for m in mappings}
        # Inject one observed opposition into the graph-salience field.
        picked=next(m for m in mappings if m["id"] in ledger)
        after_nodes,changes=propagate(graph,nodes,picked,ledger)
        after={m["id"]:candidate_score(m,"SIDE",after_nodes,macro,ledger,"coupled",set())["score"]
               for m in mappings}
        differences={k:round(after[k]-before[k],4) for k in before}
        self.assertTrue(changes)
        self.assertTrue(any(x>0 for x in differences.values()))
        self.assertGreater(len(set(differences.values())),1,
            "propagation must discriminate candidates, not boost everyone equally")

    def test_all_conditions_use_identical_geometry_candidates_and_budget(self):
        rr=[simulate(c,"scalene",seed=3,budget=8) for c in CONDITIONS]
        for r in rr:
            self.assertEqual(r["geometry"],rr[0]["geometry"])
            self.assertEqual(r["graph"],rr[0]["graph"])
            self.assertEqual(r["opposition_mappings"],rr[0]["opposition_mappings"])
            self.assertEqual(r["construction_ledger"],rr[0]["construction_ledger"])
            self.assertEqual(r["metrics"]["rebases"],8)
            self.assertEqual(r["metrics"]["duplicate_mapping_rebases"],0)

    def test_every_selected_mapping_was_on_frontier_and_is_unique(self):
        for condition in CONDITIONS:
            for mode in MODES:
                r=simulate(condition,mode,seed=7,budget=8)
                selected=[]
                for event in r["timeline"][1:]:
                    edge=event["selected"]["new_opposition_edge"]["id"]
                    self.assertIn(edge,event["candidate_scores_before"])
                    self.assertNotIn(edge,selected)
                    selected.append(edge)
                    self.assertIn(event["from"],("ANGLE","SIDE"))
                    self.assertIn(event["to"],("ANGLE","SIDE"))
                    self.assertNotEqual(event["from"],event["to"])
                    self.assertEqual(event["certified_metric_equalities"],[])
                self.assertEqual(len(selected),len(set(selected)))
                self.assertEqual(r["metrics"]["false_metric_assertions"],0)

    def test_fixed_order_does_not_change_ranking_based_on_group(self):
        r=simulate("fixed_order","isosceles",seed=1)
        self.assertEqual(r["metrics"]["dynamic_rank_reorderings"],0)
        self.assertEqual(r["metrics"]["feedback_events"],0)
        self.assertTrue(all(not event.get("changed_node_activation") for event in r["timeline"]))

    def test_dynamic_feedback_and_genealogy_ablation_are_real(self):
        coupled=simulate("coupled","isosceles",seed=1)
        nofeedback=simulate("macro_no_feedback","isosceles",seed=1)
        nogenealogy=simulate("macro_no_genealogy","isosceles",seed=1)
        self.assertGreater(coupled["metrics"]["feedback_events"],0)
        self.assertEqual(nofeedback["metrics"]["feedback_events"],0)
        self.assertTrue(all(e["selected_score"]["coorigin_support"]==0
                             for e in nogenealogy["timeline"][1:]))
        self.assertTrue(any(e["selected_score"]["coorigin_support"]>0
                             for e in coupled["timeline"][1:]))

    def test_structural_generic_does_not_certify_equality(self):
        for mode in MODES:
            graph=build_material(mode)
            packets,ledger=coorigin_ledger(graph)
            candidates=opposite_roles(graph)
            for i,a in enumerate(candidates):
                for b in candidates[i+1:]:
                    gs=pair_generic(graph,{},a,b,packets)
                    if gs:
                        self.assertEqual(gs["status"],"candidate_GS_no_metric_certification")
                        q=question_if_given(graph,gs)
                        if q:
                            self.assertEqual(q["epistemic_status"],"HYPOTHESIS_ONLY")
                            self.assertFalse(q["proven"])
                            self.assertEqual(q["target"]["relation"],"equal?")
                        if mode=="ordinary_cevian":
                            self.assertIsNone(q)

    def test_scalene_bisector_and_generic_cevian_controls(self):
        for mode in ("isosceles","scalene","ordinary_cevian"):
            r=simulate("coupled",mode,seed=4,budget=8)
            self.assertEqual(r["metrics"]["false_metric_assertions"],0)
            if mode=="ordinary_cevian":
                self.assertFalse(r["source_given_angles"])
                self.assertFalse(r["analogical_questions"])
            if mode=="scalene":
                self.assertFalse(r["geometry"]["observations"]["base_halves_equal_by_coordinates"])

    def test_seeds_deterministic(self):
        self.assertEqual(simulate("coupled","isosceles",seed=17),
                         simulate("coupled","isosceles",seed=17))

    def test_multi_seed_experiment(self):
        e=experiment(range(3),budget=8)
        self.assertEqual(len(e["runs"]),len(CONDITIONS)*len(MODES)*3)
        self.assertTrue(e["no_proof"] and e["no_jev"])
        self.assertTrue(all(e["aggregates"][m][c]["n"]==3
                            for m in MODES for c in CONDITIONS))
        self.assertEqual(e["aggregates"]["ordinary_cevian"]["coupled"]["transfer_question_rate"],0)

if __name__=="__main__":
    unittest.main()
