"""Tests for Panoptikon Gestalt Dynamics; no credentials, no network."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from core import (
    ROLE_SCHEMA,run_deterministic,trace_construction,backpropagation,
    deformation_series,interior_wedge_C_through_AB,lerp,A,B,
)
from jev_probe import model_payload,CHOICES

class TestGestaltDynamics(unittest.TestCase):
    def test_same_state_but_distinct_genealogies(self):
        report=run_deterministic()
        base,fan=report["histories"]
        self.assertEqual(base["final_material"],fan["final_material"])
        self.assertEqual(base["final_material_sha256"],fan["final_material_sha256"])
        self.assertEqual(base["final_candidates"],fan["final_candidates"])
        self.assertEqual(base["final_roles"],fan["final_roles"])
        self.assertNotEqual(base["events"],fan["events"])

    def test_first_appearance_records_provenance(self):
        a=trace_construction("base_first")
        b=trace_construction("fan_first")
        self.assertEqual(a["first_appearance_provenance"]["base_AD_DB"]["stage"],1)
        self.assertEqual(b["first_appearance_provenance"]["base_AD_DB"]["stage"],2)
        self.assertIn("ray_from_C",b["snapshots"][1]["candidates"])
        self.assertNotIn("ray_from_C",a["snapshots"][1]["candidates"])
        self.assertNotIn("ray_from_C",b["snapshots"][-1]["candidates"])

    def test_backpropagation_changes_roles_of_existing_objects(self):
        a=trace_construction("base_first")
        events=backpropagation(a)
        self.assertTrue(any(
            e["object"]=="AB" and
            "carrier_of_adjacent_base_parts" in e["new_interpretive_roles"]
            for e in events
        ))
        self.assertTrue(any(
            e["object"]=="C" and
            "vertex_of_adjacent_angular_sectors" in e["new_interpretive_roles"]
            for e in events
        ))

    def test_deformation_destroys_internal_partitions(self):
        series=deformation_series()
        self.assertTrue(series[0]["strictly_within_AB"])
        self.assertIn("generic_paired_regions",series[0]["active_mental_spaces"])
        for x in series[1:]:
            self.assertFalse(x["strictly_within_AB"])
            for role in ("base_AD_DB","angular_ACD_DCB","regions_ACD_BCD",
                         "bridge_angle_base","generic_paired_regions"):
                self.assertNotIn(role,x["active_mental_spaces"])

    def test_ray_inside_apex_wedge(self):
        self.assertTrue(interior_wedge_C_through_AB(lerp(A,B,0.37)))
        self.assertFalse(interior_wedge_C_through_AB(lerp(A,B,1.1)))

    def test_proposed_generic_space_not_proven_congruence(self):
        row=ROLE_SCHEMA["generic_paired_regions"]
        self.assertEqual(row["status"],"candidate")
        self.assertNotIn("equal",json.dumps(ROLE_SCHEMA).lower())

    def test_jev_final_only_payloads_identical(self):
        a=trace_construction("base_first")
        b=trace_construction("fan_first")
        final_a=model_payload(a,False)
        final_b=model_payload(b,False)
        self.assertEqual(final_a,final_b)
        self.assertNotEqual(model_payload(a,True),model_payload(b,True))
        self.assertEqual(len(final_a["questions"]["focus"]["criteria"]),4)
        self.assertEqual(
            set(final_a["questions"]["focus"]["criteria"]),set(CHOICES)
        )

    def test_jev_payload_excludes_truth_and_credential(self):
        for g in ("base_first","fan_first"):
            state=model_payload(trace_construction(g),True)
            public=json.dumps(state).lower()
            for forbidden in ("api_key","bearer ","equal_angles","proof_i10","congruent"):
                self.assertNotIn(forbidden,public)

if __name__=="__main__":
    unittest.main()
