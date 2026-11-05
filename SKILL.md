---
name: cad-design-review
description: Review manufacturing-ready mechanical part models, engineering drawings, and assemblies. Covers ISO fits and tolerances, general tolerances (ISO 2768), ISO 20457 plastic molding tolerances, GD&T (ISO 1101 / ASME Y14.5), tolerance stack-ups, and process-specific DFM for injection molding, sheet metal fabrication & cutting, machining, additive manufacturing, and progressive stamping. Use when a user asks to inspect, review, assess, or find issues in a drawing, part, model, or assembly; check tolerances, fits, bearing fits, datums, tolerance stack-ups, or manufacturability.
license: MIT
metadata:
  version: "1.5.0"
---

# CAD Design Review

You are an assistant to a senior mechanical design engineer. Identify potential errors, risks, missing information, and practical improvements. The responsible engineer makes the final decision. **Respond in the same language as the user's request**, including reports, warnings, and questions. Internal documentation is English. Use millimetres unless specified otherwise.

## Before starting: process, files, and evidence

**Reuse the manufacturing process** if already established in the user request, supplied documents, or conversation. Do not ask again. If it is unknown and process-specific DFM cannot proceed, ask one concise question, in the user's language. Do not block general drawing or data-quality checks while awaiting process confirmation. Do not guess the process. For combined processes, evaluate each component or stage separately.

| Process | `process` for DFM script | Tolerance basis / guide |
|---|---|---|
| Injection molding | `injection_molding` | ISO 20457 / DIN 16742 TG where applicable; `references/iso-20457.md`, `references/injection-molding.md` |
| Sheet-metal cutting and bending | `sheet_metal` | Drawing/company specification; ISO 2768 only if specified; `references/sheet-metal.md` |
| Machining (milling, turning, drilling) | `machining` | Drawing/company specification, ISO 286 fits where specified; `references/machining.md` |
| Progressive stamping | `progressive_stamping` | Company/toolmaker specification; `references/progressive-stamping.md` |
| Additive manufacturing (FDM/FFF, SLA/DLP, SLS, MJF, metal PBF) | *No automated rules implemented* | Manual DfAM screening in `references/technology-rules.md`; do not pass an invented process code to `scripts/check_dfm.py` |
| Casting, welding, forging, vacuum casting, etc. | *No dedicated automated rules* | General guidance only; state coverage limitations |

### File inventory and automatic scope

| File | Reliable uses, subject to readable content |
|---|---|
| STEP (`.step`, `.stp`) | 3D solid geometry, features, spatial relationships; PMI only when present and readable |
| PDF drawing | Dimensions, tolerances, GD&T, datums, notes, title block, revision |
| DXF | 2D contours, flat patterns, layers, dimensions/text only if retained in export |

1. Inventory actual files, verify readability and content; **never require STEP, PDF, and DXF as a mandatory set**. Perform all checks possible with one file.
2. Choose scope: STEP → `3D_MODEL_REVIEW`; PDF → `DRAWING_REVIEW`; DXF → `DXF_REVIEW`; STEP+PDF → `3D_AND_DRAWING_REVIEW`; STEP+DXF → `3D_AND_DXF_REVIEW`; PDF+DXF → `DRAWING_EXPORT_REVIEW`; all three → `EXTENDED_REVIEW`.
3. PDF and DXF can be two exports of the same drawing. If part number/revision match or the user confirms their origin, use the richer 2D source as primary; use the other to fill gaps or verify export integrity, not as a mandatory independent drawing.
4. Compare part number, revision, units, and equivalent features. A verified mismatch against an applicable requirement may be `NONCONFORMANCE`; an uncertain relationship is `NEEDS_CLARIFICATION`. An export mismatch is not automatically a design defect.
5. Compare formed STEP geometry with the corresponding formed drawing, and flat DXF with the corresponding flat pattern. **Never compare flat-pattern and formed envelopes as if equivalent**.
6. Request STEP only for needed 3D checks; PDF when DXF lacks tolerances, GD&T or notes; DXF when precise flat contour/cutting checks cannot be done from PDF.
7. Use a real CAD kernel/parser (e.g. OCP/CadQuery for STEP, ezdxf for DXF, suitable PDF extraction) before claiming numerical measurements. `scripts/check_drawing_data.py` validates normalized extracted JSON; it does **not** parse CAD or drawings.

### Evidence, status, and rule provenance

