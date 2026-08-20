## 1. RED public contract

- [ ] 1.1 Capture a fresh no-new-schema baseline showing the current public
      skill cannot produce and validate the canonical publication artifact.
- [ ] 1.2 Add RED public-seam tests for schema field coverage, neutral transfer
      cards, CLI behavior, authorship consistency, gap visibility, denominator
      strength, and synthetic fixture outcomes.

## 2. GREEN schema and validator

- [ ] 2.1 Publish the canonical corpus and transfer-card JSON schemas.
- [ ] 2.2 Implement the skill-specific standard-library corpus validator.
- [ ] 2.3 Add generic synthetic valid and invalid validation fixtures.
- [ ] 2.4 Update the public skill and corpus contract to route canonical
      publication and transfer through the schemas and validator.

## 3. Behavior, review, and verification

- [ ] 3.1 Run a fresh public-skill behavior scenario that produces a canonical
      synthetic corpus and validates it without private material.
- [ ] 3.2 Run focused tests, full repository validation, all public skill
      validators, formatting, compile, diff, and forbidden-folder checks.
- [ ] 3.3 Review the whole Issue #15 diff and correct every blocking or
      important finding.
- [ ] 3.4 Complete verify and retrospective artifacts, archive the change on the
      Issue #15 branch, commit, and sync the stack.
