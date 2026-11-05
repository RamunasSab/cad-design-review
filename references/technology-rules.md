# Process-Specific DFM Rules & Engineering Reference Guidelines

## Purpose and status

This document provides practical screening guidance. Unless a value is explicitly tied to a verified standard, approved company requirement, or supplier capability specification, it is **not a universal acceptance limit** and must not be presented as an ISO requirement.

- `NONCONFORMANCE`: a verified drawing, contractual, company, or standard requirement is clearly violated.
- `RISK`: a plausible concern requiring engineering or supplier confirmation.
- `NEEDS_CLARIFICATION`: required process, material, geometry, tooling, or functional information is missing.
- Do not convert a general guideline into `NONCONFORMANCE` solely because a nominal value falls outside it.

Identify the actual process, material and condition, thickness, feature geometry, orientation, production volume, tooling, and inspection method before applying a rule. If a material input is unknown, request clarification.

## Process identification

1. **CNC machining:** milling, turning, drilling; assess tool access, workholding, setups, radii, pocket depth, thin walls, threads, and inspection.
2. **Injection molding:** assess polymer, nominal wall, transitions, ribs, bosses, draft, texture, shrinkage, warpage, gates, venting, ejection, and undercuts.
3. **Sheet metal:** assess material/temper, thickness, rolling direction, bend tooling, bend radius, flange length, reliefs, cutting process, kerf, burrs, and flat pattern.
4. **Progressive stamping:** assess strip layout, carrier bridges, pilots, station sequence, slug evacuation, burr direction, forming strain, springback, and die access.
5. **Additive manufacturing:** identify FDM/FFF, SLA/DLP, SLS, MJF, or metal powder-bed fusion (PBF). These technologies do not share one set of minimum feature, overhang, clearance, or powder/resin removal limits.
6. **Other processes:** for casting, welding, forging, vacuum casting, etc., provide general observations only unless a dedicated validated guide is available.

---

## 1. CNC machining DFM

### Tool access, internal radii, and pockets
- Avoid sharp internal corners that a rotating cutter cannot reproduce. Select radii based on cutter diameter, tool reach, material, finish, and mating-part requirements.
- Consider dog-bone or T-bone reliefs when square mating components must fit into milled pockets; verify that reliefs do not compromise strength or sealing.
- A pocket depth-to-width ratio around 4:1 is an early warning threshold for standard tooling, not a universal limit. Greater ratios may require long-reach tools, special strategies, or additional operations.
- Check narrow slots, deep cavities, undercuts, and inaccessible faces against the actual machine/tool envelope.

### Thin walls and workholding
- Do not apply one minimum wall thickness to all metals or plastics. Assess material, wall height/span, cutting forces, clamping, residual stress, tool strategy, and allowable distortion.

### Threads and blind holes
- Specify thread standard, nominal size, pitch, tolerance class, full thread depth, drill depth, entry chamfer, and bottom clearance.
- Engagement ratios such as approximately 1.0d for some steels and 1.5d or more for some lower-strength materials are preliminary estimates only. Actual engagement depends on both material strengths, thread form, load, lubrication, failure mode, and manufacturing method.
- A nominal 75% thread engagement is a common tap-drill convention in many applications; do not claim a universal pull-out-strength percentage or torque reduction from it.
- For blind tapped holes, distinguish full thread depth from total drill depth. Account for drill-point geometry, tap lead, chip accumulation, and the selected tap. A 25% or 0.5d reserve may be an initial estimate where appropriate, not a universal requirement.
- Confirm drawing callout notation against the applicable standard and company practice.

### Setups and cost
- Minimize reorientations where practical, but do not impose a universal maximum setup count. Review workholding, datum transfer, deburring/inspection access, and whether tight tolerances are functionally justified.

---

## 2. Injection molding DFM

### Wall thickness and transitions
- Aim for reasonably uniform nominal wall thickness and core out thick solid sections where feasible to reduce sink, voids, and differential cooling.
- The supplied draft lists the following indicative wall ranges. Actual limits depend on resin grade, additives, flow length, gate, process settings, tool design, and supplier capability.

