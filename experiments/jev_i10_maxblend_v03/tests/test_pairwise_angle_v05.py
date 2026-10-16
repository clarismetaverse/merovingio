"""No-network checks for the visual angle-partition experiment."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))

from pairwise_angle_v05 import gap, prepare, PROMPT
from scalene_visuals import SHAPES

class PairwiseChecks(unittest.TestCase):
    def test_geometrically_different(self):
        for shape in SHAPES:
            self.assertLess(gap(shape,"angle"),0.0001)
            self.assertGreater(gap(shape,"segment"),1.0)

    def test_candidate_orders_both_tested(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for shape in SHAPES:
                a,ma=prepare(root,shape,False)
                b,mb=prepare(root,shape,True)
                self.assertEqual(ma["K1"],"angle")
                self.assertEqual(mb["K1"],"segment")
                self.assertEqual(len(a["assets"]),3)
                self.assertEqual(len(b["assets"]),3)

    def test_no_answer_or_proof_label_leakage(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload,_=prepare(Path(tmp),"left",False)
            exposed=json.dumps({k:v for k,v in payload.items() if k!="assets"}).lower()
            for forbidden in ("bisector","median","i.10","i.4","midpoint","sas","congruence"):
                self.assertNotIn(forbidden,exposed)
            self.assertEqual(payload["questions"]["best_bridge"]["type"],"choice")
            self.assertEqual(len(payload["questions"]["best_bridge"]["criteria"]),2)

if __name__=="__main__":
    unittest.main()
