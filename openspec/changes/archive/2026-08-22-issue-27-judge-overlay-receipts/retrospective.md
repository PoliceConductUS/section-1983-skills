# Retrospective

## Outcome

Issue 27 makes assigned-judge overlay execution observable without weakening the
existing evidence or anti-gaming boundaries. A version-local receipt now proves
which frozen filing, overlay, corpus, conduct sources, transfer cards, and
prohibited-inference checks were used.

## What RED established

The repository documented overlay degradation, but judge-specific prose could
not distinguish a completed no-change run from an overlay that never ran. No
install-local execution packet or immutable receipt writer joined the overlay,
corpus, transfer-card, artifact, and quality-control contracts.

## What worked

- Keeping the writer in the always-loaded generic drafting package gave every
  assigned-judge overlay one install-local interface.
- Injected UTC time and run ID made the exclusive immutable report path fully
  testable without weakening the production defaults.
- Separating structural packet validation from outcome normalization allowed an
  invalid anti-gaming set to produce an auditable fail-closed receipt.
- Recording all supplied cards separately from the cards used by a drafting
  change preserved input provenance while keeping unsupported changes closed.
- Expected and actual fingerprints in the report made non-mutation review
  independently checkable.

## Review finding and correction

The first renderer converted every hyphen in the normalized outcome to a space.
The API returned the correct stable value, but the Markdown failed to state the
required exact degradation phrase. The existing RED test caught that observable
contract defect before the implementation commit.

## Deviations

- The writer preserves declared validation statuses and does not rerun the
  corpus, transfer-card, court-source, authority, or Filing CI validators.
- A path or output-preflight failure cannot create a receipt; the CLI reports a
  stable bounded error and writes nowhere else.
- Issue 27 adds no recommendation field and does not research, compose, or edit
  judge-specific filing language.

## Reusable lesson

No specialized prose is ambiguous evidence. A bounded immutable receipt can
prove that a specialized stage ran and correctly degraded to no change without
turning the receipt writer into another research or drafting system.
