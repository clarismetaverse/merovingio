import base64,json,math,tempfile,unittest
from pathlib import Path
from benchmark import *
class BenchmarkTests(unittest.TestCase):
 def test_geometry_and_final_pixel_identity(self):
  for a in (0,37):
   for r in (-1,1):
    A,B,C=points(a,r);lengths=[math.dist(A,B),math.dist(A,C),math.dist(B,C)]
    self.assertLess(max(lengths)-min(lengths),1e-8)
    self.assertEqual(render("circle",2,a,r).tobytes(),render("translation",2,a,r).tobytes())
    self.assertEqual(render("circle",0,a,r).tobytes(),render("translation",0,a,r).tobytes())
    self.assertNotEqual(render("circle",1,a,r).tobytes(),render("translation",1,a,r).tobytes())
 def test_nonleakage_and_pair_control(self):
  with tempfile.TemporaryDirectory() as td:
   out=Path(td)
   for condition in CONDITIONS:
    for seed in range(6):
     p,m=payload(out,"circle",condition,37,-1,seed)
     q,n=payload(out,"translation",condition,37,-1,seed)
     text=json.dumps({k:v for k,v in p.items() if k!="assets"})
     for forbidden in ("correct","offline_mapping","workspace_","GEN_EQ_","offline_history", "sha256"):
      self.assertNotIn(forbidden,text)
     self.assertEqual(len(p["questions"]),1)
     self.assertEqual(p["questions"]["origin"]["type"],"choice")
     self.assertIn("none",p["questions"]["origin"]["criteria"])
     # Only criteria define the opaque option IDs, no suggested answer elsewhere.
     no_options=json.dumps({k:v for k,v in p.items() if k!="questions"})+p["questions"]["origin"]["instructions"]
     for code in m:self.assertNotIn(code,no_options)
     if condition=="final_only":self.assertEqual(p,q)
 def test_offline_has_no_accuracy(self):
  rows=[{"condition":"sequence","history":"circle","predicted":"not_run","correct":None}]
  self.assertIsNone(summarize(rows)["sequence"]["genealogy_accuracy"])
 def test_sanitize_removes_free_text(self):
  result=sanitize({"secret":"sensitive","answers":{"origin":{"choice":"none","confidence":.5,"reliability":"sensitive","rationale":"sensitive"}},"usage":{"input_tokens":10,"secret":"sensitive"}})
  self.assertNotIn("sensitive",json.dumps(result))
  self.assertEqual(result["usage"],{"input_tokens":10})
 def test_sources(self):
  ps=provenance();ids={n["id"] for s in ps for n in s["nodes"]}
  self.assertTrue({"GEN_EQ_CIRCLE","GEN_EQ_TRANSLATION","M_RADIUS_PACKET","M_TRANSLATION_PACKET"}<=ids)
 def test_unidentifiable_not_scored(self):
  rows=[{"condition":"final_only","history":"circle","predicted":"circle","correct":None}]
  s=summarize(rows)["final_only"]
  self.assertIsNone(s["genealogy_accuracy"])
if __name__=="__main__":unittest.main()
