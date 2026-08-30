# Issue #80 implementation plan

## Goal

Make independent authority supervision explicit, immutable-byte bound,
fail-closed, and continuously tested without adding a package or persistence
abstraction.

## Steps

1. Publish this OpenSpec design on a branch stacked on Issue #79 and open a
   draft PR.
2. RED-test the stage-provenance schema, deterministic supervision classifier,
   audit instructions, human-reserved boundary, and complete versioned corpus.
3. Extend the authority audit record and instructions with generation-stage,
   audit-stage, exact-byte, distinct-output, and result-taxonomy requirements.
4. Implement the pure relationship classifier and the complete synthetic YAML
   corpus without filesystem or network authority.
5. Run focused tests, the full corpus, governance validation, OpenSpec
   validation, and `npm run validate`.
6. Review the whole story, archive OpenSpec, verify the exact remote head and
   checks, and mark the PR ready while leaving PR #99 and Issue #80 open.
