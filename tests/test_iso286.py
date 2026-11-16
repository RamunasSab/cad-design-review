"""Numerical acceptance from the supplied ISO 286-1:2010, not web fit charts."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import iso286

class ISO286Tests(unittest.TestCase):
    def test_annex_b_examples(self):
        for code, expected in [('H8/f7',[.025,.089]),('H7/n6',[-.033,.008]),('H7/s6',[-.059,-.018])]:
            self.assertEqual(iso286.calculate(code,36)['signed_difference_mm'],expected)

    def test_delta_and_exception(self):
        self.assertEqual(iso286.deviations('K7',20,True),(-15,6))
        self.assertEqual(iso286.deviations('M6',300,True),(-41,-9))
        self.assertEqual(iso286.deviations('K9',20,True),(-52,0))

    def test_h7g6_and_interval_boundaries(self):
        self.assertEqual(iso286.calculate('H7/g6',20)['signed_difference_mm'],[.007,.041])
        self.assertEqual(iso286.deviations('H7',18,True),(0,18))
        self.assertEqual(iso286.deviations('H7','18.000001',True),(0,21))
        self.assertEqual(iso286.deviations('r6',65,False),(41,60))
        self.assertEqual(iso286.deviations('r6','65.000001',False),(43,62))

    def test_recommendation_filter(self):
        result=iso286.recommend('hole','clearance',40,.024,.092)
        self.assertIn('H8/f7',[c['designation'] for c in result['candidates']])
        self.assertEqual(iso286.recommend('hole','clearance',20,.020,.200)['candidates'][0]['type'],'clearance')
        for c in iso286.recommend('shaft','transition',20)['candidates']:
            self.assertEqual(c['type'],'transition')
        self.assertEqual(iso286.recommend('hole','clearance',20,1,2)['status'],'NO_MATCH_IN_VERIFIED_SUBSET')

    def test_invalid_and_unsupported(self):
        for size in [0,-1,501,'NaN','Infinity',True]:
            with self.subTest(size=size),self.assertRaises(ValueError):iso286.calculate('H7/g6',size)
        for code in ['h7/G6','H7/z6','H4/g6','H7/g6/extra','H7/jS6']:
            with self.subTest(code=code),self.assertRaises(ValueError):iso286.calculate(code,20)
        with self.assertRaises(ValueError):iso286.recommend('hole','clearance',20,.2,.1)

    def test_candidate_properties(self):
        for basis in ['hole','shaft']:
            for size in [1,3,6,10,18,20,30,36,50,65,80,120,180,250,300,400,500]:
                for c in iso286.load()['candidates'][basis]:
                    r=iso286.calculate(c['code'],size)
                    self.assertLessEqual(*r['signed_difference_um'])
                    lo,hi=r['signed_difference_um']
                    width=sum(v[1]-v[0] for v in [r['hole_deviations_um'],r['shaft_deviations_um']])
                    self.assertEqual(hi-lo,width)

    def test_cli_and_retired_dataset(self):
        r=subprocess.run([sys.executable,str(ROOT/'scripts/check_tolerances.py'),'fit','H7/g6','--size','20','--json'],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)['standard'],'ISO 286-1:2010')
        d=json.loads((ROOT/'references/tolerance-data.json').read_text())
        self.assertNotIn('fit_series',d)
        self.assertNotIn('fits',d)

if __name__=='__main__':unittest.main()
