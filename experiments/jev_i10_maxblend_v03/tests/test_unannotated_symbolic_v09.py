"""Offline validation; no TypeSafe credentials or API calls required."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import unannotated_symbolic_v09 as m

class TestUnannotatedSymbolic(unittest.TestCase):
    def test_eight_hypotheses_and_negative_controls(self):
        self.assertEqual(len(m.HYPOTHESES),8)
        self.assertEqual(sum(expected for expected,_ in m.HYPOTHESES.values()),4)
        self.assertEqual(sum(not expected for expected,_ in m.HYPOTHESES.values()),4)

    def test_same_questions_across_modalities(self):
        with tempfile.TemporaryDirectory() as f:
            for i in m.REPETITIONS:
                image=m.build_request(Path(f),"diagram",i)
                sym=m.build_request(Path(f),"symbolic",i)
                self.assertEqual(image["questions"],sym["questions"])
                self.assertIn("assets",image)
                self.assertNotIn("assets",sym)
                self.assertEqual(set(image["assets"]),{"workspace-image"})
                self.assertEqual(len(image["questions"]),8)

    def test_symbolic_state_contains_only_unmeasured_geometry(self):
        for i in m.REPETITIONS:
            s=m.symbolic_workspace(i)
            self.assertIn({"start":"A","middle":"D","end":"B"},s["between"])
            self.assertEqual(set(s["points"]),{"A","B","C","D"})
            self.assertEqual(set(s["segments"]),{"AB","AC","BC","CD"})
            self.assertNotIn("coordinates",s)
            self.assertNotIn("equality",s)
            self.assertNotIn("measured_angles",s)
            self.assertEqual(len(s["incidence"]),9)

    def test_diagrams_uncolored_unhighlighted(self):
        with tempfile.TemporaryDirectory() as f:
            for rot in (0,90,180,270):
                png=m.render_unannotated(Path(f)/(str(rot)+".png"),rot)
                with Image.open(png) as im:
                    self.assertEqual(im.size,(900,900))
                    colors=im.getcolors(maxcolors=100000)
                    self.assertIsNotNone(colors)
                    self.assertTrue(all(rgb[0] <= rgb[1] <= rgb[2] for _,rgb in colors))
                    self.assertGreater(len(colors),1)

    def test_no_answer_key_or_goal_in_requests(self):
        with tempfile.TemporaryDirectory() as f:
            for modality in m.CONDITIONS:
                s=m.build_request(Path(f),modality,0)
                body=json.dumps({k:v for k,v in s.items() if k!="assets"}).lower()
                for forbidden in ("expected","correct_at","proof of i.10",
                                  "bisector", "midpoint", "angle_equality",
                                  "hypotheses","true_positive"):
                    self.assertNotIn(forbidden,body)

    def test_scoring_is_independent_of_model(self):
        mock={"answers":{
            key:{"type":"noul","noul":0.95 if correct else 0.05}
            for key,(correct,_) in m.HYPOTHESES.items()
        }}
        result=m.validate_response(mock)
        self.assertEqual(sum(x["correct_at_0_5"] for x in result.values()),8)
        self.assertEqual(sum(x["confident_at_0_8"] for x in result.values()),8)

if __name__=="__main__":
    unittest.main()
