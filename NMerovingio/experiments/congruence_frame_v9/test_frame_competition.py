"""v9: frame competition must follow independently warranted congruences."""
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from frame_competition import (
    make_workspace,preconstruction_evidence,role_schema,
    check_witnesses,score_frames,certify_sas,simulate,experiment,
    GOALS,SHAPES,CONDITIONS,FRAMES
)
sys.path.insert(0,str(HERE.parent/"prospective_blending_v8"))
from prospective import division_goal,candidate_constructions,construct,prospective_blend

class CompetingCongruenceFrames(unittest.TestCase):
    def test_original_euclid_given_is_available_before_bisector(self):
        ws=make_workspace("equilateral")
        self.assertEqual(len(ws["points"]),3)
        self.assertEqual(len(ws["faces"]),1)
        self.assertEqual(ws["construction_events"],[])
        self.assertEqual(ws["given_angular_equalities"],[])
        for vertex in GOALS:
            pre=preconstruction_evidence(ws,vertex)
            self.assertEqual(pre["equal_outer_legs"]["status"],"verified")
            self.assertEqual(pre["equal_shared_side"]["status"],"uninstantiated")
            self.assertEqual(pre["equal_included_angles"]["status"],"uninstantiated")
            self.assertEqual(pre["equal_base_halves"]["status"],"uninstantiated")

    def test_sas_uses_only_two_sides_and_included_angle(self):
        for goal in GOALS:
            run=simulate("equilateral",goal,"balanced",seed=4)
            evidence=run["evidence_at_selection"]
            self.assertEqual([evidence[k]["status"] for k in FRAMES["LAL"]["slots"]],
                             ["verified","verified","verified"])
            self.assertEqual(evidence["equal_base_halves"]["status"],"unavailable")
            self.assertTrue(run["frame_attraction"]["LAL"]["fully_supported"])
            self.assertFalse(run["frame_attraction"]["LLL"]["fully_supported"])
            self.assertTrue(run["frame_attraction"]["LLL"]["proof_circularity_risk"])
            self.assertTrue(run["independent_proof_verifier"]["licensed"])
            self.assertEqual(run["independent_proof_verifier"]["status"],
                             "DERIVED_BY_SAS_RULE")
            self.assertEqual(run["postconstruction"]["certified_segment_equalities"],[])
            self.assertTrue(run["metrics"]["certified_base_halves_by_SAS"])

    def test_included_angle_is_geometrically_between_equal_sides(self):
        ws=make_workspace("equilateral");goal=division_goal(ws,"C")
        op=next(x for x in candidate_constructions(ws) if x["origin_vertex"]=="C")
        after=construct(ws,op)
        roles=role_schema(ws,after,goal)
        r=check_witnesses(ws,after,roles,"balanced")
        self.assertTrue(certify_sas(r,roles,"LAL")["licensed"])
        # A false "included angle" with the wrong vertex must be rejected
        # even if an attention score had classified all slots as complete.
        corrupted={**roles,"role_pairs":dict(roles["role_pairs"])}
        bad_angles=[x[:] for x in roles["role_pairs"]["equal_included_angles"]]
        bad_angles[0][0]=roles["correspondence"]["external_vertex_pair"][0]
        corrupted["role_pairs"]["equal_included_angles"]=bad_angles
        with self.assertRaises(AssertionError):
            certify_sas(r,corrupted,"LAL")

    def test_prior_can_favor_lll_initially_but_evidence_reverses_attraction(self):
        run=simulate("equilateral","C","LLL_initially_favored",seed=2)
        start=run["timeline"][0]["frame_attraction"]
        end=run["frame_attraction"]
        self.assertGreater(start["LLL"]["attraction_probability"],
                           start["LAL"]["attraction_probability"])
        self.assertGreater(end["LAL"]["attraction_probability"],
                           end["LLL"]["attraction_probability"])
        self.assertFalse(end["LLL"]["fully_supported"])
        self.assertTrue(end["LAL"]["fully_supported"])

    def test_cognitive_preference_and_rule_certificate_are_independent(self):
        # The geometry and strict verifier are independent of which
        # stochastic frame is cognitively selected.
        a=simulate("equilateral","C","balanced",seed=3)
        b=simulate("equilateral","C","LLL_initially_favored",seed=3)
        self.assertEqual(a["postconstruction"]["points"],
                         b["postconstruction"]["points"])
        self.assertEqual(a["independent_proof_verifier"]["derived_segment_equalities"],
                         b["independent_proof_verifier"]["derived_segment_equalities"])

    def test_counterfactual_independent_base_equality_can_license_lll(self):
        found_lll=False
        for seed in range(18):
            r=simulate("equilateral","C","counterfactual_base_given",seed)
            evidence=r["evidence_at_selection"]["equal_base_halves"]
            self.assertEqual(evidence["status"],"verified")
            self.assertEqual(evidence["source"],"COUNTERFACTUAL_EXTRA_GIVEN")
            self.assertTrue(r["frame_attraction"]["LLL"]["fully_supported"])
            self.assertTrue(r["LLL_licensed_without_using_conclusion"])
            found_lll |= r["selected_frame"]=="LLL"
        self.assertTrue(found_lll)

    def test_isosceles_can_support_sas_and_scalene_cannot(self):
        iso=simulate("isosceles","C","balanced",seed=0)
        scalene=simulate("scalene","C","balanced",seed=0)
        self.assertTrue(iso["independent_proof_verifier"]["licensed"])
        self.assertFalse(scalene["independent_proof_verifier"]["licensed"])
        self.assertFalse(scalene["frame_attraction"]["LAL"]["fully_supported"])
        self.assertFalse(scalene["frame_attraction"]["LLL"]["fully_supported"])
        self.assertFalse(scalene["metrics"]["certified_base_halves_by_SAS"])
        self.assertEqual(scalene["independent_proof_verifier"]["derived_segment_equalities"],[])

    def test_missing_angle_equality_does_not_license_sas(self):
        r=simulate("equilateral","C","angle_witness_masked",seed=1)
        self.assertFalse(r["frame_attraction"]["LAL"]["fully_supported"])
        self.assertFalse(r["independent_proof_verifier"]["licensed"])
        self.assertTrue(r["postconstruction"]["given_angular_equalities"],
                        "The geometric event is unchanged: only attention was masked")

    def test_prospective_frame_changes_attention_not_proof(self):
        a=simulate("equilateral","C","balanced",seed=2)
        b=simulate("equilateral","C","without_prospection",seed=2)
        self.assertIsNotNone(a["prospective"])
        self.assertIsNone(b["prospective"])
        self.assertTrue(a["binding"]["matched"])
        self.assertFalse(b["binding"]["matched"])
        self.assertTrue(a["independent_proof_verifier"]["licensed"])
        self.assertTrue(b["independent_proof_verifier"]["licensed"])

    def test_evidence_order_not_hardcoded(self):
        orders=set()
        for seed in range(18):
            x=simulate("equilateral","C","balanced",seed)
            orders.add(tuple(s["newly_inspected_slot"] for s in x["timeline"][2:4]))
            self.assertEqual(x["timeline"][0]["stage"],"BEFORE_CD")
            self.assertEqual(x["timeline"][1]["stage"],"CONSTRUCT_AND_FIND_TWO_FACES")
            self.assertEqual(x["timeline"][-1]["stage"],"COMPETING_FRAME_BINDING")
        self.assertEqual(len(orders),2)

    def test_ablation_evidence_and_material_are_separated(self):
        runs=[simulate("equilateral","C",cond,seed=2) for cond in CONDITIONS]
        for run in runs:
            self.assertEqual(run["preconstruction"]["points"],
                             runs[0]["preconstruction"]["points"])
            self.assertEqual(run["postconstruction"]["points"],
                             runs[0]["postconstruction"]["points"])
            self.assertEqual(run["structural_role_schema"],
                             runs[0]["structural_role_schema"])
            self.assertEqual(run["metrics"]["false_metric_certifications"],0)

    def test_aggregation_and_negative_controls(self):
        data=experiment(range(3))
        self.assertEqual(len(data["runs"]),(
            3*len(CONDITIONS)+len(CONDITIONS)+(len(CONDITIONS)-1))*3)
        for shape,goals in data["aggregates"].items():
            for vertex,cases in goals.items():
                for cond,stat in cases.items():
                    self.assertEqual(stat["n"],3)
                    self.assertEqual(stat["false_metric_certifications"],0)
        self.assertEqual(
            data["aggregates"]["scalene"]["C"]["balanced"]["certified_SAS_rate"],0)
if __name__=="__main__": unittest.main()
