#!/usr/bin/env python3
"""
Tolerance stack-up calculator: worst case, RSS, Monte Carlo, and sensitivity analysis.
Uses only the Python standard library (no packages required).

Usage:
    python stackup.py stackup.json            # text report
    python stackup.py stackup.json --json     # JSON output
    python stackup.py --example > stackup.json  # example input

Input format (mm):
{
  "name": "Shaft-to-hole clearance",
  "requirement": {"min": 0.02, "max": 0.20},        # permitted result interval
  "contributors": [
    {"name": "Hole diameter", "nominal": 20.0, "tolerance": 0.05, "direction": 1,
     "distribution": "normal", "cpk": 1.33},
    {"name": "Shaft diameter", "nominal": 19.9, "tolerance": 0.03, "direction": -1}
  ],
  "samples": 100000                                  # optional Monte Carlo sample count
}

Fields:
  nominal      nominal dimension (mm)
  tolerance    HALF the tolerance band, i.e. ±T (mm); for a dimension 20 +0.10/0, first
               convert it to 20.05 ±0.05
  direction    +1 if the dimension increases the result, -1 if it decreases it
  distribution "uniform" (default when process data is unavailable) or "normal" (only with a documented Cpk)
  cpk          process capability for a normal distribution (required when distribution=normal): sigma = T / (3*Cpk)
"""
import argparse
import hashlib
import html
from decimal import Decimal
from pathlib import Path
import json
import math
import random
import sys

DEFAULT_SAMPLES = 100_000
MAX_SAMPLES = 1_000_000
CALCULATOR_VERSION = "2.0.0"


def _sigma(c):
    t = float(c["tolerance"])
    distribution = c.get("distribution", "uniform")
    if distribution == "uniform":
        return t / math.sqrt(3.0)
    if distribution != "normal":
        raise ValueError(f"{c.get('name', '?')}: distribution must be 'uniform' or 'normal'")
    if "cpk" not in c:
        raise ValueError(f"{c.get('name', '?')}: a process Cpk value is required for a normal distribution")
    cpk = float(c["cpk"])
    if not math.isfinite(cpk) or cpk <= 0:
        raise ValueError(f"{c.get('name', '?')}: Cpk must be finite and > 0")
    return t / (3.0 * cpk)


