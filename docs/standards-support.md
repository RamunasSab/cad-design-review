# Standard provenance and supported claims

| Area | Actual basis | Supported claim |
|---|---|---|
| Fits | Supplied ISO 286-1:2010, Tables 1–5, Figures 12–13, Annex B | Numeric and candidate subset, 0 < D ≤ 500 mm; no application table or full-standard certification |
| General tolerances | Historical DIN ISO 2768:1991 | Independent historical lookup, not ISO 286 data |
| Bearings | No application recommendation under ISO 286-1 | Historical bearing-fit lookup disabled; ask for functional limits |
| Plastic TG lookup | DIN 16742:2013-derived data | Not a verified reproduction of ISO 20457:2026 tables |
| GD&T guidance | ISO 1101 / ASME concepts as requested by the project | Manual review; no automated edition-specific conformance certification |
| DFM rules | Supplier/general heuristic sources recorded in JSON; edition often unavailable | Preliminary risk screening, not an ISO requirement |
| Snap-fit | Supplier design guide, edition/date unestablished | Manual geometry/material evidence review; no universal material limits |

Record the project-specified standard and edition in review input and reports. Missing or unverified editions are clarification items. There is no implemented edition selector: offering one would imply alternative verified datasets that are not supplied. Do not silently apply a current edition to historical tables.

