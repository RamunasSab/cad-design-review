# Fits, general tolerances and bearing fits

## Fit source and scope

Use **ISO 286-1:2010** for fit designations, basis systems, deviations and signed clearance/interference calculations. The supplied edition is the sole source for fit selection in this development version. DIN 7157 series and application tables have been removed; do not reuse them as ISO recommendations.

- Clauses 4.3.2 and Tables 1–5: IT values, fundamental deviations and hole delta corrections.
- Clause 5.3.4, Figures 12–13: preferable combinations for hole/shaft basis; framed combinations are first choice for economic reasons. This is not a DIN first/second series classification.
- Clauses 5.3.2 and 5.3.5, Annex B.2–B.4: establish functional minimum/maximum differences, then filter combinations numerically. Do not claim a bearing, sliding, locating or force requirement is satisfied from its name alone.

## Commands

```sh
python scripts/check_tolerances.py fit H7/g6 --size 20 --json
python scripts/check_tolerances.py recommend --basis hole --type clearance --size 40 --min 0.024 --max 0.092 --json
```

Units are mm at the interface; source IT/deviation values are in µm. Both requirement bounds use signed **hole minus shaft** differences: positive is clearance, negative is interference. For an interference magnitude of 0.010–0.030 mm, enter `--min -0.030 --max -0.010`. Bounds are inclusive. A class without a size is only a membership inquiry and returns `NEEDS_CLARIFICATION` for calculation.

`C_min = hole_min - shaft_max`; `C_max = hole_max - shaft_min`. Classification uses actual limits, not a fixed classification attached to a letter. Zero-boundary cases may have zero clearance or zero interference.

## Verified implementation subset

The standard has more data than the implementation. `iso-286-1-2010.json` covers **0 < nominal size ≤ 500 mm**, grades IT5–IT11 and letters E/F/G/H/JS/K/M/N/P/R/S and lowercase equivalents, subject to explicitly unsupported hole IT5 delta cases. Candidate recommendations are a documented subset of Figures 12–13. Unsupported sizes/classes fail closed; absence of a candidate means **no match in this subset**, not that no ISO solution exists. Never extrapolate, invent application text, or silently use another edition. The original PDF is not distributed with this repository.

The module uses tabulated values rather than unrounded approximation formulas, applies the Table 2 M6 exception and 4.3.2.5 delta rules, and tests the three Annex B examples. Tests do not independently certify every transcription entry.

Size limits alone do not control form, orientation, location, coating, temperature or assembly forces. Confirm these separately under 5.3.2 and the project's GPS requirements. ISO 286-1 does not supply application-specific rolling-bearing selection rules.

## Other independent tolerance modules

General linear/angular/geometrical tolerances retain their historical DIN ISO 2768 source and plastic TG data retain DIN 16742 provenance. These are separate modules, not ISO 286-1 tables. The legacy bearing command is disabled for recommendations: request functional requirements rather than apply the former DIN 5425 fit table. See `docs/standards-support.md` for supported claims.