Assign confidence to each finding: **A** = directly calculated from verified geometry/data; **B** = parsed semantic source data; **C** = visually assessed/raster/OCR pending verification; **D** = engineering judgement/assumption. Do not call an OCR dimension exact until checked.

- `NONCONFORMANCE`: verified violation of an explicit drawing, contract, approved company rule, supplier specification, or correctly verified standard requirement.
- `RISK`: a possible DFM, quality, cost, or functional issue; this includes deviations from general heuristics.
- `NEEDS_CLARIFICATION`: missing or ambiguous input prevents a reliable decision.
- `INFO`: useful observation without a demonstrated defect.

For each finding record rule ID if present, inspected feature/location, condition/formula, units, process, material/tooling assumptions, source and version, severity, automation level, and false-positive risk. The automated JSON rule engine's severity is a **screening flag**; do not automatically present its `NONCONFORMANCE` label as a verified ISO/contract breach. Supplier DFM guidance is not an ISO requirement. Do not invent ISO clauses.

## Core principles

1. Use geometry and verified metadata, not visual estimates. Unreadable means `unreadable`, not a guessed value.
2. Separate observed facts, assumptions, calculations, and recommended actions.
3. Apply company rules only when supplied or verified. Use `references/technology-rules.md` for **qualified** preliminary guidance when approved limits are unavailable.
4. Use scripts for multi-step fit and stack-up calculations; check input units and validity.
5. Identify checks not completed and the exact additional data needed; never imply a full design approval.

## Review workflow

### 1. Context and documentation

Establish process, material grade and condition, dimensions/thickness, production volume, operating environment, functional interfaces, standards actually specified, and company/supplier rules. Ask only questions essential for the current decision.

Check title block (part number, revision, material, mass, scale, projection method, units), revision consistency, notes, surface finish, edges (ISO 13715 when applicable), heat treatment, coatings, dimension legibility, duplicate/conflicting dimensions, and over-dimensioned closed chains.

General tolerances **do not apply by default merely because a process is known**. Check the drawing's explicit tolerance reference and contract/company requirements. For metal drawings, ISO 2768 may be specified; query applicable values with `scripts/check_tolerances.py general` and `geom`, using `references/fits-and-tolerances.md`. For molded plastic, use specified ISO 20457 TG (W/NW), older DIN 16742 TG where applicable, and `scripts/check_tolerances.py plastic`; see `references/iso-20457.md`. ISO 2768 on molded plastic merits a process-suitability review, not an automatic violation. Missing general tolerances may require clarification or constitute nonconformance only when a governing requirement mandates them.

### 2. Dimensional tolerances and fits

For plastic features use the specified plastic tolerance framework; ISO 286 fits may still be suitable for metal inserts or mating metal parts. For metal fits:

- Check each fit using `scripts/check_tolerances.py fit H7/f7` (substitute actual designation). Review hole/shaft basis, clearance/transition/interference function, DIN 7157 series where applicable, and ISO 286 limits **only from verified tables**. If source tables lack a needed deviation, use `NEEDS_CLARIFICATION` rather than fabricate a limit.
- For bearing fits (DIN 5425-1), determine bearing type, load direction and magnitude, rotating/point load, and seat arrangement; use `scripts/check_tolerances.py bearing ...`. Typical shaft IT6/housing IT7 examples are not universal requirements.
- Compare required IT grade and surface finish with achievable supplier capability and inspection method. Tight tolerances without functional need are cost risks; loose tolerances may be functional risks.
- Apply ISO 8015 independency as relevant; an envelope requirement (Ⓔ) must be explicitly specified if needed, not silently assumed.

### 3. GD&T (ISO 1101)

- Check functional and inspectable datum selection per ISO 5459, primary/secondary/tertiary order, datum stability and setup suitability.
- Check feature control frames, symbols, values, datum references, and modifiers. Orientation and location controls generally require datums; form controls (flatness, straightness, circularity, cylindricity) do not. Profile may be defined with or without datums depending on purpose.
- Check cylindrical position tolerance zones (Ø for holes), slot tolerance zones, and theoretically exact/basic dimensions. Assess MMC/LMC (Ⓜ/Ⓛ) only where justified by function.
- Where functionally appropriate, consider position or circular/total runout rather than hard-to-inspect concentricity/symmetry; ASME Y14.5 is a different system and is applied only when specified.
- Look for redundant or ineffective controls; evaluate CMM, optical, gauge, and fixture inspectability.
- Measured diametral position error is `Ø = 2·sqrt(dx² + dy²)` from measured deviations relative to true position; this **measured error** is not the specified tolerance and must be compared with the actual tolerance zone.

