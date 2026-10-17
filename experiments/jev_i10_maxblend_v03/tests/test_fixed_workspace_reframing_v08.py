"""No-network safeguards for v0.8: one construction, four views."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import fixed_workspace_reframing_v08 as m

class TestFixedWorkspace(unittest.TestCase):
    def test_proof_free_non_metrical_construct(self):
        v=m.geometry_checks()
        self.assertNotAlmostEqual(v["base_fraction"],v["median_base_fraction"],places=2)
        self.assertNotAlmostEqual(v["base_fraction"],v["angle_bisector_base_fraction"],places=2)
        self.assertNotAlmostEqual(v["base_fraction"],v["perpendicular_base_fraction"],places=2)

    def test_true_same_construction_all_options(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            a,am=m.trial_payload(root,"angular",0,"visual")
            b,bm=m.trial_payload(root,"angular",0,"structured")
            self.assertEqual(am,bm)
            self.assertEqual(set(a["assets"]),set(b["assets"]))
            self.assertEqual(len(a["assets"]),5)
            self.assertTrue(a["state"]["same_construction_in_every_candidate"])
            for condition,content in (("visual",a),("structured",b)):
                self.assertEqual(
                    "candidate_mental_spaces" in content["state"],
                    condition=="structured"
                )
                self.assertEqual(len(content["questions"]["best_bridge"]["criteria"]),4)

    def test_all_role_options_represented_at_equal_frequency(self):
        choices=[]
        for focus in m.ROLES:
            for repeat in (0,1):
                names=m.mapping_for(focus,repeat)
                self.assertEqual(set(names.values()),set(m.ROLES))
                choices.extend([k for k,v in names.items() if v==focus])
        self.assertCountEqual(choices,["K1","K1","K2","K2","K3","K3","K4","K4"])

    def test_no_truth_labels_or_proofs_in_request(self):
        with tempfile.TemporaryDirectory() as temp:
            for focus in m.ROLES:
                for condition in ("visual","structured"):
                    p,_=m.trial_payload(Path(temp),focus,0,condition)
                    txt=json.dumps({k:v for k,v in p.items() if k!="assets"}).lower()
                    for forbidden in (
                        "expected_method","oracle","selected_role","correct",
                        "base_fraction","bisector_fraction","measured_degrees",
                        "proof_of_i10","verified_equality","sas_criterion"
                    ):
                        self.assertNotIn(forbidden,txt)
                    self.assertEqual(p["questions"]["best_bridge"]["type"],"choice")

if __name__=="__main__":
    unittest.main()
