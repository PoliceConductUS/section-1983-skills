# Proposal: Assess case records against police-policy requirements

## Why

Issue #57 produces source-bounded policy requirements but deliberately does not
apply them to conduct. Issue #58 needs a separate offline invocation that
assesses each requirement, actor, event, and phase without changing any input or
turning policy analysis into a legal conclusion.

## What changes

- Add `assessing-police-policy-compliance` with exact `policy-catalog`, `actor`,
  `event`, `phase`, `case-record`, and `assessment-scope` folders.
- Validate the selected catalog, ordinary evidence files, adjacent domain source
  YAML, relative paths, hashes, dates, and cross-record identities before
  assessment.
- Preserve separate applicability, violation, and evidence states for every
  atomic assessment unit.
- Return deterministic assessment YAML, gap YAML, Markdown, and domain
  validation bytes for trusted-host publication.
- Reject unsupported `no` findings, inapplicable-as-no-violation treatment,
  collapsed actor/phase units, stale provenance, and legal conclusions.

## Capability

- `assessing-police-policy-compliance`

## Non-goals

- No collection, internet research, package, graph, compliance enforcement,
  constitutional or Monell conclusion, negligence conclusion, evidence ruling,
  strategy selection, allegation drafting, or filing-readiness decision.
