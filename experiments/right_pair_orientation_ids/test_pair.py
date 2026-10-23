import copy,hashlib,json,math,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image,ImageDraw,ImageFont
import benchmark_pair as b

class PairFactorTests(unittest.TestCase):
 def test_same_two_bridges_and_references_at_both_orientations(self):
  for rotated in (False,True):
   for index,method in enumerate(b.METHODS):
    objects=b.objects_for(method,rotated);cert=b.native.prior.certificate(objects)
    self.assertEqual(len(cert['generic_space_bindings']),2);self.assertEqual(b.prior.reference(objects)[0],index==0)
    self.assertEqual(objects['BRIDGE']['endpoints'],b.prior.objects_for('right_scalene',method)['BRIDGE']['endpoints'])

 def test_rotation_preserves_distances_topology_chirality_scale_and_center(self):
  for method in b.METHODS:
   first=b.objects_for(method,False);second=b.objects_for(method,True)
   vertices=[k for k,v in first.items() if v['type']=='point']
   for a in vertices:
    self.assertAlmostEqual(math.dist(first[a]['xy'],[160,160]),math.dist(second[a]['xy'],[160,160]),places=7)
    for c in vertices:self.assertAlmostEqual(math.dist(first[a]['xy'],first[c]['xy']),math.dist(second[a]['xy'],second[c]['xy']),places=7)
   for k,v in first.items():
    if v['type']!='point':self.assertEqual(v,second[k])
   cross=lambda o:b.base.checker.cross(*(o[v]['xy'] for v in 'ABC'))
   self.assertGreater(cross(first)*cross(second),0)

 def test_isolation_is_only_removal_of_two_candidates_images_and_questions(self):
  isolated=b.isolated_input();source=copy.deepcopy(b.OLD['model_input']);state=source['state']
  state['admissible_bridges']={c:v for c,v in state['admissible_bridges'].items() if c in b.PAIR}
  self.assertEqual(state,isolated['state']);self.assertEqual(set(isolated['questions']),{'Q001','Q003'})
  self.assertEqual(set(isolated['assets']),{'image_C914','image_C850','initial'})
  for q,v in isolated['questions'].items():self.assertEqual(v,source['questions'][q])

 def test_original_pngs_are_the_actual_historical_bytes(self):
  with tempfile.TemporaryDirectory() as t:
   _,_,assets=b.build_payload(Path(t),'original')
   for asset in assets:
    original=next(a for a in b.OLD['asset_audit'] if a['asset']==asset['asset'])
    self.assertEqual(asset['sha256'],original['sha256']);self.assertEqual((Path(t)/asset['file']).read_bytes(),(b.prior.HERE/'fixtures'/original['file']).read_bytes())

 def test_renderer_and_style_match_baseline_before_applying_factors(self):
  with tempfile.TemporaryDirectory() as t:
   for c,m in list(b.PAIR.items())+[(None,b.METHODS[0])]:
    path=Path(t)/'render.png';b.base.render(b.objects_for(m,False),b.labels_for(False),path,bridge=c is not None)
    asset=next(a for a in b.OLD['asset_audit'] if a['asset']==('image_'+c if c else 'initial'))
    # Renderer/style equality concerns pixels; PNG compression can vary by zlib build.
    with Image.open(path) as rendered,Image.open(b.prior.HERE/'fixtures'/asset['file']) as archived:self.assertEqual(rendered.tobytes(),archived.tobytes())

 def test_factorial_changes_only_images_or_bijectively_renames_references(self):
  with tempfile.TemporaryDirectory() as t:
   values={cell:b.build_payload(Path(t),cell)[0] for cell in b.CELLS}
   original=values['original'];inverse={v:k for k,v in b.ID_MAP.items()}
   for cell,p in values.items():
    common={k:v for k,v in p.items() if k!='assets'}
    if b.CELLS[cell][1]:common=b.rename(common,inverse)
    self.assertEqual(common,{k:v for k,v in original.items() if k!='assets'})
   self.assertEqual(values['ids_only']['assets'].keys(),values['orientation_and_ids']['assets'].keys())
   for key in original['assets']:self.assertNotEqual(original['assets'][key],values['orientation_only']['assets'][key])

 def test_id_bijection_does_not_change_semantic_roles_or_predicates(self):
  self.assertEqual(len(b.ID_MAP),len(set(b.ID_MAP.values())));self.assertFalse(set(b.ID_MAP)&set(b.ID_MAP.values()))
  with tempfile.TemporaryDirectory() as t:
   old=b.build_payload(Path(t),'original')[0]['state'];new=b.build_payload(Path(t),'ids_only')[0]['state']
   self.assertEqual(list(old['generic_spaces'].values()),list(new['generic_spaces'].values()))
   for value in new['admissible_bridges'].values():
    for binding in value['verified_certificate']['generic_space_bindings'].values():self.assertEqual(binding['host'],'host')
   self.assertEqual(new['active_objective']['description'],b.native.EXPLICIT);self.assertEqual(new['evidence_policy'],b.native.POLICY)

 def test_id_image_changes_are_confined_to_label_glyphs(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);font=ImageFont.load_default(size=15)
   for oldcell,newcell,rotated in [('original','ids_only',False),('orientation_only','orientation_and_ids',True)]:
    _,_,aa=b.build_payload(out,oldcell);_,_,bb=b.build_payload(out,newcell)
    for index,(a,c) in enumerate(zip(aa,bb)):
     with Image.open(out/a['file']) as im:old=im.copy()
     with Image.open(out/c['file']) as im:new=im.copy()
     objects=b.objects_for(b.METHODS[index] if index<2 else b.METHODS[0],rotated)
     names=list('ABC')+([v for v in objects['BRIDGE']['endpoints'] if v not in 'ABC'] if index<2 else [])
     boxes=[];draw=ImageDraw.Draw(old)
     for labels in (b.labels_for(False),b.labels_for(True)):
      for v in names:
       x,y=objects[v]['xy'];box=draw.textbbox((x+5,y+3),labels[v],font=font);boxes.append((math.floor(box[0])-2,math.floor(box[1])-2,math.ceil(box[2])+2,math.ceil(box[3])+2))
     differences=0
     for j,(px,py) in enumerate(zip(old.getdata(),new.getdata())):
      if px!=py:
       differences+=1;x,y=j%320,j//320
       self.assertTrue(any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in boxes))
     self.assertGreater(differences,0)

 def test_no_reference_coverage_condition_or_historical_answers_in_input(self):
  forbidden={'reference','gold','correct','cell','rotated','new_ids','candidate_mapping','historical_context','p_yes_by_method','observer_material_certificates','coverage','covered_fraction','covered_intervals','certified_original_side_coverage','weights','composite','expected_answer'}
  def walk(value):
   if isinstance(value,dict):
    self.assertFalse(set(value)&forbidden)
    for v in value.values():walk(v)
   elif isinstance(value,list):
    for v in value:walk(v)
  with tempfile.TemporaryDirectory() as t:
   for cell in b.CELLS:
    p,_,_=b.build_payload(Path(t),cell);walk(p)

 def test_budget_type_order_and_explicit_request_are_fixed(self):
  with tempfile.TemporaryDirectory() as t:
   count=0
   for cell in b.CELLS:
    p,m,assets=b.build_payload(Path(t),cell);count+=len(p['questions']);self.assertEqual(len(assets),3)
    self.assertEqual(list(p['questions']),['Q001','Q003']);self.assertEqual(p['state']['active_objective']['description'],b.native.EXPLICIT)
    for q in p['questions'].values():self.assertEqual(q['type'],'noul');self.assertEqual(set(q),{'type','instructions'})
    self.assertEqual(sum(m['reference'].values()),1)
   self.assertEqual(count,8)

 def test_fixed_probability_contrasts_and_baseline_error_reproduction(self):
  calls=[]
  with tempfile.TemporaryDirectory() as t:
   for cell,(positive,negative) in zip(b.CELLS,[(.4,.6),(.8,.2),(.7,.3),(.9,.1)]):
    p,m,_=b.build_payload(Path(t),cell);m['response']={'answers':{'Q001':{'noul':positive},'Q003':{'noul':negative}},'usage':{}};calls.append(m)
  result=b.analyze(calls);self.assertTrue(result['historical_two_errors_reproduced_in_isolated_baseline']);self.assertAlmostEqual(result['margin_interaction'],-.4)
  self.assertEqual(result['cells']['original']['summary']['correct'],0);self.assertEqual(result['cells']['orientation_only']['summary']['correct'],2)

 def test_live_guard_and_rejection_never_make_unintended_calls(self):
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{},clear=True),patch.object(b.native,'transport') as transport:
   with self.assertRaises(SystemExit):b.main(Path(t),True)
   transport.assert_not_called()
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{'GITHUB_ACTIONS':'true','TYPESAFE_API_KEY':'test-only'},clear=True),patch.object(b.native,'transport',return_value={'failure':'HTTP_403'}) as transport:
   with self.assertRaises(SystemExit):b.main(Path(t),True)
   self.assertEqual(transport.call_count,1);self.assertEqual(json.loads((Path(t)/'results.json').read_text())['status'],'request_rejected')

 def test_offline_and_partial_live_artifacts_are_auditable(self):
  from audit_pair import audit
  with tempfile.TemporaryDirectory() as t:
   b.main(Path(t));result=audit(Path(t));self.assertEqual(result['native_noul_answers_verified'],0);self.assertEqual(result['requests_reconstructed'],4)
  def fixture(p):return {'response':b.native.sanitize({'model':'jev-1.14.0','answers':{q:{'type':'noul','noul':.25} for q in p['questions']}},p['questions']),'elapsed_seconds':0.}
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{'GITHUB_ACTIONS':'true','TYPESAFE_API_KEY':'test-only'},clear=True),patch.object(b.native,'transport',side_effect=fixture) as transport:
   b.main(Path(t),True);self.assertEqual(transport.call_count,4);result=audit(Path(t));self.assertEqual(result['native_noul_answers_verified'],8);self.assertEqual(result['material_contract_checks'],16)
  # Mock probabilities exist only in temporary test directories, never empirical output.

if __name__=='__main__':unittest.main()
