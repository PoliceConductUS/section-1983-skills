# Municipal Profile Prerequisite Resolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the public municipal-profile skill deterministically route and
validate its missing police-policy prerequisites before resuming unchanged
profile compilation.

**Architecture:** Add a pure domain planner to the existing municipal-profile
helper. It receives only validated state supplied by the trusted host and emits
ordinary YAML/Markdown next-step artifacts; it never opens folders or launches
commands. The installed skill uses that plan to sequence existing collection,
analysis, assessment, and compilation as separate invocations.

**Tech Stack:** Python 3 standard library, PyYAML, unittest, Markdown skills,
OpenSpec.

**Spec:** `openspec/changes/issue-108-municipal-prerequisites/design.md` and
`openspec/changes/issue-108-municipal-prerequisites/specs/building-municipal-monell-profiles/spec.md`

## Global Constraints

- Keep municipal-profile compilation's exact seven read-only roles and disabled
  internet unchanged.
- Every stage has one separate caller-supplied full absolute output folder and
  output-local `temp/`.
- Collection candidates cannot approve themselves.
- Valid substantive gaps remain valid; mechanical postcondition failures block.
- Add no network client, dependency, general workflow engine, graph, CaseGraph,
  repository operation, or persistence abstraction.

## Task 1: RED state-machine contract

**Files:**

- Modify: `evaluations/tests/test_building_municipal_monell_profiles.py`
- Test: `evaluations/tests/test_building_municipal_monell_profiles.py`

**Interfaces:**

- Consumes: current `load_module()` test loader.
- Produces: the required
  `build_prerequisite_plan(*, policy_source_state, policy_catalog, policy_assessment, available_roles, output_folders, collection_authorization)`
  public helper contract.

- [ ] **Step 1: Add reusable exact workflow fixtures**

  Add stage-role constants matching each installed folder contract and helper
  values shaped as follows:

  ```python
  valid_upstream = {
      "state": "valid",
      "terminal_receipt": True,
      "expected_artifacts": True,
      "validation_passed": True,
      "fingerprints_match": True,
  }
  unavailable = {
      "state": "absent",
      "terminal_receipt": False,
      "expected_artifacts": False,
      "validation_passed": False,
      "fingerprints_match": False,
  }
  ```

- [ ] **Step 2: Add one failing test per next-stage class**

  Cover these observable results:

  ```python
  self.assertEqual(plan["status"], "ready-for-analysis")
  self.assertEqual(plan["next_skill"], "analyzing-police-policy-sources")
  self.assertEqual(plan["internet"], "disabled")
  self.assertEqual(
      [item["path"] for item in plan["artifacts"]],
      [
          "municipal-profile-prerequisites.yaml",
          "municipal-profile-prerequisites.md",
      ],
  )
  ```

  Include absent sources ready for collection, missing internet authorization,
  fee-required without fee approval, candidate sources requiring review,
  approved sources ready for analysis, valid catalog ready for assessment, valid
  catalog and assessment ready for profile, missing roles, and missing output
  folders.

- [ ] **Step 3: Add mechanical-postcondition and gap tests**

  Assert that `state: valid` with any false receipt/artifact/validation/
  fingerprint flag yields `blocked-invalid`, while the same fully true record
  plus a `substantive_gaps: True` field remains eligible for the next stage.

- [ ] **Step 4: Verify RED**

  Run:

  ```bash
  python3 -m unittest evaluations.tests.test_building_municipal_monell_profiles
  ```

  Expected: existing profile tests pass and every prerequisite-planner test
  errors because `build_prerequisite_plan` is absent.

- [ ] **Step 5: Commit and push RED tests**

  ```bash
  git add evaluations/tests/test_building_municipal_monell_profiles.py
  git commit -m "test: require municipal prerequisite resolution"
  git push
  ```

## Task 2: Deterministic prerequisite planner

**Files:**

- Modify:
  `skills/building-municipal-monell-profiles/scripts/municipal_profile_records.py`
- Test: `evaluations/tests/test_building_municipal_monell_profiles.py`

**Interfaces:**

- Consumes: exact state records and caller-supplied availability booleans from
  Task 1.
- Produces: `build_prerequisite_plan(...) -> dict` with top-level `status`,
  `next_skill`, `internet`, and ordered `artifacts`.

- [ ] **Step 1: Add exact enums and stage contracts**

  Define immutable stage metadata for collection, analysis, assessment, and
  profile, including exact required roles, installed skill name, internet mode,
  expected artifacts, and ordered postconditions.

- [ ] **Step 2: Validate exact planner inputs**

  Reject unknown source/upstream states, unknown stage keys, duplicate or
  unknown roles, non-boolean authorization/output values, and additional fields
  with stable `MunicipalProfileError` codes.

