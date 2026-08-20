# Retrospective: issue-14-judgment-rules-governance

> Written: 2026-08-20 (after pre-archive verification passed) Commit range:
> `fefaeb2..c870c58` Worktree:
> `/Users/dalelotts/dev/PoliceConductUS/section-1983-skills/.worktrees/issue-14-governance`

---

## 0. Evidence

- **Commit range**: `fefaeb2..c870c58` (5 commits).
- **Diff size**: +1,528 / -3 lines across 24 files before the Task 3 evidence
  files.
- **Tasks done**: 9/10; Task 3.4 remains intentionally unchecked because this
  dispatch does not archive.
- **Active hours**: 28 minutes and 29 seconds by author timestamps from
  `5c15067` through `c870c58`; elapsed effort is not otherwise inferred.
- **Subagent dispatches**: n/a for the implementation history; Task 3 used 0, as
  its brief prohibited delegation.
- **New external dependencies**: none; the validator uses the Python standard
  library and the package manifest adds no dependency.
- **Bugs encountered post-merge**: none; the branch is pre-archive and has not
  merged.
- **OpenSpec validate state at archive**: archive not run by scope; pre-archive
  `npx openspec validate --all --json` reported 10 valid items and 0 failures.
- **Test coverage signal**: 21 focused governance tests passed; the full gate
  passed 16 skill-script tests, 149 evaluation tests, 20 skill quick validators,
  and all repository validation stages.

Commit chain:

```text
5c15067 docs: design repository skill governance
ff2469b test: define repository governance contracts
f4c2cce test: cover governance registry invariants
4ebe519 feat: enforce repository skill governance
c870c58 fix: harden governance provenance validation
```

---

## 1. Wins

- [evidence: `GOVERNANCE.md`, `governance/rules-provenance.json`, and the 21
  focused tests] One public policy plus one registry made all 20 public skills
  mechanically auditable without adding a rules-retrieval system.
- [evidence: `scripts/validate_governance.py` and its invalid-state tests]
  Fail-closed validation covers mismatched entries, invalid modes and dates,
  missing provenance, insecure URLs, missing jurisdiction references, and
  missing protected-review language.
- [evidence: Task 3 quick validation: 20 total, 0 failures] Narrow additions to
  eight runtime-sourced skills made their required artifact provenance explicit
  without adding executable general-purpose tooling.

## 2. Misses

- None observed in the verified pre-archive scope.

## 3. Plan deviations

| Plan task | What changed                                                                                                                                 | Why                                                                                                                                                                                                      |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.2 / 2.3 | The implementation added explicit output-provenance contract text to all eight runtime-sourced SKILL files and hardened its validator tests. | The controller ruled that the runtime-output contract required this narrow scope expansion so the registry requirement was reflected in every affected public contract, not solely in registry metadata. |
| 3.4       | Archive and canonical-spec sync are not performed in this dispatch.                                                                          | The Task 3 brief expressly reserves archive to the controller after task and whole-branch review.                                                                                                        |

## 4. Skill / workflow compliance

| Skill                                              | Used |
| -------------------------------------------------- | ---- |
| `superpowers:brainstorming`                        | ✓    |
| `superpowers:writing-plans`                        | ✓    |
| `superpowers:using-git-worktrees`                  | ✓    |
| `superpowers:subagent-driven-development`          | ✓    |
| `(transitive) superpowers:test-driven-development` | ✓    |
| `(transitive) superpowers:requesting-code-review`  | ✓    |
| `superpowers:finishing-a-development-branch`       | ✗    |

### Deliberately Skipped Skills

- **`superpowers:finishing-a-development-branch`**
  - **What was skipped**: the post-verification finishing and archive phase.
  - **Why this cycle**: the Task 3 brief says “Do not archive” and assigns
    controller review before an archive request; Task 3.4 therefore remains the
    sole unchecked task.
  - **How to prevent recurrence**: scope-judgment rule — in a pre-archive
    verification dispatch, stop after committed evidence and let the controller
    invoke the finishing workflow in the separately authorized archive cycle.

## 5. Surprises

- The original registry metadata was structurally valid but did not make the
  runtime-output promise visible in every affected public SKILL. The controller
  ruling led to the small, explicit eight-skill contract expansion in `c870c58`.

## 6. Promote candidates → long-term learning

- [ ] 📌 **Recheck runtime contracts alongside registry metadata whenever a
      registry mode describes returned-artifact behavior.** → **Promote to**
      one-off
  > **Why**: The controller’s Issue #14 ruling required a narrow expansion from
  > registry-only metadata to eight public SKILL contracts. **How to apply**:
  > During review of a mode-specific registry promise, search every classified
  > public contract for the corresponding user-visible output obligation before
  > marking the implementation complete.
