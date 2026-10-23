"""Independent construction/structural controls for flat-angle medial REBASE."""
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from flat_angle import (
    generate_material,partition_families,prospective_schemata,case_initial_focus,
    activated_macro,anticipated,new_generic_events,productivity_feedback,
    candidate_scores,graph_neighbors,simulate,experiment,
    SCENARIOS,CONDITIONS,ATTENTION
)

class FlatAngleTests(unittest.TestCase):
    def test_w1_constructs_angular_and_segmental_partitions(self):
        g=generate_material("flat_ray")
        families=partition_families(g)
        anchor=[f for f in families if f["anchor"]=="O"]
        self.assertEqual(len(anchor),2)
        self.assertEqual({f["kind"] for f in anchor},{"ANGLE","SIDE"})
        self.assertEqual(anchor[0]["root_event"],anchor[1]["root_event"])
        schemas=prospective_schemata(families)
        self.assertEqual(len(schemas),1)
        s=next(iter(schemas.values()))
        self.assertEqual(set(s["slots"]),{f["id"] for f in anchor})
        self.assertEqual(g["certified_metric_equalities"],[])

    def test_crossing_creates_four_sectors_and_vertical_opposition_without_equality(self):
        g=generate_material("crossed_lines")
        fam=partition_families(g)
        self.assertEqual(len([f for f in fam if f["anchor"]=="O" and f["kind"]=="ANGLE"]),2)
        self.assertEqual(len([f for f in fam if f["anchor"]=="O" and f["kind"]=="SIDE"]),1)
        pairs=[e for e in g["edges"].values() if e["kind"]=="vertical_opposite"]
        self.assertEqual(len(pairs),2)
        self.assertTrue(all(e["epistemic_status"]=="structural_opposition_not_equality" for e in pairs))
        self.assertEqual(len(prospective_schemata(fam)),2)
        self.assertEqual(g["given_metric_equalities"],[])

    def test_independent_splits_have_no_common_causal_root(self):
        g=generate_material("independent_partitions")
        families=partition_families(g)
        self.assertGreaterEqual(len([f for f in families if f["kind"]=="ANGLE"]),2)
        self.assertGreaterEqual(len([f for f in families if f["kind"]=="SIDE"]),2)
        self.assertEqual(prospective_schemata(families),{})
        for a in (f for f in families if f["kind"]=="ANGLE"):
            for b in (f for f in families if f["kind"]=="SIDE"):
                self.assertNotEqual(a["root_event"],b["root_event"])

    def test_actual_generic_needs_both_roles_not_an_answer_label(self):
        families=partition_families(generate_material("flat_ray"))
        schema=next(iter(prospective_schemata(families).values()))
        angle=next(f for f in families if f["kind"]=="ANGLE" and f["id"] in schema["slots"])
        side=next(f for f in families if f["kind"]=="SIDE" and f["id"] in schema["slots"])
        self.assertEqual(anticipated(side,{angle["id"]},{schema["id"]:schema})[0]["kind"],"complete")
        first=new_generic_events({angle["id"]},{schema["id"]:schema},{})
        self.assertEqual(first[0]["kind"],"INCOMPLETE_GENERIC")
        memory={x["id"]:x for x in first}
        second=new_generic_events({angle["id"],side["id"]},{schema["id"]:schema},memory)
        self.assertEqual(second[0]["kind"],"COMPLETED_GENERIC")
        self.assertEqual(second[0]["missing_roles"],[])
        self.assertNotIn("equal",second[0]["epistemic_status"])

    def test_only_real_generic_event_can_emit_productivity_feedback(self):
        f=partition_families(generate_material("flat_ray"))
        schema=next(iter(prospective_schemata(f).values()))
        angle=next(x for x in f if x["kind"]=="ANGLE" and x["id"] in schema["slots"])
        side=next(x for x in f if x["kind"]=="SIDE" and x["id"] in schema["slots"])
        partial=new_generic_events({angle["id"]},{schema["id"]:schema},{})
        macro=activated_macro("productivity_feedback")
        reward,next_macro,causes=productivity_feedback(partial,{schema["id"]:schema},{},macro,"productivity_feedback")
        self.assertGreater(reward[side["id"]],0)
        self.assertTrue(causes)
        blank,unchanged,none=productivity_feedback([],{schema["id"]:schema},{},macro,"productivity_feedback")
        self.assertEqual(blank,{})
        self.assertEqual(unchanged,macro)
        self.assertEqual(none,[])
        _,_,no_feedback=productivity_feedback(partial,{schema["id"]:schema},{},macro,"predictive_only")
        self.assertFalse(no_feedback)

    def test_macro_and_genealogy_ablations_differ(self):
        self.assertEqual(activated_macro("topology_only")["opposition"],0.)
        self.assertEqual(activated_macro("genealogy_blind")["coorigin"],0.)
        g=generate_material("flat_ray")
        f=partition_families(g);s=prospective_schemata(f)
        init=case_initial_focus(f)
        act={x["id"]:.1 for x in f}
        n=graph_neighbors(f)
        scores1=candidate_scores(f,{init["id"]},"ANGLE",act,
            activated_macro("productivity_feedback"),s,{},"productivity_feedback",n)
        scores2=candidate_scores(f,{init["id"]},"ANGLE",act,
            activated_macro("topology_only"),s,{},"topology_only",n)
        key=next(x["id"] for x in f if x["kind"]=="SIDE" and x["anchor"]=="O")
        self.assertGreater(scores1[key]["prospective"],scores2[key]["prospective"])
        self.assertEqual(scores2[key]["genealogy"],0.)

    def test_matched_material_across_five_ablations(self):
        for s in SCENARIOS:
            runs=[simulate(c,s,seed=3,budget=3,attention="competing") for c in CONDITIONS]
            for r in runs:
                self.assertEqual(r["nodes"],runs[0]["nodes"])
                self.assertEqual(r["edges"],runs[0]["edges"])
                self.assertEqual(r["families"],runs[0]["families"])
                self.assertEqual(r["templates"],runs[0]["templates"])
                self.assertEqual(r["metrics"]["false_metric_certifications"],0)
                self.assertEqual(r["metrics"]["false_genealogy_pairings"],0)
                for t in r["timeline"]:
                    self.assertEqual(t.get("certified_metric_equalities",[]),[])
            self.assertEqual(simulate("productivity_feedback",s,3),
                             simulate("productivity_feedback",s,3))

    def test_independent_never_achieves_cogenerative_generic(self):
        for c in CONDITIONS:
            for a in ATTENTION:
                for seed in range(7):
                    r=simulate(c,"independent_partitions",seed,budget=3,attention=a)
                    self.assertFalse(r["metrics"]["medial_generic_complete"])
                    self.assertEqual(r["metrics"]["partial_count"],0)
                    self.assertFalse(r["generic_spaces"])

    def test_w1_completion_is_structural_only(self):
        seen=False
        for seed in range(24):
            result=simulate("productivity_feedback","flat_ray",seed,budget=3,attention="competing")
            if result["metrics"]["medial_generic_complete"]:
                seen=True
                self.assertTrue(all(e["epistemic_status"]=="structural_mapping_not_metric_proof"
                                    for e in result["generic_spaces"]))
                self.assertEqual(result["metrics"]["false_metric_certifications"],0)
        self.assertTrue(seen)

    def test_two_focus_rebases_in_w2_may_create_second_generic(self):
        any_second=False
        for seed in range(32):
            r=simulate("productivity_feedback","crossed_lines",seed,budget=3,attention="clean")
            if r["metrics"]["completed_count"]>=2:any_second=True
        self.assertTrue(any_second)

    def test_aggregate_bookkeeping(self):
        d=experiment(range(3),budget=3)
        self.assertEqual(len(d["runs"]),len(CONDITIONS)*len(SCENARIOS)*len(ATTENTION)*3)
        self.assertTrue(d["no_proof"] and d["no_jev"])
        for a in ATTENTION:
            for s in SCENARIOS:
                for c in CONDITIONS:
                    x=d["aggregates"][a][s][c]
                    self.assertEqual(x["n"],3)
                    self.assertEqual(x["false_metric_certifications"],0)
                    self.assertEqual(x["false_genealogy_pairings"],0)
        self.assertEqual(d["aggregates"]["clean"]["independent_partitions"]["productivity_feedback"]["completion_rate"],0)

if __name__=="__main__":
    unittest.main()
