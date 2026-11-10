# Agent compatibility status

These records distinguish utility execution, directed instruction use, and actual product installation. They are not interchangeable.

| Environment | Evidence | Status |
|---|---|---|
| Hosted Codex workspace | Executed Python utilities, STEP/DXF parser checks, and one directed review | Partial validation; [detailed report](codex-validation.md) |
| Claude AI | User supplied a review response on 2026-11-10 | Basic calculation correct; recommendation review partially failed |
| Windows Skills CLI copy installation | User supplied a successful clone, discovery of one skill, and copy-install transcript on 2026-11-10 | Installation reported successful; agent activation not tested |
| Claude Code | No actual session tested | Not tested |
| Codex CLI clean installation | Package download blocked in hosted workspace; user-side testing deferred | Not verified |

## Claude AI: user-reported case

The user clarified that the test was run in **Claude AI, not Claude Code**. Model, product version, installed skill snapshot, and operating system were not recorded. Tool execution was described in the response, but raw tool logs were not supplied.

Input: hole 20.065 ± 0.065 mm, shaft 19.985 ± 0.015 mm, required diametral clearance 0.020–0.200 mm.

Observed in the supplied response:

- Correct minimum/maximum clearance: **0.000–0.160 mm**.
- Correct minimum-clearance nonconformance and Lithuanian response.
- Explicit evidence levels and unchecked-scope statements.
- Claimed reading of SKILL.md and execution of stackup.py; these are reported, not independently verified.
- An incorrect general recommendation: the response concluded that changing only the shaft could not solve the problem after evaluating one insufficient shaft reduction.

### Correction to the recommendation

Keeping the original hole limits of 20.000–20.130 mm, a candidate shaft specification of **19.965 ± 0.015 mm** gives shaft limits of 19.950–19.980 mm:

- Minimum clearance = 20.000 − 19.980 = **0.020 mm**.
- Maximum clearance = 20.130 − 19.950 = **0.180 mm**.

This satisfies the stated scalar dimensional requirement, so a shaft-only change can solve this example. It remains subject to the other functional/manufacturing requirements and has no extra minimum-clearance margin. No standard fit designation or production approval is implied.

Also distinguish statistical independence of random variables from the ISO 8015 independency principle; they are not the same concept.

**Assessment:** numeric case passed; recommendations partially failed. This observation does not establish a defect in the deterministic calculator, overall Claude AI compatibility, automatic skill activation, or Claude Code support.

## Reporting future checks

Record product name, version/model when available, operating system, skill tag/commit, prompt, source inputs, actual output, and relevant tool logs. Keep customer data and private files out of public reports. Prefer a minimal example and identify whether the skill was explicitly requested or selected automatically.

[Back to README](../README.md#agent-compatibility)