| Polymer | Indicative nominal wall range |
|---|---:|
| ABS | 1.15–3.5 mm |
| Polycarbonate (PC) | 1.0–4.0 mm |
| Nylon (PA66) | 0.8–3.0 mm |
| Polypropylene (PP) | 0.8–3.8 mm |

- Do not apply a universal ±15% wall-thickness variation limit. Amorphous and semi-crystalline polymers, flow length, geometry, and cosmetic requirements can justify different limits.
- Evaluate abrupt wall transitions, thick junctions, ribs, bosses, and local mass concentrations for sink, voids, weld lines, and warpage.

### Ribs, bosses, radii, and draft
- Rib thickness around 50–60% of nominal wall is a common initial guideline, not a universal limit. Rib height, spacing, base radius, and draft must be reviewed together.
- A rib height around 3× wall thickness and a base radius around 0.25–0.50× wall thickness are preliminary checks only.
- Draft around 1–2° per side can be a starting point for some untextured walls. Required draft depends on wall depth, polymer, shrinkage, texture, polish, and ejection direction.
- Texture-related draft increments are texture- and supplier-specific.
- Review inner/outer radii, boss support, core pins, undercuts, slides/lifters, gate location, venting, cooling, ejection, and parting line.
- Specify SPI/VDI finish by the applicable designation and approved sample/specification. Do not infer a guaranteed Ra value from a finish label unless the applicable source defines it.

### Tolerances
- Use the applicable edition of ISO 20457 and specified tolerance group where contractually required. Older DIN 16742 data must not be represented as current ISO 20457 data.
- Consider shrinkage, anisotropy, moisture conditioning, post-mold conditioning, and warpage before assigning tight tolerances.

---

## 3. Sheet-metal fabrication, cutting, and bending DFM

### DXF preparation
- Check units, scale, layer visibility, duplicate/overlapping entities, zero-length segments, open contours, self-intersections, stray points, blocks/xrefs, and contour closure.
- Separate cutting geometry from dimensions, centre lines, text, and title-block content. Confirm whether the DXF is a flat pattern or formed profile.
- Do not compare a flat-pattern envelope directly with a formed STEP envelope.

### Bending and feature clearances
- Select inside bend radius from material grade/temper, thickness, rolling direction, grain direction, tooling, and supplier bend tables. A radius near 1×T is only a preliminary starting point for some materials.
- Check flange length, bend-to-bend spacing, relief geometry, springback, cracking, distortion, and punch/die access against the actual tooling.
- When using a preliminary hole-to-bend expression such as `D >= 2T + R_inside`, define `D` explicitly as **hole-centre to bend-line distance**. If measuring from the hole edge, convert using the hole radius. Confirm with the material, hole size, bend tooling, and supplier.
- Do not apply a universal hole-to-edge or hole-to-hole minimum without a defined process/material basis.
- Add bend reliefs where needed; size them for the material and tooling rather than applying a fixed width/depth blindly.

### Cutting and kerf
- Laser and waterjet kerf depend on material, thickness, equipment, parameters, and required cut quality. Values such as 0.2–0.4 mm for some laser operations or 1.0–1.2 mm for some waterjet operations are illustrative only.
- Use the supplier's actual kerf compensation, minimum hole/slot size, corner radius, pierce/lead-in, micro-joint, and edge-quality limits.
- Review burr direction/height, heat-affected zone, dross, distortion, nesting, and cut sequence where relevant.

---

## 4. Additive manufacturing / 3D printing DFM

### Mandatory technology split
Do not review "3D printing" as one generic process. Establish at least:
- FDM/FFF (material extrusion)
- SLA/DLP (vat photopolymerization)
- SLS (polymer powder-bed fusion)
- MJF (multi-jet fusion)
- Metal powder-bed fusion (e.g. LPBF/PBF-LB)

If the exact process, material, machine, or build orientation is unknown, use `NEEDS_CLARIFICATION` for process-dependent limits.

### Orientation, overhangs, and bridges
- Review orientation for support volume, surface quality, dimensional accuracy, anisotropic strength, thermal distortion, and post-processing access.
- A 45° overhang value is a common screening heuristic for some FDM and selected resin/metal workflows. Angle conventions differ (horizontal/build-plate versus vertical), and the actual limit varies by machine, material, feature length, and parameters.
- SLS/MJF powder supports the part during the build; do not apply FDM-style support-angle rules to them. Trapped powder removal remains a separate concern.
- Bridge limits are process-dependent. A 5 mm value may be a cautious FDM screening value for some setups; it is not a universal limit for SLA, SLS, MJF, or metal PBF.
- Consider chamfers or teardrop-shaped horizontal channels where they reduce support or improve internal surface quality.

