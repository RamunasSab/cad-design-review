#!/usr/bin/env python3
"""Look up fits, general tolerances, and bearing fits using references/tolerance-data.json.

The dataset was transcribed from user-provided reference material. Verify standard
editions and contractual requirements against authoritative copies.

Usage examples:
  python check_tolerances.py fit H7/f7
  python check_tolerances.py general --type linear --size 45 --class m
  python check_tolerances.py general --type radius --size 4 --class v
  python check_tolerances.py general --type angle --size 30 --class c
  python check_tolerances.py geom --kind flatness --size 120 --class K
  python check_tolerances.py geom --kind runout --class L
  python check_tolerances.py bearing --ring inner --load circumferential --level medium --bearing-type ball
  python check_tolerances.py bearing --thrust combined --load point
  python check_tolerances.py plastic --tg 6 --size 40
  python check_tolerances.py plastic --tg 6 --size 40 --kind W
  python check_tolerances.py plastic --find --size 40 --tol 0.15 --kind W
  python check_tolerances.py plastic --series 1

Add --json to return JSON. A result of None / "not specified" means the table
contains no value (mark NEEDS_CLARIFICATION; do not guess). This utility does not
provide ISO 286 limit-deviation values.
"""
import argparse
import json
import os
import sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "tolerance-data.json")


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def pick_index(ranges, size):
    """Interval: (lower; upper]; the lower bound of the first interval is inclusive."""
    for i, (lo, hi) in enumerate(ranges):
        above = size >= lo if i == 0 else size > lo
        if above and (hi is None or size <= hi):
            return i
    return None


def fmt_range(r):
    lo, hi = r
    return f"{lo}–{hi}" if hi is not None else f"> {lo}"


def fmt_minutes(m):
    d, mm = divmod(int(m), 60)
    return f"±{d}°" if mm == 0 else (f"±{d}°{mm:02d}'" if d else f"±0°{mm:02d}'")


# ---------- Fits ----------
def cmd_fit(d, a):
    code = a.designation.replace(" ", "")
    hit = None
    for f in d["fits"]:
        if code in (f.get("hole_basis"), f.get("shaft_basis"), f.get("shaft_basis_suggested")):
            hit = f
            break
    s1, s2 = d["fit_series"]["series_1_priority"], d["fit_series"]["series_2"]
    series = 1 if code in s1 else (2 if code in s2 else None)
    system = "hole basis" if code.startswith("H") else ("shaft basis" if "/h" in code else "other")
    res = {"designation": code, "system": system, "series": series, "in_table": hit is not None}
    if hit:
        res.update({k: hit.get(k) for k in ("type", "name", "application", "hole_basis", "shaft_basis",
                                           "interference_level", "pdf_note")})
    if series is None and not hit:
        res["verdict"] = ("Not listed among the DIN 7157 recommended fits (neither series 1 nor series 2). "
                          "RISK: justify the choice by function or select a recommended fit.")
    elif series == 2:
        res["verdict"] = "Series 2 (permitted, but series 1 has priority). Check whether a series 1 fit is unsuitable."
    elif series == 1:
        res["verdict"] = "Series 1 (highest priority)."
    else:
        res["verdict"] = "Present in the description table but not assigned to series 1 or 2 (check the PDF note)."
    if code == "F7/h6":
        res["note"] = "F7/h6 is not listed in DIN 7157; F8/h6 is recommended for the H7/f7 pair."
    if series and not hit:
        res["note"] = "Listed in series 1/2 but absent from the description table (the PDF does not provide an application description)."
    return res


# ---------- General tolerances ----------
def cmd_general(d, a):
    key = {"linear": "general_linear", "radius": "general_radius_chamfer", "angle": "general_angular"}[a.type]
    t = d[key]
    cls = a.cls.lower()
    if cls not in t["classes"]:
        return {"error": f"Unknown class '{a.cls}'. Available: {', '.join(t['classes'])}"}
    i = pick_index(t["ranges"], a.size)
    res = {"type": a.type, "size": a.size, "class": cls, "standard": "ISO 2768-1"}
    if i is None:
        res.update({"tolerance": None, "verdict": "Dimension is outside the table range: not specified; NEEDS_CLARIFICATION (an individual tolerance is required)."})
        return res
    v = t["classes"][cls][i]
    res["range"] = fmt_range(t["ranges"][i])
    if v is None:
        res.update({"tolerance": None, "verdict": "No value is listed for this interval and class: NEEDS_CLARIFICATION."})
    elif a.type == "angle":
        res.update({"tolerance": fmt_minutes(v), "tolerance_minutes": v})
    else:
        res.update({"tolerance": f"±{v} mm", "tolerance_mm": v})
    return res


def cmd_geom(d, a):
    g = d["geometric"]
    cls = a.cls.upper()
    if a.kind == "runout":
        v = g["runout"]["classes"].get(cls)
        return {"kind": "runout", "class": cls, "tolerance_mm": v, "standard": "ISO 2768-2"} if v is not None \
            else {"error": f"Unknown class '{a.cls}' (H, K, L)"}
    key = {"flatness": "straightness_flatness", "straightness": "straightness_flatness",
           "perpendicularity": "perpendicularity", "symmetry": "symmetry"}[a.kind]
    t = g[key]
    if cls not in t["classes"]:
        return {"error": f"Unknown class '{a.cls}' (H, K, L)"}
    if a.size is None:
        return {"error": "Specify --size"}
    i = pick_index(t["ranges"], a.size)
    res = {"kind": a.kind, "size": a.size, "class": cls, "standard": "ISO 2768-2"}
    if i is None:
        res.update({"tolerance_mm": None, "verdict": "Dimension is outside the table range: NEEDS_CLARIFICATION."})
    else:
        res.update({"range": fmt_range(t["ranges"][i]), "tolerance_mm": t["classes"][cls][i]})
    return res


