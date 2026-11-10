# Codex environment checks

## Result and scope

**Status: partial validation, not end-to-end Codex compatibility certification.**

Checked on **2026-11-10** against repository commit `e3e5c646ed26c87208b3a5ed122316b3ca10c1ae` on main. Files were retrieved through the GitHub connector, then executed in the hosted Linux workspace. This was not a clean installation through the Skills CLI.

| Environment component | Observed version |
|---|---|
| Operating system | Linux x86_64 |
| Available Codex CLI binary | 0.167.0-alpha.4 |
| Python | 3.12.14 |
| Node.js / npm | 24.22.1 / 11.9.0 |
| CadQuery / OCP | 2.7.0 / 7.8.1.1.post1 |
| ezdxf | 1.4.4 |

The CLI version was obtained with `codex --version`. It identifies the installed binary, not a completed standalone CLI agent evaluation. No model-specific compatibility claim is made. Parser packages were already installed in the workspace; the skill does not bundle or install them.

## Checks performed

| Check | Result | Evidence and limits |
|---|---|---|
| Python compilation | PASS | `python -m compileall -q scripts tests` returned exit code 0. |
| Repository smoke tests | PASS | `python tests/test_smoke.py` printed `Smoke tests: OK`. Includes DFM examples, unsafe-expression rejection, package-scope/revision checks, and stack-up execution. |
| Reference/example JSON | PASS | All five reference JSON files and both example JSON files parsed. |
| Original clearance calculation | PASS | Utility returned min 0.000 mm, max 0.160 mm, requirement pass=false, margin -0.020 mm. |
| Revised clearance calculation | PASS | Utility returned min 0.040 mm, max 0.160 mm, requirement pass=true, margin 0.020 mm. |
| STEP parser availability and actual import | PASS, environment-specific | CadQuery imported `tests/gearbox-shaft.step`: one solid, valid geometry, bounding box approximately 340 × 75 × 75 mm. Basic import only; not full feature, PMI, or DFM validation. |
| DXF parser availability and actual import | PASS, environment-specific | ezdxf read `tests/gearbox-shaft.DXF`: AC1032, INSUNITS=4 (mm), zero audit errors. Semantic GD&T interpretation and cross-file agreement were not validated. |
| Explicit instruction-file behavioral check | PASS for one case | A fresh hosted agent was given only the skill path and a Lithuanian dimensional-review request. It read the instructions, ran the bundled stack-up utility, returned 0.000–0.160 mm, classified the minimum-clearance failure as NONCONFORMANCE with confidence A, and stated unchecked scope in Lithuanian. This was not standalone Codex CLI invocation or automatic discovery. |
| Skills CLI download / installation | BLOCKED | `npx --yes skills --version` failed fetching the package from registry.npmjs.org with HTTP 403. The add/install command could not be reached. This is a workspace access limitation, not evidence of a skill defect. |
| Codex discovery after installation | NOT TESTED | No clean Skills CLI installation completed. |
| Automatic skill selection | NOT TESTED | Requires a fresh agent session without manually injecting instructions. |
| PDF inspection / OCR | NOT TESTED | No PDF fixture was used. Installed package availability alone is not a parsing test. |
| Windows / desktop / IDE integration | NOT TESTED | Results above apply only to this hosted Linux workspace. |

DXF modelspace entity counts observed: LINE 88, INSERT 26, MTEXT 22, ARC 22, DIMENSION 25, TOLERANCE 6, LEADER 8, HATCH 3, SOLID 4, LWPOLYLINE 2, CIRCLE 1, OLE2FRAME 1. These counts show that entities were read; they do not establish their engineering correctness.

## Reproduce the utility and parser checks

From the repository root, with Python 3:

```bash
python -m compileall -q scripts tests
python tests/test_smoke.py
python scripts/stackup.py examples/clearance-input.json --json
python scripts/stackup.py examples/clearance-revised.json --json
```

For optional geometry inspection, install CadQuery and ezdxf separately in a suitable environment. With those packages available:

```python
import cadquery as cq
import ezdxf

part = cq.importers.importStep("tests/gearbox-shaft.step")
print("Solids:", len(part.solids().vals()))
print("Valid:", part.val().isValid())
box = part.val().BoundingBox()
print("Bounding box:", box.xlen, box.ylen, box.zlen)

drawing = ezdxf.readfile("tests/gearbox-shaft.DXF")
print("Version:", drawing.dxfversion)
print("Units:", drawing.header.get("$INSUNITS"))
print("Audit errors:", len(drawing.audit().errors))
```

The STEP units must be interpreted through the importer's unit conversion; the approximate millimetre envelope above is the observed imported result.

## Behavioral case

The fresh agent received this request in Lithuanian, without the expected result or access to the worked example:

> Peržiūrėk veleno ir skylės sujungimą. Skylė 20,065 ± 0,065 mm, velenas 19,985 ± 0,015 mm. Reikalaujamas diametrinis tarpas 0,020–0,200 mm. Apskaičiuok ribinius tarpus, pateik išvadas su įrodymų lygiu ir nurodyk, kas nepatikrinta. Jei gali, naudok įtrauktą Python įrankį.

Observed: Lithuanian output, explicit endpoint calculations, nominal clearance 0.080 mm, one verified minimum-clearance nonconformance, and a list of unverified geometry, manufacturing, thermal, coating, and inspection factors. The agent executed the repository utility with input held in memory. It did not claim CAD measurement or production approval. This single directed evaluation does not measure automatic triggering, negative controls, or repeatability across models.

## Remaining end-to-end Codex checks

On a machine with npm and GitHub access, record the OS, Codex version, model, Skills CLI version, and skill tag/commit before testing.

1. Install one chosen channel; for the current main version, target Codex globally:

   `npx skills add RamunasSab/cad-design-review --global --agent codex --yes`

   For the stable snapshot, use `RamunasSab/cad-design-review@v1.5.0` instead. Do not treat results for main as a separate test of the stable tag.

2. List installed skills with `npx skills ls --global`. Verify that the agent itself discovers `cad-design-review` in a fresh session.
3. Explicitly invoke `$cad-design-review` with a dimensional input and record the output and tool trace.
4. Repeat in a fresh session with an engineering request that does not name the skill. Record whether automatic selection actually occurs.
5. Ask an unrelated question as a negative control.
6. Check a Lithuanian request for Lithuanian findings, evidence levels, and an explicit unchecked-scope section.
7. Attach representative PDF, DXF, and STEP files separately. Record the tools used and distinguish visual review from numerical measurements.

Use [the clearance demonstration](../examples/clearance-review.md) for expected numeric results. Passing that single case does not establish general engineering correctness.

[Back to README](../README.md#codex-environment-checks)