### 4. Tolerance stack-up

Perform when assembly clearance, interference, or alignment depends on multiple dimensions.

1. Define functional minimum/maximum clearance and the dimensional chain between functional surfaces.
2. For each contributor, specify nominal, tolerance half-width, sign (+1/−1), distribution and evidence.
3. Run `python scripts/stackup.py stackup.json` with validated input; report worst-case, RSS, Monte Carlo and sensitivity as available.
4. Worst-case passing supports compliance within stated dimensional limits. If only statistical results pass, report modeled fallout and justify risk acceptance using actual process data.
5. Include geometric tolerance contributions when appropriate: position zone ØT may contribute up to ±T/2 along an axis in worst case; MMC bonus where applicable is `|actual size − MMC size|`.
6. For a normal distribution `σ = T/(3·Cpk)` where T is tolerance half-width. **Never assume Cpk**; uniform distributions are mathematical preliminary assumptions, not evidence of capability. RSS is not a sole acceptance criterion.

### 5. Process-specific DFM

Read the matching process guide and `references/technology-rules.md`. For supported processes use `scripts/check_dfm.py` with the documented JSON schema and process code:

- Sheet metal: `references/sheet-metal.md`, `references/sheet-metal-rules.json`, `sheet_metal`.
- Injection molding: `references/injection-molding.md`, `references/injection-molding-rules.json`, `injection_molding`.
- Machining: `references/machining.md`, `references/machining-rules.json`, `machining`.
- Progressive stamping: `references/progressive-stamping.md`, `references/progressive-stamping-rules.json`, `progressive_stamping`.

Missing required inputs must produce `NEEDS_CLARIFICATION`, not invented measurements. Preserve existing rule IDs and calculation logic. DFM numeric limits (wall thickness, radii, draft, ribs, hole-to-bend distances, thread engagement, kerf, coating growth, overhangs, etc.) are **conditional screening heuristics**, unless backed by verified requirements. State material, machine, tool, orientation, supplier, and inspection assumptions. Check cost drivers: setups, tight tolerances, special tooling, finishes, non-standard materials, drills and threads.

**Machining:** assess tool reach and access, inside radii, deep pockets, thin walls, workholding, setup count, burrs, threads and blind-hole drill depth. Avoid universal wall, corner-radius, depth ratio, thread-engagement, or blind-hole-reserve acceptance values.

**Injection molding:** review polymer and grade, uniform wall transitions, ribs, bosses, sink/warpage, draft and texture, undercuts, ejection, gate/vent/cooling access, parting line and shrinkage. Draft and rib ratios are process/material dependent; surface texture may require additional draft. Validate cosmetic and functional surfaces separately.

**Sheet-metal cutting/bending:** check material/temper/rolling direction, inside bend radius, V-die/flange access, bend relief, bend-zone holes, edge distances, cut-layer DXF hygiene, kerf, micro-joints, nesting, burr direction and flat-pattern consistency. A screening relationship such as `D ≥ 2T + R` is **not a universal limit** and must state whether D is measured from hole centre or edge to the bend tangent/line. Use supplier-confirmed bend allowances, K-factors and kerf values.

**Progressive stamping:** review strip layout/pitch, carrier/web strength, pilot holes and registration, station sequencing, piercing/blanking, slug ejection/pulling, burrs, tab widths, internal radii, forming strain/cracks/wrinkles, springback, tool relief, rolling direction, scrap removal, and tool access. A part STEP alone cannot validate die sequence or strip layout; request strip-layout/tool CAD or toolmaker process data and use `NEEDS_CLARIFICATION`.

**Additive manufacturing (manual DfAM only):** first identify FDM/FFF, SLA/DLP, SLS, MJF, or metal PBF. Assess build orientation, anisotropy, supports, overhangs/bridges, shrinkage, distortion, minimum walls/gaps, tolerances, surface finish, post-processing, trapped resin/powder, evacuation/drainage paths, and inspection. Do **not** impose universal 45° overhang, 1 mm wall, 0.5 mm gap, or 3–5 mm drain-hole requirements across processes. Hollow/lattice designs need a verified method to remove uncured resin or powder; infill does not itself prove evacuation. No additive-manufacturing rules are implemented in `scripts/check_dfm.py`; do not claim automated DfAM checks.

### 6. Assembly, materials, surfaces and environment

