## 1. RED public contract

- [x] 1.1 Capture a fresh no-new-schema baseline showing the current public
      skill cannot produce and validate the canonical publication artifact.
- [x] 1.2 Add RED public-seam tests for schema field coverage, neutral transfer
      cards, CLI behavior, authorship consistency, gap visibility, denominator
      strength, and synthetic fixture outcomes.

## 2. GREEN schema and validator

- [x] 2.1 Publish the canonical corpus and transfer-card JSON schemas.
- [x] 2.2 Implement the skill-specific standard-library corpus validator.
- [x] 2.3 Add generic synthetic valid and invalid validation fixtures.
- [x] 2.4 Update the public skill and corpus contract to route canonical
      publication and transfer through the schemas and validator.

## 3. Behavior, review, and verification

- [x] 3.1 Run a fresh public-skill behavior scenario that produces a canonical
      synthetic corpus and validates it without private material.
- [x] 3.2 Run focused tests, full repository validation, all public skill
      validators, formatting, compile, diff, and forbidden-folder checks.
- [x] 3.3 Review the whole Issue #15 diff and correct every blocking or
      important finding.
- [x] 3.4 Complete verify and retrospective artifacts, archive the change on the
      Issue #15 branch, commit, and sync the stack.
