#!/usr/bin/env python3
"""
DFM checker (sheet-metal bending, plastic injection molding, machining): deterministically compares features against
rules in references/*-rules.json. Uses only the Python standard library.

Usage:
    python check_dfm.py part.json                  # Markdown table
    python check_dfm.py part.json --json           # JSON
    python check_dfm.py part.json --rules my.json  # alternative rule file
    python check_dfm.py --example sheet_metal      # example input (sheet metal)
    python check_dfm.py --example injection_molding
    python check_dfm.py --example machining

Input (mm; angles in degrees). The field "process": "sheet_metal" (default) or
"injection_molding" or "machining" selects the rule file. Nominal thickness (for sheet metal and plastics):
"thickness" or "nominal_wall"; not required for machining. Part-level variables (e.g.
"min_tool_diameter") can be used in rule expressions.
{
  "process": "sheet_metal", "part": "BRK-001", "material": "S235", "thickness": 2.0,
  "features": [ {"id": "Bend1", "type": "bend", "inner_radius": 1.0, "flange_length": 7} ]
}
For plastics, additionally use: "polymer_class": "amorphous" or "semi_crystalline".

Missing field -> NEEDS_CLARIFICATION (the script never guesses). A feature type without rules is
reported as "not evaluated". In a rule, "op": >=, <=, ~= (with "tol"), between (with "max"); "when" = condition;
"optional": true = if the feature does not contain the field, the rule is skipped without a message.
"""
import ast
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")
RULE_FILES = {"sheet_metal": "sheet-metal-rules.json", "injection_molding": "injection-molding-rules.json",
              "machining": "machining-rules.json", "progressive_stamping": "progressive-stamping-rules.json"}
ORDER = {"NONCONFORMANCE": 0, "RISK": 1, "NEEDS_CLARIFICATION": 2}
SAFE_FUNCS = {"max": max, "min": min, "abs": abs, "round": round}


def _raw(expr, env):
    """Safely evaluates arithmetic, comparisons, Boolean logic, and permitted functions only."""
    tree = ast.parse(str(expr), mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression): return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str, bool)): return node.value
        if isinstance(node, ast.Name):
            if node.id not in env: raise NameError(node.id)
            return env[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod):
            a, b = visit(node.left), visit(node.right)
            return {ast.Add: lambda: a+b, ast.Sub: lambda: a-b, ast.Mult: lambda: a*b,
                    ast.Div: lambda: a/b, ast.Pow: lambda: a**b, ast.Mod: lambda: a%b}[type(node.op)]()
        if isinstance(node, ast.UnaryOp) and type(node.op) in (ast.UAdd, ast.USub, ast.Not):
            v = visit(node.operand)
            return +v if isinstance(node.op, ast.UAdd) else (-v if isinstance(node.op, ast.USub) else not v)
        if isinstance(node, ast.BoolOp) and isinstance(node.op, (ast.And, ast.Or)):
            vals = [bool(visit(v)) for v in node.values]
            return all(vals) if isinstance(node.op, ast.And) else any(vals)
        if isinstance(node, ast.Compare):
            left = visit(node.left)
            for op, comp in zip(node.ops, node.comparators):
                right = visit(comp)
                funcs = {ast.Eq: lambda: left == right, ast.NotEq: lambda: left != right,
                         ast.Lt: lambda: left < right, ast.LtE: lambda: left <= right,
                         ast.Gt: lambda: left > right, ast.GtE: lambda: left >= right}
                if type(op) not in funcs or not funcs[type(op)](): return False
                left = right
            return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in SAFE_FUNCS and not node.keywords:
            return SAFE_FUNCS[node.func.id](*(visit(a) for a in node.args))
        raise ValueError(f"Disallowed rule expression: {ast.dump(node, include_attributes=False)}")

    return visit(tree)


def _num(expr, env):
    return float(_raw(expr, env))


def _types(r):
    a = r["applies_to"]
    return a if isinstance(a, list) else [a]


