"""Co-generation, medial binding, genealogy blindness and no-metric-leak tests."""
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from poristic import (build_material,partition_families,common_term,co_generations,
                      packet_groups,run,experiment,CONDITIONS,MODES)
from endogenous import side,angle,group_from_edges

class PoristicGestaltTests(unittest.TestCase):
    def test_geometry_produces_dual_partitions_and_common_term(self):
        for mode in MODES:
            graph=build_material(mode)
            families=partition_families(graph)
            self.assertTrue(any(p["domain"]=="side" for p in families))
            self.assertTrue(any(p["domain"]=="angle" for p in families))
            packets=co_generations(graph)
            self.assertGreaterEqual(len(packets),1)
            hit=next(x for x in packets if x["mediator"]["carrier"]==side("C","D"))
            self.assertEqual(hit["mediator"]["contact"],"D")
            self.assertEqual(hit["mediator"]["vertex"],"C")
            self.assertIn(side("A","D"),hit["segment_partition"]["children"])
            self.assertIn(side("B","D"),hit["segment_partition"]["children"])
            self.assertEqual(len(hit["regions"]),2)
            self.assertEqual(len(hit["oppositions"]),2)
            self.assertTrue(all(p["structural_status"]=="co_generated_role_packet"
                                for p in packets))

    def test_does_not_assert_equal_halves_from_arbitrary_cevian(self):
        ordinary=build_material("ordinary_cevian")
        scalene=build_material("scalene")
        self.assertFalse(ordinary["given_equal_angles"])
        self.assertFalse(ordinary["certified_metric_equalities"])
        self.assertFalse(ordinary["geometry"]["observations"]["base_halves_equal_by_coordinates"])
        self.assertTrue(scalene["given_equal_angles"])
        self.assertTrue(co_generations(ordinary))
        self.assertFalse(co_generations(ordinary)[0]["angle_equality_evidence"])
        self.assertTrue(co_generations(scalene)[0]["angle_equality_evidence"])

    def test_rebase_only_available_after_event_group_selected(self):
        graph=build_material("isosceles");packets=co_generations(graph)
        before=packet_groups(graph,packets,{},set())
        co=next(x for x in before.values() if x["operator"]=="COFRAME")
        self.assertFalse(any(x["operator"]=="REBASE" for x in before.values()))
        after=packet_groups(graph,packets,{co["id"]:co},{co["id"]})
        self.assertTrue(any(x["operator"]=="REBASE" for x in after.values()))
        for x in after.values():
            self.assertIn(co["id"],x["parents"])
            self.assertEqual(x["mediator"],side("C","D"))
            self.assertEqual(x["direction"],"angles→sides")

    def test_arbitrary_line_has_no_metric_source_for_angular_transfer(self):
        graph=build_material("ordinary_cevian");packets=co_generations(graph)
        groups=packet_groups(graph,packets,{},set())
        co=next(iter(groups.values()))
        rebases=packet_groups(graph,packets,{co["id"]:co},{co["id"]})
        self.assertTrue(rebases)
        self.assertTrue(all(x["direction"]=="undirected_structural_analogy" for x in rebases.values()))
        self.assertTrue(all(not x["has_angular_equality"] for x in rebases.values()))

    def test_matched_conditions_have_identical_geometry(self):
        runs=[run(c,"isosceles",9,12) for c in CONDITIONS]
        base=runs[0]["graph"]
        self.assertTrue(all(r["graph"]==base for r in runs))
        self.assertTrue(all(r["geometry"]==runs[0]["geometry"] for r in runs))
        self.assertTrue(all(r["construction_packets"]==runs[0]["construction_packets"] for r in runs))
        self.assertTrue(all(r["metrics"]["false_metric_certifications"]==0 for r in runs))
        self.assertEqual(runs[0]["timeline"][0]["macro_after"]["genealogy"],0)
        self.assertGreater(runs[3]["timeline"][0]["macro_after"]["genealogy"],0)
        self.assertEqual(runs[4]["timeline"][0]["macro_after"]["genealogy"],0)

    def test_no_cognitive_binding_is_promoted_to_equality(self):
        for mode in MODES:
            for condition in CONDITIONS:
                r=run(condition,mode,seed=2,budget=22)
                self.assertEqual(r["metrics"]["false_metric_certifications"],0)
                for event in r["timeline"]:
                    self.assertFalse(event.get("certified_metric_equalities"))
                    hyp=event.get("new_analogical_hypothesis")
                    if hyp:
                        self.assertEqual(hyp["epistemic_status"],"HYPOTHESIS_ONLY")
                        self.assertFalse(hyp["licensed_by_theorem"])
                        self.assertNotEqual(mode,"ordinary_cevian")

    def test_seed_reproducibility(self):
        self.assertEqual(run("coupled","scalene",6,12),run("coupled","scalene",6,12))

    def test_experiment_ablations_and_aggregates(self):
        data=experiment(range(2),budget=14)
        self.assertEqual(len(data["runs"]),len(CONDITIONS)*len(MODES)*2)
        self.assertTrue(data["no_proof"])
        for mode in MODES:
            for condition in CONDITIONS:
                self.assertEqual(data["aggregates"][mode][condition]["n"],2)
                self.assertEqual(data["aggregates"][mode][condition]["false_metric_certifications"],0)
                self.assertGreater(data["aggregates"][mode][condition]["cogeneration_detected_rate"],0)
        self.assertEqual(data["aggregates"]["ordinary_cevian"]["coupled"]["transfer_question_rate"],0)

if __name__=="__main__":
    unittest.main()
