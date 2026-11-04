# Progressive Stamping – Design for Manufacturability Review

This guide applies to sheet-metal parts made in a progressive die. It provides design-review guidance, not universal mandatory limits. Numerical rules must be confirmed by the stamper for the material, thickness, press, tooling, and operation sequence.

## 1. Required inputs
Material standard and grade, temper/condition, thickness and tolerance, rolling direction, strip/blank width if known, press direction, annual volume, press force, and die type. Mark missing information `NEEDS_CLARIFICATION`.

## 2. Contour and piercing geometry
- Small piercings, narrow slots, thin tabs, and small internal radii may weaken the punch or cause tool breakage.
- Check distances between holes, holes to outer edges, notches to edges, and narrow web widths.
- Identify sharp internal corners that require fragile or very small punch sections.
- Review piercing/blanking direction, burr side, and burr-height requirements.
- Check slug clearance and risks of slug pulling, slug stacking, or scrap jamming.

## 3. Strip layout and carrier
- Review part orientation in the strip, pitch, strip width, and material utilization.
- Carrier width and bridges must support the part until the cut-off operation.
- Check whether the geometry supports reliable piloting and registration at every station.
- Review station positioning errors and their accumulation.
- Distinguish pierced dimensions, formed dimensions, and dimensions measured after forming.

## 4. Forming operations
- Review forming, embossing, coining, and drawing strain, thinning, cracking, wrinkling, and springback.
- Check bend direction relative to rolling direction, minimum radius, and cracking risk.
- Confirm tool access, relief, and sequence feasibility.

## 5. Burrs, edges, and surface
- Specify preferred burr direction and maximum burr height where required.
- Check whether burrs affect assembly, contact, sealing, electrical insulation, or operator safety.
- If deburring or tumbling is planned, consider dimensional and edge changes.
- Coatings may affect dimensions and contact properties; define coated areas and masking.

## 6. Data not visible in a part STEP file
Strip layout, station sequence, die clearance, punch/die material and hardness, press force/speed, stripper design, pilots, scrap evacuation, and tool life require process/tool data. Mark these topics `NEEDS_CLARIFICATION`, not automatic nonconformance.

## 7. Recommended output
For each finding, state the feature/zone, risk mechanism, required additional information, recommended design change, and confidence level. The final decision must be confirmed by a stamping specialist.