def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def analyse(data):
    # Canonical JSON rejects NaN/Infinity anywhere, including optional fields.
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    req = data["requirement"]
    lo, hi = float(req["min"]), float(req["max"])
    if not (math.isfinite(lo) and math.isfinite(hi)) or lo > hi:
        raise ValueError("Requirement bounds must be finite and min <= max")
    cs = data["contributors"]
    if not cs:
        raise ValueError("At least one stack-up contributor is required")
    for c in cs:
        if not math.isfinite(float(c["nominal"])) or not math.isfinite(float(c["tolerance"])):
            raise ValueError(f"{c.get('name', '?')}: nominal value and tolerance must be finite")
        if isinstance(c.get("direction"), bool) or c.get("direction") not in (1, -1):
            raise ValueError(f"{c.get('name', '?')}: direction must be +1 or -1")
        if float(c["tolerance"]) < 0:
            raise ValueError(f"{c.get('name', '?')}: tolerance must not be negative")

    # Decimal endpoints prevent cancellation errors at inclusive requirement bounds.
    dn = sum((Decimal(str(c["direction"])) * Decimal(str(c["nominal"])) for c in cs), Decimal(0))
    dt = sum((Decimal(str(c["tolerance"])) for c in cs), Decimal(0))
    dlo, dhi = Decimal(str(req["min"])), Decimal(str(req["max"]))
    nominal = float(dn)

    # 1) Worst-case analysis
    wc_t = float(dt)
    wc_min, wc_max = float(dn - dt), float(dn + dt)
    wc_pass = dn - dt >= dlo and dn + dt <= dhi
    wc_margin = float(min(dn - dt - dlo, dhi - dn - dt))

    # Implementation note (English translation required for public distribution).
    rss_t = math.sqrt(sum(float(c["tolerance"]) ** 2 for c in cs))
    sigmas = [_sigma(c) for c in cs]
    sigma = math.sqrt(sum(s * s for s in sigmas))
    mean = nominal
    p_out = 1.0 - (_norm_cdf((hi - mean) / sigma) - _norm_cdf((lo - mean) / sigma)) if sigma > 0 else (
        0.0 if lo <= mean <= hi else 1.0)
    cpk_assy = min((hi - mean) / (3 * sigma), (mean - lo) / (3 * sigma)) if sigma > 0 else None

    # 3) Monte Carlo analysis
    n = data.get("samples", DEFAULT_SAMPLES)
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= MAX_SAMPLES:
        raise ValueError(f"Monte Carlo samples must be an integer from 1 to {MAX_SAMPLES}")
    seed = data.get("seed", 12345)
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("Seed must be an integer")
    rng = random.Random(seed)  # fixed seed -> reproducible results
    out = 0
    vals_min, vals_max = float("inf"), float("-inf")
    total, total_sq = 0.0, 0.0
    for _ in range(n):
        v = 0.0
        for c, s in zip(cs, sigmas):
            x = float(c["nominal"])
            if c.get("distribution", "uniform") == "uniform":
                x += rng.uniform(-float(c["tolerance"]), float(c["tolerance"]))
            else:
                x += rng.gauss(0.0, s)
            v += c["direction"] * x
        total += v
        total_sq += v * v
        vals_min = min(vals_min, v)
        vals_max = max(vals_max, v)
        if v < lo or v > hi:
            out += 1
    mc_mean = total / n
    mc_sigma = math.sqrt(max(total_sq / n - mc_mean ** 2, 0.0))

    # 4) Sensitivity (contribution to variance) and contribution to the worst case
    sens = []
    for c, s in zip(cs, sigmas):
        share = (s * s / (sigma * sigma) * 100.0) if sigma > 0 else 0.0
        wc_share = abs(float(c["tolerance"])) / wc_t * 100.0 if wc_t > 0 else 0.0
        sens.append({"contributor": c.get("name", "Unnamed"), "variance_percent": round(share, 1),
                     "worst_case_percent": round(wc_share, 1)})
    sens.sort(key=lambda r: r["variance_percent"], reverse=True)

    assumptions = [
        "Explicit scalar signed dimension chain in mm; no CAD extraction or design approval.",
        "Contributor limits may attain independent extremes; cancel shared variables before input.",
        "Statistical contributors are modeled as independent; normal inputs are centered on nominal.",
        "Cpk-to-sigma conversion assumes a centered process; Cpk alone does not identify an off-center distribution.",
        "Uniform distributions and modeled assembly Cpk are not evidence of process capability.",
        "Gaussian-tail estimate uses a normal approximation for mixed/uniform inputs; Monte Carlo is modeled sampling."
    ]
    return {
        "audit": {"schema_version": "1.0", "calculator": "stackup", "calculator_version": CALCULATOR_VERSION,
                  "calculator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  "input_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
                  "input": data, "units": "mm", "seed": seed, "assumptions": assumptions,
                  "formula": "R = sum(direction_i * nominal_i); T = sum(tolerance_i); limits = R +/- T",
                  "exact_limits_mm": {"min": str(dn - dt), "max": str(dn + dt)},
                  "acceptance_basis": "Inclusive decimal worst-case endpoints; displayed values may be rounded"},
        "name": data.get("name", "Tolerance stack-up"),
        "requirement": {"min": lo, "max": hi},
        "nominal_result": round(nominal, 6),
        "worst_case": {"min": round(wc_min, 6), "max": round(wc_max, 6),
                       "tolerance": round(wc_t, 6), "pass": wc_pass, "margin": round(wc_margin, 6)},
        "rss_classic": {"tolerance": round(rss_t, 6), "min": round(nominal - rss_t, 6),
                        "max": round(nominal + rss_t, 6)},
        "statistical": {"mean": round(mean, 6), "sigma": round(sigma, 6),
                        "min_3sigma": round(mean - 3 * sigma, 6), "max_3sigma": round(mean + 3 * sigma, 6),
                        "percent_out_of_spec": round(p_out * 100.0, 4), "cpk": None if cpk_assy is None else round(cpk_assy, 3), "basis": "modeled, not measured capability"},
        "monte_carlo": {"samples": n, "mean": round(mc_mean, 6), "sigma": round(mc_sigma, 6),
                        "min_observed": round(vals_min, 6), "max_observed": round(vals_max, 6),
                        "percent_out_of_spec": round(out / n * 100.0, 4)},
        "sensitivity_ranking": sens,
    }


