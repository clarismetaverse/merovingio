"""Test role-only recursive rebase, novelty, genealogy and no theorem leakage."""
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from rebase_loop import (build_material,retrieve_opposition_pair,role_witnesses,
                         run,experiment,CONDITIONS,MODES)

class RecursiveRebaseTest(unittest.TestCase):
    def test_actual_graph_supports_each_role_witness(self):
        for mode in MODES:
            graph=build_material(mode)
            packet=retrieve_opposition_pair(graph)
            pool,opposites=role_witnesses(graph,packet)
            self.assertEqual(len(opposites),2)
            self.assertTrue(all(e in graph["edges"] for e in opposites))
            self.assertIn("common_incidence_point",[w["name"] for w in pool["SIDE"]])
            self.assertIn("common_bisecting_ray",[w["name"] for w in pool["ANGLE"]])
            equals=[w for w in pool["ANGLE"] if w["name"]=="angular_equality_given"]
            self.assertEqual(bool(equals),mode!="ordinary_cevian")
            for items in pool.values():
                for w in items:
                    self.assertTrue(all(e in graph["edges"] for e in w["edges"]))

    def test_only_angular_segment_rebases_and_no_duplicate_evidence(self):
        for mode in MODES:
            for cond in CONDITIONS:
                for seed in range(7):
                    result=run(cond,mode,seed=seed,budget=10)
                    observed={result["timeline"][0]["new_witness"]["id"]}
                    for e in result["timeline"][1:]:
                        if e["event"]=="REBASE_OPPOSITION":
                            self.assertIn(e["direction"],("ANGLE→SIDE","SIDE→ANGLE"))
                            self.assertEqual(e["new_witness"]["domain"],e["focus"])
                            self.assertTrue(e["provenance_chain"][0].startswith("CONSTRUCT:"))
                            self.assertNotIn(e["new_witness"]["id"],observed)
                            observed.add(e["new_witness"]["id"])
                            self.assertEqual(e["certified_metric_equalities"],[])
                    self.assertEqual(result["metrics"]["redundant_rebases"],0)
                    self.assertEqual(result["metrics"]["false_metric_assertions"],0)
                    self.assertLessEqual(result["metrics"]["rebase_count"],4)

    def test_revisiting_a_domain_adds_new_structural_content(self):
        found=None
        for seed in range(180):
            trial=run("recursive_coupled","isosceles",seed=seed,budget=9)
            if trial["metrics"]["recursive_loop"] and trial["metrics"]["rebase_count"]>=3:
                found=trial;break
        self.assertIsNotNone(found)
        self.assertGreaterEqual(found["metrics"]["new_role_supports"],3)
        self.assertTrue(any(e.get("return_to_prior_focus") for e in found["timeline"]))
        self.assertEqual(len(found["interpretations"]),found["metrics"]["rebase_count"]+1)

    def test_one_way_control_cannot_revisit_angles(self):
        for seed in range(80):
            r=run("one_way","isosceles",seed)
            self.assertFalse(r["metrics"]["recursive_loop"])
            self.assertEqual(r["metrics"]["side_to_angle_count"],0)
            self.assertLessEqual(r["metrics"]["rebase_count"],1)

    def test_arbitrary_transversal_does_not_project_false_equalities(self):
        for seed in range(60):
            r=run("recursive_coupled","ordinary_cevian",seed)
            self.assertFalse(r["source_equality_given"])
            self.assertEqual(r["metrics"]["questions_raised"],0)
            self.assertEqual(r["analogical_questions"],[])
            self.assertFalse(r["geometry"]["observations"]["base_halves_equal_by_coordinates"])
        scalene=run("recursive_coupled","scalene",2)
        self.assertTrue(scalene["source_equality_given"])
        self.assertFalse(scalene["geometry"]["observations"]["base_halves_equal_by_coordinates"])

    def test_all_conditions_use_exactly_same_material_graph_and_mapping(self):
        rr=[run(c,"scalene",seed=4) for c in CONDITIONS]
        for r in rr:
            self.assertEqual(r["graph"],rr[0]["graph"])
            self.assertEqual(r["mapping"],rr[0]["mapping"])
            self.assertEqual(r["evidence_pool"],rr[0]["evidence_pool"])
            self.assertEqual(r["geometry"],rr[0]["geometry"])

    def test_projected_equality_is_only_a_question(self):
        for seed in range(60):
            r=run("recursive_coupled","isosceles",seed)
            for q in r["analogical_questions"]:
                self.assertEqual(q["epistemic_status"],"HYPOTHESIS_ONLY")
                self.assertFalse(q["licensed"])
                self.assertEqual(q["destination"]["relation"],"equal?")
                self.assertEqual(q["through"],r["mapping"]["paired_opposition_edges"])
            for e in r["timeline"]:
                self.assertEqual(e.get("certified_metric_equalities",[]),[])

    def test_seed_stability_and_aggregate_bounds(self):
        self.assertEqual(run("recursive_coupled","isosceles",17),
                         run("recursive_coupled","isosceles",17))
        d=experiment(range(5),budget=8)
        self.assertEqual(len(d["runs"]),len(CONDITIONS)*len(MODES)*5)
        self.assertTrue(d["no_proof"] and d["no_jev"])
        for m in MODES:
            for c in CONDITIONS:
                self.assertEqual(d["aggregates"][m][c]["n"],5)
                self.assertEqual(d["aggregates"][m][c]["redundant_rebases"],0)
                self.assertEqual(d["aggregates"][m][c]["false_metric_assertions"],0)
        self.assertEqual(d["aggregates"]["ordinary_cevian"]["recursive_coupled"]["mean_questions"],0)

if __name__=="__main__":
    unittest.main()
