# Sheet Metal Design for Manufacturability Review

Use this guide for sheet-metal parts made by laser cutting, punching, bending, or related fabrication. Numerical limits are stored in `sheet-metal-rules.json`; treat them as preliminary guidance unless confirmed by the material supplier and manufacturing company.

## Required inputs
Material standard and grade, temper/condition, thickness and tolerance, rolling direction, bend direction, inside bend radius, production volume, machine/tooling constraints, and the applicable company standard. Missing critical inputs must be marked `NEEDS_CLARIFICATION`.

## Geometry and cutting
- Check minimum hole and slot sizes relative to thickness and available tooling.
- Check hole-to-edge, hole-to-bend, slot-to-bend, and feature-to-feature distances.
- Avoid sharp internal corners and narrow tabs that may tear, distort, or be difficult to cut.
- Check contour closure, duplicate entities, self-intersections, and scale in the flat-pattern DXF.
- Confirm that dimensions, centre lines, and annotations are not included in the cutting contour.

## Bending
- Check inside bend radius against material, thickness, temper, and rolling direction.
- Check minimum flange length against the selected punch and V-die opening.
- Check bend reliefs, corner reliefs, and feature interference near bend zones.
- Consider springback, bend allowance, bend deduction, and K-factor using validated supplier/company data; do not treat them as universal constants.
- Check whether bends collide with tools or adjacent features during forming.

## Tolerances and assembly
- Compare achievable tolerances with the selected process and supplier capability.
- Consider distortion, accumulated bend tolerances, coating thickness, and assembly stack-up.
- Verify formed-part interfaces and functional datums.

## Surface and finishing
- Specify burr direction and maximum burr height where functionally important.
- Ensure burrs do not interfere with assembly, sealing, electrical insulation, or operator safety.
- Consider dimensional changes from deburring, grinding, plating, painting, or other finishing.

## Data limitations
A part STEP file alone may not reveal the actual tooling, bend sequence, machine setup, or nesting plan. Mark these items `NEEDS_CLARIFICATION` unless the relevant process data is supplied.

## Recommended finding format
For each finding, state the feature/location, risk mechanism, evidence, missing information, recommended design change, and confidence level.
