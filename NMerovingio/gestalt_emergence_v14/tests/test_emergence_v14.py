"""Offline invariants of the v1.4 three-modality emergence experiment."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import emergence_v14 as m

class TestEmergenceV14(unittest.TestCase):
    def test_coincidence_and_noncoincidence(self):
        for shape in m.SHAPES:
            g=m.geometry(shape)
            self.assertEqual(g["same_support"],shape.startswith("iso_"))
            self.assertEqual(g["supports"]["upper"]==g["supports"]["lower"],
                             g["same_support"])

    def test_registration_and_history(self):
        for history in m.HISTORIES:
            self.assertEqual(m.registered(history,0),{"upper":False,"lower":False})
            self.assertEqual(m.registered(history,2),{"upper":True,"lower":True})
            self.assertEqual(sum(m.registered(history,1).values()),1)
        self.assertNotEqual(m.registered("upper_first",1),
                            m.registered("lower_first",1))

    def test_same_final_material_different_genealogy(self):
        for shape in m.SHAPES:
            geo=m.geometry(shape)
            first=m.material_segments(geo,"upper_first",2)
            second=m.material_segments(geo,"lower_first",2)
            self.assertEqual(set(first),set(second))
            self.assertNotEqual(m.events("upper_first",2),
                                m.events("lower_first",2))

    def test_abstract_vs_shared_carrier_not_confused(self):
        for history in m.HISTORIES:
            for shape in m.SHAPES:
                for stage in m.STAGES:
                    oracle=m.expected(shape,history,stage)
                    self.assertEqual(oracle["joint_abstract"],stage==2)
                    self.assertEqual(oracle["joint_carrier"],
                                     stage==2 and shape.startswith("iso_"))
                    self.assertFalse(oracle["cross_metric"])

    def test_three_modalities_share_questions_and_history(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for shape in ("iso_low","scalene_left"):
                for history in m.HISTORIES:
                    for stage in m.STAGES:
                        p={mode:m.make_request(root,shape,history,stage,mode) for mode in m.MODES}
                        self.assertEqual(
                            len({json.dumps(x["questions"],sort_keys=True)
                                 for x in p.values()}),1)
                        timeline=[x["state"]["process_clock"] for x in p.values()]
                        self.assertEqual(timeline[0],timeline[1])
                        self.assertEqual(timeline[1],timeline[2])
                        self.assertEqual(set(p["annotated"]["assets"]),{"w"})
                        self.assertEqual(set(p["plain"]["assets"]),{"w"})
                        self.assertNotIn("assets",p["symbolic"])

    def test_no_future_carriers_leak_into_symbolic_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for shape in m.SHAPES:
                for history in m.HISTORIES:
                    for stage in m.STAGES:
                        req=m.make_request(root,shape,history,stage,"symbolic")
                        graph=req["state"]["material_graph"]
                        self.assertEqual(len(graph["on_AB"]),stage)
                        self.assertEqual(len(req["state"]["process_clock"]["completed_events"]),stage)
                        self.assertEqual(
                            len(graph["carrier_endpoints"]),
                            len(m.material_segments(m.geometry(shape),history,stage)))

    def test_isosceles_plain_pixels_equal_stage_one_two(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for shape in ("iso_low","iso_high"):
                for history in m.HISTORIES:
                    plain1=m.draw(root/"one.png",shape,history,1,False).read_bytes()
                    plain2=m.draw(root/"two.png",shape,history,2,False).read_bytes()
                    self.assertEqual(plain1,plain2)
                    marked1=m.draw(root/"aone.png",shape,history,1,True).read_bytes()
                    marked2=m.draw(root/"atwo.png",shape,history,2,True).read_bytes()
                    self.assertNotEqual(marked1,marked2)

    def test_no_offline_oracle_fields_in_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            for mode in m.MODES:
                body=m.make_request(Path(temp),"iso_low","upper_first",1,mode)
                public=json.dumps({k:v for k,v in body.items() if k!="assets"}).lower()
                for forbidden in ("truth_scoring_only","correct_at_0_5",
                                  "oracle_expected","shared_carrier_certified"):
                    self.assertNotIn(forbidden,public)

if __name__=="__main__":
    unittest.main()
