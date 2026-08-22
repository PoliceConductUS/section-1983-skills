# Section 1983 complaint routing

The drafting-section-1983-complaints package is the canonical owner of the
complete general Section 1983 complaint skeleton and detailed count contract.
This umbrella package owns no fallback general skeleton or count contract.

Before drafting, revising, or auditing a complaint, amended complaint, or
amendment proffer, load drafting-section-1983-complaints and require it to read
both of its install-local canonical references:

- `references/complaint-contract.md`
- `references/complaint-structure-contract.json`

If the canonical package or either reference is unavailable, report **complaint
contract unavailable** and do not draft, revise, or audit the complaint. Do not
invent or reconstruct the missing requirements. Apply this umbrella package's
localization and writing system only after the canonical route succeeds.
