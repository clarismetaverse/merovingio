"""Local tests independent of Jev API and GitHub secrets."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import graph_genealogy_v12 as p


class TestCausalGraph(unittest.TestCase):
    def test_geo_oracle(self):
        for shape in p.SHAPES:
            geometry = p.geometry(shape)
            self.assertEqual(geometry["shared_carrier"], shape.startswith("iso_"))
            self.assertFalse(geometry["cross_level_angle_equal"])

    def test_same_final_workspace_distinct_histories(self):
        for shape in p.SHAPES:
            for h in p.HISTORIES:
                item = p.construct_payload(shape, h, "canonical")
                self.assertEqual(item["state"]["workspace"], p.final_workspace(shape))
            u = p.graph(shape, "upper_first")
            l = p.graph(shape, "lower_first")
            self.assertNotEqual(p.graph_signature(u), p.graph_signature(l))

    def test_graph_signature_invariant_to_presentation(self):
        for shape in p.SHAPES:
            for history in p.HISTORIES:
                signatures = {p.graph_signature(p.ordered_graph(shape, history, mode))
                              for mode in p.PRESENTATIONS}
                self.assertEqual(len(signatures), 1)

    def test_graph_timestamps_and_edges(self):
        for shape in p.SHAPES:
            for hist in p.HISTORIES:
                g = p.graph(shape, hist)
                times = {x["id"]: x["time"] for x in g["nodes"]}
                earlier = "O1" if hist == "upper_first" else "O2"
                later = "O2" if hist == "upper_first" else "O1"
                self.assertLess(times[earlier], times[later])
                self.assertIn({"from": earlier, "to": later, "relation": "precedes"}, g["edges"])
                self.assertEqual(times["O3"], 3)

    def test_no_oracle_leak(self):
        for shape in p.SHAPES:
            for hist in p.HISTORIES:
                req = p.construct_payload(shape, hist, "shuffled")
                value = json.dumps(req).lower()
                for forbidden in ("shared_carrier", "carrier_shared", "cross_level_equal",
                                  "expected_last_event_offline", "correct_answer", "proof of euclid"):
                    self.assertNotIn(forbidden, value)
                self.assertNotIn("assets", req)

    def test_baseline_identical_across_histories(self):
        for shape in p.SHAPES:
            self.assertEqual(p.construct_payload(shape), p.construct_payload(shape))
            self.assertNotIn("construction_graph", p.construct_payload(shape)["state"])
            self.assertEqual(len(p.construct_payload(shape)["questions"]),3)
            self.assertEqual(len(p.construct_payload(shape,"upper_first","canonical")["questions"]),4)

    def test_factorial_schedule(self):
        schedule = p.run_schedule()
        self.assertEqual(len(schedule),32)
        self.assertEqual(sum(x["condition"] == "final_only" for x in schedule),8)
        self.assertEqual(sum(x["condition"] == "causal_graph" for x in schedule),24)
        self.assertEqual(len({(x["shape"], x["history"], x["presentation"])
                              for x in schedule if x["condition"] == "causal_graph"}),24)

if __name__ == "__main__":
    unittest.main()