### Walls, holes, gaps, and tolerances
- There is no universal 1.0 mm minimum wall. Check machine/material capability, supported versus unsupported wall condition, wall span, orientation, load, and post-processing.
- Set moving/mating clearances by process, material, orientation, finish, shrinkage, and intended fit. Validate critical clearances with a coupon or supplier test where appropriate.
- Printed holes and threads may require drilling, reaming, tapping, inserts, or other post-machining.
- Do not assume one build axis is always unsuitable for precision holes. Consider stair-stepping, anisotropy, support marks, distortion, and post-machining.

### Powder and resin evacuation
- Enclosed SLS/MJF cavities need a practical route for loose powder removal; SLA/DLP cavities need drainage and cleaning for uncured resin. Metal PBF channels/cavities need process-specific powder-removal and inspection planning.
- Opening count, diameter, and location depend on cavity volume, channel geometry, material, access, and supplier cleaning capability. "Two holes of 3–5 mm" is not a universal rule.
- Lattice/infill structures may reduce mass or change stiffness, but do **not** replace powder/resin evacuation paths and can make cleaning more difficult.
- Consider trapped material, inaccessible internal surfaces, drain orientation, inspection, and post-processing.

### Strength and post-processing
- Review load direction relative to build layers, fatigue, creep, temperature, chemical compatibility, surface finish, support removal, stress relief, heat treatment, machining allowances, and inspection.
- Do not infer structural suitability from printability alone. Material properties are machine-, parameter-, orientation-, and post-process-dependent.

---

## 5. Progressive stamping DFM

Use `progressive-stamping.md` and `progressive-stamping-rules.json`. Treat automated limits as preliminary heuristics, not universal ISO requirements. Confirm carrier/web dimensions, pilots, forming radii, burr limits, station sequence, slug evacuation, and press/tool capability with the stamper/toolmaker. A part STEP model alone usually cannot verify strip layout or die sequence.

---

## 6. Coating thickness and dimensional impact

Specify coating thickness by the applicable process standard, supplier specification, or drawing requirement. Distinguish coating thickness normal to the surface, external dimensional growth, internal dimensional reduction, and substrate penetration/reaction.

The following are indicative values from the supplied draft, not guaranteed process limits:

| Finish / coating | Indicative per-surface value in supplied draft | Review action |
|---|---:|---|
| Type II anodizing | +0.005–0.010 mm | Verify coating class/thickness and dimensional growth; recheck precision fits. |
| Type III hard anodizing | +0.025–0.050 mm | Confirm oxide thickness and growth/penetration ratio with the anodizer. |
| Powder coating / liquid paint | +0.060–0.150+ mm | Obtain supplier's specified range; mask functional interfaces where required. |
| Electroless nickel | No generic value specified | Obtain deposit thickness and tolerance from the plating specification; do not use an unverified numeric value. |

For threads, bearing seats, electrical contacts, grounding points, sealing faces, and precision mating surfaces, specify coating coverage, masking/plugging, post-machining, or allowance only as required by function and the agreed process. Do not impose blanket masking on every threaded hole without checking the coating and thread requirements.

---

## 7. Automation coverage and reporting

The current `scripts/check_dfm.py` rule engine has rule files for machining, injection molding, sheet metal, and progressive stamping. It does **not** contain an additive-manufacturing rule set. Additive checks in this document are manual engineering guidance unless a future validated rule set is added.

For every finding, state feature/location, rule or heuristic, evidence, units, material/process assumptions, source, severity, confidence, and recommended action. State whether it was calculated by a script, measured from geometry, extracted from a document, visually assessed, or based on engineering judgement. Never claim a STEP/DXF/PDF measurement unless the required parser or measurement tool was actually used.

If required information is missing, report `NEEDS_CLARIFICATION`; do not guess. Confirm process-dependent limits with the responsible supplier/toolmaker before production release.
