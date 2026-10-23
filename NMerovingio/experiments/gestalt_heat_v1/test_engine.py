"""Behavioral and epistemic tests for macro→micro Gestalt propagation."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import CODELETS, FIXTURE, MEMORY, fixture_contract, geometry, run, experiment

class GestaltHeatTests(unittest.TestCase):
    def test_grounded_in_existing_repository_fixtures(self):
        self.assertTrue(FIXTURE.exists())
        self.assertTrue(MEMORY.exists())
        contract = fixture_contract()
        self.assertEqual(contract["historical_generic"], "GS_HIST_DOUBLE_TRIANGLE")
        self.assertIn("MS_LEFT", contract["workspace_mental_spaces"])

    def test_construction_creates_true_angular_bisector_but_not_arbitrary_median(self):
        iso, scal = geometry("isosceles"), geometry("scalene")
        self.assertTrue(iso["observations"]["base_halves_equal_by_coordinates"])
        self.assertFalse(scal["observations"]["base_halves_equal_by_coordinates"])
        self.assertTrue(iso["construction_given"])
        self.assertTrue(scal["construction_given"])
        for g in (iso, scal):
            self.assertNotIn("AD = DB", " ".join(g["verified_material"] + g["construction_given"]))
            self.assertEqual(len(g["hypotheses_only"]), 1)

    def test_three_conditions_share_candidate_space_budget_and_construction(self):
        results = [run(c, "isosceles", 3, budget=12) for c in ("bottom_up","top_down","reciprocal")]
        self.assertTrue(all(r["budget"] == 12 for r in results))
        self.assertEqual(results[0]["construction"], results[1]["construction"])
        self.assertEqual(results[0]["construction"], results[2]["construction"])
        self.assertEqual(results[0]["metrics"]["macro_inherited_selections"], 0)
        self.assertTrue(results[1]["metrics"]["macro_inherited_selections"] > 0)
        self.assertEqual(results[1]["metrics"]["feedback_events"], 0)
        self.assertTrue(results[2]["metrics"]["feedback_events"] > 0)

    def test_reciprocal_feedback_is_causal_and_traceable(self):
        r = run("reciprocal","isosceles",0,16)
        events = [e for e in r["timeline"] if e.get("codelet")]
        self.assertTrue(any(e["feedback_delta"] for e in events))
        self.assertTrue(any(e["macro_after"] != e["macro_before"] for e in events))
        self.assertTrue(any("microgroup→macrofeedback" in e["causal_chain"] for e in events))
        self.assertTrue(any(e["chosen_score"]["macro_inherited"] > 0 for e in events))
        for e in events:
            self.assertIn("CONSTRUCTION_CD",e["causal_chain"])
            self.assertTrue(set(e["chosen_score"]["ready_because"]).issubset(
                {prior["codelet"] for prior in events if prior["tick"]<e["tick"]}))

    def test_hypothesis_is_never_certified_even_for_symmetric_case(self):
        for mode in ("isosceles","scalene"):
            for condition in ("bottom_up","top_down","reciprocal"):
                r = run(condition, mode, 7, 16)
                self.assertEqual(r["metrics"]["false_certified_metric_equalities"], 0)
                self.assertEqual(r["macro_tension"]["epistemic_status"], "hypothesis_only")
                self.assertTrue(all(not x.get("metric_assertions_certified") for x in r["timeline"]))
                for e in r["timeline"]:
                    if e.get("codelet") == "TRANSFER_TENSION":
                        self.assertEqual(e["status"], "hypothesis_not_proof")

    def test_same_seed_is_reproducible(self):
        self.assertEqual(run("reciprocal", "scalene", 5), run("reciprocal", "scalene", 5))

    def test_multiple_seeds_and_non_tautological_observables(self):
        data = experiment(range(8),budget=12)
        self.assertEqual(len(data["runs"]),48)
        self.assertTrue(data["no_proof"])
        self.assertTrue(data["no_jev"])
        self.assertEqual(data["aggregates"]["scalene"]["reciprocal"]["false_certified_metric_equalities"],0)
        self.assertEqual(len(CODELETS),len({c.id for c in CODELETS}))
        self.assertTrue(any(len(r["formed_groups"])<len(CODELETS) for r in data["runs"]))

if __name__ == "__main__":
    unittest.main()
