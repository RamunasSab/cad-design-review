# Manufacturing Technology Rules and Capability Guidance

This document provides general engineering guidance. It is not a substitute for a company process specification, supplier capability data, or a recognized standard. Do not report a general guideline as an ISO requirement.

## General review principles
- Match tolerances to functional need and demonstrated process capability.
- Identify the manufacturing process before applying process-specific limits.
- Consider material grade, condition, thickness, feature size, production volume, tooling, and inspection method.
- If a required input is unknown, mark the finding `NEEDS_CLARIFICATION`.
- Use `RISK` for a plausible concern that requires engineering judgement; use `NONCONFORMANCE` only when a defined requirement is clearly violated.

## Machining
Review tool access, cutter/drill availability, depth-to-diameter ratios, internal radii, thin walls, workholding, number of setups, thread details, achievable tolerances, and surface finish. Confirm limits with the machine shop.

## Sheet metal
Review bend radius, minimum flange length, hole-to-bend distance, reliefs, rolling direction, springback, flat-pattern accuracy, burrs, and coating allowances. Confirm values against material and tooling data.

## Injection molding
Review nominal wall thickness, wall transitions, ribs, bosses, draft, radii, gates, weld lines, venting, shrinkage, warpage, ejection, and undercuts. Confirm material-specific limits with the mold maker. See `injection-molding.md` and `iso-20457.md`.

## Progressive stamping
Review strip layout, carrier bridges, pilots, station sequence, slug evacuation, burr direction, forming strain, springback, and die access. These checks generally require strip-layout and tool data, not just the part model. See `progressive-stamping.md`.

## Other processes
For casting, welding, additive manufacturing, forging, and other processes, provide only general observations unless a dedicated validated process guide is available. Clearly state the limits of the review.
