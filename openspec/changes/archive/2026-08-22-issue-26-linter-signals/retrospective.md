# Retrospective

## Outcome

Issue 26 preserves the useful score delta while turning the drafting linter into
an editor-facing locator. Legal terms that actually misfired no longer bury real
rhetoric, and dense analysis becomes a visible review prompt without becoming a
legal or filing gate.

## What RED established

The previous linter could count `unbearably`, `almost`, and `immediately`, but
it could not identify their artifact or paragraph. It also treated three
controlling phrases as violations, exposed no paragraph density warnings, and
left the drafting workflow with an inaccurate zero-banned-word target.

## What worked

- Retaining the aggregate interface avoided breaking existing score comparisons.
- Paragraph-level grouping produced stable locations without adding fragile
  character offsets.
- Probing every suggested phrase prevented four inert exemptions from entering
  policy.
- Separate exemption and warning records kept legal terminology and review
  heuristics out of violation totals.
- Leaving quotation accuracy to source verification kept the linter within its
  mechanical boundary.

## Review finding and correction

The first GREEN record keyed each exemption by paragraph and phrase. Repeating
one phrase in a paragraph therefore created duplicate IDs and made exhaustive
reconciliation ambiguous. A direct regression required stable occurrence
ordinals before the implementation added them.

## Deviations

- Citation density uses a bounded reporter-form expression rather than a full
  citation parser. It is intentionally a review heuristic.
- Findings group a check's hits within one paragraph instead of emitting
  character offsets for every token. The count retains every hit and the source
  location remains stable under ordinary edits.
- The linter does not validate quotation accuracy or legal sufficiency.

## Reusable lesson

A style metric becomes useful when it tells the editor where to look and why a
residual remains. It becomes dangerous when an exemption is inert, a heuristic
pretends to decide readiness, or a quote receives an accuracy label without its
source.
