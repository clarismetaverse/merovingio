"""v6: productive analogical loop tests, geometry and epistemic controls."""
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from productive import (
    build_material,coorigin_ledger,opposite_roles,packet_schema,
    generic_increment,realize,feedback_signal,initialize,simulate,experiment,
    CONDITIONS,MODES,ATTENTION,rank
)

class ProductivityTests(unittest.TestCase):
    def test_generic_schemas_generated_from_graph_and_carrier(self):
        for mode in MODES:
            g=build_material(mode)
            packets,_=coorigin_ledger(g)
            schemas=packet_schema(g,packets)
            self.assertTrue(schemas)
            candidates=opposite_roles(g)
            ids={c["id"] for c in candidates}
            for s in schemas.values():
                self.assertEqual(len(s["slots"]),2)
                self.assertTrue(set(s["slots"])<=ids)
                self.assertEqual(len(s["angel_roles"]),2)
                self.assertEqual(len(s["side_roles"]),2)
            self.assertEqual(bool(g["given_equal_angles"]),mode!="ordinary_cevian")

    def test_partial_analogical_schema_completes_only_with_correct_partner(self):
        g=build_material("isosceles")
        packets,_=coorigin_ledger(g)
        schemas=packet_schema(g,packets)
        slot_set=set(next(iter(schemas.values()))["slots"])
        first,second=sorted(slot_set)
        others=next(x for x in opposite_roles(g) if x["id"] not in slot_set)
        moves=opposite_roles(g)
        a=next(x for x in moves if x["id"]==first)
        b=next(x for x in moves if x["id"]==second)
        self.assertTrue(any(x["type"]=="partial" for x in generic_increment(a,set(),schemas)))
        self.assertTrue(any(x["type"]=="completion" for x in generic_increment(b,{first},schemas)))
        self.assertEqual(generic_increment(others,{first},schemas),[])
        partial=realize(a,{first},schemas,g)
        full=realize(b,{first,second},schemas,g)
        self.assertEqual(partial[0]["kind"],"INCOMPLETE_GENERIC")
        self.assertEqual(partial[0]["missing_roles"],[second])
        self.assertEqual(full[0]["kind"],"COMPLETED_GENERIC")
        self.assertFalse("metric_equalities" in full[0])

    def test_feedback_is_caused_by_an_actual_new_partial_group(self):
        g=build_material("scalene")
        packets,ledger=coorigin_ledger(g)
        schemas=packet_schema(g,packets)
        slots=next(iter(schemas.values()))["slots"]
        mappings={m["id"]:m for m in opposite_roles(g)}
        act,macro,_=initialize(g,packets,"coupled")
        before=act.copy()
        partial=realize(mappings[slots[0]],{slots[0]},schemas,g)
        available={slots[1]:mappings[slots[1]]}
        gain,updated,_,causes=feedback_signal(
            g,mappings[slots[0]],partial,schemas,{},act,macro,
            "productivity_feedback",available)
        self.assertTrue(causes)
        self.assertGreater(gain[slots[1]],0)
        self.assertGreater(updated[mappings[slots[1]]["angle"]],
                           before[mappings[slots[1]]["angle"]])
        empty_gain,empty_act,_,empty_causes=feedback_signal(
            g,mappings[slots[0]],[],schemas,{},act,macro,
            "productivity_feedback",available)
        self.assertFalse(empty_gain)
        self.assertFalse(empty_causes)
        self.assertEqual(empty_act,act)

    def test_scored_partner_after_partial_exceeds_unrelated_at_same_base(self):
        g=build_material("isosceles")
        packets,ledger=coorigin_ledger(g)
        schemas=packet_schema(g,packets)
        act,macro,_=initialize(g,packets,"coupled")
        slots=next(iter(schemas.values()))["slots"]
        all_m=opposite_roles(g)
        scores=rank(g,all_m,{slots[0]},"SIDE",act,macro,ledger,schemas,
                    "predictive_only",{})
        self.assertGreater(scores[slots[1]]["prospective_productivity"],1.0)
        for m in all_m:
            if m["id"] not in slots:
                self.assertEqual(scores[m["id"]]["prospective_productivity"],0)

    def test_conditions_same_geometry_and_simulation_is_reproducible(self):
        for attention in ATTENTION:
            rr=[simulate(c,"scalene",3,4,attention) for c in CONDITIONS]
            for r in rr:
                self.assertEqual(r["material"],rr[0]["material"])
                self.assertEqual(r["construction_schemas"],rr[0]["construction_schemas"])
                self.assertEqual(r["metrics"]["selected_oppositions"],4)
                self.assertEqual(r["metrics"]["duplicate_mapping_rebases"],0)
            self.assertEqual(simulate("productivity_feedback","isosceles",3,4,attention),
                             simulate("productivity_feedback","isosceles",3,4,attention))

    def test_only_productive_conditions_get_realized_feedback(self):
        for attention in ATTENTION:
            feed=simulate("productivity_feedback","isosceles",0,4,attention)
            pred=simulate("predictive_only","isosceles",0,4,attention)
            topo=simulate("topology_only","isosceles",0,4,attention)
            self.assertEqual(pred["metrics"]["feedback_signal_count"],0)
            self.assertEqual(topo["metrics"]["feedback_signal_count"],0)
            self.assertGreaterEqual(feed["metrics"]["feedback_signal_count"],0)
            self.assertTrue(all("prospective_productivity" in e["chosen_score"] for e in feed["timeline"][1:]))

    def test_arbitrary_cevian_cannot_project_equal_angles_to_equal_sides(self):
        for c in CONDITIONS:
            for attention in ATTENTION:
                r=simulate(c,"ordinary_cevian",seed=7,budget=6,attention=attention)
                self.assertEqual(r["analogical_questions"],[])
                self.assertFalse(r["source_given_angles"])
                self.assertFalse(r["geometry"]["observations"]["base_halves_equal_by_coordinates"])
                self.assertEqual(r["metrics"]["false_metric_certifications"],0)

    def test_scalene_bisector_is_not_automatically_a_median(self):
        for c in CONDITIONS:
            r=simulate(c,"scalene",seed=5)
            self.assertFalse(r["geometry"]["observations"]["base_halves_equal_by_coordinates"])
            for q in r["analogical_questions"]:
                self.assertEqual(q["epistemic_status"],"HYPOTHESIS_ONLY")
                self.assertFalse(q["proven"])
                self.assertEqual(q["target"]["relation"],"equal?")
            for event in r["timeline"]:
                self.assertEqual(event.get("certified_metric_equalities",[]),[])

    def test_experiment_bookkeeping(self):
        d=experiment(range(2),budget=4)
        self.assertEqual(len(d["runs"]),len(CONDITIONS)*len(MODES)*len(ATTENTION)*2)
        self.assertTrue(d["no_proof"] and d["no_jev"])
        for a in ATTENTION:
            for m in MODES:
                for c in CONDITIONS:
                    v=d["aggregates"][a][m][c]
                    self.assertEqual(v["trials"],2)
                    self.assertEqual(v["false_metric_certifications"],0)
        self.assertEqual(d["aggregates"]["clean"]["ordinary_cevian"]["productivity_feedback"]["question_rate"],0)

if __name__=="__main__":
    unittest.main()
