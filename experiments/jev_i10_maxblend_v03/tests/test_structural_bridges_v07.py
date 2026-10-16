"""Deterministic, credential-free contract checks for the v0.7 bridge benchmark."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
import structural_bridges_v07 as sb

class BridgeSelectionChecks(unittest.TestCase):
    def test_all_candidates_are_valid_and_distinct(self):
        self.assertEqual(len(sb.METHODS),4)
        for shape in sb.SHAPES:
            self.assertTrue(sb.certify_geometry(shape))
            p=sb.points(shape)
            self.assertEqual(len({p[x] for x in ("D","E","F","P","Q")}),5)

    def test_oracle_is_unique_by_active_frame(self):
        for frame in sb.FRAMES:
            selected=sb.expected_method(frame)
            self.assertIn(selected,sb.METHODS)
        self.assertEqual(set(sb.expected_method(f) for f in sb.FRAMES),set(sb.METHODS))

    def test_counterbalance_and_ablate_images_fixed(self):
        ids=[]
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for shape in sb.SHAPES:
                for frame in sb.FRAMES:
                    versions=[sb.make_payload(root,shape,frame,c) for c in sb.CONDITIONS]
                    choices=[version[1] for version in versions]
                    self.assertEqual(choices[0],choices[1])
                    self.assertEqual(choices[0],choices[2])
                    self.assertEqual(set(versions[0][0]["assets"]),set(versions[1][0]["assets"]))
                    self.assertEqual(set(versions[0][0]["assets"]),set(versions[2][0]["assets"]))
                    self.assertEqual(len(versions[0][0]["assets"]),5)
                    ids.extend([k for k,m in choices[0].items() if m==sb.expected_method(frame)])
                    for condition,(payload,_) in zip(sb.CONDITIONS,versions):
                        state=payload["state"]
                        self.assertEqual("candidate_mental_spaces" in state,condition!="image")
                        self.assertEqual("candidate_generic_spaces" in state,condition=="generic")
                        self.assertEqual(len(payload["questions"]["best_bridge"]["criteria"]),4)
        self.assertCountEqual(ids,["K1","K1","K2","K2","K3","K3","K4","K4"])

    def test_no_oracle_labels_or_metric_equalities_sent(self):
        with tempfile.TemporaryDirectory() as temp:
            for frame in sb.FRAMES:
                for condition in sb.CONDITIONS:
                    payload,_=sb.make_payload(Path(temp),"left",frame,condition)
                    state=json.dumps(
                        {k:v for k,v in payload.items() if k!="assets"},ensure_ascii=False
                    ).lower()
                    for forbidden in (
                        "from_c","from_a","from_b","edge_link",
                        "expected_method","oracle_expected",
                        "correct_candidate","measured_degrees",
                        "angle_bisector","euclid i.10","congruence",
                        "verified_equal"
                    ):
                        self.assertNotIn(forbidden,state)
                    self.assertNotIn("truth",state)

if __name__=="__main__":
    unittest.main()
