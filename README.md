# CAD Design Review

**An engineering-focused AI skill for reviewing mechanical parts, drawings, assemblies, tolerances, and manufacturability.**

The package is maintained in English. The skill is instructed to respond to users in the language of their request.

## What it reviews

- Manufacturing drawing and 3D part review based on the files actually supplied.
- ISO fits and tolerances, general tolerances, bearing fits, and GD&T.
- Tolerance stack-ups: worst-case, RSS, Monte Carlo, and sensitivity.
- Design for manufacturability (DFM) for machining, sheet-metal fabrication, injection molding, and progressive stamping.
- Drawing-data consistency and missing-information checks.

## Package contents

- `SKILL.md` — main skill instructions and review workflow.
- `references/` — technical guidance, checklists, schemas, and editable JSON rule/tolerance datasets.
- `scripts/` — deterministic DFM, tolerance, stack-up, and normalized drawing-data checks.
- `tests/` — lightweight regression/smoke tests.

## Installation

Copy the `cad-design-review` folder into the skills directory supported by your AI agent. The exact location and activation method depend on the agent. Consult that agent's documentation for its skills directory.

This package follows the portable Agent Skills folder convention: a `SKILL.md` file with YAML frontmatter plus optional scripts and reference resources. See [Agent Skills](https://agentskills.io/). Compatibility depends on the host agent's implementation and its ability to read bundled resources and execute Python scripts.

## Quick validation

Requires Python 3.

```bash
python -m py_compile scripts/*.py tests/*.py
python tests/test_smoke.py
python -c "import json, pathlib; [json.loads(p.read_text(encoding='utf-8')) for p in pathlib.Path('references').glob('*.json')]"
```

## Example commands

```bash
python scripts/check_dfm.py --example sheet_metal > part.json
python scripts/check_dfm.py part.json
python scripts/check_dfm.py part.json --json
python scripts/check_dfm.py --example progressive_stamping > stamped_part.json
python scripts/stackup.py --example > stackup.json
python scripts/stackup.py stackup.json
```

## Engineering limitations

This skill provides advisory design-review findings, not certified proof of compliance. It does not automatically parse STEP, PDF, or DXF files; `check_drawing_data.py` validates normalized JSON produced by a separate parser or extraction adapter. DFM limits are heuristics unless supported by an approved company or supplier specification. Standards editions and contractual requirements must be verified against authoritative, current copies. Final approval belongs to the responsible engineer and manufacturing specialist.

## Language behavior

All package documentation, scripts, and bundled rule descriptions are written in English. User-facing questions, explanations, findings, and reports should follow the language used in the user's request.

## License and third-party material

Original project code and documentation are released under the [MIT License](LICENSE).
