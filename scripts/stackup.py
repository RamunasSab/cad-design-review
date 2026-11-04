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
import json
import math
import random
import sys

DEFAULT_SAMPLES = 100_000


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
    if cpk <= 0:
        raise ValueError(f"{c.get('name', '?')}: Cpk must be > 0")
    return t / (3.0 * cpk)


def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def analyse(data):
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
        if c.get("direction") not in (1, -1):
            raise ValueError(f"{c.get('name', '?')}: direction must be +1 or -1")
        if float(c["tolerance"]) < 0:
            raise ValueError(f"{c.get('name', '?')}: tolerance must not be negative")

    nominal = sum(c["direction"] * float(c["nominal"]) for c in cs)

    # 1) Worst-case analysis
    wc_t = sum(abs(float(c["tolerance"])) for c in cs)
    wc_min, wc_max = nominal - wc_t, nominal + wc_t
    wc_pass = wc_min >= lo and wc_max <= hi
    wc_margin = min(wc_min - lo, hi - wc_max)

    # Implementation note (English translation required for public distribution).
    rss_t = math.sqrt(sum(float(c["tolerance"]) ** 2 for c in cs))
    sigmas = [_sigma(c) for c in cs]
    sigma = math.sqrt(sum(s * s for s in sigmas))
    mean = nominal
    p_out = 1.0 - (_norm_cdf((hi - mean) / sigma) - _norm_cdf((lo - mean) / sigma)) if sigma > 0 else (
        0.0 if lo <= mean <= hi else 1.0)
    cpk_assy = min((hi - mean) / (3 * sigma), (mean - lo) / (3 * sigma)) if sigma > 0 else float("inf")

    # 3) Monte Carlo analysis
    n = int(data.get("samples", DEFAULT_SAMPLES))
    if n < 1:
        raise ValueError("Monte Carlo samples must be >= 1")
    rng = random.Random(int(data.get("seed", 12345)))  # fixed seed -> reproducible results
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
        sens.append({"contributor": c["name"], "variance_percent": round(share, 1),
                     "worst_case_percent": round(wc_share, 1)})
    sens.sort(key=lambda r: r["variance_percent"], reverse=True)

    return {
        "name": data.get("name", "Tolerance stack-up"),
        "requirement": {"min": lo, "max": hi},
        "nominal_result": round(nominal, 6),
        "worst_case": {"min": round(wc_min, 6), "max": round(wc_max, 6),
                       "tolerance": round(wc_t, 6), "pass": wc_pass, "margin": round(wc_margin, 6)},
        "rss_classic": {"tolerance": round(rss_t, 6), "min": round(nominal - rss_t, 6),
                        "max": round(nominal + rss_t, 6)},
        "statistical": {"mean": round(mean, 6), "sigma": round(sigma, 6),
                        "min_3sigma": round(mean - 3 * sigma, 6), "max_3sigma": round(mean + 3 * sigma, 6),
                        "percent_out_of_spec": round(p_out * 100.0, 4), "cpk": round(cpk_assy, 3)},
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
        f"Statistical (Cpk): σ={s['sigma']}, ±3σ: {s['min_3sigma']} ... {s['max_3sigma']}, "
        f"out of specification {s['percent_out_of_spec']} %, assembly Cpk {s['cpk']}",
        f"Monte Carlo (N={m['samples']}): mean {m['mean']}, σ {m['sigma']}, "
        f"min {m['min_observed']}, max {m['max_observed']}, out of specification {m['percent_out_of_spec']} %",
        "",
        "Contributor impact (variance %, worst-case %):",
    ]
    for row in r["sensitivity_ranking"]:
        lines.append(f"  {row['contributor']:<30} {row['variance_percent']:>6} %   {row['worst_case_percent']:>6} %")
    lines.append("")
    lines.append("Note: statistical results are meaningful only when process distributions and Cpk values are supported by real data and contributors are independent. A uniform distribution is a simplifying assumption, not evidence of process capability. Worst-case analysis remains a separate result.")
    return "\n".join(lines)


EXAMPLE = {
    "name": "Shaft-to-hole clearance",
    "requirement": {"min": 0.02, "max": 0.20},
    "contributors": [
        {"name": "Hole diameter", "nominal": 20.065, "tolerance": 0.065, "direction": 1,
         "distribution": "normal", "cpk": 1.33},
        {"name": "Shaft diameter", "nominal": 19.985, "tolerance": 0.015, "direction": -1,
         "distribution": "uniform"}
    ],
    "samples": 100000
}


def main(argv):
    if "--example" in argv:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    paths = [a for a in argv[1:] if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 1
    with open(paths[0], encoding="utf-8") as f:
        data = json.load(f)
    result = analyse(data)
    print(json.dumps(result, indent=2, ensure_ascii=False) if "--json" in argv else report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