def check(part, rules):
    tval = part.get("thickness", part.get("nominal_wall"))
    base_env = {k: v for k, v in part.items() if k != "features" and isinstance(v, (int, float, str))}
    if tval is not None:
        base_env.update({"t": float(tval), "w": float(tval)})
    known_types = set()
    for r in rules:
        known_types |= set(_types(r))
    results, unknown = [], set()

    def add(f, r, sev, msg, value=None, limit=None, op=None, limit_max=None):
        results.append({"feature": f.get("id", "?"), "type": f.get("type"), "rule": r["id"], "severity": sev,
                        "message": msg, "value": value, "limit": limit, "limit_max": limit_max,
                        "op": op, "source": r.get("source", "")})

    for f in part["features"]:
        ftype = f.get("type")
        types = {ftype} | ({"hem"} if ftype in ("hem_teardrop", "hem_open") else set())
        if not (types & known_types):
            unknown.add(ftype)
            results.append({"feature": f.get("id", "?"), "type": ftype, "rule": "NO-RULE",
                            "severity": "NEEDS_CLARIFICATION", "message": "No DFM rules are defined for this feature type; it was not evaluated.",
                            "value": None, "limit": None, "limit_max": None, "op": None, "source": ""})
            continue
        env = {**base_env, **{k: v for k, v in f.items() if isinstance(v, (int, float, str))}}
        for r in rules:
            if not (set(_types(r)) & types):
                continue
            if r.get("when"):
                try:
                    if not _raw(r["when"], env):
                        continue
                except (NameError, KeyError, TypeError, ValueError, ZeroDivisionError) as e:
                    add(f, r, "NEEDS_CLARIFICATION", f"Could not evaluate condition ({e}): {r['message']}")
                    continue
            fld = r["field"]
            if fld not in f or f[fld] is None:
                if not r.get("optional"):
                    add(f, r, "NEEDS_CLARIFICATION", f"Missing field '{fld}': {r['message']}")
                continue
            try:
                lim = _num(r["limit"], env)
                lim_max = _num(r["max"], env) if r["op"] == "between" else None
                tol = _num(r.get("tol", "0"), env)
            except (NameError, KeyError, TypeError, ValueError, ZeroDivisionError) as e:
                add(f, r, "NEEDS_CLARIFICATION", f"Could not calculate limit ({e}): {r['message']}", value=f[fld])
                continue
            v, op = float(f[fld]), r["op"]
            if op == ">=":
                ok = v >= lim - 1e-9
            elif op == "<=":
                ok = v <= lim + 1e-9
            elif op == "~=":
                ok = abs(v - lim) <= tol + 1e-9
            elif op == "between":
                ok = lim - 1e-9 <= v <= lim_max + 1e-9
            else:
                raise ValueError(f"Unknown operator {op} in rule {r['id']}")
            if not ok:
                add(f, r, r["severity"], r["message"], value=v, limit=round(lim, 4), op=op,
                    limit_max=None if lim_max is None else round(lim_max, 4))

    # Keep only the most severe finding for the same feature field (avoid duplicates).
    rule_field = {r["id"]: r["field"] for r in rules}
    best = {}
    for r in results:
        key = (r["feature"], rule_field.get(r["rule"]), r["severity"] == "NEEDS_CLARIFICATION" and r["rule"])
        if key not in best or ORDER[r["severity"]] < ORDER[best[key]["severity"]]:
            best[key] = r
    results = sorted(best.values(), key=lambda x: (ORDER.get(x["severity"], 9), str(x["feature"])))
    return results, sorted(x for x in unknown if x)


