# Example review: a shaft-to-hole clearance that fails at the limits

This is a constructed, reproducible engineering demonstration, not a finding from the gearbox-shaft CAD files. Inputs are explicitly supplied dimensions in millimetres. No CAD parsing, geometry measurement, ISO fit lookup, or agent compatibility claim is involved.

## Input and requirement

| Item | Original specification | Limits |
|---|---|---|
| Hole diameter D | 20.065 ± 0.065 mm | 20.000–20.130 mm |
| Shaft diameter d | 19.985 ± 0.015 mm | 19.970–20.000 mm |
| Required diametral clearance C = D − d | 0.020–0.200 mm | Must hold for every permitted dimension combination |

The requirement is part of this demonstration; it is not attributed to an ISO standard. These are diametral clearances, not radial gaps.

## Review result

| Location | Finding | Status | Evidence | Recommended action |
|---|---|---|---|---|
| Hole/shaft interface | Minimum clearance is 20.000 − 20.000 = **0.000 mm**, below the required 0.020 mm. | NONCONFORMANCE | A — worst-case arithmetic from the explicit demonstration inputs | Revise the dimensional limits and repeat the calculation. |
| Hole/shaft interface | Maximum clearance is 20.130 − 19.970 = **0.160 mm**, within the 0.200 mm upper limit. Nominal clearance alone, 0.080 mm, does not establish compliance. | INFO | A — worst-case arithmetic | Assess both limits rather than the nominal result alone. |
| Manufacturing and inspection | Material, achievable process capability, form errors, thermal conditions, and coating effects have not been supplied. | NEEDS_CLARIFICATION | D — review scope limitation | Obtain these inputs before accepting a production specification. |

**Assessment:** corrections required for the original dimensional specification. This is one demonstrated dimensional nonconformance, not a complete design approval.

## Candidate correction and recheck

A candidate hole specification is **20.085 ± 0.045 mm** (20.040–20.130 mm), with the shaft unchanged.

- Minimum clearance: 20.040 − 20.000 = **0.040 mm**.
- Maximum clearance: 20.130 − 19.970 = **0.160 mm**.
- Result: **PASS** against the stated 0.020–0.200 mm dimensional requirement.
- Worst-case margin to the closest requirement boundary: **0.020 mm**.

This is a candidate for engineering review, not an approved manufacturing change. Confirm the hole limits are practical and include other relevant contributors before release.

## Reproduce with the included utility

Download the repository or clone it, then run these commands from its root with Python 3:

```bash
python scripts/stackup.py examples/clearance-input.json --json
python scripts/stackup.py examples/clearance-revised.json --json
```

The input files are [original](clearance-input.json) and [revised](clearance-revised.json). Expected worst-case fields:

| Field | Original | Revised |
|---|---|---|
| nominal_result | 0.08 | 0.10 |
| worst_case.min | 0.00 | 0.04 |
| worst_case.max | 0.16 | 0.16 |
| worst_case.pass | false | true |
| worst_case.margin | -0.02 | 0.02 |

The results were executed and checked against independent endpoint arithmetic using the repository's unchanged `scripts/stackup.py`. That script is identical in v1.5.0 and main at the time this example was added.

Both inputs use uniform distributions as mathematical assumptions and a fixed seed. The utility also outputs statistical and Monte Carlo estimates. Those are not measured process capability or acceptance evidence; its normal-approximation statistical estimates need not match a bounded uniform simulation. The table above deliberately uses the deterministic worst-case result.

## Try the review with an AI agent

With `cad-design-review` installed and available to your agent, provide the original JSON or paste the input table and ask:

> Use cad-design-review to assess this shaft-to-hole interface. The required diametral clearance is 0.020–0.200 mm. Calculate the worst-case limits, distinguish verified findings from missing evidence, and evaluate the revised hole specification of 20.085 ± 0.045 mm. Use scripts/stackup.py if Python execution is available; otherwise show the endpoint arithmetic and state that the utility was not run.

Expected engineering conclusion: the original limits fail the minimum-clearance requirement; the revised limits pass this dimensional check. Agent wording may vary.

## Scope and coverage

- **Checked automatically:** scalar dimensional worst-case stack-up using the included Python utility.
- **Checked independently:** nominal value, minimum/maximum endpoints, pass/fail, and margin.
- **Not checked:** CAD geometry, GD&T, surface finish, loads, thermal expansion, coatings, supplier capability, and complete assembly function.
- **Language:** user-facing reports should follow the language of the request.

[Back to README](../README.md#example-review)
