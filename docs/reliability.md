# Reliability changes and remaining scope

The development branch implements version-consistency checks, decimal worst-case acceptance, auditable stack-up reporting, golden/invariant/negative tests, prompt-contract checks, DFM heuristic provenance and broader CI. These are not part of the immutable v1.6.0 tag.

## Assessment of external suggestions

- Fix version inconsistency: implemented without rewriting historical changelog/release entries.
- Golden tests: ten constructed dimensional cases plus generated invariants; expected statuses apply only to explicit dimensional requirements. They are not real CAD reviews or AI-model certification.
- Audit trail and report formats: implemented for stackup.py, not retroactively claimed for every utility. JSON is finite; hash uses sorted, compact UTF-8 JSON of supplied input. Whitespace/key order does not affect the hash; numeric spelling may. Record exact code hash separately.
- Input adapters: document a versioned envelope with source/provenance and consumer payloads. Actual parsers remain external, not placeholder modules advertised as working.
- DFM metadata: extend existing rule data, retain IDs/numeric expressions and raw rule severity. Default violations are risks. A custom binding rule must state its requirement reference.
- Standard selection: defer until verified edition-specific tables are available; do not relabel old datasets as current ISO editions.
- GD&T syntax: defer an actual parser/grammar until a typed frame representation and test drawings are defined. An invented field-count check is not GD&T validation.
- Property-based testing: seeded generated invariants use only the standard library; no new dependency is required.
- PDF: HTML reports support browser Print/Save as PDF, not a native PDF conversion service.
- Interactive website: keep the accepted two-image hero; add a separate opt-in calculator instead of restoring the removed worked-example marketing section.

## Statistical caveats

Normal inputs are centered on nominal. The Cpk conversion is valid only under that assumption; Cpk alone is insufficient for an off-center process. RSS and modeled Gaussian tails/Monte Carlo do not establish production capability. Uniform is an explicit simplifying distribution, not measured evidence. Shared dimensions must be cancelled before input; correlated contributors need another model. The sampled extrema are not worst-case limits.
