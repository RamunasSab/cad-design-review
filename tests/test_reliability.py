"""Deterministic golden, boundary, negative and generated checks; no AI model is called."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
stackup = load("stackup")
dfm = load("check_dfm")
CASES = json.loads((ROOT / "examples/golden-stackups.json").read_text(encoding="utf-8"))

class ReliabilityTests(unittest.TestCase):
    def test_golden(self):
        for c in CASES:
            with self.subTest(c["id"]):
                r=stackup.analyse(c["input"]); w=r["worst_case"]
                self.assertAlmostEqual(w["min"], c["expected"]["min"])
                self.assertAlmostEqual(w["max"], c["expected"]["max"])
                self.assertEqual(w["pass"], c["expected"]["passes"])
                self.assertEqual("INFO" if w["pass"] else "NONCONFORMANCE", c["expected"]["status"])
                json.dumps(r, allow_nan=False)
    def test_generated_interval_invariants(self):
        rng=random.Random(467)
        for _ in range(100):
            a,b=[rng.randrange(-1000,1000)/100 for _ in range(2)]
            ta,tb=[rng.randrange(0,100)/100 for _ in range(2)]
            d={"requirement":{"min":-100,"max":100},"contributors":[{"name":"a","nominal":a,"tolerance":ta,"direction":1},{"name":"b","nominal":b,"tolerance":tb,"direction":-1}],"samples":2}
            r=stackup.analyse(d);w=r["worst_case"]
            for x in (a-ta,a+ta):
                for y in (b-tb,b+tb):
                    self.assertGreaterEqual(x-y+1e-10,w["min"])
                    self.assertLessEqual(x-y-1e-10,w["max"])
            d["contributors"].reverse()
            self.assertEqual(w, stackup.analyse(d)["worst_case"])
    def test_negative_inputs(self):
        for key,value in [("samples",0),("samples",1.5),("samples",True),("samples",1000001),("seed",1.2)]:
            d=copy.deepcopy(CASES[0]["input"]);d[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):stackup.analyse(d)
        for field,value in [("tolerance",-.1),("nominal",float("inf")),("direction",True),("direction",0)]:
            d=copy.deepcopy(CASES[0]["input"]);d["contributors"][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):stackup.analyse(d)
        for cpk in [None,0,-1,float("nan"),float("inf")]:
            d=copy.deepcopy(CASES[0]["input"]);d["contributors"][0].update(distribution="normal")
            if cpk is not None:d["contributors"][0]["cpk"]=cpk
            with self.subTest(cpk=cpk),self.assertRaises(ValueError):stackup.analyse(d)
    def test_audit_and_repeatability(self):
        d=CASES[0]["input"];r=stackup.analyse(d)
        self.assertEqual(r,stackup.analyse(d))
        canonical=json.dumps(d,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
        self.assertEqual(r["audit"]["input_sha256"],hashlib.sha256(canonical.encode()).hexdigest())
        self.assertIsNone(stackup.analyse(CASES[8]["input"])["statistical"]["cpk"])
    def test_cli(self):
        with tempfile.TemporaryDirectory() as temp:
            f=Path(temp)/"input.json";f.write_text(json.dumps(CASES[0]["input"]))
            cmd=[sys.executable,str(ROOT/"scripts/stackup.py"),str(f)]
            for fmt in ["md","html","json"]:
                r=subprocess.run(cmd+["--report",fmt],capture_output=True,text=True,encoding="utf-8")
                self.assertEqual(r.returncode,0,r.stderr)
                if fmt=="json":self.assertIn("audit",json.loads(r.stdout))
                if fmt=="html":self.assertIn("<!doctype html>",r.stdout)
            self.assertEqual(subprocess.run(cmd+["--fail-on","nonconformance"],capture_output=True).returncode,2)
    def test_dfm_heuristic_not_nonconformance(self):
        part={"features":[{"id":"x","type":"rib","draft":0}]}
        rule={"id":"r","applies_to":"rib","field":"draft","op":">=","limit":"1","severity":"NONCONFORMANCE","message":"draft"}
        r,_=dfm.check(part,[rule]);self.assertEqual(r[0]["severity"],"RISK");self.assertEqual(r[0]["rule_severity"],"NONCONFORMANCE")
        rule.update(basis="binding_requirement",requirement_reference="Approved drawing note 7")
        self.assertEqual(dfm.check(part,[rule])[0][0]["severity"],"NONCONFORMANCE")
    def test_version_contract(self):
        v=json.loads((ROOT/"project-version.json").read_text(encoding="utf-8"))
        readme=(ROOT/"README.md").read_text(encoding="utf-8")
        installs=re.findall(r"npx skills add RamunasSab/cad-design-review@v([0-9.]+)",readme)
        self.assertTrue(installs);self.assertEqual(set(installs),{v["stable"]})
        self.assertIn("Use the pinned stable installation for v"+v["stable"]+".",readme)
        self.assertIn('version: "'+v["development"]+'"',(ROOT/"SKILL.md").read_text(encoding="utf-8"))
        self.assertTrue((ROOT/("docs/releases/v"+v["stable"]+".md")).exists())
        self.assertIn("## "+v["stable"]+" ",(ROOT/"CHANGELOG.md").read_text(encoding="utf-8"))
    def test_prompt_contracts(self):
        snap=(ROOT/"prompt-templates/plastic_snap_fit.md").read_text(encoding="utf-8")
        for expected in ["STEP assembly","section","NEEDS_CLARIFICATION","both parts","CAD parser/kernel"]:self.assertIn(expected,snap)
        machining=(ROOT/"prompt-templates/machining.md").read_text(encoding="utf-8")
        for expected in ["worst-case","verified tolerance tables","language of my request"]:self.assertIn(expected,machining)

if __name__=="__main__":unittest.main()
