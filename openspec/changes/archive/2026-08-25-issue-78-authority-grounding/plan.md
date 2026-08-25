# Issue #78 implementation plan

## Goal

Make authority approval proposition-specific, source-voice aware, and explicit
about correctness and groundedness while preserving the existing folder and
human-judgment boundaries.

## Steps

1. Publish this OpenSpec design on a branch stacked on Issue #17 and open a
   draft PR.
2. Add RED contract tests for the proposition schema, audit instructions, shared
   drafting protocol, and six required regression fixtures.
3. Add the proposition-audit schema and update the audit workflow, record
   contract, skill entrypoint, and shared drafting authority protocol.
4. Add the six synthetic passing/regression fixtures and prove that each
   permanent regression produces its expected deterministic finding.
5. Run focused authority tests, corpus evaluation, governance validation, and
   full repository validation.
6. Review the whole story, archive OpenSpec, verify the exact remote head and
   checks, and mark the PR ready while leaving the PR and Issue #78 open.
