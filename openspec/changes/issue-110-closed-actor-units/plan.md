# Closed Actor Application Units Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Require functionally closed actor-specific complaint applications and
preserve a paired semantic regression fixture for multi-officer false-arrest
pleadings.

**Architecture:** Strengthen the existing canonical complaint and false-arrest
Markdown references without changing the mechanical complaint checker. Extend
the established synthetic fixture corpus with one narrow deterministic shortcut
finding and independent rubric criteria for semantic closure.

**Tech Stack:** Markdown agent skills, OpenSpec, Python `unittest`, JSON
evaluation manifests, deterministic fixture grading, independent judgment
rubrics.

**Spec:**
`openspec/changes/issue-110-closed-actor-units/specs/drafting-section-1983-complaints/spec.md`

## Global Constraints

- No new QI skill, parser, dependency, or legal-sufficiency checker.
- No fixed paragraph count or needless repetition requirement.
- No case-specific name, paragraph, packet, litigation-position, or strategy
  change.
- Only alternative offenses actually raised by an opponent, controlling ruling,
  or governing law require treatment.
- Deterministic grading may preserve the explicit shortcut but cannot establish
  semantic closure or filing readiness.

---

### Task 1: OpenSpec contract and stack

**Files:**

- Create: `openspec/changes/issue-110-closed-actor-units/**`

**Interfaces:**

- Consumes: Issue #110 and the exact PR #109 branch head.
- Produces: strict change requirements, implementation boundaries, and task
  checklist.

- [ ] Strictly validate the change before implementation.
- [ ] Commit, push, and open the stacked draft PR against PR #109's branch.

### Task 2: RED contract and fixture seam

**Files:**

- Modify: `evaluations/tests/test_complaint_candor_contract.py`

**Interfaces:**

- Consumes: the three current installed references and fixture corpus.
- Produces: failing assertions for closed-unit language, audit failures,
  false-arrest fields, and the named paired fixture.

- [ ] Add focused assertions for the approved contract and fixture assets.
- [ ] Run the focused test and confirm failure for missing behavior.
- [ ] Preserve fresh-context baseline behavior before editing the references.

### Task 3: Minimal installed reference changes

**Files:**

- Modify:
  `skills/drafting-section-1983-complaints/references/complaint-contract.md`
- Modify:
  `skills/drafting-section-1983-complaints/references/completion-audit.md`
- Modify:
  `skills/drafting-false-arrest-complaints/references/false-arrest-complaint-delta.md`

**Interfaces:**

- Consumes: the approved positive actor-unit recipe.
- Produces: aligned general, audit, and false-arrest requirements.

- [ ] Add the minimal functionally closed actor-unit contract.
- [ ] Run the focused reference assertions and confirm GREEN.

### Task 4: Paired semantic regression fixture

**Files:**

- Create: `evaluations/fixtures/complaint-open-actor-unit/**`
- Modify: `evaluations/tests/test_complaint_candor_contract.py`

**Interfaces:**

- Consumes: synthetic multi-officer facts and a bounded fictional authority.
- Produces: one passing candidate, one permanent regression candidate, a narrow
  deterministic finding, and semantic rubric criteria.

- [ ] Add prompt, bounded sources, manifest, paired candidates, and rubric.
- [ ] Confirm the passing candidate is clean and the regression yields only its
      declared explicit-shortcut finding.
- [ ] Run corrected fresh-context pressure and record the observable result.

### Task 5: Completion

**Files:**

- Modify: `openspec/changes/issue-110-closed-actor-units/tasks.md`
- Create: `openspec/changes/issue-110-closed-actor-units/verify.md`
- Create: `openspec/changes/issue-110-closed-actor-units/retrospective.md`

**Interfaces:**

- Consumes: exact RED/GREEN evidence, completed change, and Git state.
- Produces: archived durable specs and a freshly verified ready stacked PR.

- [ ] Run focused mutation checks, neighboring tests, strict change validation,
      and `npm run validate`.
- [ ] Review the complete diff against Issue #110 and record verification.
- [ ] Archive the OpenSpec change, validate again, commit, push, verify exact
      remote head and checks, and mark the PR ready while leaving issue and PR
      open.
