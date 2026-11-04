# Injection Molding Design for Manufacturability Review

Use this guide for thermoplastic injection-molded parts. Numerical limits are stored in `injection-molding-rules.json`; they are general recommendations and must be confirmed for the polymer, mold, and supplier.

## Workflow
1. Identify nominal wall thickness `w`, polymer grade, and whether it is amorphous (e.g. PC, ABS) or semi-crystalline (e.g. PA, PE). If polymer class is unknown, mark applicable checks `NEEDS_CLARIFICATION`.
2. If normalized feature data is available, run `python scripts/check_dfm.py part.json` with `"process": "injection_molding"`. Example: `python scripts/check_dfm.py --example injection_molding`.
3. If only a drawing or model is available, measure what can be established, explicitly list what cannot be measured, and perform a qualified manual review.
4. Review items not covered by the script, then report using the format in `SKILL.md`.

## Key design checks
- Keep wall thickness as uniform as practical; avoid abrupt thickness changes and heavy solid sections.
- Review ribs: thickness relative to wall, height, base radius, and draft.
- Review bosses: wall connection, support ribs, draft, core design, and risk of sink marks.
- Provide adequate draft for the polymer, texture, and mold surface.
- Use generous transitions and radii to reduce stress concentrations and improve filling.
- Review holes, slots, side actions, undercuts, shut-offs, and parting-line placement.
- Consider gate location, flow length, weld lines, air traps, venting, packing, cooling, and ejection.
- Assess shrinkage, warpage, fibre orientation, and dimensional stability.
- Confirm that cosmetic and functional surfaces are compatible with the mold split and ejection strategy.

## Tolerance considerations
Use `iso-20457.md` for TG guidance. Do not apply metal fit/tolerance tables to plastic features without justification. Tight tolerances require material shrinkage data, process capability evidence, and agreement with the molder.

## Cost and risk
Flag unnecessary side actions, complex cores, deep thin ribs, difficult ejection, uneven wall sections, high cosmetic demands, and tolerances tighter than demonstrated capability.

## What a part model cannot establish
A STEP model alone cannot reliably establish gate design, cooling layout, venting, mold construction, process window, or actual Cpk. Mark these items `NEEDS_CLARIFICATION` and identify the required mold/process data.
