# Mechanical Design Review Checklist

This checklist supplements process-specific DFM rules. It does not replace calculations, testing, or company design standards.

## Function and interfaces
- Is the part function and its critical contact surfaces clearly defined?
- Do datums reflect the actual assembly and inspection method?
- Do critical dimensions and GD&T control function, not geometry alone?
- Is there sufficient clearance for motion, thermal expansion, coatings, and assembly variation?
- Is unintended over-constraint avoided?

## Assembly and serviceability (DFA)
- Can the part be installed only in the correct orientation (poka-yoke), or are orientation features provided?
- Are fasteners, tools, and cables accessible?
- Is the assembly sequence feasible without temporary deformation or undocumented special tools?
- Are fasteners standardized, and is thread engagement justified for the material and load?
- Can wear parts be replaced or serviced without dismantling the entire assembly?

## Materials and surfaces
- Is the material specified by standard, grade, condition/temper, and direction where relevant?
- Is compatibility with loads, temperature, corrosion, chemicals, and environment assessed?
- Are coating type, thickness, coverage, masking, and dimensional effects specified?
- Are heat treatment and hardness specified where required?
- Are surface finish and edge requirements limited to functionally relevant areas?

## Structural integrity
- Have loads, stresses, fatigue, vibration, impact, temperature, and deformation been considered?
- Are abrupt section changes, stress concentrations, and unnecessary sharp corners avoided?
- Are wall/thickness changes compatible with the selected process?
- Are safety factors and calculation assumptions documented?
- Are FEM results supported by valid loads, boundary conditions, mesh convergence, and validation?

## Drawing and document control
- Are part number, revision, title, material, scale, projection, and sheet numbering consistent?
- Do STEP, PDF, and DXF represent the same revision?
- Are the general tolerance standard and class stated, and is the current company edition confirmed?
- Are ambiguous, duplicate, conflicting, or redundant dimensions avoided?
- Is an inspection method or control characteristic defined for critical dimensions?
- Does the change history explain what changed and why?

## Manufacturing and quality readiness
- Do the selected process and supplier capabilities suit the geometry and tolerances?
- Are critical/significant characteristics (CTQ/SC) identified where applicable?
- Are inspection strategy, measurement equipment, and acceptance criteria defined?
- Are Cp/Cpk requirements stated only when agreed and supported by data?
- Are first article inspection (FAI), material certificates, and tests planned where required?

## Limits of the review
Functional purpose, loads, environment, material certificates, actual manufacturing capability, and measurement systems are often not visible in CAD files. In such cases, ask for the missing information or mark `NEEDS_CLARIFICATION` rather than making a categorical claim.
