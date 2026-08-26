# Arresting Officer First Defendant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Require the source-documented primary arresting officer to lead every
ordered defendant presentation in new or materially revised Section 1983
filings.

**Architecture:** The umbrella skill owns the cross-document trigger. The
canonical complaint references own complaint presentation and completion. The
false-arrest actor audit supplies arresting-officer identity and primary
designation state. Synthetic evaluations cover every decision branch.

**Tech stack:** Markdown agent skills, OpenSpec, Python `unittest`, JSON or YAML
synthetic fixtures.

**Spec:**
`openspec/changes/issue-100-arresting-officer-first/specs/arresting-officer-defendant-ordering/spec.md`

## Global Constraints

- Use only caller-declared recursive read-only input folders and one exact full
  absolute output folder.
- Keep temporary work beneath `<output-folder>/temp/`.
- Add no package, graph, CaseGraph, repository abstraction, or runtime tool.
- Do not hard-code Markham or infer a primary among several arresting officers.

---

### Task 1: RED regression evaluation

**Files:**

- Create: `evaluations/tests/test_arresting_officer_defendant_order.py`
- Create: `evaluations/fixtures/arresting-officer-defendant-order/`

**Interfaces:**

- Consumes: synthetic arrest status, caller designation, defendant order, and
  chronology order.
- Produces: focused assertions for one officer, legacy correction, several
  officers with and without designation, and no arrest.

- [ ] Write fixtures with literal expected outcomes and a test that checks the
      real installed guidance and candidate filing behavior.
- [ ] Run
      `python3 -m unittest evaluations.tests.test_arresting_officer_defendant_order`
      and confirm failure because the current instructions omit the contract.
- [ ] Commit and push the RED evaluation evidence.

### Task 2: Minimal skill guidance

**Files:**

- Modify: `skills/section-1983-drafting/SKILL.md`
- Modify:
  `skills/drafting-section-1983-complaints/references/complaint-contract.md`
- Modify:
  `skills/drafting-section-1983-complaints/references/completion-audit.md`
- Modify:
  `skills/drafting-false-arrest-complaints/references/false-arrest-complaint-delta.md`

**Interfaces:**

- Consumes: caller-declared source folders and any caller-declared primary.
- Produces: one arrest status, one selected primary or clarification request,
  and compliant defendant presentation order.

- [ ] Add the umbrella pre-draft arrest audit and cross-document ordering rule.
- [ ] Add the complaint-specific ordered presentations and completion check.
- [ ] Add primary-designation state to the false-arrest actor audit.
- [ ] Run the focused test and confirm every scenario passes.
- [ ] Commit and push the minimal guidance.

### Task 3: Verification and archive

**Files:**

- Modify: `openspec/changes/issue-100-arresting-officer-first/tasks.md`
- Create after verification:
  `openspec/changes/issue-100-arresting-officer-first/verify.md`
- Create after verification:
  `openspec/changes/issue-100-arresting-officer-first/retrospective.md`

**Interfaces:**

- Consumes: complete implementation and exact Git state.
- Produces: archived durable spec and verified ready stacked PR.

- [ ] Remove one operative guidance clause in a temporary mutation, confirm the
      focused test fails, restore it, and confirm the test passes.
- [ ] Run `npx openspec validate issue-100-arresting-officer-first --strict`.
- [ ] Run `npm run validate` and inspect the complete output.
- [ ] Complete verification and retrospective artifacts, archive the change,
      commit, push, and verify the remote head.
- [ ] Mark the PR ready while leaving the PR and Issue #100 open.
