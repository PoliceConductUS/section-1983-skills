# Recorded-Evidence Contract Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:test-driven-development and superpowers:writing-skills.

**Goal:** Preserve the intended recorded-evidence prose on a dedicated,
test-backed stacked branch and keep all three public drafting contracts aligned.

**Architecture:** A standard-library `unittest` module treats the three public
Markdown contracts as the public seam. It checks semantic obligations with
bounded regular expressions and parses the Rule 59(e) final-review numbers.

**Tech Stack:** Python 3 standard library, `unittest`, Markdown, OpenSpec 1.3.1.

## Global Constraints

- Preserve the exact intended two-file prose patch.
- Make no case-specific, dependency, workflow, or executable behavior change.
- Add no root `docs` or `.superpowers` directory and no code comments.
- Commit and run `git town sync` after every commit.

### Task 1: RED public-contract tests

**Files:**

- Create: `evaluations/tests/test_recorded_evidence_contracts.py`

- [ ] Read the three install-local public contract files.
- [ ] Require the visible-recording, verified-transcript, exact-quote,
      bounded-paraphrase, uncertain-speaker, present-recollection,
      unresolved-recording, later-correction, and failure/gap obligations.
- [ ] Extract and verify continuous Rule 59(e) final-review numbers.
- [ ] Run focused RED, commit the test and design, and sync.

### Task 2: GREEN exact prose transfer

**Files:**

- Modify:
  `skills/drafting-section-1983-complaints/references/claim-specific-contracts.md`
- Modify: `skills/drafting-section-1983-rule-59e/SKILL.md`

- [ ] Apply the exact intended `main` patch to the child worktree.
- [ ] Run focused GREEN, skill validation, and full repository validation.
- [ ] Commit and sync.

### Task 3: Review and archive

- [ ] Review test discrimination, exact prose preservation, numbering, and
      branch scope.
- [ ] Record verification and retrospective evidence.
- [ ] Archive with OpenSpec, run post-archive validation, commit, and sync.
- [ ] Confirm branch/origin parity before restoring the two `main` files.
