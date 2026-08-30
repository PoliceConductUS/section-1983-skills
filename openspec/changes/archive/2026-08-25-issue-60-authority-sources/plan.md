# Issue #60 implementation plan

## Goal

Add a folder-native authorized collector and narrow validator that return
ordinary legal-authority source files with domain YAML for later independent
authority audit.

## Steps

1. Correct the live issue, create the stacked worktree, and publish the OpenSpec
   design in a draft PR.
2. RED-test the exact six-role contract, authorized internet, strict source
   provenance, classifications, candidate identities, and gaps.
3. Implement the installable skill and deterministic in-memory source planner.
4. RED-test duplicates, incomplete coverage, changed content, mistaken identity,
   unofficial-source classification, and collector/auditor separation.
5. Test trusted-host internet provenance, input preservation, output
   confinement, and output-local temporary work.
6. Run focused and full validation, archive OpenSpec, verify the exact remote
   head, and mark the PR ready while leaving PR and issue open.
