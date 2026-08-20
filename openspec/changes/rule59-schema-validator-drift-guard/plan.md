# Rule 59 Schema-Validator Drift Guard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:test-driven-development to implement this plan in RED and GREEN
> commits.

**Goal:** Make structural drift between the Rule 59 public schemas and custom
validator fail CI automatically.

**Architecture:** A focused evaluation test loads both schemas, imports the
validator, inventories every required-field and enum node, and compares
explicitly mapped nodes to named validator constants. The runtime validator only
replaces inline allowed-value sets with those named constants.

**Tech Stack:** Python 3 standard library, `unittest`, JSON Schema documents,
OpenSpec 1.3.1.

## Global Constraints

- Preserve all accepted values and validator output.
- Keep real-CLI behavioral tests authoritative for semantic rules.
- Add no dependency, CI workflow, root `docs`, or `.superpowers` directory.
- Add no code comments.
- Commit and run `git town sync` after every commit.

### Task 1: RED alignment test

**Files:**

- Create: `evaluations/tests/test_rule59_schema_validator_alignment.py`

- [ ] Load both public schemas and import the validator from install-local
      repository paths.
- [ ] Inventory all required-field and enum paths.
- [ ] Compare explicit required-field and enum mappings with readable mismatch
      diagnostics.
- [ ] Add mutation checks proving schema-only required fields and enum values
      are detected.
- [ ] Run focused RED, commit only the test, and sync.

### Task 2: GREEN constant extraction

**Files:**

- Modify: `skills/studying-rule-59e-decisions/scripts/validate_corpus.py`

- [ ] Add named sets for sampling method, completeness status, Rule subsection,
      representation status, gap status, evidence level, and metric type.
- [ ] Replace the corresponding inline sets with the named constants.
- [ ] Run focused GREEN and the existing Rule 59 corpus suite.
- [ ] Commit the validator refactor and sync.

### Task 3: Verify and archive

**Files:**

- Modify: `openspec/changes/rule59-schema-validator-drift-guard/tasks.md`
- Create: `openspec/changes/rule59-schema-validator-drift-guard/verify.md`
- Create:
  `openspec/changes/rule59-schema-validator-drift-guard/retrospective.md`

- [ ] Run all evaluation tests and `npm run validate`.
- [ ] Run OpenSpec validation, compile, formatting, diff, forbidden-folder, and
      comment checks.
- [ ] Archive through OpenSpec, commit, and sync.
