import base64,copy,io,json,math,os,tempfile,unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from benchmark_order import *

class OrderAblationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name)
  self.trial=next(t for t in manifest() if t["condition"]=="ordered")
 def tearDown(self):self.tmp.cleanup()
 def make(self,condition,history=None):
  return build_payload(self.out,dict(self.trial,condition=condition,history=history or self.trial["history"]))
 def test_balanced_manifest_and_unseen_transforms(self):
  ts=manifest();self.assertEqual(len(ts),192)
  self.assertEqual(Counter(t["condition"] for t in ts),Counter({c:32 for c in CONDITIONS}))
  self.assertEqual(manifest(),ts)
  self.assertTrue(all(tuple(t["permutation"])!=(0,1,2) for t in ts))
  for c in CONDITIONS:
   for h in ("circle","translation"):
    self.assertEqual(sum(t["condition"]==c and t["history"]==h for t in ts),16)
 def test_pixel_geometry_all_transforms(self):
  for angle,reflection in TRANSFORMS:
   A,B,C=pilot.points(angle,reflection)
   self.assertLess(max(math.dist(A,B),math.dist(A,C),math.dist(B,C))-min(math.dist(A,B),math.dist(A,C),math.dist(B,C)),1e-8)
   for f in (0,2):self.assertEqual(pilot.render("circle",f,angle,reflection).tobytes(),pilot.render("translation",f,angle,reflection).tobytes())
 def test_shuffle_same_image_multiset_neutral_keys(self):
  ordered,_,_=self.make("ordered");shuffled,_,audit=self.make("shuffled")
  self.assertEqual(ordered["state"],shuffled["state"])
  self.assertEqual(ordered["questions"],shuffled["questions"])
  images=lambda p:[a["data_base64"] for a in p["assets"].values()]
  self.assertCountEqual(images(ordered),images(shuffled));self.assertNotEqual(images(ordered),images(shuffled))
  self.assertEqual(list(shuffled["assets"]),["view1","view2","view3"])
  self.assertNotIn("frame",json.dumps({k:v for k,v in shuffled.items() if k!="assets"}))
  self.assertNotEqual([a["original_frame"] for a in audit],[0,1,2])
 def test_middle_is_exact_same_diagnostic_image(self):
  p,_,_=self.make("ordered");q,_,_=self.make("middle_only")
  self.assertEqual(p["assets"]["view2"],q["assets"]["view1"])
  self.assertEqual(p["questions"],q["questions"])
 def test_final_control_pair_requests_identical(self):
  p,_,_=self.make("final_only","circle");q,_,_=self.make("final_only","translation")
  self.assertEqual(p,q)
 def test_text_only_has_no_images_and_identical_structures(self):
  p,_,_=self.make("ordered_spaces");q,_,_=self.make("spaces_only")
  self.assertNotIn("assets",q);self.assertEqual(q["state"]["views"],[])
  self.assertEqual(p["state"]["structural_observations"],q["state"]["structural_observations"])
  self.assertEqual(p["questions"],q["questions"])
 def test_no_answer_keys_or_original_indices_in_model_input(self):
  for c in CONDITIONS:
   p,m,_=self.make(c)
   text=json.dumps({k:v for k,v in p.items() if k!="assets"})
   for forbidden in ("original_frame","permutation","option_seed","offline_mapping","correct","workspace_","GEN_EQ_"):
    self.assertNotIn(forbidden,text)
   self.assertEqual(len(p["questions"]),1);self.assertEqual(p["questions"]["origin"]["type"],"choice")
   outside=json.dumps(p["state"])+p["questions"]["origin"]["instructions"]
   for code in m:self.assertNotIn(code,outside)
   for asset in p.get("assets",{}).values():self.assertFalse(Image.open(io.BytesIO(base64.b64decode(asset["data_base64"]))).info)
 def test_live_guard_before_network_and_output(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):main(self.out/"no_output",True)
   with self.assertRaises(RuntimeError):transport({})
  self.assertFalse((self.out/"no_output").exists())
 def test_offline_null_and_failure_denominators(self):
  r=dict(self.trial,predicted="not_run",correct=None)
  s=summarize([r])["ordered"];self.assertEqual(s["attempted_n"],0);self.assertIsNone(s["origin_accuracy"])
  rows=[dict(r,predicted=r["history"],correct=True),dict(r,predicted="failure",correct=False)]
  self.assertEqual(summarize(rows)["ordered"]["origin_accuracy"],.5)
  self.assertIsNone(summarize([dict(r,condition="final_only",predicted="circle")])["final_only"]["origin_accuracy"])
 def test_paired_contrasts_and_repeat_agreement(self):
  rows=[dict(self.trial,condition=c,predicted=self.trial["history"] if c=="ordered" else "none",correct=c=="ordered") for c in ("ordered","shuffled")]
  s=comparisons(rows)["ordered_vs_shuffled"]
  self.assertEqual(s["paired_n"],1);self.assertEqual(s["left_only_correct"],1)

if __name__=="__main__":unittest.main()
