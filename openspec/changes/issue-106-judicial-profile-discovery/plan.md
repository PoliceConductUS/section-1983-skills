# Issue #106 implementation plan

## Goal

Add a reproducible, judge-first CourtListener acquisition path and optional
authorization-gated PACER/CM-ECF fallback to the generic judicial-profile skill
and public judge-overlay guide without adding a repository-owned network client.

## Steps

1. Publish the OpenSpec design on a stacked draft PR.
2. RED-test the install-local discovery, verification, provenance, candidate-
   disposition, secret-exclusion, and fallback contracts.
3. Update the judicial-profile acquisition instructions and source-folder
   provenance guidance.
4. Update the public judge-overlay authoring guide with the same bounded path.
5. Run focused and full validation, archive OpenSpec, verify the exact remote
   head, and mark the PR ready while leaving the PR and issue open.
