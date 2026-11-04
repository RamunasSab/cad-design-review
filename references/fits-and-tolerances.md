# Fits, General Tolerances, and Bearing Fits

Source data is based on a supplied reference PDF titled “Recommended fits and permissible deviations for general mechanical engineering and bearings.” Numerical values are stored in `tolerance-data.json`; query them with `scripts/check_tolerances.py`.

**Editions represented in the source PDF:** DIN 7157 (1966-01), DIN ISO 2768-1 (1991-06), DIN ISO 2768-2 (1991-04), and DIN 5425-1 (1984-11). These are old editions and may have been withdrawn or replaced. Reports must identify the source and ask the user to confirm the currently applicable company edition.

**These tables do not apply to plastic moldings.** ISO 286 / ISO 2768 were developed for metal parts. For plastic, see `iso-20457.md`.

## 1. Which lookup to use

| Drawing question | Reference | Command |
|---|---|---|
| Is a fit (e.g. H7/f7) recommended for the function? | Fits | `check_tolerances.py fit H7/f7` |
| What general tolerance applies to an undimensioned linear size? | ISO 2768-1 | `check_tolerances.py general --type linear --size 45 --class m` |
| What general form/position tolerance applies? | ISO 2768-2 | `check_tolerances.py geom --kind flatness --size 120 --class K` |
| General tolerance for molded plastic? | `iso-20457.md` | `check_tolerances.py plastic --tg 6 --size 40` |
| Are bearing shaft and housing fits appropriate for the load? | Bearing fits | `check_tolerances.py bearing ...` |

## 2. DIN 7157 fit series

Series 1 has highest priority; series 2 is permitted where justified.

- **Series 1:** C11/h9, D10/h9, E9/h9, F8/h9, H8/f7, F8/h6, H7/f7, H8/h9, H7/h6, H7/n6, H7/r6, H8/u8, H8/x8.
- **Series 2:** C11/h11, D10/h11, H8/d9, H8/e8, H7/g6, G7/h6, H11/h9, H7/j6, H7/k6, H7/s6.

The source data contains descriptive applications for common clearance, transition, and interference fits. Always compare the described application with the actual assembly function; do not select a fit from its code alone.

## 3. ISO 2768 general tolerances

General tolerances are stated in the title block rather than repeated beside every nominal dimension (e.g. `ISO 2768-mK`, where `m` is the linear/angular class and `K` is the geometrical class). Query the exact value using the script. The supplied tables represent older editions and must be confirmed before contractual use.

## 4. Bearing fits (DIN 5425-1)

Determine whether the load is circumferential or point relative to the ring, the load magnitude, and whether the bearing is ball or roller type. The source data provides recommended shaft and housing fit letters. Typical grades are shaft IT6 and housing IT7, but the actual selection depends on the application and current bearing-manufacturer guidance.

## 5. Review rules
1. Run the `fit` lookup for every fit. If it is not in series 1 or 2, mark `RISK` and request functional justification.
2. If a series 2 fit is used, mention that series 1 has priority and check whether a series 1 option is suitable.
3. Compare the fit type with function. For example, a moving joint specified with an interference fit is a potential `NONCONFORMANCE`.
4. Use a consistent basis system (usually hole basis). A shaft-basis system may be justified when several parts with different fits are mounted on one shaft.
5. The title block must specify the general tolerance standard and class. Without it, undimensioned sizes are ambiguous.
6. Compare the class with process capability. Tight classes increase cost; loose classes may compromise precision assemblies.
7. For bearing fits, identify load direction, magnitude, and bearing type before using the lookup. Compare the actual fit letter and tolerance grade with the recommendation.
8. If a table value is absent, mark `NEEDS_CLARIFICATION`; do not extrapolate.

## 6. Source-data caveats
The source PDF contains some ambiguous or corrected table headings and merged cells. Treat the data as a transcription, not an authoritative replacement for the standards. Verify all critical applications and current editions.

## 7. Missing data
The source does not contain the full ISO 286 fundamental deviation and IT tables, so the script does not calculate actual limit clearances/interferences. Add verified ISO 286 data if those calculations are required. Some fit applications and ISO 1101 geometrical tolerances are also outside the source dataset.
