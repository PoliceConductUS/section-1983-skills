# Issue #79 implementation plan

## Goal

Make legal-authority collection premise-aware, temporally and jurisdictionally
bounded, and auditable while preserving its candidate-only handoff to Issue
#78's independent authority audit.

## Steps

1. Publish this design on a branch stacked on Issue #78 and open a draft PR.
2. Add RED tests for strict retrieval-frame, premise, source-provenance,
   rejected-candidate, gap, and synthetic regression contracts.
3. Extend the installed pure helper, domain YAML references, and collection
   skill instructions.
4. Add one network-independent fixture with permanent regressions for every
   Issue #79 failure mode.
5. Run focused collection tests, corpus checks, governance, formatting, and full
   repository validation.
6. Review the whole story, archive OpenSpec, verify the exact remote head and
   checks, and mark the PR ready while leaving the PR and Issue #79 open.
