# Proposal: Make independent quality control non-mutating

## Why

Issue 22 requires audits, verifications, reviews, evaluations, Filing CI, and
behaviorally equivalent quality checks to remain separate from remediation.
Current skills do not express that boundary consistently, and fresh-agent RED
controls changed three canonical artifacts in place.

## What Changes

- Add the general non-mutation rule to the existing governance owner.
- Add a compact conditional contract to every current public skill that can act
  as an independent quality-control stage.
- Extend existing repository governance validation with a stable deterministic
  finding.
- Add omission, inversion, byte-preservation, and pressure tests.

## Capabilities

### New capabilities

None.

### Modified capabilities

- `repository-skill-governance`: add the independent quality-control stage
  contract and its deterministic validation boundary.

## Impact

Governance, existing public skill instructions, repository-specific tests, and
OpenSpec only. No new checker, drafting tool, automatic remediation workflow,
dependency, release workflow, or parallel governance owner.
