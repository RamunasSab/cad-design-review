# Changelog

## Unreleased

### Added
- Added five ready-to-copy English review prompts in `prompt-templates/`: progressive stamping, sheet-metal cutting and bending, machining, plastic injection molding, and additive manufacturing / 3D printing.
- Included editable input fields, documentation and dimension-chain checks, worst-case tolerance stack-ups with minimum/maximum values, process-specific DFM checks, and explicit evidence and coverage limitations.

### Improved
- Integrated closed-chain and duplicate-dimension screening into the core drawing-review workflow, including actual dimension references, view scales, tolerance overrides, and reference-only dimensions.
- Added `references/dimension-chains-and-symmetry.md` with worst-case minimum/maximum rules for functional open chains, asymmetric intervals, shared-variable cancellation, rounding, and redundant-constraint limitations.
- Added guidance on functional datums, median planes, centring versus size, full-width/half-width redundancy, and free-state versus restrained inspection.
- Updated all five templates to request reports in the language of the user's request.
- Preserved existing Python utilities and numeric reference datasets; these changes strengthen review instructions and do not add automatic CAD parsing.

### Documentation
- Added README links to all five templates and instructions for selecting, completing, and using them with available CAD/drawing files.
- Clarified that template reports follow the language of the user's request unless another output language is explicitly chosen.
- Clarified that the additive-manufacturing template provides manual DfAM guidance without adding automated DfAM rules.

### Project presentation and contributor support
- Added a README quick start, tag-pinned stable installation, and explicit stable/main channel guidance.
- Added a reproducible clearance-review example with original and revised JSON inputs.
- Added test, release, and MIT badges, CONTRIBUTING.md, and issue forms for installation problems, engineering findings, and feature requests.
- Recorded scoped hosted-Codex checks and a user-reported Claude AI example; kept Claude Code and clean CLI installation claims unverified.
- Added an agent-compatibility overview, documented a correction to the Claude AI recommendation, and clarified FAQ and manual additive-manufacturing coverage.

### Maintenance
- Upgraded actions/checkout and actions/setup-python to v6, using Node.js 24; the updated workflow completed successfully.

## 1.5.0 – Expanded process coverage and review controls

- Expanded manufacturing-process identification and review guidance, including additive manufacturing (FDM/FFF, SLA/DLP, SLS, MJF, and metal powder-bed fusion).
- Added a process-coverage distinction: additive-manufacturing guidance is currently manual and is not evaluated by `scripts/check_dfm.py`.
- Refined the process-selection workflow so the skill reuses process information already present in the user's message, supplied files, or conversation context instead of asking redundant questions.
- Clarified automatic file-scope selection and cross-checking of STEP, PDF, and DXF data, including part/revision correlation and the limits of comparing flat-pattern and formed geometry.
- Added A–D evidence/confidence levels and stronger requirements to distinguish calculated, parsed, visually assessed, and engineering-judgement findings.
- Expanded guidance for CNC machining, injection molding, sheet-metal cutting/bending, additive manufacturing, coatings, materials, and process-dependent manufacturing risks.
- Reclassified generic numeric DFM values as screening heuristics unless supported by a verified standard, approved company requirement, or supplier capability specification.
- Clarified hole-to-bend distance measurement convention and removed the unverified electroless-nickel thickness value from the generic coating table.
- Preserved existing automated JSON rule IDs, formulas, schemas, and calculation logic; no new additive-manufacturing automation is claimed.
- Clarified that geometry checks must not be reported as measured unless an appropriate parser/CAD measurement tool was actually used.

## 1.4.0 – Public GitHub release preparation

- Added MIT license, security policy, Git ignore rules, and automated GitHub Actions checks.
- Expanded the README with installation, validation, compatibility, and engineering-limitations guidance.
- Translated the remaining localized JSON rule descriptions and tolerance-dataset text into English without changing numeric data, rule IDs, formulas, or schema keys.
- Translated user-facing script output and documentation where applicable; retained calculation logic.


## 1.3.0 – English-language public release

- Translated skill instructions, documentation, reference guides, rule descriptions, and user-facing tool messages into English.
- Explicitly require all user-facing responses to follow the language of the user's request, regardless of the English language of the skill package.
- Removed generated Python bytecode/cache files from the distribution.
- Preserved the existing review workflow, calculation logic, rule identifiers, and data structures.

## 1.2.0 – Automatic file-scope selection

- Removed the requirement to provide STEP, PDF, and DXF together.
- Selects STEP, PDF, and DXF review scope from the files actually supplied.
- Treats PDF and DXF as exports of the same SolidWorks drawing rather than independent mandatory sources.
- Allows DXF as the only 2D source when required dimensions and text are retained; otherwise requests PDF only for missing information.
- `check_drawing_data.py` selects scope automatically and reports specific missing capabilities.
- Added DXF-only and STEP+PDF tests.

## 1.1.0

- Added progressive-stamping DFM module and preliminary rule JSON.
- Supports partial review without all three file formats; requires scope and limitations to be declared.
- Added DFA/assembly, materials, coatings, heat treatment, and quality-readiness checklists.
- Expanded DXF/PDF/STEP data-quality and cross-file validation.
- Added `check_drawing_data.py` for normalized extraction validation.
- `check_dfm.py`: uses safe AST expression evaluation instead of `eval`; reports unknown feature types as not evaluated; added progressive-stamping process.
- `stackup.py`: removed assumed Cpk=1.33; requires Cpk for normal distribution and treats uniform distribution as an explicit preliminary assumption; added input validation.
- Added smoke/regression tests.

## Notes

This release does not implement automatic STEP/DXF/PDF parsing. `check_drawing_data.py` validates JSON supplied by a separate extraction adapter. DFM limits are guidelines unless supported by an approved company or supplier specification.
