# Change: Strengthen complaint candor, pruning, and bounded fair-warning drafting

## Why

The canonical complaint shape is now unified, but a generated complaint showed
four substantive gaps: legal self-assessment can leak into filed text,
fair-warning units can become authority briefs, uncertain paragraphs can remain
without a pleaded job, and incorporated-record ambiguity can be candidly stated
without completing the material alternative-offense analysis.

## What changes

- Add a canonical filed-text no-concession rule that distinguishes factual
  qualification from adverse legal merits assessment.
- Bound complaint-level fair-warning drafting while preserving separately
  necessary authority.
- Require a purpose-based pruning audit for the draft's own uncertainty labels.
- Require count-level treatment or a filing-critical GAP when an unresolved
  incorporated-record fact is material to an alternative offense actually in
  dispute.
- Add synthetic structural, mutation, corpus, and fresh-context behavior tests.

## Capabilities

### Modified capabilities

- `drafting-section-1983-complaints`

## Impact

- Modified skills: `drafting-section-1983-complaints` and
  `drafting-false-arrest-complaints`.
- Modified tests and synthetic evaluation fixtures under `evaluations/`.
- No executable checker, dependency, workflow, linter, or judge-overlay change.
