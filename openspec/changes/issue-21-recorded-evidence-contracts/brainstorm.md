# Recorded-Evidence Contract Alignment Brainstorm

## Approved direction

Preserve the intended prose currently present only as uncommitted changes in the
`main` checkout. Put it on a dedicated test-backed branch stacked after Issue
16, and align the complaint claim-specific contract and Rule 59(e) packet gate
with the already-committed complaint completion audit.

## Boundaries

- Preserve the intended prose without adding a new evidence rule.
- Add a focused structural test for the shared public contract and Rule 59(e)
  list continuity.
- Do not add case-specific facts, a dependency, a workflow, a root `docs`
  directory, a `.superpowers` directory, or code comments.
- Restore the two accidental `main` edits only after this branch is committed,
  synced, pushed, and verified.

## Rejected alternatives

- Committing the prose directly on `main` would bypass the stacked TDD and
  OpenSpec history.
- Rebasing every existing branch to inherit the accidental checkout state would
  rewrite already-pushed history and obscure the story that owns the change.
- Testing exact paragraphs byte-for-byte would make harmless formatting changes
  fail without proving the evidence boundary remains complete.
