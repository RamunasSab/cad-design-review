# Contributing to CAD Design Review

Contributions to documentation, review workflows, calculation utilities, and reproducible examples are welcome.

## Report an issue

Search [existing issues](https://github.com/RamunasSab/cad-design-review/issues) before opening a new one. Choose the relevant [issue form](https://github.com/RamunasSab/cad-design-review/issues/new/choose):

- **Installation problem:** exact commands, error output, skill version, agent, operating system, Node.js/npm versions, and installation scope.
- **Incorrect engineering finding:** minimal input and prompt, actual output, expected result, units, requirement/source, and affected feature or rule.
- **Feature request:** the engineering problem, proposed behavior, applicability, and how success could be verified.

If a version or input is unknown, say so. A small anonymized example is usually more useful than a complete project. English is preferred for shared documentation; issue reports may be written in your language.

Issues and attachments are public. Remove credentials, personal information, customer identifiers, and proprietary drawing/CAD data. Share only content you are entitled to publish. Report vulnerabilities using [SECURITY.md](SECURITY.md), not a public issue.

## Propose a change

1. For a substantial workflow or calculation change, open an issue to explain the problem and approach.
2. Fork the repository and create a focused branch from `main`.
3. Make the smallest coherent change and describe its user-visible effect.
4. Update relevant documentation/examples. Add a meaningful regression test when fixing calculation logic or a repeatable bug.
5. Run the checks relevant to your change and open a pull request against `main`. Include the rationale, validation performed, and remaining limitations.

Keep repository documentation and internal instructions in English. Preserve user-facing responses in the language of the user's request.

## Engineering evidence

- Separate supplied facts, parsed/measured data, calculations, visual assessments, and engineering judgement.
- State dimensions, units, signs, tolerance conventions, process/material assumptions, and rule applicability.
- Distinguish an explicit requirement from a screening heuristic. Do not present a generic DFM guideline as a verified standards violation.
- For standards references, identify the edition and clause when verified. Do not invent references or include restricted standard text or tables.
- Explain changes to numeric datasets, formulas, schemas, and rule IDs explicitly. Provide a reproducible before/after result for calculation changes.
- Do not claim CAD geometry was measured unless a suitable parser or CAD tool was actually used.

## Validation

For Python, rule-data, or numeric-example changes, run from the repository root with Python 3:

```bash
python -m compileall -q scripts tests
python tests/test_smoke.py
python -c "import json, pathlib; [json.loads(p.read_text(encoding='utf-8')) for folder in ('references', 'examples') for p in pathlib.Path(folder).glob('*.json')]"
```

For the clearance demonstration:

```bash
python scripts/stackup.py examples/clearance-input.json --json
python scripts/stackup.py examples/clearance-revised.json --json
```

Compare the worst-case results with [the documented example](examples/clearance-review.md). Statistical estimates are not measured process capability.

For documentation-only changes, check Markdown structure, relative links, and stable/main version statements. For issue forms, check YAML syntax, unique field IDs, required fields, and the GitHub form schema.

The existing CI checks Python compilation, smoke tests, and reference JSON parsing. It does not certify all engineering rules, CAD parsing, issue-form rendering, or compatibility with every agent.

## Versions and contribution rights

New contributions land on `main` and are not part of an existing release until a new release is published. Do not move release tags to include later changes.

Contribute only original material or material you have permission to redistribute under compatible terms. The project's MIT license does not itself grant redistribution rights to third-party standards or source datasets.
