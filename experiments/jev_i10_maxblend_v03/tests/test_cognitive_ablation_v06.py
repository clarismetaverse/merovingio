"""Jev v0.6 structural ablation tests; all checks run without API."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cognitive_ablation_v06 import CONDITIONS, candidate_space, generic_alignment, payload_for


class TestAblation(unittest.TestCase):
    def test_conditions_share_same_visual_candidates(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            a, mapping = payload_for(root, "left", False, "visual")
            b, mapping_b = payload_for(root, "left", False, "mental")
            c, mapping_c = payload_for(root, "left", False, "generic")
            self.assertEqual(mapping, mapping_b)
            self.assertEqual(mapping, mapping_c)
            self.assertEqual(set(a["assets"]), set(b["assets"]))
            self.assertEqual(set(a["assets"]), set(c["assets"]))
            self.assertEqual(len(a["assets"]), 3)
            self.assertEqual(set(mapping.values()), {"angle", "segment"})

    def test_nested_structures_only_in_their_conditions(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for condition in CONDITIONS:
                request, mapping = payload_for(root, "right", True, condition)
                state=request["state"]
                self.assertEqual("conceptual_partition" in state, condition != "visual")
                self.assertEqual("generic_space_candidates" in state, condition == "generic")
                self.assertEqual(len(request["questions"]["best_bridge"]["criteria"]),2)

    def test_no_label_or_equality_leakage(self):
        with tempfile.TemporaryDirectory() as folder:
            for cond in CONDITIONS:
                request,_ = payload_for(Path(folder),"left",False,cond)
                visible=json.dumps({k:v for k,v in request.items() if k != "assets"}).lower()
                for forbidden in (
                    '"equal_angle_pair":', '"measured_angles":',
                    '"verified_equal_angles":', "angle_bisector",
                    '"selected_method":', '"correct":', "i.10", "i.4",
                    "congruent triangles", "sas criterion"
                ):
                    self.assertNotIn(forbidden,visible)
                assert "CA" in visible or cond=="visual"

    def test_generic_space_candidate_not_certified(self):
        a=generic_alignment("K1")
        self.assertEqual(a["status"],"hypothetical_alignments_only")
        self.assertIn("Do not assume",a["forbidden_inference"])
        ms=candidate_space("K1")
        self.assertEqual(len(ms["mental_spaces"]),2)
        self.assertEqual(ms["construction_skeleton"]["between"], [["A","D","B"]])


if __name__ == "__main__":
    unittest.main()
