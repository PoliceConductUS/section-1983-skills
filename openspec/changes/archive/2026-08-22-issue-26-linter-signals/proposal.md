# Proposal: Location-bearing drafting-linter signals

## Why

The drafting linter currently returns aggregate counts. Controlling legal
phrases can appear as banned-word hits, and real rhetoric can be buried among
those false positives. The linter also gives no paragraph-level signal that
legal analysis is growing into an authority memorandum.

## What Changes

- Add location-bearing findings while preserving existing aggregate counts and
  score-delta behavior.
- Exempt only `active resistance`, `materially similar`, and
  `reasonably trustworthy`, the requested phrases proven by RED to trigger
  current checks.
- Add paragraph-level long-sentence-density and case-citation-density warnings
  as non-gating review heuristics.
- Require a complete residual-hit reconciliation in the drafting workflow.
- Add synthetic calibration and mutation tests for rhetoric, controlling legal
  analysis, artifacts, locations, thresholds, and non-gating semantics.

## Capabilities

### New capabilities

- `drafting-linter-signals`: reports mechanical prose findings and review
  heuristics with artifact and paragraph locations while preserving explicit
  term-of-art and quotation reconciliation.

### Modified capabilities

None.

## Impact

Modifies the existing drafting linter, its focused tests, and the owning skill
and writing-system guidance. Adds one focused evaluation contract and one active
OpenSpec change. Adds no dependency, workflow, case-specific content, root
`docs/`, `.superpowers/`, PR, issue closure, or filing edit.
