# Proposal: Reusable judge-overlay method

## Why

The repository contains a disciplined Judge Scholer overlay and a validated
decision-corpus contract, but it does not explain how another maintainer can
create an evidence-bounded overlay without copying conclusions or gaming a
court.

## What Changes

- Add a concise root guide for authoring judge overlays.
- Route README users to the guide.
- Require canonical corpus validation, neutral transfer cards, explicit
  conclusion strength, degradation, anti-gaming, and sourced court-conduct
  checks.
- Add focused tests for discovery, local link confinement, method boundaries,
  and generic synthetic examples.

## Capabilities

### New capabilities

- `judge-overlay-authoring`: documents and tests the reusable method.

### Modified capabilities

None.

## Impact

Documentation and repository tests only. No new public skill, dependency,
workflow, executable checker, judge-specific overlay, or court research.