- [ ] **Step 3: Implement fixed precedence**

  Select exactly one state in this order:

  ```text
  invalid catalog/assessment mechanical state -> blocked-invalid
  valid catalog + valid assessment -> profile readiness
  valid catalog -> assessment readiness
  approved source -> analysis readiness
  candidate source -> review-required
  absent source -> collection input, authorization, fee, output, readiness
  ```

  For each stage, missing required roles precede a missing output folder.

- [ ] **Step 4: Render deterministic artifacts**

  Emit sorted, stable YAML and concise Markdown. The YAML includes:

  ```yaml
  version: 1
  workflow: municipal-profile-prerequisites
  status: ready-for-assessment
  next_skill: assessing-police-policy-compliance
  required_roles: []
  missing_roles: []
  internet: disabled
  output_folder:
    required: true
    supplied: true
  blocking_reasons: []
  postconditions: []
  ```

- [ ] **Step 5: Verify GREEN**

  Run the focused module and confirm every old and new test passes.

- [ ] **Step 6: Commit and push the planner**

  ```bash
  git add skills/building-municipal-monell-profiles/scripts/municipal_profile_records.py
  git commit -m "feat: plan municipal profile prerequisites"
  git push
  ```

## Task 3: Installed public workflow guidance

**Files:**

- Create:
  `skills/building-municipal-monell-profiles/references/prerequisite-resolution.md`
- Modify: `skills/building-municipal-monell-profiles/SKILL.md`
- Modify:
  `skills/building-municipal-monell-profiles/references/source-documented-folders.md`
- Modify: `README.md`
- Modify: `evaluations/tests/test_building_municipal_monell_profiles.py`

**Interfaces:**

- Consumes: Task 2 prerequisite plan states.
- Produces: one discoverable installed workflow that chooses exactly one
  operation and never changes upstream folder contracts.

- [ ] **Step 1: Add failing installed-surface assertions**

  Require the skill and reference to state: separate resolution/compilation,
  exact staged skills, fresh invocation and output folder per stage, mandatory
  post-collection review, terminal receipt/artifact/validation/fingerprint
  postconditions, valid-gap continuation, no inherited network authority, and no
  self-approval or invented inputs.

- [ ] **Step 2: Verify the guidance RED state**

  Run the focused module and confirm only the new installed-surface assertions
  fail.

- [ ] **Step 3: Write the minimal reference and routing changes**

  Add a status quick-reference table, preflight order, stage preconditions,
  postconditions, and stop conditions. Link it from the installed skill and
  update README step 11 to describe prerequisite resolution before compilation.

- [ ] **Step 4: Verify the complete focused module**

  Run:

  ```bash
  python3 -m unittest evaluations.tests.test_building_municipal_monell_profiles
  ```

  Expected: all tests pass.

- [ ] **Step 5: Commit and push installed guidance**

  ```bash
  git add README.md evaluations/tests/test_building_municipal_monell_profiles.py skills/building-municipal-monell-profiles
  git commit -m "docs: resolve municipal profile prerequisites"
  git push
  ```

## Task 4: Verification and archive

**Files:**

- Modify: `openspec/changes/issue-108-municipal-prerequisites/tasks.md`
- Create: `openspec/changes/issue-108-municipal-prerequisites/verify.md`
- Create: `openspec/changes/issue-108-municipal-prerequisites/retrospective.md`
- Modify: `openspec/specs/building-municipal-monell-profiles/spec.md`

- [ ] **Step 1: Run focused and strict checks**

  ```bash
  python3 -m unittest evaluations.tests.test_building_municipal_monell_profiles
  npx openspec validate issue-108-municipal-prerequisites --strict
  ```

- [ ] **Step 2: Run complete repository validation**

  ```bash
  npm run validate
  ```

- [ ] **Step 3: Review the exact stacked diff**

  Compare against `origin/codex/issue-106-judicial-profile-discovery` and verify
  no upstream skill contract, dependency, network client, or unrelated file was
  changed.

- [ ] **Step 4: Complete verification, retrospective, and archive**

  Record RED/GREEN evidence and the initial load-sensitive baseline rerun, then:

  ```bash
  npx openspec archive issue-108-municipal-prerequisites -y
  npm run validate
  ```

- [ ] **Step 5: Commit and push the archived cycle**

  ```bash
  git add openspec
  git commit -m "docs: archive municipal prerequisite resolution spec"
  git push
  ```

- [ ] **Step 6: Verify live exact-head readiness**

  Confirm PR #109 remains stacked on PR #107, its head equals the pushed SHA,
  GitHub checks pass, and Issue #108 remains open. Mark PR #109 ready while
  leaving both open.
