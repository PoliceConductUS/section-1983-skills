# Unknown and New-Defendant Limitations Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Require a complete defendant-specific limitations analysis before a
complaint amendment that adds, identifies, or substitutes an at-risk individual
can be treated as filing-ready.

**Architecture:** The canonical complaint contract owns the record-driven
trigger and the ten-part per-defendant record. Its completion audit owns the
filing-critical result. A synthetic evaluator exercises the gate without adding
a runtime dependency or modifying specialized false-arrest guidance.

**Tech Stack:** Markdown agent skills, OpenSpec, Python `unittest`, YAML
synthetic fixtures.

**Spec:**
`openspec/changes/issue-102-unknown-defendant-limitations/specs/drafting-section-1983-complaints/spec.md`

## Global Constraints

- Do not invent a universal numeric definition of "near limitations."
- Keep Rule 15(c)(1)(A) and Rule 15(c)(1)(C) analyses separate.
- Keep every required record defendant-specific where applicable.
- Treat every missing or unresolved required entry as an internal
  filing-critical GAP that blocks filing-ready status.
- Do not change the false-arrest seizure-point or general actor-causation
  contracts.
- Add no runtime dependency, package, graph, repository, or persistence layer.

---

### Task 1: RED limitations-gate evaluation

**Files:**

- Create: `evaluations/unknown-defendant-limitations/v1/scenarios.yaml`
- Create: `evaluations/tests/test_unknown_defendant_limitations_gate.py`

**Interfaces:**

- Consumes: synthetic amendment timing, identified risk sources, affected
  defendants, candidate limitations records, and claimed readiness.
- Produces: literal stable findings for trigger omission, missing defendant
  records, missing required entries, collapsed Rule 15 analysis, and incorrect
  filing-ready status.

- [ ] Write YAML scenarios for a passed deadline, identified pre-deadline risk,
      two affected defendants, a complete record, and unresolved entries.
- [ ] Write a focused evaluator whose expected findings are literal fixture
      values and whose guidance checks cover the approved contract.
- [ ] Run
      `python3 -m unittest evaluations.tests.test_unknown_defendant_limitations_gate`
      and confirm failure because the current complaint references omit the
      gate.
- [ ] Commit and push the RED evaluation evidence.

### Task 2: Minimal complaint contract

**Files:**

- Modify:
  `skills/drafting-section-1983-complaints/references/complaint-contract.md`
- Modify:
  `skills/drafting-section-1983-complaints/references/completion-audit.md`

**Interfaces:**

- Consumes: the calculated limitations deadline and any covered risk raised by
  the supplied record, an opposing party, the court, or the caller.
- Produces: one complete internal limitations record per affected individual or
  a filing-critical GAP that blocks filing-ready status.

- [ ] Add one canonical limitations-gate section containing the approved trigger
      and all ten required categories.
- [ ] Add one completion-audit item requiring a complete record for every
      affected individual and the filing-critical result for every unresolved
      entry.
- [ ] Run the focused test and confirm every scenario passes.
- [ ] Commit and push the minimal guidance.

### Task 3: Verification and archive

**Files:**

- Modify: `openspec/changes/issue-102-unknown-defendant-limitations/tasks.md`
- Create after implementation:
  `openspec/changes/issue-102-unknown-defendant-limitations/verify.md`
- Create after verification:
  `openspec/changes/issue-102-unknown-defendant-limitations/retrospective.md`

**Interfaces:**

- Consumes: completed contract, evaluation, and exact Git state.
- Produces: archived durable specification and a freshly verified stacked PR.

- [ ] Temporarily remove one operative guidance clause, confirm the focused
      evaluation fails, restore it, and confirm it passes.
- [ ] Run the focused neighboring complaint suites and confirm they pass.
- [ ] Run
      `npx openspec validate issue-102-unknown-defendant-limitations --strict`.
- [ ] Run `npm run validate` and inspect the complete output.
- [ ] Complete verification and retrospective artifacts, archive the change,
      commit, push, and verify the exact remote head.
- [ ] Mark PR #103 ready while leaving it and Issue #102 open.
