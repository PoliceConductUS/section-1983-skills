# Proposal: Independent Adversarial Filing Review

## Why

A filing drafted inside one context needs an independent adversarial reviewer
that cannot inherit the drafter's history or conclusions. Existing skills own
drafting, authority verification, response planning, or deterministic Filing CI,
but none owns this clean-room filing review.

## What Changes

- Add a public `adversarial-filing-review` skill with a fail-closed fresh-review
  packet and read-only output contract.
- Add a standard-library launcher that validates and dispatches only the
  fingerprinted bounded packet to a configured no-history, no-tool reviewer.
- Add universal and document-specific attack checklists for the seven existing
  supported filing families.
- Require five distinct finding classes, exact attacked text, and copy-ready
  replacements for every proposed correction.
- Route retain, narrow, or omit choices to the plaintiff without selecting an
  outcome.
- Add structural and synthetic behavioral evaluation coverage.

## Capabilities

### New Capabilities

- `adversarial-filing-review`

### Modified Capabilities

None.

## Impact

The change adds one skill directory with a small launcher script, synthetic
evaluation fixtures, focused tests, README discovery text, and a durable
OpenSpec capability. It adds no external runtime dependency, provider SDK,
secret, automatic filing edit, or filing-readiness determination.