def report(r):
    w, s, m = r["worst_case"], r["statistical"], r["monte_carlo"]
    lines = [
        f"== {r['name']} ==",
        f"Requirement: {r['requirement']['min']} ... {r['requirement']['max']} mm",
        f"Nominal result: {r['nominal_result']} mm",
        "",
        f"Worst case: {w['min']} ... {w['max']} mm (±{w['tolerance']})  ->  "
        f"{'PASS' if w['pass'] else 'FAIL'}  (margin {w['margin']} mm)",
        f"RSS (classical): ±{r['rss_classic']['tolerance']} mm  ({r['rss_classic']['min']} ... {r['rss_classic']['max']})",
        f"Statistical model (not measured capability): σ={s['sigma']}, ±3σ: {s['min_3sigma']} ... {s['max_3sigma']}, "
        f"out of specification {s['percent_out_of_spec']} %, assembly Cpk {s['cpk']}",
        f"Monte Carlo (N={m['samples']}): mean {m['mean']}, σ {m['sigma']}, "
        f"min {m['min_observed']}, max {m['max_observed']}, out of specification {m['percent_out_of_spec']} %",
        "",
        "Contributor impact (variance %, worst-case %):",
    ]
    for row in r["sensitivity_ranking"]:
        lines.append(f"  {row['contributor']:<30} {row['variance_percent']:>6} %   {row['worst_case_percent']:>6} %")
    lines.append("")
    lines.extend(["", "Assumptions:", *["- " + x for x in r["audit"]["assumptions"]]])
    lines.append("Note: statistical results are meaningful only when process distributions and Cpk values are supported by real data and contributors are independent. A uniform distribution is a simplifying assumption, not evidence of process capability. Worst-case analysis remains a separate result.")
    return "\n".join(lines)


EXAMPLE = {
    "name": "Shaft-to-hole clearance",
    "requirement": {"min": 0.02, "max": 0.20},
    "contributors": [
        {"name": "Hole diameter", "nominal": 20.065, "tolerance": 0.065, "direction": 1,
         "distribution": "uniform"},
        {"name": "Shaft diameter", "nominal": 19.985, "tolerance": 0.015, "direction": -1,
         "distribution": "uniform"}
    ],
    "samples": 100000
}


def main(argv):
    parser = argparse.ArgumentParser(description="Tolerance stack-up from explicit JSON input (mm).")
    parser.add_argument("input", nargs="?")
    parser.add_argument("--example", action="store_true")
    parser.add_argument("--json", action="store_true", help="Alias for --report json")
    parser.add_argument("--report", choices=("md", "html", "json"), default="md")
    parser.add_argument("--summary", action="store_true", help="Compact result (full audit remains in JSON output)")
    parser.add_argument("--fail-on", choices=("nonconformance",), help="Exit 2 when worst-case limits fail the supplied requirement")
    a = parser.parse_args(argv[1:])
    if a.example:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False, allow_nan=False))
        return 0
    if not a.input:
        parser.error("provide a JSON file or use --example")
    try:
        data = json.loads(Path(a.input).read_text(encoding="utf-8"))
        result = analyse(data)
    except (ValueError, TypeError, KeyError, OSError, OverflowError) as exc:
        parser.error(str(exc))
    fmt = "json" if a.json else a.report
    text = report(result)
    if a.summary:
        w = result["worst_case"]
        text = f"{result['name']}: {w['min']} ... {w['max']} mm; {'PASS' if w['pass'] else 'FAIL'} (diameter/chain limits only)"
    if fmt == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    elif fmt == "html":
        print('<!doctype html><html lang="en"><meta charset="utf-8"><title>Stack-up report</title>'
              '<style>body{font:16px/1.6 system-ui;max-width:1000px;margin:40px auto;padding:20px}pre{white-space:pre-wrap}</style>'
              '<h1>Stack-up report</h1><pre>' + html.escape(text) + '</pre></html>')
    else:
        print(text)
    return 2 if a.fail_on and not result["worst_case"]["pass"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
