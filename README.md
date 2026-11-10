<p align="center">
  <img src="assets/cad-design-review-icon.png"
       alt="CAD Design Review"
       width="160">
</p>

# CAD Design Review

[![Tests](https://github.com/RamunasSab/cad-design-review/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/RamunasSab/cad-design-review/actions/workflows/tests.yml)
[![Latest release](https://img.shields.io/github/v/release/RamunasSab/cad-design-review)](https://github.com/RamunasSab/cad-design-review/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![skills.sh installs](https://skills.sh/b/ramunassab/cad-design-review)](https://skills.sh/ramunassab/cad-design-review/cad-design-review)

**A portable AI agent skill for reviewing mechanical drawings, tolerances, GD&T, and manufacturability.**

Use a structured engineering workflow and included Python tools to identify dimensional conflicts, manufacturing risks, and missing requirements.

## Quick start

Requires **Node.js 22.20+**, npm, and a compatible AI agent. Install the **stable v1.5.0 release** globally for all agents supported by the Skills CLI:

```bash
npx skills add RamunasSab/cad-design-review@v1.5.0 --global --all
npx skills ls --global
```

Look for `cad-design-review`, then restart your agent if it was already open. In the agent, ask it to use `cad-design-review` and paste this first check:

> Review this shaft-to-hole interface. Hole: 20.065 ± 0.065 mm; shaft: 19.985 ± 0.015 mm. Required diametral clearance: 0.020–0.200 mm. Calculate the worst-case clearance, report any verified nonconformance, and state what remains unchecked.

**Expected result:** clearance is **0.000–0.160 mm**, so the minimum-clearance requirement fails. No CAD parser is needed for this explicit dimensional input. See the [verified example and candidate correction](#example-review).

`--all` targets CLI-supported agents, not every AI application. File-reading and Python execution capabilities depend on the host. This skill does not install a CAD application or a STEP/PDF/DXF parser. Python 3 is only needed to run the bundled utilities.

[Find on skills.sh](https://skills.sh/ramunassab/cad-design-review/cad-design-review) · [Detailed installation](#installation) · [Stable release](https://github.com/RamunasSab/cad-design-review/releases/tag/v1.5.0) · [Report an issue](https://github.com/RamunasSab/cad-design-review/issues)

## Stable release and development version

| Channel | Contents | Documentation |
|---|---|---|
| **Stable: v1.5.0** | Published release, including expanded process guidance and evidence controls | [Release README](https://github.com/RamunasSab/cad-design-review/blob/v1.5.0/README.md) · [Release changelog](https://github.com/RamunasSab/cad-design-review/blob/v1.5.0/CHANGELOG.md) |
| **Development: main** | Stable functionality plus unreleased review guidance, five process prompt templates, and the demonstration linked below | This README · [Unreleased changes](CHANGELOG.md#unreleased) |

This README describes **main** unless a section says otherwise. An unpinned repository installation follows the default branch; it does not select the latest GitHub release. To try the current development version instead:

```bash
npx skills add RamunasSab/cad-design-review --global --all
```

Choose one channel. To reproduce v1.5.0, use the pinned command above and its tag-specific documentation. The five prompt templates and dimension-chain/symmetry additions are currently **main-only**, not part of v1.5.0. The example files below are also added on main; the stack-up utility they use already exists unchanged in v1.5.0.

## Example review

A nominal clearance of **0.080 mm** looks acceptable, but checking the permitted limits reveals a zero-clearance condition.

| Check | Original dimensions | Candidate correction |
|---|---|---|
| Hole diameter | 20.065 ± 0.065 mm | 20.085 ± 0.045 mm |
| Shaft diameter | 19.985 ± 0.015 mm | Unchanged |
| Worst-case diametral clearance | **0.000–0.160 mm** | **0.040–0.160 mm** |
| Requirement: 0.020–0.200 mm | **FAIL** | **PASS** for this dimensional check |

This is a constructed, reproducible example, not an assessment of the bundled CAD part. Both results were checked with the included Python utility and independent endpoint arithmetic. The candidate correction still needs manufacturing and functional validation.

[**Read the findings, evidence, limitations, and reproduction steps →**](examples/clearance-review.md)

## Key capabilities

- **Drawing and model review** — inspect available technical information, identify inconsistencies, and highlight missing or ambiguous requirements.
- **Fits and dimensional tolerances** — review ISO fits, general tolerances, bearing fits, and tolerance selection.
- **Geometrical tolerancing** — assess GD&T concepts, datum selection, feature control frames, and inspectability.
- **Tolerance stack-ups** — perform worst-case, RSS, Monte Carlo, and sensitivity analysis.
- **Dimension chains and symmetry (main-only additions)** — check closed chains and duplicate dimensions, calculate functional open-chain minimum/maximum limits, and assess functional datums and centring. See the [dimension-chain and symmetry guidance](references/dimension-chains-and-symmetry.md).
- **Design for Manufacturability (DFM)** — identify potential manufacturing risks for machining, sheet-metal fabrication, injection molding, and progressive stamping.
- **Structured engineering findings** — distinguish nonconformances, risks, clarification requests, and informational observations.
- **Multilingual interaction** — internal instructions and documentation are in English, while user-facing responses follow the language of the user's request.

## Who is it for?

CAD Design Review is intended for:

- Mechanical design engineers
- Product development engineers
- Manufacturing and process engineers
- CAD designers and technical drawing reviewers
- Engineering teams looking for a more consistent design-review workflow

It can be useful during design development, drawing release preparation, manufacturability assessment, and engineering documentation reviews.

## How it works

The skill guides an AI agent through a structured engineering review:

1. **Establish the context** — identify the manufacturing process, material, functional requirements, and available documentation.
2. **Inspect the supplied information** — review only the data that can actually be read or reliably extracted.
3. **Check engineering requirements** — assess dimensions, tolerances, fits, datums, GD&T, and manufacturing constraints where applicable.
4. **Run calculations** — use the included Python utilities for supported tolerance and DFM checks.
5. **Report findings** — explain potential issues, their significance, assumptions, and recommended follow-up actions.

Findings are separated into:

- `NONCONFORMANCE` — a clear conflict with a stated requirement.
- `RISK` — a potential engineering or manufacturing issue.
- `NEEDS_CLARIFICATION` — information is missing or ambiguous.
- `INFO` — an observation that may be useful to the reviewer.

## Manufacturing processes covered

| Process | Review focus |
|---|---|
| Machining | Fits, dimensional tolerances, geometric features, and machining DFM |
| Sheet-metal fabrication | Thickness, bends, holes, cut-outs, and fabrication DFM |
| Injection molding | Plastic part design, molding constraints, and ISO 20457 tolerance considerations |
| Progressive stamping | Strip and part design considerations, tooling-related risks, and process DFM |
| Additive manufacturing / 3D printing | Manual DfAM guidance; no automated rules in `check_dfm.py` |

Coverage and available checks vary by process and by the information supplied.

## Prompt templates

**Development / main only:** these five templates are not included in v1.5.0.

Ready-to-copy English review prompts are available in [`prompt-templates/`](prompt-templates/):

| Manufacturing process | Template |
|---|---|
| Progressive stamping | [progressive_stamping.md](prompt-templates/progressive_stamping.md) |
| Sheet-metal cutting and bending | [sheet_metal_cutting_and_bending.md](prompt-templates/sheet_metal_cutting_and_bending.md) |
| Machining | [machining.md](prompt-templates/machining.md) |
| Plastic injection molding | [plastic_injection_molding.md](prompt-templates/plastic_injection_molding.md) |
| Additive manufacturing / 3D printing | [additive_manufacturing_3d_printing.md](prompt-templates/additive_manufacturing_3d_printing.md) |

### Using a template

1. Open the template for your manufacturing process and copy its contents.
2. Replace the bracketed fields with known material, process, and functional requirements. Leave unknown inputs marked as “unknown.”
3. Paste the prompt into your AI agent with CAD Design Review available, and attach the files you have. STEP, PDF, and DXF are not all required.
4. Review the findings, assumptions, and checks that could not be completed.

The templates cover documentation, dimensions, datums, closed dimension chains, worst-case tolerance stack-ups with minimum/maximum results, and process-specific manufacturing risks. Actual checks depend on the supplied data and the host environment's tools.

The templates request reports in the language of your request unless you explicitly choose another output language. Their English source text does not require English output. Additive-manufacturing review is manual DfAM guidance; it is not automated by `scripts/check_dfm.py`.

## Agent compatibility

| Environment | Current evidence |
|---|---|
| Hosted Codex workspace | Partial utility, parser, and directed-review checks; see below |
| Claude AI | User-reported example: correct clearance calculation, one incorrect recommendation; tool logs unavailable |
| Claude Code | Not tested |

[Compatibility details and the corrected recommendation](docs/agent-compatibility.md). Claude AI results do not establish Claude Code compatibility. Clean CLI installation checks are deferred.

## Codex environment checks

Partial checks completed on **2026-11-10** in a hosted Linux workspace with Codex CLI **0.167.0-alpha.4** available. This is not an end-to-end CLI installation certification.

| Area | Observed result |
|---|---|
| Python utilities, smoke tests, and example calculations | Passed on Python 3.12.14 |
| Directed instruction-file review and Lithuanian output | Passed one fresh-agent case; automatic skill selection not tested |
| STEP / DXF import | Passed basic import with separately installed CadQuery/OCP and ezdxf |
| Skills CLI installation and subsequent Codex discovery | Not verified: npm package fetch blocked by workspace HTTP 403 |
| PDF, Windows, desktop, and IDE integration | Not tested |

[Detailed evidence, package versions, limitations, and remaining checks](docs/codex-validation.md). Parser availability is environment-specific; the skill does not include a CAD parser.

## Installation

CAD Design Review can be installed with the [Skills CLI](https://skills.sh/docs/cli), which downloads the skill from this GitHub repository and makes it available to compatible AI agents.

### Requirements

- **Node.js 22.20 or later**
- npm (included with Node.js)
- At least one AI agent supported by the Skills CLI

Check your installed versions:

```bash
node -v
npm -v
```

If Node.js is not installed or is outdated, download the current LTS release from [nodejs.org](https://nodejs.org/).

### Recommended: Stable release, global installation for all supported agents

Open a terminal (Windows PowerShell, Command Prompt, macOS Terminal, or a Linux shell) and run:

```bash
npx skills add RamunasSab/cad-design-review@v1.5.0 --global --all
```

For development additions described in this README, use the unpinned command in [Stable release and development version](#stable-release-and-development-version).

This command:

- Downloads CAD Design Review from the v1.5.0 tag in this public GitHub repository.
- Installs the skill for all agents supported by the Skills CLI.
- Uses **global scope**, making the skill available across your projects for your operating-system user account.
- Skips the interactive agent and skill selection prompts.

The repository currently provides one skill: `cad-design-review`.

**Important:** `--all` means all agents supported by the Skills CLI; it does not mean every AI application on your computer. An agent must support the Agent Skills format and be recognized by the CLI. Availability and activation behavior may vary between agents.

### Optional: Preview before installing

To list the skill or skills in the stable release without installing them, run:

```bash
npx skills add RamunasSab/cad-design-review@v1.5.0 --list
```

To use the interactive installation flow for the stable release instead, run:

```bash
npx skills add RamunasSab/cad-design-review@v1.5.0
```

The CLI will guide you through selecting the skill, compatible agent(s), and installation scope.

### Verify the installation

List globally installed skills:

```bash
npx skills ls --global
```

Look for `cad-design-review` in the output. If your AI agent was already open during installation, restart it so it can discover the newly installed skill.

### Updating

A tag-pinned installation selects a specific version. To move to a newer stable release, explicitly install its published tag. An installation from the unpinned repository follows the development channel. After updating, check the source/ref before assuming you are running a stable release.

To update globally installed skills, run:

```bash
npx skills update --global
```

To check whether installed skills have updates available:

```bash
npx skills check
```

### Uninstalling

To remove CAD Design Review from the global installation:

```bash
npx skills remove --global cad-design-review
```

### Installation scope and method

- **Global installation** makes the skill available across projects for the current operating-system user. It does not install the skill separately for every user account on the computer.
- The Skills CLI recommends **symlink installation** when supported. This keeps a canonical copy of the skill and links it to the agent's skill directory.
- If symbolic links are not supported or suitable in your environment, use the CLI's copy option when available.
- Installing this skill adds its instructions and supporting resources to the agent's skill directory. It does not install or modify a CAD application.
- The included Python utilities are separate from the skill installation. To run them, install Python 3 and use the commands in the [Included tools](#included-tools) section below.

For further details, supported-agent information, and additional CLI options, see the [Skills CLI documentation](https://skills.sh/docs/cli).

## Included tools

The repository contains:

- `SKILL.md` — main instructions and engineering review workflow.
- `references/` — technical guidance, checklists, schemas, and reference datasets.
- `scripts/` — Python utilities for supported DFM, tolerance, stack-up, and drawing-data checks.
- `examples/` — reproducible clearance review, original input, and revised input (main only).
- `prompt-templates/` — ready-to-copy review prompts for five manufacturing-process categories.
- `tests/` — lightweight smoke and validation tests. The `tests/` directory also includes STEP, DXF, and PNG files for the gearbox shaft test component, allowing quick manual verification.

### Running the Python utilities

Requires Python 3.

```bash
# Validate Python files
python -m py_compile scripts/*.py tests/*.py

# Run smoke tests
python tests/test_smoke.py

# Example DFM check
python scripts/check_dfm.py --example sheet_metal > part.json
python scripts/check_dfm.py part.json

# Example tolerance stack-up
python scripts/stackup.py --example > stackup.json
python scripts/stackup.py stackup.json
```

## Frequently asked questions

### Is this a SolidWorks add-in?

No. It is an AI agent skill with supporting Python utilities. It does not install into SolidWorks or modify a CAD application.

### Do I need Python?

Python 3 is needed to execute the bundled calculation utilities. The review instructions can also guide an agent without Python, provided it clearly states which calculations and checks were actually performed.

### Can it automatically measure STEP, PDF, and DXF files?

The repository does not include automatic CAD/drawing parsers. Numerical geometry inspection requires suitable tools in the host environment. Being able to attach a file does not establish that its geometry, dimensions, or tolerances were read.

### Which version should I use?

Use the pinned stable installation for v1.5.0. Use the unpinned repository for current main additions. Check the [channel table](#stable-release-and-development-version) before choosing; documentation and examples on main may not exist in the stable snapshot.

## Important limitations

CAD Design Review is an engineering support tool, not a replacement for professional engineering judgement.

- It does not independently guarantee that a design complies with every applicable standard.
- It does not automatically parse STEP, PDF, or DXF files. File inspection depends on the host environment and available parsing tools.
- `check_drawing_data.py` validates normalized JSON data supplied by a separate parser or extraction adapter.
- DFM recommendations may be heuristic and should be checked against actual process capability, tooling, supplier requirements, and company standards.
- Standards editions, clauses, and contractual requirements must be verified against authoritative, current sources.

Always verify critical findings before approving a design or releasing it for manufacturing. Final approval remains the responsibility of the qualified engineer and relevant manufacturing specialists.

## Language behavior

The skill's internal instructions, technical documentation, and bundled descriptions are maintained in English. User-facing questions, explanations, findings, and reports should follow the language used in the user's request.

## License and reference materials

The repository includes an MIT license. Before reusing or redistributing bundled reference datasets or material derived from external standards and publications, verify the applicable rights, permissions, and attribution requirements. Public accessibility of a source does not automatically grant redistribution rights.

---

## Contributing and feedback

See [CONTRIBUTING.md](CONTRIBUTING.md) for reporting guidance, contribution steps, and validation commands. Use the [issue forms](https://github.com/RamunasSab/cad-design-review/issues/new/choose) for installation problems, incorrect engineering findings, or feature requests.

The Tests badge reports the Python compilation, smoke tests, and reference-JSON validation in the workflow; it is not certification of engineering correctness or agent compatibility.
