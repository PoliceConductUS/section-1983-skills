## Why

The Judicial Reasoning Profile skill authorizes public acquisition but does not
currently explain how to discover a judge's Section 1983 police cases through
CourtListener or how to use PACER when public coverage is incomplete. Without a
declared discovery and verification method, a researcher can collapse
authorship, assignment, and referral, treat search metadata as proof, or build a
non-reproducible and selectively screened corpus.

## What Changes

**Judicial-profile source discovery**

- From: Generic acquisition of public material within an assigned scope.
- To: A CourtListener discovery recipe that resolves judge identity, preserves
  relationship type, narrows candidates, verifies corpus eligibility from
  primary materials, and records provenance, exclusions, coverage, and gaps.
- Reason: Make judge-name-to-responsive-corpus acquisition reproducible and
  source bounded.
- Impact: Additive guidance and tests; no network client or profile schema
  migration.

**Official fallback**

- From: Paid sources remain generic unavailable gaps unless separately
  authorized.
- To: PACER/CM-ECF is expressly available as an optional official fallback only
  with authorized access and separate approval before any fee.
- Reason: Preserve official docket verification when CourtListener/RECAP is
  incomplete.
- Impact: Additive authorization guidance; credentials remain outside outputs.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `building-judicial-reasoning-profiles`: Add CourtListener judge discovery,
  Section 1983 police-case verification, candidate disposition, and optional
  PACER/CM-ECF fallback requirements.
- `judge-overlay-authoring`: Add the same acquisition path to the public
  lifecycle guide and preserve source hierarchy and denominator limits.

## Impact

The change affects `skills/building-judicial-reasoning-profiles/SKILL.md`, its
source-folder reference, `JUDGE_OVERLAYS.md`, focused public evaluations, and
the two durable OpenSpec capabilities. It adds no dependency, executable API
client, credential store, persistence layer, or profile-schema field.
