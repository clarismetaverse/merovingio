import base64,io,json,os,tempfile,unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from benchmark_direction import *

class DirectionAcrossModalitiesTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name);self.trial=manifest()[0]
 def tearDown(self):self.tmp.cleanup()
 def payload(self,condition,history="circle"):
  return build_payload(self.out,dict(self.trial,condition=condition,history=history))[0]
 def test_full_balanced_factorial(self):
  ts=manifest();self.assertEqual(len(ts),192);self.assertEqual(ts,manifest())
  self.assertEqual(Counter(t["condition"] for t in ts),Counter({c:32 for c in CONDITIONS}))
  self.assertTrue(all(t["condition"]==t["modality"]+"_"+t["direction"] for t in ts))
  for c in CONDITIONS:self.assertEqual(sum(t["condition"]==c and t["history"]=="circle" for t in ts),16)
 def test_parent_payloads_exactly_preserved(self):
  for c,alias in (("images_forward","ordered_images"),("images_reverse","reverse_images"),("text_forward","spaces_only"),("combined_forward","ordered_spaces")):
   for h in ("circle","vector"):
    t=dict(self.trial,condition=c,history=h)
    p=build_payload(self.out,t)[0];q=base.build_payload(self.out,dict(t,condition=alias))[0]
    self.assertEqual(p,q)
 def test_reverse_text_same_records_exact_reverse(self):
  for h in ("circle","vector"):
   a=self.payload("text_forward",h);b=self.payload("text_reverse",h)
   self.assertNotIn("assets",a);self.assertNotIn("assets",b)
   self.assertEqual(a["state"]["structural_observations"],list(reversed(b["state"]["structural_observations"])))
   self.assertEqual(a["questions"],b["questions"])
   self.assertEqual(b["state"]["ordering_convention"],"latest to earliest")
   aa={k:v for k,v in a["state"].items() if k not in ("ordering_convention","structural_observations")}
   bb={k:v for k,v in b["state"].items() if k not in ("ordering_convention","structural_observations")}
   self.assertEqual(aa,bb)
 def test_combined_reverse_aligns_images_and_structures(self):
  for h in ("circle","vector"):
   a=self.payload("combined_forward",h);b=self.payload("combined_reverse",h)
   images=lambda p:[x["data_base64"] for x in p["assets"].values()]
   self.assertEqual(images(a),list(reversed(images(b))))
   self.assertEqual(a["state"]["structural_observations"],list(reversed(b["state"]["structural_observations"])))
   self.assertEqual(b["state"]["ordering_convention"],"latest to earliest")
 def test_text_projection_identical_between_modalities(self):
  for direction in DIRECTIONS:
   a=self.payload("combined_"+direction);b=self.payload("text_"+direction)
   a.pop("assets");a["state"]["views"]=[]
   self.assertEqual(a,b)
   a=self.payload("combined_"+direction);b=self.payload("images_"+direction)
   a["state"].pop("structural_observations");self.assertEqual(a,b)
 def test_gold_invariant_under_text_direction(self):
  for h in ("circle","vector"):
   for direction in DIRECTIONS:
    p=self.payload("text_"+direction,h);observations=p["state"]["structural_observations"]
    chronological=observations if direction=="forward" else list(reversed(observations))
    activated=[o for o in chronological if o["active_carriers"]]
    relation=activated[0]["active_carriers"][0]["relation"]
    derived="circle" if "center to boundary" in relation else "vector"
    self.assertEqual(derived,h)
 def test_opposite_histories_same_text_multiset(self):
  for direction in DIRECTIONS:
   a=self.payload("text_"+direction,"circle");b=self.payload("text_"+direction,"vector")
   vals=lambda p:[json.dumps(v,sort_keys=True) for v in p["state"]["structural_observations"]]
   self.assertCountEqual(vals(a),vals(b));self.assertNotEqual(vals(a),vals(b))
 def test_no_answer_or_hidden_temporal_rank_leakage(self):
  for c in CONDITIONS:
   p,m,_=build_payload(self.out,dict(self.trial,condition=c))
   text=json.dumps({k:v for k,v in p.items() if k!="assets"})
   for forbidden in ("correct","offline_mapping","source_commit","history","option_seed","original_frame","temporal_rank","first_support_is"):
    self.assertNotIn(forbidden,text)
   self.assertEqual(len(p["questions"]),1);self.assertEqual(p["questions"]["origin"]["type"],"choice")
   outside=json.dumps(p["state"])+p["questions"]["origin"]["instructions"]
   for code in m:self.assertNotIn(code,outside)
   for i,(key,asset) in enumerate(p.get("assets",{}).items(),1):
    self.assertEqual(key,f"view{i}");self.assertFalse(Image.open(io.BytesIO(base64.b64decode(asset["data_base64"]))).info)
 def test_guard_before_any_live_request(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):main(self.out/"blocked",True)
   with self.assertRaises(RuntimeError):base.previous.transport({})
  self.assertFalse((self.out/"blocked").exists())
 def test_offline_null_and_failure_denominator(self):
  r=dict(self.trial,condition="text_reverse",predicted="not_run",correct=None)
  self.assertIsNone(summarize([r])["text_reverse"]["order_accuracy"])
  rows=[dict(r,predicted=r["history"],correct=True),dict(r,predicted="failure",correct=False)]
  self.assertEqual(summarize(rows)["text_reverse"]["order_accuracy"],.5)
 def test_opposite_and_abstention_errors_separated(self):
  r=dict(self.trial,condition="text_reverse",history="circle")
  rows=[dict(r,predicted="vector",correct=False),dict(r,predicted="none",correct=False)]
  s=summarize(rows)["text_reverse"];self.assertEqual(s["none_n"],1);self.assertEqual(s["opposite_order_n"],1)
 def test_paired_direction_contrast(self):
  rows=[dict(self.trial,condition="text_forward",predicted="circle",correct=True),dict(self.trial,condition="text_reverse",predicted="none",correct=False)]
  s=contrasts(rows)["text_forward_vs_reverse"];self.assertEqual(s["paired_n"],1);self.assertEqual(s["left_only_correct"],1)

if __name__=="__main__":unittest.main()
