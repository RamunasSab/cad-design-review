# Dimension chains, derived limits, and symmetry

## Establish the evidence

- Map each dimension to its actual referenced surfaces, edges, centres, or theoretical intersections. Record view, direction, units, displayed nominal, upper/lower deviations, source, and confidence.
- For DXF, account for view scale, dimension-style scale factors and per-entity overrides. Read both explicit dimension text and native tolerance data without applying a tolerance twice. Verify against the rendered drawing.
- Distinguish projected dimensions from true lengths, flat patterns from formed geometry, and local detail axes from part datums. Do not join endpoints merely because they share one coordinate across unrelated views.
- Use the displayed nominal for drawing acceptance calculations. If the underlying geometry has more precision, disclose significant rounding and nominal inconsistencies rather than silently changing the drawing requirement.

## Closed chains and duplicate requirements

- Treat an independent path of dimensions plus a dimension controlling the same endpoints/direction as a closed chain. Verify topology before claiming a loop. Separate direct linear loops from dependencies involving angles, radii, tangency, symmetry, or model-defined geometry.
- Check repeated requirements across views for differing tolerances. Reference dimensions in parentheses are informational and are not independent acceptance constraints.
- Compare nominal closure and interval consistency. A redundant loop is a documentation or inspection risk unless it demonstrably violates an applicable requirement; it is not automatically impossible to manufacture.
- Example: 11 +/-0.10 + 1 +/-0.05 + 9.5 +/-0.05 permits a sum of 21.30 to 21.70 mm. An additional 21.5 +/-0.10 requirement restricts that sum to 21.40 to 21.60 mm. Both requirements can be met, but not every contributor combination passes.
- Recommend removing a redundant dimension or making it reference-only according to function. Do not automatically discard the tight functional requirement.

## Open chains and worst-case limits

For L = sum(a_i * x_i), with each x_i in [l_i, u_i]:
- L_min = sum(min(a_i*l_i, a_i*u_i)).
- L_max = sum(max(a_i*l_i, a_i*u_i)).
- For symmetric deviations +/-t_i: L_nom = sum(a_i*n_i), T = sum(abs(a_i)*t_i), limits = L_nom +/-T.
- For subtraction, reverse the contributing interval: (A-B)_min = A_min-B_max; (A-B)_max = A_max-B_min. Support unilateral and asymmetric deviations explicitly; do not force them into a symmetric tolerance about the original nominal.
- Combine repeated instances of the same variable algebraically before accumulation. A shared baseline cancels in an appropriate difference. Two separately dimensioned features with equal nominal sizes are not automatically the same variable.
- The difference between two independently toleranced baseline coordinates includes both coordinate tolerances, not all intervening dimensions.
- Label unconstrained interval sums as conservative bounds when redundant constraints or dependencies also apply. Where tighter guaranteed limits are needed, solve all relevant constraints together using a validated method; never claim a standalone chain's extremes are simultaneously achievable under all drawing requirements.
- Report only functional or geometrically meaningful chains: location, equation, nominal, contributor limits, result minimum/maximum in mm, assumptions, and acceptance requirement if supplied. Distinguish level differences from actual free surface clearances.
- Use scripts for multi-step calculations. Use the existing stack-up utility for its supported schema; do not invent Cpk or statistical process data. Keep worst-case acceptance distinct from RSS/Monte Carlo estimates.

## Symmetry and functional datum strategy

- A visually symmetric shape or centreline expresses nominal intent; it does not alone define a datum establishment method or a numerical centring tolerance.
- Determine which surfaces or holes actually locate the part in service. Distinguish a drawn axis from a datum derived from a physical feature or feature pattern.
- Compare edge-chain dimensioning with baseline coordinates from a functional median plane. Prefer the latter where left/right alignment is functional; retain local widths, clearances, and critical feature sizes.
- Do not retain a toleranced full width and both toleranced half-widths as independent controls. Likewise avoid replacing a chain with redundant coordinates and an independently toleranced spacing unless the requirements are intentional.
- Do not halve a full-width tolerance and assign it to each side without a defined centring requirement. A specified width controls size; feature position requires an appropriate additional control where function demands it.
- Do not infer equal side gaps from a difference in widths. Show the total residual, and report individual side gaps only when the centring/position relationship is specified.
- Propose datum-related position or profile controls with theoretically exact dimensions when appropriate, but do not invent tolerance values without assembly clearance and inspection requirements. Treat ISO and ASME systems separately.
- Explain whether a proposed redimensioning preserves, tightens, or relaxes the original acceptance envelope. Address free-state versus restrained inspection for flexible formed parts.

## Report additions

Provide a closed-chain/duplicate table and a separate derived-limit table when relevant. Label each result as verified, conditional, or blocked. State evidence confidence and remaining geometry/inspection assumptions. Identify non-calculated chains rather than implying full coverage.
