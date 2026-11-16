# Standard provenance and supported claims

| Area | Actual basis | Supported claim |
|---|---|---|
| Fit/general/bearing lookup | Bundled historical source: DIN 7157:1966, DIN ISO 2768:1991, DIN 5425-1:1984 as documented in SKILL.md | Lookup only entries present; verify governing project edition separately |
| Plastic TG lookup | DIN 16742:2013-derived data | Not a verified reproduction of ISO 20457:2026 tables |
| GD&T guidance | ISO 1101 / ASME concepts as requested by the project | Manual review; no automated edition-specific conformance certification |
| DFM rules | Supplier/general heuristic sources recorded in JSON; edition often unavailable | Preliminary risk screening, not an ISO requirement |
| Snap-fit | Supplier design guide, edition/date unestablished | Manual geometry/material evidence review; no universal material limits |

Record the project-specified standard and edition in review input and reports. Missing or unverified editions are clarification items. There is no implemented edition selector: offering one would imply alternative verified datasets that are not supplied. Do not silently apply a current edition to historical tables.
