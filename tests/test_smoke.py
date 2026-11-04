"""Lightweight regression tests with no external dependencies: python tests/test_smoke.py"""
import importlib.util
import json
import pathlib
import tempfile
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

# DFM rules parse and execute all process examples
for process in ("sheet_metal", "injection_molding", "machining", "progressive_stamping"):
    example = subprocess.check_output([sys.executable, str(ROOT / "scripts/check_dfm.py"), "--example", process], text=True)
    part = json.loads(example)
    rules_file = {"sheet_metal":"sheet-metal-rules.json", "injection_molding":"injection-molding-rules.json",
                  "machining":"machining-rules.json", "progressive_stamping":"progressive-stamping-rules.json"}[process]
    rules = json.loads((ROOT / "references" / rules_file).read_text(encoding="utf-8"))["rules"]
    mod = load("check_dfm_"+process, "scripts/check_dfm.py")
    issues, unknown = mod.check(part, rules)
    assert isinstance(issues, list)

# Safe expression evaluator must reject attribute access / imports
mod = load("check_dfm_safe", "scripts/check_dfm.py")
assert mod._raw("max(2*t, 3)", {"t": 2}) == 4
try:
    mod._raw("__import__('os').system('echo bad')", {})
    raise AssertionError("Unsafe expression accepted")
except ValueError:
    pass

# Drawing package sample passes; revision mismatch is caught
mod2 = load("check_drawing_data", "scripts/check_drawing_data.py")
example = mod2.EXAMPLE
assert mod2.check(example)["status"] == "PASS"
assert mod2.check(example)["scope"] == "EXTENDED_REVIEW"
bad = json.loads(json.dumps(example)); bad["files"]["dxf"]["metadata"]["revision"] = "C"
assert any(x["code"] == "PKG-010" for x in mod2.check(bad)["findings"])
# One file is sufficient to start; scope is inferred and only relevant limitations are reported.
dxf_only = {"files": {"dxf": {"metadata": {}, "drawing": {}, "geometry": {"unit": "mm"}}}}
r_dxf = mod2.check(dxf_only)
assert r_dxf["scope"] == "DXF_REVIEW" and r_dxf["provided_files"] == ["dxf"]
assert not any("missing pdf" in x["message"].lower() for x in r_dxf["findings"])
step_pdf = {"files": {"step": {"metadata": {}, "geometry": {"unit": "mm", "solid_count": 1}},
                       "pdf": {"metadata": {}, "drawing": {}}}}
assert mod2.check(step_pdf)["scope"] == "3D_AND_DRAWING_REVIEW"

# Stack-up example runs and validates bounds
mod3 = load("stackup", "scripts/stackup.py")
r = mod3.analyse(mod3.EXAMPLE)
assert "worst_case" in r and "monte_carlo" in r
print("Smoke tests: OK")
