# Retrospective: issue-108-municipal-prerequisites

> Written: 2026-08-26 (after verification passed)  
> Commit range:
> `824bff09fc6d94529222b16f92e348ea6a0f6fdf..b807c16d6082f95da84bef449e82b5ca5ac67192`  
> Worktree:
> `/Users/dalelotts/dev/PoliceConductUS/section-1983-skills/.worktrees/issue-108-municipal-prerequisites`

---

## 0. Evidence

- **Commit range**:
  `824bff09fc6d94529222b16f92e348ea6a0f6fdf..b807c16d6082f95da84bef449e82b5ca5ac67192`
  (6 commits)
- **Diff size**: +1549 / -20 lines across 13 implementation and planning files
  before verification and retrospective artifacts
- **Tasks done**: 11/13; the two remaining tasks are archive and post-push
  exact-head readiness
- **Active hours**: about 0.5 hours from first to last pre-archive commit
- **Subagent dispatches**: 0
- **New external dependencies**: none
- **Bugs encountered post-merge**: none; the branch is unmerged
- **OpenSpec validate state at archive**: pre-archive pass, 39/39 items valid
- **Test coverage signal**: 16 focused tests, 27 core tests, and 661 evaluation
  tests passed; corpus and governance validation passed

Commit chain:

```text
95b27f7 docs: design municipal prerequisite resolution
e1258e7 docs: make municipal prerequisite change implementation-ready
2c39583 test: require municipal prerequisite resolution
bbe2131 feat: plan municipal profile prerequisites
3bdddf4 docs: resolve municipal profile prerequisites
b807c16 docs: record municipal prerequisite verification
```

## 1. Wins

- The correction at `e1258e7` changed the branch from three planning artifacts
  to a strict-valid six-artifact implementation packet before production work.
- `test_prerequisite_plan_*` captured every accepted status transition, missing
  collection authority, missing assessment and profile roles, fresh-output
  requirements, exact validation, invalid fingerprints, and valid substantive
  gaps before the planner existed.
- `bbe2131` added a pure state-to-artifact planner without changing the existing
  seven-role `build_profile_plan` compilation path or any upstream skill.
- `prerequisite-resolution.md` names the actual analysis and assessment
  artifacts, preserves mandatory independent source review, and makes every
  later stage a new least-privilege invocation.
- The full `npm run validate` result proves the installed skill remains
  discoverable and satisfies formatting, 688 automated tests, OpenSpec, corpus,
  and governance checks.

## 2. Misses

- 🟡 **Painful**: The supplied branch initially had only brainstorm, design, and
  proposal artifacts. It was correctly rejected as not implementation-ready;
  `e1258e7` supplied the missing delta spec, tasks, and executable plan.
- 🟡 **Painful**: The first plan used nonexistent names `policy-gaps.yaml` and
  `policy-assessment.yaml`. Inspecting the owning helpers before GREEN showed
  the real names `policy-analysis-gaps.yaml` and `policy-assessments.yaml`,
  corrected in `bbe2131`.
- 📌 **Nit**: Renaming the standard `## Folder inputs and output` heading broke
  `test_every_installed_skill_explains_its_exact_contract`. Restoring the
  governance-recognized heading made all 661 evaluation tests pass.
- 📌 **Nit**: Independent agent-behavior pressure testing was unavailable in
  this cycle, so the branch has deterministic public-seam coverage but no fresh
  simulated-agent RED/GREEN result.

## 3. Plan deviations

| Plan task                 | What changed                                                                                                  | Why                                                                                                                                                                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task 2 artifact contract  | Corrected two planned artifact names before implementing stage metadata.                                      | The producing helpers and installed skills are authoritative.                                                                                                                                                                      |
| Task 3 guidance tests     | Did not add regex assertions over prose.                                                                      | `writing-good-tests` requires agent behavior tests for instructional documents; deterministic planner tests and repository governance cover executable/configuration behavior, while fresh agent pressure testing was unavailable. |
| Task 3 operation boundary | Clarified resolution as pure trusted-host state preflight and compilation as the unchanged folder invocation. | A union or alternate compilation folder contract would violate the accepted least-privilege design.                                                                                                                                |

## 4. Skill / workflow compliance

| Skill                                            | Used |
| ------------------------------------------------ | ---- |
| superpowers:brainstorming                        | ✓    |
| superpowers:writing-plans                        | ✓    |
| superpowers:using-git-worktrees                  | ✓    |
| superpowers:subagent-driven-development          | ✗    |
| (transitive) superpowers:test-driven-development | ✓    |
| (transitive) superpowers:requesting-code-review  | ✗    |
| superpowers:finishing-a-development-branch       | ✗    |

### Deliberately Skipped Skills

- **`superpowers:subagent-driven-development`**
  - **What was skipped**: Fresh-context implementation and skill pressure-test
    agents.
  - **Why this cycle**: The active controller did not authorize spawning new
    subagents. The cycle therefore used the written executing plan inline and
    recorded zero dispatches.
  - **How to prevent recurrence**: **Scope-judgment rule** — when the controller
    does not authorize new agents, use inline executable RED/GREEN tests and
    record the missing independent behavior test instead of claiming it ran.
- **`superpowers:requesting-code-review`**
  - **What was skipped**: Independent post-implementation subagent review.
  - **Why this cycle**: The same no-new-subagent controller condition remained
    active after `b807c16`; no independent reviewer could be dispatched.
  - **How to prevent recurrence**: **Scope-judgment rule** — require the next
    authorized fresh-agent cycle to review the exact archived PR head, while
    keeping deterministic full-suite verification mandatory now.
- **`superpowers:finishing-a-development-branch`**
  - **What was skipped**: The post-archive finishing step at retrospective
    write-time.
  - **Why this cycle**: The OpenSpec graph requires retrospective before
    archive, while the plan requires finishing only after archived exact-head
    validation.
  - **How to prevent recurrence**: **Schema graph fix** — move finishing-branch
    compliance out of the pre-archive retrospective table or add a post-archive
    completion artifact that can record it truthfully.

## 5. Surprises

- An implementation plan can be structurally complete yet still be operationally
  wrong when it copies plausible artifact names instead of inspecting the owning
  installed skill.
- Repository governance depends on the exact standard folder-guidance heading; a
  semantically clearer heading was not compatible with the existing public
  validation contract.
- The prerequisite resolver cannot be modeled as a second union-folder
  compilation mode without weakening the exact seven-role contract. The safe
  seam is pure host-validated state that proposes one later invocation.

## 6. Promote candidates → long-term learning

- [ ] 🟡 **Verify every cross-skill artifact name against its producing helper
      before declaring an OpenSpec plan implementation-ready.** → **Promote to
      schema**
  > **Why**: Issue #108's first executable plan named two artifacts that do not
  > exist, even though its high-level architecture was correct.  
  > **How to apply**: For any plan that sequences installed skills, inspect the
  > producer's return-artifact list and copy the exact canonical paths into the
  > plan, delta spec, tests, and guidance before implementation begins.
- [ ] 📌 **Instructional prose needs fresh-agent behavior testing, not regex
      source assertions.** → **Promote to project workflow guidance**
  > **Why**: Deterministic tests can prove planner behavior, but they cannot
  > prove an agent will follow a staged review and authorization workflow under
  > pressure.  
  > **How to apply**: When new-agent dispatch is authorized, run the same
  > missing-prerequisite scenario without and with the installed skill and
  > retain the observed behavior in the change verification record.
