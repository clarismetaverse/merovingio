"""v10 cognitive binding and consequence genealogy—not theorem proving."""
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from cognitive_memory import run,experiment,SHAPES,CONDITIONS,GOALS

class CognitiveMemoryTests(unittest.TestCase):
    def test_initial_material_has_only_original_triangle(self):
        for shape in SHAPES:
            r=run(shape,"C","normal",seed=2)
            self.assertEqual(len(r["preconstruction"]["points"]),3)
            self.assertEqual(len(r["preconstruction"]["faces"]),1)
            self.assertEqual(r["preconstruction"]["given_angular_equalities"],[])
            self.assertEqual(r["preconstruction"]["certified_segment_equalities"],[])
            self.assertEqual(r["cognitive_memory"]["proven_metric_equalities"],[])
            self.assertTrue(r["cognitive_memory"]["acyclic"])

    def test_new_relation_follows_cognitive_frame_completion(self):
        for goal in GOALS:
            r=run("equilateral",goal,"normal",seed=3)
            nodes=r["cognitive_memory"]["entries"]
            kinds=[n["kind"] for n in nodes]
            self.assertIn("COMPLETE_FRAME",kinds)
            self.assertIn("PROJECT_RELATION",kinds)
            self.assertLess(kinds.index("COMPLETE_FRAME"),kinds.index("PROJECT_RELATION"))
            projected=r["cognitive_projection"]
            self.assertEqual(projected["status"],"cognitive_inference_not_proven")
            self.assertEqual(projected["payload"]["proposed_relation"]["predicate"],
                             "cognitive_equal_segments_candidate")
            self.assertEqual(projected["parents"][0],next(
                x["id"] for x in nodes if x["kind"]=="COMPLETE_FRAME"))
            self.assertEqual(r["metrics"]["projected_equalities_marked_proven"],0)
            self.assertEqual(r["metrics"]["circular_premises_used"],0)
            self.assertTrue(r["metrics"]["median_frame_activated"])
            self.assertTrue(r["metrics"]["LLL_rereading_from_new_binding"])

    def test_projection_ancestry_records_original_given_and_actual_bindings(self):
        r=run("equilateral","C","normal",seed=0)
        ancestors=r["projection_ancestry"]
        kinds=[x["kind"] for x in ancestors]
        self.assertIn("PERCEIVE_INITIAL_RELATION",kinds)
        self.assertIn("FORM_PROSPECTIVE_BLEND",kinds)
        self.assertIn("CONSTRUCT_DIVIDER",kinds)
        self.assertIn("RECOGNIZE_FRAME_ROLES",kinds)
        self.assertEqual(kinds.count("BIND_ROLE"),2)
        self.assertLess(kinds.index("CONSTRUCT_DIVIDER"),kinds.index("BIND_ROLE"))
        self.assertLess(kinds.index("BIND_ROLE"),kinds.index("PROJECT_RELATION"))

    def test_scalene_has_no_base_equality_projection_or_median_activation(self):
        for seed in range(12):
            r=run("scalene","C","normal",seed)
            self.assertFalse(r["metrics"]["LAL_cognitive_frame_completed"])
            self.assertFalse(r["metrics"]["new_side_relation_projected"])
            self.assertIsNone(r["new_median_reading"])
            self.assertFalse(r["metrics"]["LLL_rereading_from_new_binding"])
            self.assertFalse(r["original_premise"]["status"]=="verified")
            self.assertEqual(r["cognitive_memory"]["proven_metric_equalities"],[])

    def test_masked_angle_does_not_generate_false_frame_completion(self):
        r=run("equilateral","C","angle_witness_masked",seed=4)
        self.assertFalse(r["metrics"]["LAL_cognitive_frame_completed"])
        self.assertIsNone(r["cognitive_projection"])
        self.assertIsNone(r["new_LLL_reading"])
        self.assertTrue(r["postconstruction"]["given_angular_equalities"],
                        "construction still happened; only cognitive witness masked")

    def test_counterfactual_is_explicit_extra_premise_not_hidden_in_projection(self):
        r=run("equilateral","C","counterfactual_base_given",seed=5)
        extra=r["extra_given_control"]
        self.assertEqual(extra["kind"],"RECALL_EXTRA_GIVEN")
        self.assertEqual(extra["status"],"independently_given_in_counterfactual")
        self.assertEqual(extra["payload"]["source"],"COUNTERFACTUAL_EXTRA_GIVEN")
        proj=r["cognitive_projection"]
        self.assertEqual(proj["status"],"cognitive_inference_not_proven")
        self.assertNotIn(extra["id"],proj["parents"])

    def test_medial_role_uses_actual_new_contact_not_predetermined_D(self):
        for goal in GOALS:
            r=run("equilateral",goal,"normal",seed=1)
            role=r["role_schema"]["role_pairs"]["equal_base_halves"]
            found=r["cognitive_projection"]["payload"]["proposed_relation"]["objects"]
            self.assertEqual(found,role)
            d=r["postconstruction"]["construction_events"][0]["contact_point"]
            self.assertTrue(all(d in part for part in found))
            self.assertEqual(r["new_median_reading"]["status"],
                             "hypothetical_frame_attraction")
            self.assertTrue(r["new_median_reading"]["payload"]["median_not_certified"])

    def test_lll_initially_favored_can_still_leave_cognitive_trace_of_lal(self):
        r=run("equilateral","C","LLL_initially_favored",seed=0)
        self.assertTrue(r["cognitive_projection"])
        self.assertIn("REBASE_FRAME",[x["kind"] for x in r["cognitive_memory"]["entries"]])
        self.assertTrue(r["new_LLL_reading"]["payload"]
                        ["do_not_reuse_projection_as_proof_of_itself"])

    def test_without_prospection_still_recognizes_construction_bottom_up(self):
        r=run("isosceles","C","without_prospection",seed=8)
        self.assertIsNone(r["prospective"])
        self.assertFalse(r["prospective_binding"]["matched"])
        self.assertTrue(r["metrics"]["LAL_cognitive_frame_completed"])
        self.assertTrue(r["metrics"]["new_side_relation_projected"])

    def test_reproducibility(self):
        self.assertEqual(run("equilateral","C","normal",seed=8),
                         run("equilateral","C","normal",seed=8))

    def test_aggregation(self):
        d=experiment(range(2))
        self.assertEqual(len(d["runs"]),48)
        for shape,goals in d["aggregates"].items():
            for _,conds in goals.items():
                for _,data in conds.items():
                    self.assertEqual(data["n"],2)
                    self.assertEqual(data["false_proof_promotions"],0)
                    self.assertEqual(data["circular_premises_used"],0)

if __name__=="__main__": unittest.main()