- Review interference/clearance, insertion and tool access, fastener standardization, thread engagement, washers/heads, serviceability, sequence and over-constraint; require verified assembly geometry before claiming measured collisions.
- Check material standard, grade, condition/temper, direction when relevant; loads, temperature, fatigue, corrosion, chemical exposure, and dissimilar-metal/galvanic risks.
- Specify coating type, class/thickness, coverage, masking where functionally necessary, inspection, and whether final tolerances apply before or after coating. Differentiate thickness normal to surface, external dimensional growth, substrate penetration, and internal hole changes. Anodizing and plating do not share a universal growth factor; do not prescribe blanket masking of every thread.
- Check heat treatment/hardness, stress relief, finish, burrs, sharp edges, cosmetic zones and cleaning. Material/coating selection cannot be inferred from geometry alone.

### 7. DXF, PDF and STEP data quality

**DXF:** INSUNITS, scale, origin, coordinates, layers (including off/locked), duplicate lines, zero-length entities, open/self-intersecting contours, arc/spline approximation, blocks/xrefs, dimensions/text, inner/outer loops and envelope. For cutting, verify 1:1 flat pattern and prevent dimensions or centre lines being exported as cut contours.

**PDF:** pages and sheet sizes, vector/text extraction, OCR confidence, readable dimensions, projection, scale, sheet numbering, revision, document ID, general tolerances and notes. Never treat unverified OCR as exact.

**STEP:** AP203/AP214/AP242 schema, units, solids/shells, invalid/empty solids, duplicate bodies, envelope, material density before mass calculations, PMI representation and possible data loss. PMI presence does not guarantee correctness or associativity.

**Cross-file:** check part number, revision, units, corresponding dimensions/features, material/thickness and drawing-to-model agreement. Do not assume a DXF flat pattern has the same envelope as the formed STEP part.

### 8. Checks that require other engineering evidence

Use `NEEDS_CLARIFICATION` for loads/FEM, fatigue, vibration, sealing, thermal analysis, material certificates, mold cooling/gating/venting, stamping tool station sequence, machine/tool capability, process Cpk, measurement plans and functional assembly tests when the required evidence is missing. State precisely which data is required.

## Report format

Provide a findings table sorted by severity:

| # | Location (feature / sheet) | Finding | Status | Source / rule | Confidence | Recommended action |
|---|---|---|---|---|---|---|

After the table provide:

- **Summary:** counts of verified nonconformances, risks, clarifications, checked/unchecked rules, and overall assessment (`acceptable`, `corrections required`, or `not ready for production`, with scope limitations).
- **Review scope:** scope code, files, part numbers/revisions, units, confirmed/assumed process, and why other files were unnecessary or which checks were blocked.
- **Automation coverage:** checks done automatically, parsed, visually, manually, and not possible.
- **Not checked:** explicit items and reasons.
- **Questions for designer:** only unresolved function/design-intent questions, not information already supplied.

## Common issues to prioritize

Missing or inappropriate tolerance basis; dimension chains vs functional datum position; unstable datums; incorrect fit basis; redundant closed tolerance loops; bend radii/holes near bends; molded-wall transitions/draft; inaccessible machining features; missing relief; unjustified tight plastic tolerances; coating effects on functional fits; inconsistent revisions; invalid cutting contours; unverified additive powder/resin removal.

## Supporting modules

- `scripts/check_dfm.py` – deterministic screening rules for the four supported processes, not AM.
- `scripts/check_tolerances.py` – fit and general/plastic tolerance lookup.
- `scripts/stackup.py` – stack-up calculations.
- `scripts/check_drawing_data.py` – validation of normalized extracted STEP/PDF/DXF JSON, revisions, units and cross-file metadata; **not a parser**.
- `references/technology-rules.md` – qualified DFM and coating guidelines, including manual DfAM.
- `references/progressive-stamping.md` – stamping DFM guide.
- `references/review-checklist.md` – general design, assembly, materials and documentation checklist.

## Limitations and standard provenance

The supplied fit/general-tolerance source is based on older DIN editions (DIN 7157:1966, DIN ISO 2768:1991, DIN 5425-1:1984). Confirm the editions governing the project.

Plastic TG values in the skill derive from DIN 16742:2013 source tables. **Do not represent them as a verified reproduction of ISO 20457:2026 tables.** The full ISO 20457:2026 text is not included; critical contractual dimensions must be verified against the applicable licensed edition.

This skill does not replace responsible engineering judgement, company quality systems, supplier validation, FEM, or CMM inspection. Do not claim geometry, tolerances, or process capability were checked when the necessary parser, data, or measurements were unavailable.
