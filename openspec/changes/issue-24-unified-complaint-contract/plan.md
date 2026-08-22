# Unified Section 1983 Complaint Contract Implementation Plan

> **For agentic workers:** Use `subagent-driven-development` to implement this
> plan task by task. Use `test-driven-development`, `writing-good-tests`, and
> `writing-skills` for every instruction change.

**Goal:** Give every complaint workflow one complete canonical general contract
and a stable external-checker handoff without implementing the checker here.

**Architecture:** `drafting-section-1983-complaints` owns a human reference and
a JSON mechanical contract. The umbrella routes and fails closed; the
false-arrest package adds only its issue-specific delta. Deterministic package
tests and fresh-agent pressure verify both structure and behavior.

**Tech stack:** Markdown skills, JSON, Python standard-library `unittest`,
OpenSpec superpowers bridge, Git Town, Git worktrees.

**Spec:**
`openspec/changes/issue-24-unified-complaint-contract/specs/drafting-section-1983-complaints/spec.md`

## Global constraints

- Keep one canonical general owner: `drafting-section-1983-complaints`.
- Preserve the canonical section order and one count mapping per
  claim-defendant-capacity tuple.
- The deterministic handoff covers only mechanical structure and excludes fact
  truth, legal sufficiency, authority fit, material analogy, strategy, and
  filing readiness.
- Do not add an executable filing checker, dependency, workflow, root `docs/`,
  or `.superpowers/` directory.
- Use no code comments unless self-documenting code is unreasonable and the
  comment can cite a decision; none are expected here.
- Do not modify unrelated skills or the CaseGraph repository.
- Commit and run `git town sync` after each commit. Do not create a PR or close
  either issue.

---

## Task 1: RED composition and contract tests

**Files:**

- Create: `evaluations/tests/test_complaint_contract_composition.py`
- Update: `openspec/changes/issue-24-unified-complaint-contract/brainstorm.md`
- Update: `openspec/changes/issue-24-unified-complaint-contract/tasks.md`

- [ ] Record the three baseline fresh-agent outputs and exact omissions,
      conflicts, or unavailable-contract results in `brainstorm.md`.
- [ ] Add a test helper that copies an affected package to a temporary isolated
      install, parses live Markdown links outside code examples, resolves each
      local target, and rejects escaping or missing links.
- [ ] Add tests that require one parseable canonical JSON contract under the
      general package and independently assert the literal ordered sections,
      count cardinality, required fields, conditional qualified-immunity fields,
      included mechanical checks, excluded judgments, stable finding fields, and
      nonzero-failure contract.
- [ ] Add isolated-composition tests that reject a competing general skeleton in
      the umbrella, reject a generic skeleton/count list in the false-arrest
      delta, require explicit fail-closed routing, and detect removal or
      inversion of those routes.
- [ ] Name each realistic production mutation the test catches. Do not assert
      only a phrase or mock; parse and exercise the copied package contract.
- [ ] Run
      `python3 -m unittest evaluations.tests.test_complaint_contract_composition -v`
      and verify failures are caused only by the absent canonical files and
      current duplicate ownership.
- [ ] Run
      `python3 -m py_compile     evaluations/tests/test_complaint_contract_composition.py`
      and `git diff --check`.
- [ ] Mark Task 1 checkboxes complete, commit as
      `test: expose split complaint contract ownership`, then run
      `git town sync` and verify origin parity.

## Task 2: GREEN canonical general complaint contract

**Files:**

- Create:
  `skills/drafting-section-1983-complaints/references/complaint-contract.md`
- Create:
  `skills/drafting-section-1983-complaints/references/complaint-structure-contract.json`
- Modify: `skills/drafting-section-1983-complaints/SKILL.md`
- Modify: `skills/section-1983-drafting/references/documents/complaint.md`
- Modify: `skills/section-1983-drafting/SKILL.md`

