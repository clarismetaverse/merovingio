import base64,copy,io,json,math,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from benchmark_scores import *

class NativeScoreTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def test_native_fanout_and_probe(self):
  p,m,meta,audit,probe=build_payload(self.out,"left",0)
  self.assertEqual(len(p["questions"]),100);self.assertEqual(len(probe),8)
  self.assertTrue(all(q["type"]=="score" and len(q["criteria"])==4 for q in p["questions"].values()))
  self.assertEqual(sum(v["stage"]=="bridge" for v in meta.values()),40)
  self.assertEqual(sum(v["stage"]=="generic" for v in meta.values()),60)
  self.assertEqual(len({v["schema"] for v in meta.values() if v["stage"]=="generic"}),12)
  self.assertEqual({v["axis"] for v in meta.values() if v["stage"]=="generic"},{"compatibility"})
  self.assertEqual(len(p["assets"]),5)
 def test_independent_split_geometry(self):
  for shape in geometry.SHAPES:
   for method in METHODS:
    g=proposal(shape,method)
    if method=="no_op":self.assertEqual(g["regions"],[]);continue
    a,b=g["regions"];self.assertEqual(set(a)&set(b),set(g["new_segment"]))
    self.assertAlmostEqual(area(a,g["points"])+area(b,g["points"]),area(list("ABC"),g["points"]))
    self.assertEqual(sorted([len(a),len(b)]),[3,4] if method=="edge_link" else [3,3])
 def test_reference_profiles_change_optimum(self):
  for shape in geometry.SHAPES:
   scores={m:{k:v/3 for k,v in bridge_oracle(shape,m).items()} for m in METHODS}
   for profile,weights in PROFILES.items():
    values={m:weighted(s,weights) for m,s in scores.items()}
    expected="from_C" if profile=="focus_C" else "from_A"
    self.assertEqual(max(values,key=values.get),expected)
    self.assertAlmostEqual(values[expected],1)
 def test_generic_gates_and_new_interface(self):
  self.assertEqual(len(MEMORY["entries"]),10);self.assertEqual(len(schemas()),12)
  for shape in geometry.SHAPES:
   self.assertTrue(binding_check(shape,"edge_link","NEW_SHARED_INTERFACE")["instantiated"])
   self.assertFalse(binding_check(shape,"edge_link","GS_HIST_DOUBLE_TRIANGLE")["instantiated"])
   for method in METHODS:
    for schema in ("GS_PROP_I_5","GS_PROP_I_6","GS_PROP_I_7","GS_PROP_I_18","GS_PROP_I_19","GS_HIST_RADIUS_TRIANGLE","NEW_CONGRUENT_PAIR"):
     self.assertFalse(binding_check(shape,method,schema)["instantiated"])
    if method=="no_op":self.assertTrue(all(not binding_check(shape,method,s)["instantiated"] for s,_,_ in schemas()))
 def test_score_sanitization_and_normalization(self):
  questions={"q":{"criteria":["a","b","c","d"]}}
  raw={"answers":{"q":{"score":2.4,"confidence":.7,"probabilities":{"0":0,"1":0,"2":.6,"3":.4},"secret":"sensitive"}},"usage":{"input_tokens":10,"secret":"sensitive"}}
  s=sanitize(raw,questions)
  self.assertAlmostEqual(s["answers"]["q"]["normalized_score"],.8)
  self.assertNotIn("sensitive",json.dumps(s))
  raw["answers"]["q"]["score"]=float("nan")
  with self.assertRaises(ValueError):sanitize(raw,questions)
 def test_no_oracle_labels_source_ids_or_method_names_in_payload(self):
  p,m,meta,audit,probe=build_payload(self.out,"right",1)
  text=json.dumps({k:v for k,v in p.items() if k!="assets"})
  for forbidden in ("from_C","from_A","from_B","edge_link","no_op","oracle","reference_method","accepted_binding","GS_PROP_I_5","NEW_SHARED_INTERFACE","memory_provenance","correct"):
   self.assertNotIn(forbidden,text)
  for a in p["assets"].values():self.assertFalse(Image.open(io.BytesIO(base64.b64decode(a["data_base64"]))).info)
  self.assertEqual(p["state"]["hypothetical_candidates"][0]["id"] in m,True)
 def test_model_score_cannot_override_independent_gate(self):
  p,m,meta,audit,probe=build_payload(self.out,"left",0)
  response={"answers":{q:{"normalized_score":1} for q in meta}}
  r={"shape":"left","repeat":0,"kind":"full","candidate_mapping":m,"question_metadata":meta,"response":response}
  a=analyze([r]);self.assertGreater(a["counts"]["unsupported_bindings_above_model_threshold"],0)
  self.assertTrue(all(g["independent_binding_check"]["instantiated"] for g in a["generic_space_bindings"] if g["accepted_binding"]))
  self.assertTrue(all(g["selected_method"] is None for g in a["bridge_rankings"]))
 def test_probe_and_full_context_identical(self):
  p,m,meta,audit,probe=build_payload(self.out,"left",0);q=copy.deepcopy(p)
  q["questions"]={k:v for k,v in q["questions"].items() if k in probe}
  self.assertEqual(p["state"],q["state"]);self.assertEqual(p["assets"],q["assets"])
  for key in q["questions"]:self.assertEqual(p["questions"][key],q["questions"][key])
 def test_no_fake_offline_scores(self):
  a=analyze([]);self.assertEqual(a["bridge_rankings"],[]);self.assertEqual(a["counts"]["native_score_answers"],0)
 def test_actions_guard(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):main(self.out/"blocked",True)
   with self.assertRaises(RuntimeError):transport({})
  self.assertFalse((self.out/"blocked").exists())

if __name__=="__main__":unittest.main()
