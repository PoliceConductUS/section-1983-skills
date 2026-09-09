# Post-Draft Assertion Validation Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development to
> implement this plan task-by-task.

**Goal:** Add one shared, read-only assertion-validation owner and connect every
applicable court-facing drafting and review workflow to its correction and
freshness loop.

**Architecture:** A new public skill owns the semantic validation and report
contract. Existing drafting and review skills keep their domain-specific
authority and reference the shared owner at explicit handoff points. Repository
governance tests enforce ownership and routing; behavioral fixtures pressure the
seven approved semantic scenarios without claiming deterministic legal judgment.

**Tech Stack:** Markdown public skills and references, JSON folder contracts,
Python `unittest` evaluations, OpenSpec superpowers bridge, npm repository
validation.

---

## Task 1: Establish failing public-contract tests

- [ ] **Step 1:** Add
      `evaluations/tests/test_post_draft_assertion_validation.py` with a
      missing-skill failure and assertions for required report fields, statuses,
      freshness, omission rules, and consumer references.
- [ ] **Step 2:** Run
      `python3 -m unittest evaluations.tests.test_post_draft_assertion_validation`
      and confirm failure because the shared skill does not exist.
- [ ] **Step 3:** Add paired fixtures representing the seven approved acceptance
      scenarios and a fixture evaluator that checks expected classifications.
- [ ] **Step 4:** Run the focused test again and confirm the semantic fixtures
      fail against the absent contract.
- [ ] **Step 5:** Commit the red tests and OpenSpec planning artifacts, push,
      and open the Issue #114 pull request as draft.

## Task 2: Implement the shared validation package

- [ ] **Step 1:** Create `skills/validating-court-facing-assertions/SKILL.md`
      with declared roles, one required target, denied internet, read-only
      review, specialist routing, and correction-loop handoff.
- [ ] **Step 2:** Create
      `skills/validating-court-facing-assertions/references/assertion-validation-contract.md`
      containing the atomic record, status taxonomy, source and authority
      checks, omission matrix, freshness rules, Mermaid requirements, and
      stopping criteria.
- [ ] **Step 3:** Add the install-local folder contract and any required public
      registry or README entries.
- [ ] **Step 4:** Run the focused tests and inspect the remaining failures.
- [ ] **Step 5:** Commit and push the shared package.

## Task 3: Integrate existing drafting and review skills

- [ ] **Step 1:** Update `section-1983-drafting` to load the shared validator
      for every generated court-facing final candidate and orchestrate separate
      correction and revalidation.
- [ ] **Step 2:** Update complaint, Rule 59(e), and Monell drafting at their
      canonical handoff points without copying the detailed validation contract.
- [ ] **Step 3:** Update authority audit to provide specialist proposition
      findings; keep defense review downstream and Filing CI deterministic.
- [ ] **Step 4:** Update governance validation and tests to require the shared
      semantic owner and consumer references while preserving compact
      install-local QC safeguards.
- [ ] **Step 5:** Run the focused contract, governance, drafting, authority,
      adversarial, and Filing CI tests.
- [ ] **Step 6:** Commit and push integration changes.

## Task 4: Pressure-test and verify

- [ ] **Step 1:** Run baseline and post-change fresh-context behavior checks
      required by the writing-skills discipline; store bounded evidence in the
      OpenSpec change.
- [ ] **Step 2:** Run `npm run format:check` and correct formatting only where
      required.
- [ ] **Step 3:** Run `npm run validate` and fix every in-scope failure.
- [ ] **Step 4:** Perform independent review, apply supported corrections in the
      implementation worktree, and rerun affected checks.
- [ ] **Step 5:** Complete `verify.md` and `retrospective.md`, mark every task
      complete, archive the OpenSpec change, and run `npm run validate` on the
      archived state.
- [ ] **Step 6:** Commit and push final artifacts, verify the exact remote head
      and checks, mark the PR ready for review, and leave Issue #114 and its PR
      open.
