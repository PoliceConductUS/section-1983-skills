# Complaint Candor and Pruning Implementation Plan

> Use `subagent-driven-development`, test-driven development, writing-skills,
> and the OpenSpec/Superpowers bridge. Commit and run `git town sync` after
> every commit.

**Goal:** Prevent generated complaints from conceding legal weakness,
overbuilding fair-warning analysis, retaining uncertainty that serves no pleaded
job, or leaving an actually raised alternative offense unresolved after candid
record qualification.

**Architecture:** The canonical general complaint contract owns the first three
rules. The false-arrest package owns only the offense/record integration delta.
Tests exercise isolated packages and synthetic behavior. The JSON checker
handoff, linter, and judge overlay remain unchanged.

## Task 1: RED

**Files:**

- Create: `evaluations/tests/test_complaint_candor_contract.py`
- Create four fixture directories under `evaluations/fixtures/`
- Update: `brainstorm.md`, `tasks.md`

- Record four fresh-context current-state outputs and exact failures.
- Add public-seam tests requiring affirmative, non-inverted rules while
  preserving alternative pleading, candor, and the actual-offense trigger.
- Add realistic mutations: permit adverse merits labels; permit unexplained
  multi-case complaint strings; retain an unresolved paragraph with no job; and
  treat ambiguous possible conduct as admitted or ignore its offense effect.
- Add one synthetic fixture per behavior, each with a clean passing output, one
  behavior-specific regression, and an unrelated-rule discrimination probe.
- Run focused RED, corpus evaluation, formatting, and diff checks.
- Independently review the RED suite, correct accepted findings, commit, and
  sync.

## Task 2: GREEN

**Files:**

- Modify:
  `skills/drafting-section-1983-complaints/references/complaint-contract.md`
- Modify:
  `skills/drafting-section-1983-complaints/references/completion-audit.md`
- Modify: `skills/drafting-section-1983-complaints/SKILL.md` only when routing
  to the canonical additions is needed
- Modify:
  `skills/drafting-false-arrest-complaints/references/false-arrest-complaint-delta.md`
- Modify: `skills/drafting-false-arrest-complaints/SKILL.md`

- Add the narrow filed-text no-concession rule and explicit alternative-pleading
  safe harbor.
- Add the lead-authority default and separately identified-job rule without an
  absolute citation maximum.
- Add the uncertainty-purpose ledger and prune/move outcome.
- Add the actual-offense, unresolved-record, no-admission, element-level
  analysis-or-GAP rule.
- Run the focused suite, corpus, runtime skill validators, fresh-context GREEN
  pressure, `npm run validate`, forbidden-folder checks, and diff checks.
- Commit and sync.

## Task 3: Review and archive

- Review the whole branch from Issue 24 through HEAD, including OpenSpec,
  fixtures, mutation coverage, source boundaries, and interactions among the
  four rules.
- Correct accepted Critical or Important findings test-first and re-review once.
- Write `verify.md` and `retrospective.md`, archive the change, replace
  generated TBD purpose text, run final full validation, commit, and sync.
- Confirm local/origin parity, a clean worktree, Issue 25 OPEN, and no PR.

## Constraints

- No private complaint text or case-specific paragraph numbers.
- No executable checker, linter, judge-overlay, dependency, workflow, root
  `docs/`, or `.superpowers/` change.
- No code comments are expected.
- Do not create a PR or close an issue.
