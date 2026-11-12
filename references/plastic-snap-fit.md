# Plastic snap-fit joint review

Use this manual assembly-review mode for two plastic parts joined by cantilever hooks, U-shaped arms, torsion latches, or annular snaps. Select the correct mechanical model before calculating. This is an assembly check, not a manufacturing-process code; do not pass `snap_fit` to `check_dfm.py`.

## Required evidence and scope gate

Request both of the following for a complete snap-fit assessment:
- An assembly STEP (.step/.stp) in the fully engaged position, retaining both mating parts as identifiable, separate bodies at their actual relative positions. Do not accept a fused solid as evidence of the interface.
- A section through each distinct critical snap-fit type, showing both parts together, the hook root and flexible arm, lead-in, retaining face, mating edge/recess, and adjacent walls. Prefer a dimensioned PDF with tolerances; accept a clearly identified section image for visual screening only.

Confirm matching revisions, units, section location, assembly direction, and whether geometry is free-state or deformed. Request free-state part geometry if the assembly represents deflected parts. A section through the hook alone is insufficient. A readable STEP does not establish that dimensions or collisions have been measured: use an actual CAD parser/kernel for numerical geometry claims.

If either required input is missing or unreadable, explicitly request it, mark the affected checks `NEEDS_CLARIFICATION`, and report only the limited checks supported by available evidence. Do not block unrelated drawing checks. Do not require DXF. If the environment cannot inspect STEP, disclose that limitation and request dimensioned sections for a reduced-scope review; do not call it a complete 3D assessment.

## Functional and material inputs

Establish separately for each part:
- Exact polymer grade, filler/reinforcement and proportion, conditioning/moisture state, and manufacturing process.
- Relevant supplier stress-strain or secant-modulus data and allowable strain for the actual grade, temperature, strain rate, and assembly cycles. Missing material data blocks strength/force acceptance, not geometric screening.
- Assembly direction and sequence; one-time or repeated joining; required assembly/disassembly cycles; detachable or permanent locking; release-tool access.
- Allowed insertion force, required retention load and direction, service life, temperature range, sustained loads, vibration, chemicals and humidity.
- Critical dimensions/tolerances, molding shrinkage/warpage allowances, locating surfaces, stops, intended gap/preload, and inspection state.

Never infer grade from STEP colour, substitute generic polymer properties, assume friction coefficients, or invent numeric acceptance limits.

## Review sequence

1. **Identify the joint.** Label each hook and mating feature; distinguish cantilever bending, U-arm bending, torsion, and annular deformation. State which parts can flex and how the surrounding structure supports them.
2. **Check the assembly path.** Assess lead-in geometry, maximum required deflection before engagement, space for that motion, nearby collisions, sequence and overtravel stops. A collision in rigid free-state CAD may be intentional snap interference; distinguish it from an impossible assembly path. An engaged STEP alone does not prove peak deflection or assembly feasibility.
3. **Review the flexible feature.** Inspect effective flexible length, thickness/width and taper, root radius and transition, stress concentrations, retaining-face angle, contact edges and local wall stiffness. Flag short/thick arms or sharp roots as risks, not automatic standards violations.
4. **Check engaged geometry.** Determine hook overlap, engagement depth, seating against stops, clearances, alignment and residual deflection. Assess whether the arm can recover after assembly. Where intentional preload exists, evaluate its functional need and time-dependent loss rather than automatically rejecting it.
5. **Build functional tolerance chains.** Independently calculate maximum assembly deflection, minimum retained overlap, and minimum/maximum seated gap or interference from verified dimensions. Include location/warpage effects where supported; account for shared variables and dependencies. Do not equate retaining overlap with required assembly deflection without tracing the actual contact path.
6. **Assess material response.** Compare predicted strain with grade-specific allowable data under the stated conditions. Consider notch sensitivity, fibre orientation, weld lines, moisture and temperature, creep/stress relaxation, fatigue and repeated release. Do not treat elongation at break as a universal allowable snap strain.
7. **Estimate forces only when supported.** State geometry/model, units, contact angles, friction evidence, material data and validity range. Distinguish arm-deflection force, insertion force and retention/disassembly force. Do not multiply one-hook force by hook count unless simultaneous engagement and load sharing are justified. Nonlinear contact, large deformation, complex supports or long-term behaviour may require FEA and physical tests.
8. **Review manufacturing and service.** For injection-molded parts assess mold opening, undercuts/side actions, draft, ejection-induced deflection, local thick sections, sink/void risks, gate/weld-line location when known, and release access. Keep process-specific checks conditional on the actual process.
9. **Report the result.** Use the standard findings table and A–D evidence levels. Separate geometric fit, short-term assembly strain, insertion force, retention and service life. Missing evidence is not a pass. Identify checks not performed, requested files/data and recommended prototype/force/cycle tests. The engineer retains approval responsibility.

## Calculation boundaries

Do not apply a straight, constant-section cantilever model to tapered, curved, U-shaped, torsional or annular features without justification. Verify equations and figure definitions in an accessible technical source before using them. For two flexible parts, determine their deflections from compatibility and stiffness/force response; equal deflection is justified only by approximately equal effective compliance, not merely the same polymer. State rigid-mate assumptions explicitly.

No new automatic snap-fit calculator or CAD parser is included. Existing stack-up utilities may evaluate verified dimensional chains, but they do not simulate deformation or contact.

## Technical source and provenance

Background: Bayer MaterialScience, *Snap-Fit Joints for Plastics — A Design Guide*, the user's supplied 26-page file `Plastic_Snap_fit_design.pdf` (edition/date not established).
Relevant PDF page positions:
- pp. 3–7: operating principle, joint types and rigid/flexible-mate assumptions.
- pp. 8–15: cantilever geometry, root transitions, strain, secant modulus and insertion-force considerations.
- pp. 18–23: torsion and annular models.
- p. 24: both mating parts elastic.

This guide is supplier engineering guidance, not a universal standard. Its short-term material examples are grade/condition-specific; its friction table describes plastics on steel and must not be silently applied to a plastic/plastic pair. Do not copy its figures, tables, or entire PDF into the MIT repository. This file is an original review checklist; it does not reproduce the source's proprietary datasets. The source PDF is not bundled and is not automatically available to an installed agent. If a calculation needs a source equation or property not supplied, request a readable authorized source or a current supplier datasheet rather than claiming to have accessed the Library file.
