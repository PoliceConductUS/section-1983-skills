# Verification Report

**Change**: `issue-15-rule59-corpus-contract` **Verified at**: 2026-08-20
**Verifier**: Issue #15 Task 3 archive verification

## Structural validation

- [x] `npx openspec validate --all --json` passed before archive.
- [x] All 11 pre-archive items were valid: 10 durable specs and this change.

## TDD history

- The initial public-contract RED ran 16 tests with 4 failures and 18 errors
  because the planned schemas, fixtures, and validator did not exist.
- The integrity-review RED ran 26 focused tests with 11 failures and 3 errors,
  exposing missing controlled legacy fields and record, gap, denominator, and
  transfer-card invariants.
- The final evidence-completeness RED ran 31 focused tests with 8 failures,
  exposing unverified transfer sources, non-complete-pair strong transfers, an
  inconsistent candidate inventory, and incomplete adoption-only authorship.
- The current focused suite passes all 31 tests; the full evaluation suite
  passes all 181 tests.

The implemented test and production commits are:

```text
dcca88a docs: design Rule 59 corpus contract
4a1f748 test: define Rule 59 corpus contract
92af4c5 test: strengthen Rule 59 corpus boundaries
985b2e7 feat: publish Rule 59 corpus contract
c2a356f test: expose Rule 59 corpus integrity gaps
fb88ff7 test: constrain Rule 59 gap scopes
07fe0cf fix: enforce Rule 59 corpus integrity
237187d test: expose Rule 59 evidence inventory gaps
a2ec2ef test: require complete pairs for Rule 59 tendencies
6db98db fix: enforce Rule 59 evidence completeness
```

Each completed commit is present on `origin/codex/issue-15-rule59-corpus`. Git
Town sync was run after commits; permission-gated test commits were included by
the next successful parent-agent sync. Before archive, local HEAD and origin
both resolved to `6db98db56f8ead7977aa4341d26e3dc882e2c549`.

## Fresh public behavior

A fresh worker read only the public `studying-rule-59e-decisions` package and
produced `/private/tmp/issue-15-rule59-corpus-sdd/task-3-behavior.json` from a
fictional Example District packet. The artifact contains distinct
recommendation, adoption-only, and independently reasoned stages; two
record-linked document gaps; one candidate-only gap; an incomplete attempted
census; and one bounded descriptive example transfer.

- SHA-256: `db541d1ef15121ed308daee6a89d060b2c0ac94f09584fe26780306fd54c3349`
- Validator result: `corpus validation passed`.
- Candidate equation: 3 candidates = 2 coded motion-disposition pairs + 1
  unresolved candidate.
- Validation did not change the artifact bytes.

## Exact fixture outcomes

| Fixture                            | Exit | Output                          |
| ---------------------------------- | ---- | ------------------------------- |
| `valid-complete.json`              | 0    | `corpus validation passed`      |
| `valid-incomplete-example.json`    | 0    | `corpus validation passed`      |
| `invalid-incomplete-tendency.json` | 1    | `incomplete-tendency`           |
| `invalid-authorship-stage.json`    | 1    | `authorship-stage-inconsistent` |

## Verification gates

- [x] `npm run validate` passed: formatting, 16 drafting-script tests, 181
      evaluation tests, 20-skill discovery, OpenSpec, evaluation corpus, and
      governance validation.
- [x] `python3 -m compileall -q skills/studying-rule-59e-decisions/scripts`
      passed; generated cache was removed.
- [x] The installed skill quick validator reported `Skill is valid!` when
      invoked through Python because the script itself is not executable.
- [x] Prettier passed for the public skill package and OpenSpec Markdown/JSON.
      Prettier did not parse or format Python.
- [x] `git diff --check` passed.
- [x] No root `docs` or `.superpowers` directory exists.
- [x] No Python code comments were added.
- [x] No private path, private case identifier, unpublished real material, or
      user identity appears in the Issue #15 fixtures or fresh behavior
      artifact.
- [x] The whole-branch review is clean after all Important findings and their
      corrective-test review findings were resolved test-first.

## Archive result

`npx openspec archive issue-15-rule59-corpus-contract -y` completed without
skipping spec sync or validation. It moved the change to
`openspec/changes/archive/2026-08-20-issue-15-rule59-corpus-contract/` and
created `openspec/specs/studying-rule-59e-decisions/spec.md` with eight durable
requirements and a meaningful Purpose.

Post-archive verification passed:

- 31 focused Rule 59 corpus tests and all 181 evaluation tests;
- the preserved fresh behavior artifact and exact four-fixture CLI matrix;
- Python compile and installed-skill quick validation;
- package/OpenSpec Prettier checks and `npm run validate`;
- `npx openspec validate --all --json` with 11 durable specs passed, 0 failed,
  and 0 active changes; and
- diff, forbidden-folder, comment, private-material, scope, and generated-cache
  checks.

## Overall decision

- [x] PASS — implementation verification and archive are complete.
