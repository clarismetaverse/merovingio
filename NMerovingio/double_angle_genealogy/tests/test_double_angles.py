"""Deterministic tests for double-angle genealogy and Jev request contracts."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core import derive,genealogy,benchmark,GEOMETRIES
from jev_double_angle import payload,cases,QUESTIONS

class TestGenealogyDoubleAngles(unittest.TestCase):
    def test_right_angles_and_apex_halves_distinct_in_measure(self):
        for shape in GEOMETRIES:
            g=derive(shape)
            self.assertTrue(g["certified"]["apex_sectors_equal"])
            self.assertTrue(g["certified"]["base_angles_right"])
            self.assertFalse(g["certified"]["cross_level_angles_equal"])
            self.assertLess(g["apex_half_degrees"],90.0)

    def test_coinciding_support_requires_isosceles(self):
        for shape in GEOMETRIES:
            g=derive(shape)
            expected=shape.startswith("iso_")
            self.assertEqual(g["carrier_coincidence_verified"],expected)
            if expected:
                self.assertEqual(g["carriers"]["upper"],g["carriers"]["lower"])
                self.assertEqual(g["carriers"]["upper"],"CD")
            else:
                self.assertNotEqual(g["carriers"]["upper"],g["carriers"]["lower"])

    def test_distinct_first_appearances_same_end_state(self):
        for shape in GEOMETRIES:
            apex=genealogy(shape,"apex_first")
            foot=genealogy(shape,"base_first")
            self.assertEqual(apex["final_material_fingerprint"],
                             foot["final_material_fingerprint"])
            self.assertNotEqual(apex["events"],foot["events"])
            self.assertEqual(apex["first_emergence"]["upper_left"],1)
            self.assertEqual(foot["first_emergence"]["upper_left"],2)
            self.assertEqual(apex["first_emergence"]["lower_left"],2)
            self.assertEqual(foot["first_emergence"]["lower_left"],1)
            self.assertFalse(apex["candidate_generic_space"]["cross_level_metric_equality"])

    def test_no_history_requests_identical_within_modalities(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)
            for shape in GEOMETRIES:
                for modality in ("symbolic","image"):
                    a=payload(shape,"apex_first",modality,"final",out)
                    b=payload(shape,"base_first",modality,"final",out)
                    self.assertEqual(a,b)

    def test_reverse_presentation_preserves_event_order_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)
            a=payload("iso_low","apex_first","symbolic","chronological",out)
            b=payload("iso_low","apex_first","symbolic","reverse_list",out)
            ev_a=a["state"]["construction_events"]
            ev_b=b["state"]["construction_events"]
            self.assertEqual(ev_a,list(reversed(ev_b)))
            self.assertEqual(ev_a[0]["step"],1)
            self.assertEqual(ev_b[0]["step"],2)
            self.assertEqual(a["questions"],b["questions"])

    def test_image_plain_and_symbolic_no_images(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)
            for shape in GEOMETRIES:
                img=payload(shape,"apex_first","image","final",out)
                sym=payload(shape,"apex_first","symbolic","final",out)
                self.assertEqual(len(img["assets"]),1)
                self.assertNotIn("assets",sym)
                self.assertEqual(img["questions"],sym["questions"])
                with Image.open(out/"images"/(shape+".png")) as im:
                    self.assertEqual(im.size,(880,720))

    def test_question_and_case_count_no_answer_key(self):
        cs=cases()
        self.assertEqual(len(cs),24)
        self.assertEqual(len(QUESTIONS),3)
        with tempfile.TemporaryDirectory() as folder:
            request=payload("iso_high","base_first","symbolic","chronological",Path(folder))
            text=json.dumps(request).lower()
            for forbidden in ("ground_truth_shared","carrier_coincidence_verified",
                              "cross_level_angles_equal","api_key","bearer ",
                              "oracle_expected","correct_answer"):
                self.assertNotIn(forbidden,text)
            self.assertEqual(request["questions"]["shared"]["type"],"noul")
            self.assertEqual(request["questions"]["focus"]["type"],"choice")

    def test_report_is_not_proof(self):
        report=benchmark()
        self.assertEqual(len(report["cases"]),4)
        self.assertIn("candidate",report["status"])

if __name__=="__main__":
    unittest.main()
