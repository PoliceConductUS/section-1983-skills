# Plan

## Goal

Publish and deterministically validate the contributor norms requested by Issue
20 while preserving the existing governance and publishing owners.

## RED

1. Extend governance tests with a valid temporary contribution contract.
2. Assert the live guide's stacked-story, TDD, OpenSpec, human-control,
   measurement, code-comment, validation, and tagged-release boundaries.
3. Mutate a temporary contract to prove the validator fails closed.
4. Run focused RED, commit, and sync.

## GREEN

1. Update `CONTRIBUTING.md` with the concise contract and owner links.
2. Add deterministic contribution-contract validation to
   `scripts/validate_governance.py`.
3. Run focused and complete validation, commit, and sync.

## Review and archive

1. Independently review the whole story and mutation boundaries.
2. Correct Important findings test-first.
3. Record verification and retrospective artifacts.
4. Archive the change, validate the durable specification, commit, and sync.
