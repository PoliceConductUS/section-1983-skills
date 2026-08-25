# Issue #57 implementation plan

## Goal

Add a folder-native policy-analysis skill and narrow validator that turn
reviewed policy sources into source-bounded atomic requirement records.

## Steps

1. Correct the live issue, create the stacked worktree, and publish the OpenSpec
   design in a draft PR.
2. RED-test the exact offline four-role contract and selected source YAML/hash
   boundary.
3. Implement the installable skill and strict source/requirement contracts.
4. RED-test all requirement types, conditions, exceptions, cross-references,
   dates, model-policy separation, gaps, and deterministic outputs.
5. Implement the in-memory validator and trusted-host artifact plan.
6. Run focused and full validation, archive OpenSpec, verify the exact remote
   head, and mark the PR ready while leaving PR and issue open.