- [ ] Create the JSON mechanical contract with version `1`, canonical owner
      `drafting-section-1983-complaints`, the approved section order,
      cardinality and field lists, deterministic checks, excluded judgments,
      finding shape, and nonzero failure status.
- [ ] Create the human contract by moving the umbrella skeleton and detailed
      general count requirements under the canonical package. Preserve all
      governing requirements; do not create a second divergent summary.
- [ ] Make the general `SKILL.md` require both install-local references before
      complaint drafting, revision, or audit and fail closed when either is
      unavailable. Keep only the compact core standard in `SKILL.md` where a
      summary is useful.
- [ ] Replace the umbrella complaint document with a routing/fail-closed entry.
      Update the umbrella workflow so complaints never draft from a local
      fallback while other document skeletons remain unchanged.
- [ ] Run the focused test and the runtime skill validator for both affected
      packages. Verify the remaining RED failures concern only the false-arrest
      duplicate and README composition.

## Task 3: GREEN false-arrest delta and public composition

**Files:**

- Rename:
  `skills/drafting-false-arrest-complaints/references/complaint-contract.md` to
  `skills/drafting-false-arrest-complaints/references/false-arrest-complaint-delta.md`
- Modify: `skills/drafting-false-arrest-complaints/SKILL.md`
- Modify: `README.md`
- Modify: `skills/filing-ci/SKILL.md` only if the existing text does not already
  state the approved external-checker boundary

- [ ] Retain only false-arrest-specific seizure, offense, actor, chronology,
      incorporated-material, warrant, and compression rules in the renamed
      delta. Remove the generic whole skeleton, generic count list, general
      qualified-immunity matrix, and generic Monell contract.
- [ ] Require the canonical general complaint package and both canonical
      references before applying the delta. Fail closed rather than promote the
      delta to a replacement contract.
- [ ] Update workflow and audit-output references so they add specialization
      requirements without restating the general contract.
- [ ] Update README to identify the general owner, load order, fail-closed
      dependency, and CaseGraph checker boundary.
- [ ] Change `filing-ci` only if needed to preserve thin project-configured
      orchestration; do not add checker logic or invent an invocation.
- [ ] Run the focused test until GREEN, run all three isolated GREEN pressure
      scenarios, and record exact results and hashes in `brainstorm.md`.
- [ ] Run runtime skill validation, full evaluation tests, `npm run validate`,
      `git diff --check`, and forbidden-folder checks.
- [ ] Mark Tasks 2 and 3 complete, commit as
      `feat: unify the Section 1983 complaint contract`, then run
      `git town sync` and verify origin parity.

## Task 4: Whole-story review, verification, and archive

**Files:**

- Create: `openspec/changes/issue-24-unified-complaint-contract/verify.md`
- Create:
  `openspec/changes/issue-24-unified-complaint-contract/retrospective.md`
- Update: `openspec/changes/issue-24-unified-complaint-contract/tasks.md`
- Archive the active change through OpenSpec

- [ ] Build a whole-branch review package from the Issue 23 parent to HEAD and
      dispatch an independent spec/quality reviewer.
- [ ] If Critical or Important findings exist, dispatch one correction task,
      require covering tests, and run one scoped re-review.
- [ ] Run realistic mutations: remove a section, invert fail-closed routing, add
      a second owner, move a general count field into the delta, escape a local
      link, and turn an excluded judgment into a deterministic check.
- [ ] Complete every task checkbox and write `verify.md` with structural,
      behavioral, pressure-test, full-suite, diff, scope, branch, and origin
      evidence.
- [ ] Write the retrospective with exact RED/GREEN findings and deviations.
- [ ] Archive `issue-24-unified-complaint-contract`, validate all durable specs,
      run `npm run validate`, commit as
      `docs: archive unified complaint contract`, and run `git town sync`.
- [ ] Verify the worktree is clean, local HEAD equals origin, Issue 24 remains
      open, and no PR exists.
