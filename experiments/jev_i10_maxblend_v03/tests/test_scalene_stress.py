"""Geometry, role sensitivity and prompt checks; these tests do not call Jev."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from scalene_visuals import SHAPES, METHODS, MODES, fractions, label_order
from scalene_stress import EXPECTED, make_trial


class TestScaleneVision(unittest.TestCase):
    def test_distinct_constructions(self):
        for shape in SHAPES:
            frac = fractions(shape)
            self.assertEqual(len(frac), len(METHODS))
            self.assertEqual(len(set(round(x, 6) for x in frac.values())), 5)
            self.assertNotAlmostEqual(frac["angle"], frac["segment"], places=3)
            self.assertNotAlmostEqual(frac["angle"], frac["orthogonal"], places=3)

    def test_roles(self):
        for shape in SHAPES:
            f = fractions(shape)
            self.assertEqual(f["segment"], 0.5)
            self.assertTrue(0 < f["orthogonal"] < 1)
            self.assertTrue(0 < f["angle"] < 1)

    def test_option_randomization(self):
        a, _ = label_order("left", "angle")
        b, _ = label_order("right", "angle")
        self.assertEqual(set(a.values()), set(b.values()))
        self.assertNotEqual(list(a.values()), list(b.values()))

    def test_payload_hides_target_identity(self):
        with tempfile.TemporaryDirectory() as t:
            payload, mapping, _ = make_trial(Path(t), "left", "free")
            content = json.dumps({k: v for k, v in payload.items() if k != "assets"}).lower()
            for label in ("decoy_a", "decoy_b", "bisector", "median", "altitude", "i.10", "i.4"):
                self.assertNotIn(label, content)
            criteria = payload["questions"]["best_bridge"]["criteria"]
            for method in METHODS:
                self.assertNotIn(method, criteria)
            self.assertEqual(len(payload["assets"]), 6)
            self.assertEqual(len(mapping), 5)

    def test_conditioned_targets_defined(self):
        self.assertEqual(set(EXPECTED), set(MODES) - {"free"})


if __name__ == "__main__":
    unittest.main()
