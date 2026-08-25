# Issue #58 implementation plan

## Goal

Add a folder-native offline skill and narrow validator that assesses approved
policy requirements against source-documented case records without deciding
legal liability.

## Steps

1. Correct the live issue, create the stacked worktree, and publish the OpenSpec
   design in a draft PR.
2. RED-test the exact six-role offline contract, catalog validation, and source
   YAML/hash boundary.
3. Implement the installable skill and strict in-memory catalog/evidence gates.
4. RED-test every state, date selection, actor/phase isolation, conflicting and
   missing evidence, deterministic output, and input/output/temp confinement.
5. Implement assessment and gap validation plus trusted-host artifact plans.
6. Run focused and full validation, archive OpenSpec, verify the exact remote
   head, and mark the PR ready while leaving PR and issue open.
