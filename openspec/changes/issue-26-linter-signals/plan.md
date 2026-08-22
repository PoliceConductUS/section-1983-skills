# Drafting-Linter Signals Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans
> to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for
> tracking.

**Goal:** Add location-bearing linter findings, proven term-of-art exemptions,
non-gating paragraph-density warnings, and exhaustive reconciliation guidance.

**Architecture:** Extend the existing standard-library linter without replacing
its aggregate interface. Parse source text into line-bearing paragraphs, run the
current checks per paragraph, and add separate exemption and warning records.
Keep source verification and final quotation classification in the drafting
workflow.

**Tech Stack:** Python standard library, `unittest`, Markdown, OpenSpec.

**Spec:** `openspec/changes/issue-26-linter-signals/design.md`

## Global Constraints

- Preserve current aggregate output and score-delta behavior.
- Add no dependency or legal/file-readiness gate.
- Add only the three exemptions proven by RED.
- Use no root `docs/`, `.superpowers/`, case-specific content, or code comments.
- Commit and run `git town sync` after each commit.

---

### Task 1: Public RED contract

**Files:**

- Modify: `skills/section-1983-drafting/scripts/test_draft_lint.py`
- Create: `evaluations/tests/test_draft_linter_contract.py`

**Interfaces:**

- Consumes: current `lint(text)` and public CLI behavior.
- Produces: failing tests for `lint(text, artifact)`, `findings`, `exemptions`,
  `warnings`, and drafting reconciliation semantics.

- [ ] Add table-driven tests for the three proven false positives and four inert
      suggestions.
- [ ] Add literal multi-paragraph and multi-path location expectations.
- [ ] Add synthetic rhetoric, compliant-analysis, density-threshold, quotation,
      aggregate-reconciliation, and non-gating tests.
- [ ] Run the focused tests and confirm failures arise from missing Issue 26
      behavior.
- [ ] Commit RED and sync.

### Task 2: Minimal GREEN

**Files:**

- Modify: `skills/section-1983-drafting/scripts/draft_lint.py`
- Modify: `skills/section-1983-drafting/SKILL.md`
- Modify: `skills/section-1983-drafting/references/writing-system.md`
- Modify: `skills/section-1983-drafting/references/banned-words.md`

**Interfaces:**

- Consumes: Task 1 public tests.
- Produces: backward-compatible location-bearing report records and the exact
  final reconciliation workflow.

- [ ] Parse nonblank paragraph groups with one-based line locations.
- [ ] Emit bounded paragraph findings whose counts reconcile with aggregates.
- [ ] Add only the three proven controlling-term exemptions and their records.
- [ ] Add fixed two-long-sentence and four-case-citation warnings outside the
      score.
- [ ] Update the owning guidance with the exhaustive residual disposition and
      feedback-only rules.
- [ ] Run focused GREEN, commit, and sync.

### Task 3: Pressure, review, and archive

**Files:**

- Modify: tests and production only when a review finding first has a failing
  test.
- Create: `openspec/changes/issue-26-linter-signals/verify.md`
- Create: `openspec/changes/issue-26-linter-signals/retrospective.md`

**Interfaces:**

- Consumes: complete Issue 26 story.
- Produces: reviewed, archived, durable `drafting-linter-signals` capability.

- [ ] Pressure malformed, empty, multiline, quote, threshold, location, and
      score-reconciliation boundaries; capture accepted defects as RED.
- [ ] Run focused, full, formatting, OpenSpec, corpus, governance, compilation,
      forbidden-folder, private-marker, code-comment, and diff checks.
- [ ] Complete verification and retrospective artifacts, archive the change,
      replace any generated Purpose placeholder, validate the durable spec,
      commit, sync, and prove clean origin parity with Issue 26 open and no PR.
