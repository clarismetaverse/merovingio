import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import benchmark_color as b

class ColorBindingTests(unittest.TestCase):
 def test_same_geometry_and_both_historical_contracts(self):
  for i,method in enumerate(b.prior.METHODS):
   objects=b.prior.objects_for(method,False);cert=b.native.prior.certificate(objects)
   self.assertEqual(len(cert['generic_space_bindings']),2);self.assertEqual(b.prior.prior.reference(objects)[0],i==0)

 def test_monochrome_is_exact_prior_request_and_frozen_png_bytes(self):
  with tempfile.TemporaryDirectory() as t:
   p,_,assets=b.build_payload(Path(t),'monochrome');self.assertEqual(b.base.digest(p),b.OLD['request_sha256'])
   self.assertEqual({k:v for k,v in p.items() if k!='assets'},b.OLD['model_input'])
   for asset in assets:
    old=next(a for a in b.OLD['asset_audit'] if a['asset']==asset['asset']);self.assertEqual(asset['sha256'],old['sha256'])

 def test_color_and_legend_change_only_the_declared_fields(self):
  with tempfile.TemporaryDirectory() as t:
   values={a:b.build_payload(Path(t),a)[0] for a in b.ARMS}
   mono,color,legend=(values[a] for a in b.ARMS)
   self.assertEqual({k:v for k,v in mono.items() if k!='assets'},{k:v for k,v in color.items() if k!='assets'})
   self.assertEqual(color['assets'],legend['assets'])
   self.assertEqual(legend['state'].pop('visual_object_key'),b.visual_key());self.assertEqual(color,legend)

 def test_color_preserves_every_ink_location_and_renderer_style(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);_,_,monos=b.build_payload(out,'monochrome');_,_,colors=b.build_payload(out,'color')
   for i,(mono,color) in enumerate(zip(monos,colors)):
    method=b.prior.METHODS[i] if i<2 else b.prior.METHODS[0];path=out/'render_mono.png'
    b.render(b.prior.objects_for(method,False),b.OLD['point_labels'],path,bridge=i<2,colored=False)
    with Image.open(path) as rendered,Image.open(out/mono['file']) as archived,Image.open(out/color['file']) as colored:
     self.assertEqual(rendered.tobytes(),archived.tobytes())
     self.assertEqual(archived.size,colored.size);self.assertEqual(colored.mode,'RGB');self.assertFalse(colored.info)
     # Color changes values, never support/geometry. Text ink and shape dimensions stay fixed.
     oldpx=archived.load();newpx=colored.load();changed=0
     for y in range(320):
      for x in range(320):
       self.assertEqual(oldpx[x,y]!=(255,255,255),newpx[x,y]!=(255,255,255));changed+=oldpx[x,y]!=newpx[x,y]
     self.assertGreater(changed,100)

 def test_palette_is_independent_of_reference_and_same_for_both_contacts(self):
  self.assertEqual(b.point_color('F'),b.point_color('G'))
  with patch.object(b.prior.prior,'reference',side_effect=AssertionError('gold consulted')):
   key=b.visual_key()
   with tempfile.TemporaryDirectory() as t:
    for method in b.prior.METHODS:b.render(b.prior.objects_for(method,False),b.OLD['point_labels'],Path(t)/(method+'.png'))
  self.assertEqual({r['hex'] for r in key['new_carrier_colors']},{b.BRIDGE_COLOR['hex']})
  self.assertEqual(len(key['original_side_colors']),3);self.assertEqual(len(key['point_colors']),5)
  self.assertNotIn('region_ref',json.dumps(key));self.assertNotIn('covered_fraction',json.dumps(key))

 def test_legend_references_existing_objects_uniformly_without_new_geometry(self):
  state=b.OLD['model_input']['state'];key=b.visual_key()
  for row in key['original_side_colors']:self.assertEqual(set(row['endpoints']),set(state['mental_spaces'][row['mental_space_ref']]['endpoints']))
  self.assertEqual({r['point_ref'] for r in key['point_colors']},{b.OLD['point_labels'][v] for v in 'ABCFG'})
  for row in key['new_carrier_colors']:self.assertEqual(row['material_ref'],state['admissible_bridges'][row['candidate_ref']]['verified_certificate']['new_carrier']['material_id'])

 def test_budget_order_and_question_are_unchanged(self):
  count=0
  with tempfile.TemporaryDirectory() as t:
   for arm in b.ARMS:
    p,m,assets=b.build_payload(Path(t),arm);count+=len(p['questions'])
    self.assertEqual(p['questions'],b.OLD['model_input']['questions']);self.assertEqual(list(p['questions']),['Q001','Q003']);self.assertEqual(list(m['candidate_mapping']),['C914','C850']);self.assertEqual(len(assets),3)
    self.assertEqual(p['state']['active_objective']['description'],b.native.EXPLICIT)
   self.assertEqual(count,6)

 def test_no_gold_coverage_historical_probabilities_or_condition_in_input(self):
  forbidden={'reference','gold','correct','arm','replica','condition','candidate_mapping','historical_context','p_yes_by_method','observer_material_certificates','coverage','covered_fraction','covered_intervals','certified_original_side_coverage','weights','composite','expected_answer'}
  def walk(v):
   if isinstance(v,dict):
    self.assertFalse(set(v)&forbidden)
    for x in v.values():walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  with tempfile.TemporaryDirectory() as t:
   for arm in b.ARMS:walk(b.build_payload(Path(t),arm)[0])

 def test_matched_contrasts_are_probability_differences_not_composites(self):
  calls=[]
  with tempfile.TemporaryDirectory() as t:
   for arm,probs in zip(b.ARMS,[(.7,.6),(.8,.4),(.9,.3)]):
    _,m,_=b.build_payload(Path(t),arm);m['response']={'answers':dict(zip(('Q001','Q003'),[{'noul':p} for p in probs])),'usage':{}};calls.append(m)
  result=b.analyze(calls);self.assertEqual(result['arms']['monochrome']['summary']['correct'],1);self.assertEqual(result['arms']['color']['summary']['correct'],2)
  self.assertAlmostEqual(result['descriptive_contrasts']['monochrome_to_color']['margin'],.3)

 def test_guard_and_failure_never_retry(self):
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{},clear=True),patch.object(b.native,'transport') as transport:
   with self.assertRaises(SystemExit):b.main(Path(t),True)
   transport.assert_not_called()
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{'GITHUB_ACTIONS':'true','TYPESAFE_API_KEY':'test-only'},clear=True),patch.object(b.native,'transport',return_value={'failure':'HTTP_403'}) as transport:
   with self.assertRaises(SystemExit):b.main(Path(t),True)
   self.assertEqual(transport.call_count,1);self.assertEqual(json.loads((Path(t)/'results.json').read_text())['status'],'request_rejected')

 def test_offline_and_partial_live_artifacts_reconstruct(self):
  from audit_color import audit
  with tempfile.TemporaryDirectory() as t:
   b.main(Path(t));result=audit(Path(t));self.assertEqual(result['native_noul_answers_verified'],0);self.assertEqual(result['requests_reconstructed'],3)
  def fixture(p):return {'response':b.native.sanitize({'model':'jev-1.14.0','answers':{q:{'type':'noul','noul':.25} for q in p['questions']}},p['questions']),'elapsed_seconds':0.}
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{'GITHUB_ACTIONS':'true','TYPESAFE_API_KEY':'test-only'},clear=True),patch.object(b.native,'transport',side_effect=fixture) as transport:
   b.main(Path(t),True);self.assertEqual(transport.call_count,3);result=audit(Path(t));self.assertEqual(result['native_noul_answers_verified'],6);self.assertEqual(result['material_contract_checks'],12)
  # Synthetic fixtures are temporary unit-test data and are never empirical artifacts.

if __name__=='__main__':unittest.main()
