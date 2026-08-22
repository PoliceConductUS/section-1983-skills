# Proposal: Judge-overlay execution receipts

## Why

When a valid judge overlay supplies no qualifying proposition, the filing
correctly contains no visible judge-specific text. That absence cannot show
whether the overlay ran, used current validated inputs, passed anti-gaming
checks, or was skipped.

## What Changes

- Add a public execution-packet schema and standard-library receipt writer to
  `section-1983-drafting`.
- Write one exclusive version-local Markdown receipt that fingerprints the
  filing and records overlay, corpus, conduct, transfer-card, anti-gaming, and
  drafting-change results.
- Represent missing, stale, invalid, unavailable, or prohibited inputs as stable
  fail-closed outcomes, never passes.
- Require assigned-judge composition after document and claim skills and require
  the receipt whether the overlay changes drafting or degrades to none.
- Add behavioral tests for execution-versus-nonexecution, immutable artifacts,
  report confinement/collision, anti-gaming, and no-change degradation.

## Capabilities

### New capabilities

- `judge-overlay-execution`: validates one complete judge-overlay execution
  packet and writes its immutable version-local receipt.

### Modified capabilities

- `judge-overlay-authoring`: requires execution receipts and distinguishes
  successful no-change degradation from an overlay that never ran.

## Impact

Adds one schema and one standard-library script to the existing drafting skill,
focused tests, and documentation updates to the drafting router, generic judge
guide, and Scholer overlay. Adds no dependency, workflow, new tendency,
case-specific content, filing edit, root `docs/`, `.superpowers/`, PR, or issue
closure.
