## Why

The Monell skills already distinguish facts, inferences, and discovery leads,
but they do not consistently require paragraph-level classification and
placement. A baseline pressure test placed unavailable policy and complaint-
history expectations inside a proposed complaint even while acknowledging that
they were not present facts. The contract needs an explicit boundary.

## What Changes

**Monell proposition classification**

- From: Planning records identify supporting facts, inferences, and discovery
  leads without a paragraph-level three-class contract.
- To: Each Monell proposition is classified as a source-documented fact, a
  supported inference drawn from identified pleaded facts, or an expected-
  discovery proposition.
- Reason: Classification must survive the planning-to-drafting handoff.
- Impact: Non-breaking clarification of existing source boundaries.

**Monell proposition placement**

- From: Drafting prohibits unsupported facts but does not expressly keep all
  expected-discovery propositions out of complaint allegations.
- To: Complaints contain documented facts and supported inferences; expected-
  discovery propositions remain in the discovery plan; briefs cannot supply a
  missing complaint-level factual basis.
- Reason: Prevent expectations from being pleaded as present support.
- Impact: Stricter behavior for Monell complaint deltas and supporting briefs.

**Staged Monell development**

- From: A `preserve-internal` recommendation identifies a supported discovery or
  strategy lead but does not require a complete discovery, diligence, and
  amendment record.
- To: Presently supportable paths are pleaded narrowly; supported but incomplete
  paths remain internal and carry the missing connection, request-specific
  discovery relevance, diligence dates, amendment deadline and standard,
  evidentiary trigger, and limitations or relation-back risk.
- Reason: Preserve legitimate development paths without converting hoped-for
  discovery into a placeholder allegation or assuming that discovery or later
  amendment will be available.
- Impact: More complete internal planning and stricter gates before drafting an
  amended Monell claim.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `planning-section-1983-monell-claims`: classify each Monell proposition and
  preserve the basis for supported inferences.
- `drafting-section-1983-monell-claims`: enforce complaint, brief, and
  discovery- plan placement for the three proposition classes.
- `post-draft-assertion-validation`: detect expected-discovery propositions
  presented as existing Monell facts or used to replace a missing complaint-
  level factual basis.

## Impact

The change affects the Monell planning and drafting skill references, the shared
assertion-validation contract, the canonical complaint-handoff validator, their
OpenSpec requirements, and synthetic behavioral evaluations. It does not select
or approve a claim, modify a case repository, guarantee discovery or amendment,
or add a CaseGraph dependency.
