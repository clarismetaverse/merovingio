"""Prospective binding v1.0 unit tests: source provenance, geometry, prompt hygiene."""
import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import prospective_memory_v10 as oracle
import prospective_binding_v10 as runner

class TestMemoryDrivenBinding(unittest.TestCase):
 def test_historical_sources_are_really_in_repo(self):
  for case in ("triangle","circle","negative"):
   item=oracle.read_memory(case)
   path=oracle.ROOT/item["provenance"]["file"]
   self.assertTrue(path.is_file(),str(path))
   if item["provenance"]["workspace_id"]:
    source=json.loads(path.read_text(encoding="utf-8"))
    self.assertEqual(item["provenance"]["workspace_id"],source["workspace"]["id"])
    ids={n["id"] for n in source["nodes"]}
    self.assertTrue(set(item["provenance"]["node_ids"])<=ids)

 def test_independent_geometry_check(self):
  for shape in oracle.TRIANGLE_SHAPES:
   self.assertTrue(oracle.geometric_oracle("triangle",shape,"from_C")["completed"])
   for method in ("from_A","from_B","edge_link"):
    self.assertFalse(oracle.geometric_oracle("triangle",shape,method)["completed"])
  self.assertTrue(oracle.geometric_oracle("circle","standard","circle_opposite_same_radius")["completed"])
  for method in oracle.CIRCLE_METHODS[1:]:
   self.assertFalse(oracle.geometric_oracle("circle","standard",method)["completed"])
  for method in oracle.TRIANGLE_METHODS:
   self.assertFalse(oracle.geometric_oracle("negative","left",method)["completed"])

 def test_candidate_position_counterbalanced(self):
  for case in ("triangle","circle"):
   options=oracle.propose(case)
   winners=[]
   for shift in range(4):
    order=runner.option_mapping(case,shift)
    expected="from_C" if case=="triangle" else "circle_opposite_same_radius"
    winners.append(next(k for k,m in order.items() if m==expected))
    self.assertEqual(set(order.values()),set(options))
   self.assertCountEqual(winners,["K1","K2","K3","K4"])

 def test_all_roles_have_before_and_after_status(self):
  a=oracle.verifier_after_choice("triangle","left","from_C")
  self.assertTrue(a["successful_completion"])
  self.assertTrue(all(x=="missing" for x in a["before"].values()))
  self.assertTrue(all(x=="verified_structural" for x in a["after"].values()))
  b=oracle.verifier_after_choice("circle","standard","circle_opposite_short_radius")
  self.assertFalse(b["successful_completion"])
  self.assertEqual(b["after"]["common_intersection_C"],"verified_structural")
  self.assertEqual(b["after"]["second_circle_with_same_radius_reference"],"missing")

 def test_payload_ids_no_oracle_or_operation_labels(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)
   for case,shape in (("triangle","left"),("circle","standard"),("negative","left")):
    for mode in runner.MODES:
     payload,mapping=runner.build_payload(root,case,shape,0,mode)
     visible=json.dumps({k:v for k,v in payload.items() if k!="assets"}).lower()
     for forbidden in (
       "from_c","from_a","from_b","edge_link",
       "circle_opposite_same_radius","circle_opposite_short_radius",
       "circle_same_center","midpoint_line",
       "oracle_score","correct_candidate","completed\": true",
       "congruence_proven","i.10", "jev_prediction"
     ):
      self.assertNotIn(forbidden,visible,forbidden)
     self.assertEqual(len(payload["assets"]),5)
     self.assertEqual(set(mapping),{"K1","K2","K3","K4"})
     self.assertEqual("retrieved_generic_space" in payload["state"],mode=="historical_memory")
     self.assertEqual("none" in payload["questions"]["best_bridge"]["criteria"],case=="negative")
     self.assertEqual(payload["questions"]["best_bridge"]["type"],"choice")

 def test_negative_condition_has_no_possible_completion(self):
  for method in oracle.propose("negative"):
   self.assertEqual(oracle.rank_candidates_heuristic("negative","right")[method],0)
  self.assertFalse(oracle.verifier_after_choice("negative","right",None)["successful_completion"])

if __name__=="__main__":unittest.main()
