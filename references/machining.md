# Machining Design for Manufacturability Review

Use this guide for milling, turning, drilling, boring, reaming, tapping, and related subtractive processes. Treat numerical limits as process guidance, not universal standards; confirm them with the machine shop.

## Required inputs
Material and condition, stock form and size, production volume, machine capabilities, workholding approach, required surface finish, tolerances, and inspection method.

## Feature accessibility
- Check whether every feature is accessible with a practical tool and setup.
- Identify deep/narrow pockets, long-reach tools, thin walls, small internal radii, and inaccessible undercuts.
- Avoid unnecessarily small internal corner radii; use radii compatible with standard cutters where possible.
- Check drill depth, chip evacuation, cross holes, and breakthrough conditions.
- Check tool approach and clearance for countersinks, counterbores, spotfaces, and threads.

## Turning features
- Check tool access to shoulders, grooves, reliefs, and internal bores.
- Provide thread runout and tool relief where required.
- Avoid slender workpieces and long unsupported features unless a suitable support strategy is defined.
- Consider achievable concentricity/runout and the number of setups.

## Threads and holes
- Use standard thread sizes and drills where practical.
- Specify thread class, depth, entry chamfer, and thread relief where relevant.
- Check minimum wall thickness around tapped holes and the risk of breakthrough.
- Do not assume a blind-hole depth equals usable thread depth.

## Tolerances and surface finish
- Match tolerance grade and surface finish to function and process capability.
- Avoid tight tolerances on non-functional features.
- Consider datum strategy, setup changes, thermal effects, and inspection access.
- Treat unsupported Cpk assumptions as `NEEDS_CLARIFICATION`.

## Cost drivers
Flag unnecessary setups, special cutters, deep pockets, tight tolerances, fine finishes, non-standard threads, and difficult workholding.

## Data limitations
CAD geometry does not prove machine capability, workholding stability, cutting parameters, or inspection feasibility. Request process details when they materially affect the conclusion.
