# Monell Proposition Classification Implementation Plan

**Goal:** Make Monell proposition placement and staged development explicit
across planning, drafting, and post-draft validation.

**Architecture:** The planning contract owns the three proposition classes,
their required basis, and the staged-development record. The drafting contract
consumes approved classifications and bars speculative preservation pleadings.
Existing whole-document assertion validation remains the post-integration
reviewer and checks that expected discovery has not become a present fact.

**Tech Stack:** Markdown public skills and references, Python `unittest`
evaluations, JSON synthetic fixtures, OpenSpec, and npm repository validation.

---

## Task 1: Establish red contract and behavior checks

- [x] **Step 1:** Add focused contract tests for the three planning classes and
      drafting placement rules.
- [x] **Step 2:** Add paired behavioral regressions and a passing candidate.
- [x] **Step 3:** Run focused tests and confirm they fail because the approved
      contract is absent.

## Task 2: Implement the bounded contracts

- [x] **Step 1:** Add the proposition-classification record to the planning
      reference.
- [x] **Step 2:** Add the approved placement rule to the drafting reference and
      connect the drafting entrypoint to it.
- [x] **Step 3:** Run focused tests and confirm they pass.
- [x] **Step 4:** Require proposition records and class-specific bases in the
      install-local complaint-handoff validator.

## Task 3: Verify and deliver

- [x] **Step 1:** Run fresh-context guided pressure tests and preserve bounded
      baseline and green evidence.
- [x] **Step 2:** Run `npm run validate` and correct in-scope failures.
- [x] **Step 3:** Complete verification and retrospective artifacts, archive the
      OpenSpec change, commit, and push each commit.
- [x] **Step 4:** Record that GitHub issue and PR creation were not requested in
      this delivery.

## Task 4: Extend RED checks for staged development

- [x] **Step 1:** Preserve five fresh-context baseline runs showing omissions in
      the pre-extension staged-development response.
- [x] **Step 2:** Add focused contract tests for complete internal path records,
      request-specific relevance, diligence, amendment standards, and validation
      of expected-discovery claims.
- [x] **Step 3:** Add isolated behavioral regressions and confirm focused tests
      fail against the current contract.

## Task 5: Implement and pressure-test staged development

- [x] **Step 1:** Extend planning with the staged-development record and
      reassessment workflow.
- [x] **Step 2:** Extend drafting with the no-placeholder and amendment-entry
      gates.
- [x] **Step 3:** Extend shared validation with the Monell expected-discovery
      check.
- [x] **Step 4:** Run focused tests, five fresh guided pressure tests,
      independent review, and full repository validation.
