import unittest
import tempfile
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
import prototype as p

class TestExploratoryI10(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.temp.name)
        cls.results=p.build_all(cls.root)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_deduplicate_coincident_constructions(self):
        self.assertEqual(len(p.RAW),7)
        self.assertEqual(len(self.results),5)
        self.assertCountEqual(self.results[0]['equivalent_operations'],
                              ['angle_bisector','perpendicular','median'])

    def test_angle_partition_equal_without_proof_claim(self):
        c=self.results[0]
        self.assertAlmostEqual(c['heuristic_evidence']['angle_gap_deg'],0.0,places=4)
        self.assertEqual(len(c['groups']),2)
        self.assertEqual(c['candidate_generic_spaces'][0]['status'],'candidate')
        self.assertIn('NOT a proof',c['epistemic_status'])

    def test_noncentral_cevians_are_not_equally_aligned(self):
        for r in self.results[1:3]:
            self.assertGreater(r['heuristic_evidence']['angle_gap_deg'],1.0)
            self.assertLess(r['heuristic_blend_value'],self.results[0]['heuristic_blend_value'])

    def test_roles_and_origins_present(self):
        c=self.results[0]
        self.assertIn('CD',c['object_interpretations'])
        self.assertGreaterEqual(len(c['object_interpretations']['CD']),3)
        self.assertEqual(c['groups'][0]['generator'],'CD')
        self.assertEqual(c['groups'][0]['boundary'],['A','C','D'])
        self.assertEqual(c['construction_timeline'][-1]['order'],2)

    def test_jev_payload_does_not_leak_goal_or_answer(self):
        q=p.jev_payload(self.results,self.root)
        self.assertEqual(q['model'],'jev-1.14.0')
        self.assertIn('best_bridge',q['questions'])
        self.assertEqual(q['questions']['best_bridge']['type'],'choice')
        self.assertEqual(len(q['assets']),6)
        txt=__import__('json').dumps({k:v for k,v in q.items() if k!='assets'}).lower()
        self.assertNotIn('ad=db',txt)
        self.assertNotIn('midpoint',txt)
        self.assertNotIn('bisector',txt)
        self.assertNotIn('i.4',txt)
        self.assertNotIn('i.10',txt)
        self.assertNotIn('lal',txt)

    def test_generated_images_are_api_compatible(self):
        from PIL import Image
        for f in (self.root/'images').glob('*.png'):
            with Image.open(f) as im:
                self.assertTrue(280<=im.width<=1568)
                self.assertTrue(280<=im.height<=1568)

if __name__=='__main__':unittest.main()