def markdown(part, results, unknown):
    t = part.get("thickness", part.get("nominal_wall"))
    tinfo = f"  |  t/w = {t} mm" if t is not None else ""
    lines = [f"Part: {part.get('part', '?')}  |  process: {part.get('process', 'sheet_metal')}  |  "
             f"material: {part.get('material', '?')}{tinfo}", ""]
    if results:
        lines += ["| # | Feature | Status | Finding | Actual | Requirement | Rule (source) |",
                  "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(results, 1):
            fact = "" if r["value"] is None else f"{r['value']}"
            if r["limit"] is None:
                req = ""
            elif r["op"] == "between":
                req = f"{r['limit']} – {r['limit_max']}"
            else:
                req = f"{r['op']} {r['limit']}"
            lines.append(f"| {i} | {r['feature']} ({r['type']}) | {r['severity']} | {r['message']} | {fact} | "
                         f"{req} | {r['rule']} ({r['source']}) |")
    else:
        lines.append("No findings were generated by the rule file.")
    counts = {k: sum(1 for r in results if r["severity"] == k) for k in ORDER}
    lines += ["", f"Summary: {counts['NONCONFORMANCE']} nonconformities, {counts['RISK']} risks, "
                  f"{counts['NEEDS_CLARIFICATION']} clarification items."]
    if unknown:
        lines.append(f"Not evaluated (no rules for these types): {', '.join(unknown)}")
    lines.append("Note: these are general guidelines, not company standards. Verify them against supplier capabilities.")
    return "\n".join(lines)


EXAMPLES = {
    "sheet_metal": {
        "process": "sheet_metal", "part": "BRK-001", "material": "S235", "thickness": 2.0,
        "features": [
            {"id": "Bend1", "type": "bend", "inner_radius": 1.0, "flange_length": 7.0},
            {"id": "Bend2", "type": "bend", "inner_radius": 0.8, "flange_length": 6.0},
            {"id": "Hole1", "type": "hole", "diameter": 5.5, "dist_to_edge": 3.0, "dist_to_bend": 5.0,
             "bend_radius": 1.0, "dist_to_nearest_hole": 12.0},
            {"id": "Hole2", "type": "hole", "diameter": 1.5, "dist_to_edge": 3.0, "dist_to_bend": 4.0,
             "bend_radius": 1.0, "dist_to_nearest_hole": 3.0},
            {"id": "Notch1", "type": "notch", "width": 2.0, "length": 12.0, "corner_radius": 1.0},
            {"id": "Emboss1", "type": "emboss", "depth": 5.0},
            {"id": "Weld1", "type": "weld"}]},
    "injection_molding": {
        "process": "injection_molding", "part": "HSG-010", "material": "ABS", "nominal_wall": 2.5,
        "polymer_class": "amorphous",
        "features": [
            {"id": "Rib1", "type": "rib", "thickness": 2.0, "height": 6.0, "base_radius": 0.8, "draft": 0.8,
             "spacing_to_nearest_rib": 4.0},
            {"id": "Boss1", "type": "boss", "outer_diameter": 6.0, "height": 14.0, "base_radius": 0.5,
             "tip_radius": 0.0, "wall_thickness": 1.8, "hole_base_radius": 0.8, "draft_od": 0.3,
             "draft_id": 0.5, "spacing_to_nearest_boss": 4.0, "connected_to_wall": 0},
            {"id": "Wall1", "type": "wall_transition", "change_percent": 40},
            {"id": "Side1", "type": "sidewall", "draft_angle": 0.3},
            {"id": "Corner1", "type": "corner", "inner_radius": 0.5, "outer_radius": 2.0},
            {"id": "Hole1", "type": "blind_hole", "depth_to_diameter": 3.0},
            {"id": "UC1", "type": "undercut", "count": 1}]},
    "progressive_stamping": {
        "process": "progressive_stamping", "part": "STP-001", "material": "DC01", "thickness": 1.0,
        "max_burr_height": 0.05,
        "features": [
            {"id": "Carrier1", "type": "carrier_bridge", "web_width": 1.2},
            {"id": "Pilot1", "type": "pilot_hole", "diameter": 0.8},
            {"id": "Form1", "type": "forming_feature", "minimum_radius": 0.8},
            {"id": "Cut1", "type": "cut_edge", "burr_height": 0.08},
            {"id": "Strip1", "type": "strip_layout", "carrier_present_until_cutoff": 1},
            {"id": "Pierce1", "type": "piercing_feature", "slug_ejection_verified": 0}]},
    "machining": {
        "process": "machining", "part": "SHF-100", "material": "C45", "min_tool_diameter": 3.0,
        "features": [
            {"id": "Drill1", "type": "drilled_hole", "depth_to_diameter": 6.0, "blind": 1,
             "entry_perpendicular": 1, "flat_bottom": 1, "intersects_cavity": 0, "is_standard_size": 0},
            {"id": "Drill2", "type": "drilled_hole", "depth_to_diameter": 2.0, "blind": 0,
             "entry_perpendicular": 1, "exit_perpendicular": 0, "intersects_cavity": 1, "axis_in_cavity": 1,
             "area_in_material_percent": 60, "is_standard_size": 1},
            {"id": "Pocket1", "type": "pocket", "depth": 30.0, "corner_radius": 2.0, "standard_radii": 1,
             "side_to_bottom_angle": 85, "accessible": 1},
            {"id": "Pocket2", "type": "pocket", "depth": 8.0, "corner_radius": 0.0, "standard_radii": 1,
             "side_to_bottom_angle": 90, "accessible": 0},
            {"id": "Narrow1", "type": "narrow_region", "width": 2.0},
            {"id": "Bore1", "type": "blind_bore", "diameter": 40.0, "relief": 0.5},
            {"id": "Key1", "type": "keyway", "width": 8.0, "end_radius": 0.0, "axis_offset": 0.0},
            {"id": "Body1", "type": "turned_body", "length_to_min_diameter": 10.0},
            {"id": "Corner1", "type": "internal_corner", "radius": 0.0},
            {"id": "Prof1", "type": "od_profile", "contour_angle_from_axis": 75},
            {"id": "Slot1", "type": "axial_slot", "axis_offset": 0.3}]},
}


def main(argv):
    if "--example" in argv:
        i = argv.index("--example")
        name = argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else "sheet_metal"
        print(json.dumps(EXAMPLES[name], indent=2, ensure_ascii=False))
        return 0
    flags_with_value = {"--rules"}
    paths, skip = [], False
    for k, a in enumerate(argv[1:], 1):
        if skip:
            skip = False
        elif a in flags_with_value:
            skip = True
        elif not a.startswith("--"):
            paths.append(a)
    if not paths:
        print(__doc__)
        return 1
    with open(paths[0], encoding="utf-8") as f:
        part = json.load(f)
    if "--rules" in argv:
        rules_path = argv[argv.index("--rules") + 1]
    else:
        rules_path = os.path.join(REF, RULE_FILES[part.get("process", "sheet_metal")])
    with open(rules_path, encoding="utf-8") as f:
        rules = json.load(f)["rules"]
    results, unknown = check(part, rules)
    if "--json" in argv:
        print(json.dumps({"part": part.get("part"), "issues": results, "not_evaluated": unknown},
                         indent=2, ensure_ascii=False))
    else:
        print(markdown(part, results, unknown))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