def cmd_bearing(d, a):
    b = d["bearings"]
    out = {"standard": "DIN 5425-1", "note": b["_description"]}
    if a.thrust:
        t = b["thrust"]["combined_radial_axial" if a.thrust == "combined" else "axial_only"]
        out["bearing_types"] = t["bearing_types"]
        for wash in ("shaft_washer", "housing_washer"):
            v = t[wash]
            out[wash] = v.get(a.load) if (isinstance(v, dict) and a.load) else v
        return out
    ring = {"inner": "inner_ring_shaft", "outer": "outer_ring_housing"}[a.ring]
    rows = [r for r in b["radial"][ring]
            if (not a.load or r["load"] == a.load) and (not a.level or r["level"] in (a.level, "temporarily_high"))]
    out["ring"] = a.ring
    out["rows"] = [{**r, "recommended": (r[a.bearing_type] if a.bearing_type else None)} for r in rows]
    return out


# Implementation note (English translation required for public distribution).
def _plastic_val(P, tg, kind, i):
    v = P[kind][tg][i]
    return None if v is None else float(v)


def cmd_plastic(d, a):
    P = d["iso20457"]
    base = {"standard": "ISO 20457 (values from DIN 16742:2013; see iso-20457.md)",
            "warning": "Values have not been verified against the full text of ISO 20457:2026. Confirm critical dimensions against the standard."}
    if a.series:
        row = P["production_series"]["series"].get(str(a.series))
        if row is None:
            return {"error": "Series must be 1–4"}
        return {**base, "series": a.series, "groups_by_column": dict(zip(P["production_series"]["columns"], row)),
                "note": P["production_series"]["note"]}
    if a.size is None:
        return {"error": "Specify --size (mm)"}
    i = pick_index(P["sizes"], a.size)
    if i is None:
        return {**base, "size": a.size, "verdict": "Dimension is outside 1–315 mm: not listed in the tables; NEEDS_CLARIFICATION under the standard."}
    rng = fmt_range(P["sizes"][i])
    kinds = ["W", "NW"] if a.kind == "both" else [a.kind]
    if a.find:
        if a.tol is None:
            return {"error": "Specify --tol (± mm)"}
        out = {**base, "size": a.size, "range": rng, "required_tol": a.tol}
        for k in kinds:
            ok = [g for g in P["groups"] if (_plastic_val(P, g, k, i) is not None and _plastic_val(P, g, k, i) <= a.tol + 1e-9)]
            if not ok:
                out[k] = "Stricter than TG1, or TG1 is not defined for this size: outside the standard tables; a separate agreement is required (RISK)."
            else:
                g = ok[-1]  # loosest group that still meets the requirement
                out[k] = {"loosest_group_that_meets": g, "group_value": _plastic_val(P, g, k, i)}
                tight = [x for x in P["groups"] if x <= "TG3"]
                if g in tight:
                    out[k]["note"] = "TG1–TG3 are achievable only with production series 2–4 (see --series); agreement with the molder is required."
        return out
    if a.tg is None:
        return {"error": "Specify --tg (1–9), --find, or --series"}
    g = f"TG{a.tg}"
    if g not in P["groups"]:
        return {"error": "TG1–TG9"}
    out = {**base, "group": g, "size": a.size, "range": rng}
    for k in kinds:
        v = _plastic_val(P, g, k, i)
        if v is None:
            out[k] = "n/a: the standard does not specify a value for this size and group (TG1 is defined only up to 120 mm). NEEDS_CLARIFICATION."
        else:
            out[k] = {"tol": f"±{v} mm", "limits": f"{a.size - v:.3f} – {a.size + v:.3f}"}
    if g == "TG9":
        out["note"] = "TG9 has a single value for W and NW."
    return out


def to_text(r):
    return "\n".join(f"{k}: {v}" for k, v in r.items() if v is not None)


def main(argv):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("fit"); s.add_argument("designation")
    s = sub.add_parser("general")
    s.add_argument("--type", choices=["linear", "radius", "angle"], required=True)
    s.add_argument("--size", type=float, required=True)
    s.add_argument("--class", dest="cls", required=True)
    s = sub.add_parser("geom")
    s.add_argument("--kind", choices=["flatness", "straightness", "perpendicularity", "symmetry", "runout"], required=True)
    s.add_argument("--size", type=float)
    s.add_argument("--class", dest="cls", required=True)
    s = sub.add_parser("bearing")
    s.add_argument("--ring", choices=["inner", "outer"], default="inner")
    s.add_argument("--load", choices=["circumferential", "point"])
    s.add_argument("--level", choices=["light", "medium", "heavy"])
    s.add_argument("--bearing-type", choices=["ball", "roller"])
    s.add_argument("--thrust", choices=["combined", "axial"])
    s = sub.add_parser("plastic")
    s.add_argument("--tg", type=int)
    s.add_argument("--size", type=float)
    s.add_argument("--kind", choices=["W", "NW", "both"], default="both")
    s.add_argument("--find", action="store_true")
    s.add_argument("--tol", type=float)
    s.add_argument("--series", type=int)
    for sp in sub.choices.values():
        sp.add_argument("--json", action="store_true")
    a = p.parse_args(argv[1:])
    d = load()
    r = {"fit": cmd_fit, "general": cmd_general, "geom": cmd_geom, "bearing": cmd_bearing, "plastic": cmd_plastic}[a.cmd](d, a)
    print(json.dumps(r, indent=2, ensure_ascii=False) if a.json else to_text(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
