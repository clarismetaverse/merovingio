"""Merovingio v8: prospective frames before bisector, grounded constructions after."""
import math
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from prospective import (
    triangle_workspace,division_goal,role_oppositions,prospective_blend,
    candidate_constructions,polygon_faces_after_split,construct,
    bind_prospective,postconstruction_reading,simulate,experiment,
    SHAPES,GOALS,CONDITIONS,MEMORY
)

class ProspectiveBlendTests(unittest.TestCase):
    def test_no_construction_or_subtriangle_appears_before_elaboration(self):
        for shape in SHAPES:
            ws=triangle_workspace(shape)
            self.assertEqual(len(ws["points"]),3)
            self.assertEqual(len(ws["faces"]),1)
            self.assertEqual(len(ws["edges"]),3)
            self.assertEqual(ws["given_angular_equalities"],[])
            self.assertEqual(ws["certified_segment_equalities"],[])
            self.assertNotIn("D",ws["points"])
            self.assertNotIn("TWO_TRIANGLES",MEMORY)
            self.assertEqual(set(MEMORY),{"TRIANGLE","DIVISION"})
            for goal in GOALS:
                b=prospective_blend(ws,division_goal(ws,goal))
                self.assertIsNotNone(b)
                self.assertEqual(b["source_opposition"]["angle_vertex"],goal)
                self.assertEqual(b["blended_space"]["triangular_face_slots"],2)
                self.assertEqual(len(b["blended_space"]["correspondence_pairs"]),2)
                self.assertIn("X:unbound",str(b["blended_space"]))
                self.assertEqual(len(ws["faces"]),1)
                self.assertEqual(len(ws["points"]),3)

    def test_n_gon_splitting_is_general_not_a_hardcoded_two_triangles_template(self):
        for pivot,edge in (("A",("B","C")),("B",("A","C")),("C",("A","B"))):
            f=polygon_faces_after_split(["A","B","C"],pivot,edge,"Q")
            self.assertEqual(len(f),2)
            self.assertEqual([len(x) for x in f],[3,3])
            self.assertTrue(all(pivot in x and "Q" in x for x in f))
        # Same rule generates a triangle + quadrilateral when the parent has 4 corners.
        quad=polygon_faces_after_split(["P","Q","R","S"],"P",("Q","R"),"X")
        self.assertEqual(sorted(len(x) for x in quad),[3,4])

    def test_realized_roles_match_prospective_slots_for_every_shape_and_pivot(self):
        for shape in SHAPES:
            for vertex in GOALS:
                before=triangle_workspace(shape)
                b=prospective_blend(before,division_goal(before,vertex))
                op=next(o for o in candidate_constructions(before) if
                        o["origin_vertex"]==vertex)
                after=construct(before,op)
                self.assertEqual(len(before["points"]),3)
                self.assertEqual(len(after["points"]),4)
                self.assertEqual(len(after["faces"]),2)
                self.assertEqual([len(f) for f in after["faces"]],[3,3])
                bound=bind_prospective(b,before,after,division_goal(before,vertex))
                self.assertTrue(bound["matched"],(shape,vertex,bound))
                self.assertEqual(len(bound["bindings"]),2)
                self.assertEqual(bound["certified_segment_equalities"],[])
                self.assertEqual(after["certified_segment_equalities"],[])
                self.assertTrue(postconstruction_reading(after,division_goal(before,vertex))
                                ["goal_vertex_bisected"])
                self.assertEqual(len(after["given_angular_equalities"]),1)

    def test_relabeling_does_not_change_role_generation(self):
        # Renamed material geometry: no literal C, AB, AD, DB is needed.
        old=triangle_workspace("scalene")
        ren={"A":"J","B":"K","C":"L"}
        ws={
          **old,
          "points":{ren[k]:v for k,v in old["points"].items()},
          "faces":[[ren[x] for x in f] for f in old["faces"]],
          "edges":[tuple(sorted(ren[x] for x in e)) for e in old["edges"]],
          "angles":[{"vertex":ren[a["vertex"]],
                     "arms":sorted(ren[x] for x in a["arms"])} for a in old["angles"]],
        }
        goal=division_goal(ws,"L")
        b=prospective_blend(ws,goal)
        self.assertEqual(b["source_opposition"]["opposite_edge"],["J","K"])
        op=next(x for x in candidate_constructions(ws) if x["origin_vertex"]=="L")
        after=construct(ws,op)
        self.assertTrue(bind_prospective(b,ws,after,goal)["matched"])

    def test_no_opposition_or_no_transport_cannot_anticipate(self):
        ws=triangle_workspace("equilateral")
        goal=division_goal(ws,"C")
        self.assertEqual(role_oppositions(ws,False),[])
        self.assertIsNone(prospective_blend(ws,goal,opp_memory=False))
        self.assertIsNone(prospective_blend(ws,goal,transport=False))
        for condition in ("no_opposition","no_transport","post_construct_only","goal_only"):
            sim=simulate(condition,"equilateral","C",seed=3)
            self.assertFalse(sim["metrics"]["prospective_blend_before_construction"])
            self.assertFalse(sim["metrics"]["prospective_roles_bound"])
            # The general geometric construction grammar is still available.
            self.assertEqual(len(sim["construction_candidates"]),3)

    def test_wrong_vertex_bisection_does_not_fulfill_target(self):
        before=triangle_workspace("scalene")
        goal=division_goal(before,"C")
        b=prospective_blend(before,goal)
        other=next(c for c in candidate_constructions(before)
                   if c["origin_vertex"]=="A")
        after=construct(before,other)
        self.assertFalse(bind_prospective(b,before,after,goal)["matched"])
        self.assertFalse(postconstruction_reading(after,goal)["goal_vertex_bisected"])

    def test_scalene_bisector_not_segment_bisector(self):
        ws=triangle_workspace("scalene")
        op=next(x for x in candidate_constructions(ws) if x["origin_vertex"]=="C")
        after=construct(ws,op)
        self.assertFalse(after["observations"]["split_base_parts_equal_by_coordinates"])
        self.assertEqual(after["certified_segment_equalities"],[])
        self.assertEqual(after["given_angular_equalities"][0]["status"],"CONSTRUCTION_GIVEN")

    def test_same_operators_all_conditions_and_reproducible(self):
        for shape in SHAPES:
            for vertex in GOALS:
                rr=[simulate(c,shape,vertex,seed=3) for c in CONDITIONS]
                for x in rr:
                    self.assertEqual(x["preconstruction_material"],rr[0]["preconstruction_material"])
                    self.assertEqual(x["construction_candidates"],rr[0]["construction_candidates"])
                    self.assertEqual(x["metrics"]["false_segment_equalities"],0)
                    self.assertEqual(x["metrics"]["preconstruction_false_subtriangles"],0)
                self.assertEqual(simulate("full_blend",shape,vertex,seed=4),
                                 simulate("full_blend",shape,vertex,seed=4))

    def test_aggregate_all_shapes_vertices_and_ablations(self):
        e=experiment(range(3))
        self.assertEqual(len(e["runs"]),len(SHAPES)*len(GOALS)*len(CONDITIONS)*3)
        self.assertTrue(e["no_proof"] and e["no_jev"])
        for shape in SHAPES:
            for goal in GOALS:
                for condition in CONDITIONS:
                    x=e["aggregates"][shape][goal][condition]
                    self.assertEqual(x["n"],3)
                    self.assertEqual(x["false_metric_assertions"],0)
                    self.assertEqual(x["false_pre_material_subtriangles"],0)
                    self.assertEqual(x["prospective_rate"],
                                     1 if condition=="full_blend" else 0)
if __name__=="__main__":unittest.main()
