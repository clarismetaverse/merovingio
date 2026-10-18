"""v0.8 fixture invariants — Generic Spaces are abstract, visualizable, and epistemically scoped."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"graph"/"examples"/"generic_spaces_v0_8.json"

class TestGenericSpacesV08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(FILE.read_text(encoding="utf-8"))
        cls.spaces=cls.data["generic_spaces"]

    def test_three_origins_and_distinct_ids(self):
        self.assertEqual({s["source"] for s in self.spaces},{"memory","induced","blend"})
        self.assertEqual(len({s["id"] for s in self.spaces}),len(self.spaces))
        self.assertEqual(len(self.spaces),4)

    def test_mapped_objects_exist_and_are_not_duplicated_as_material_carriers(self):
        known={"A","B","C","D","AB","AD","DB","CA","CB","CD",
               "angleACD","angleDCB","angleACB"}
        self.assertEqual(set(self.data["points"]),{"A","B","C","D"})
        for gs in self.spaces:
            for role in gs["roles"]:
                for key in ("left_object","right_object"):
                    self.assertTrue(role[key] is None or role[key] in known)
        self.assertIn("CD",self.spaces[0]["roles"][1].values())

    def test_stage_activation_and_incompleteness(self):
        stages=self.data["stages"]
        self.assertEqual(len(stages),3)
        recalled=[s for s in self.spaces if s["source"]=="memory"]
        induced=[s for s in self.spaces if s["source"]=="induced"]
        blended=[s for s in self.spaces if s["source"]=="blend"]
        self.assertTrue(all(s["activation_stage"]==0 for s in recalled))
        self.assertTrue(all(s["activation_stage"]==1 for s in induced))
        self.assertTrue(all(s["activation_stage"]==2 for s in blended))
        self.assertTrue(any(g["resolved_at"] is None for s in recalled for g in s["missing"]))
        self.assertTrue(any(g["resolved_at"]==1 for s in recalled for g in s["missing"]))

    def test_all_examples_explicitly_non_proven(self):
        self.assertIn("no theorem",self.data["meta"]["epistemic_note"].lower())
        for gs in self.spaces:
            self.assertEqual(len(gs["statuses"]),3)
            self.assertEqual(len(gs["salience"]["context"]),3)
            self.assertEqual(len(gs["salience"]["generative"]),3)
            self.assertTrue(gs["genealogical_sources"])
            self.assertTrue(0<=gs["activation_stage"]<=2)
            for values in gs["salience"].values():
                self.assertTrue(all(0<=s<=1 for s in values))
            for role in gs["roles"]:
                self.assertNotIn("verified_equal",role)
                self.assertNotIn("proven",role)

    def test_prospective_role_not_claimed_constructed(self):
        prospective=next(s for s in self.spaces if s["id"]=="GS_PARALLEL_TRANSPORT")
        self.assertTrue(any(r["available_at"]>2 for r in prospective["roles"]))
        self.assertTrue(any(g["resolved_at"] is None for g in prospective["missing"]))
        self.assertIn("non è stato costruito",prospective["epistemic_status"].lower())

if __name__=="__main__":
    unittest.main()
