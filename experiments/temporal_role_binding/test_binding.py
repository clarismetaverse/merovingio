import base64,copy,io,json,os,tempfile,unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from PIL import Image,ImageDraw
from benchmark_binding import *

class TemporalBindingTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name)
  self.trial=manifest()[0]
 def tearDown(self):self.tmp.cleanup()
 def build(self,condition,history):return build_payload(self.out,dict(self.trial,condition=condition,history=history))
 def test_observer_role_state_machine(self):
  for history in ("circle","vector"):
   trace=role_trace(timeline(history))
   self.assertIsNone(trace[0]["initial_support"])
   self.assertEqual(trace[1]["initial_support"],history)
   self.assertEqual(trace[-1]["initial_support"],history)
   self.assertEqual(len(trace[-1]["secondary_supports"]),1)
   self.assertNotEqual(trace[-1]["secondary_supports"][0],history)
   self.assertTrue(trace[-1]["triangle_selected"])
  with self.assertRaises(ValueError):role_trace(("circle","circle"))
 def test_balanced_fixed_manifest(self):
  ts=manifest();self.assertEqual(len(ts),224);self.assertEqual(ts,manifest())
  self.assertEqual(Counter(t["condition"] for t in ts),Counter({c:32 for c in CONDITIONS}))
  for c in CONDITIONS:
   self.assertEqual(sum(t["condition"]==c and t["history"]=="circle" for t in ts),16)
 def test_ordered_pair_exact_same_frames_different_order(self):
  for angle,reflection in TRANSFORMS:
   a=build_payload(self.out,dict(self.trial,condition="ordered_images",history="circle",angle=angle,reflection=reflection))[0]
   b=build_payload(self.out,dict(self.trial,condition="ordered_images",history="vector",angle=angle,reflection=reflection))[0]
   aa=[v["data_base64"] for v in a["assets"].values()];bb=[v["data_base64"] for v in b["assets"].values()]
   self.assertEqual(a["state"],b["state"]);self.assertEqual(a["questions"],b["questions"])
   self.assertCountEqual(aa,bb);self.assertNotEqual(aa,bb)
   self.assertEqual(aa[0],bb[0]);self.assertEqual(aa[-1],bb[-1]);self.assertEqual(aa[1],bb[2]);self.assertEqual(aa[2],bb[1])
 def test_nonidentifiable_controls_exact_pair_requests(self):
  for c in set(CONDITIONS)-IDENTIFIABLE:
   a=self.build(c,"circle")[0];b=self.build(c,"vector")[0]
   self.assertEqual(a,b)
 def test_reverse_direction_requires_last_presented_activation(self):
  for h in ("circle","vector"):
   ordered=self.build("ordered_images",h)[0];reverse=self.build("reverse_images",h)[0]
   data=lambda p:[a["data_base64"] for a in p["assets"].values()]
   self.assertEqual(data(ordered),list(reversed(data(reverse))))
   self.assertEqual(reverse["state"]["ordering_convention"],"latest to earliest")
   _,_,audit=self.build("reverse_images",h)
   active=[a["event"] for a in audit if a["event"] in ("circle","vector")]
   self.assertEqual(active[-1],h);self.assertNotEqual(active[0],h)
 def test_structural_observation_multiset_and_text_only(self):
  a=structures("circle");b=structures("vector")
  self.assertCountEqual([json.dumps(x,sort_keys=True) for x in a],[json.dumps(x,sort_keys=True) for x in b])
  self.assertEqual(a[1],b[2]);self.assertEqual(a[2],b[1])
  for h in ("circle","vector"):
   p=self.build("spaces_only",h)[0];q=self.build("ordered_spaces",h)[0]
   self.assertNotIn("assets",p);self.assertEqual(p["state"]["structural_observations"],q["state"]["structural_observations"])
   self.assertEqual(p["questions"],q["questions"])
 def test_no_model_visible_history_or_time_index_leakage(self):
  for c in CONDITIONS:
   p,m,a=self.build(c,"circle");text=json.dumps({k:v for k,v in p.items() if k!="assets"})
   for forbidden in ("option_seed","history","original_frame","offline_mapping","source_commit","correct","GEN_EQ_","first_support_is"):
    self.assertNotIn(forbidden,text)
   self.assertEqual(len(p["questions"]),1);self.assertEqual(p["questions"]["origin"]["type"],"choice")
   self.assertIn("none",p["questions"]["origin"]["criteria"])
   outside=json.dumps(p["state"])+p["questions"]["origin"]["instructions"]
   for k in m:self.assertNotIn(k,outside)
   for i,(key,img) in enumerate(p.get("assets",{}).items(),1):
    self.assertEqual(key,f"view{i}");self.assertFalse(Image.open(io.BytesIO(base64.b64decode(img["data_base64"]))).info)
 def test_no_image_text_and_unchanged_geometry(self):
  with patch.object(ImageDraw.ImageDraw,"text",side_effect=AssertionError("Image text prohibited")):
   for e in EVENTS:render(e,37,-1)
  for angle,reflection in TRANSFORMS:
   self.assertEqual(len({render(e,angle,reflection).size for e in EVENTS}),1)
   A,B,C=pilot.points(angle,reflection)
   self.assertLess(abs(math.dist(A,B)-math.dist(B,C)),1e-8)
 def test_guard_before_any_output_or_http(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):main(self.out/"blocked",True)
   with self.assertRaises(RuntimeError):previous.transport({})
  self.assertFalse((self.out/"blocked").exists())
 def test_control_null_and_failure_denominator(self):
  base=dict(self.trial,history="circle",predicted="circle",correct=True)
  for c in set(CONDITIONS)-IDENTIFIABLE:self.assertIsNone(summarize([dict(base,condition=c)])[c]["order_accuracy"])
  rows=[dict(base,condition="ordered_images"),dict(base,condition="ordered_images",predicted="failure",correct=False)]
  self.assertEqual(summarize(rows)["ordered_images"]["order_accuracy"],.5)
  self.assertIsNone(summarize([dict(base,condition="ordered_images",predicted="not_run",correct=None)])["ordered_images"]["order_accuracy"])
 def test_counterfactual_pair_metric_requires_both_correct(self):
  rows=[dict(self.trial,condition="ordered_images",history=h,predicted=h,correct=True) for h in ("circle","vector")]
  s=contrasts(rows)["ordered_images"];self.assertEqual(s["history_pairs"],1);self.assertEqual(s["both_correct"],1)
  rows[1].update(predicted="circle",correct=False)
  self.assertEqual(contrasts(rows)["ordered_images"]["both_correct"],0)

if __name__=="__main__":unittest.main()
