# Retrospective: issue-1-filing-ci-review-fixes

> Written: 2026-08-20 (after verification passed)  
> Commit range: `5ffa109..0e1281e`  
> Worktree: `.worktrees/issue-1-filing-ci`

## 0. Evidence

- **Commit range**: `5ffa109..0e1281e` (2 commits)
- **Diff size**: +268 / -2 lines across 8 files
- **Tasks done**: 7/7
- **Active hours**: less than 0.1 hours from correction commit to verification
  commit
- **Subagent dispatches**: 5 fresh review or behavioral dispatches
- **New external dependencies**: none
- **Bugs encountered post-merge**: none; the stacked branch remains unmerged
- **OpenSpec validate state at archive**: pass before archive; 2 items passed
  and 0 failed
- **Test coverage signal**: 4 additional independent fresh-context scenarios
  passed; 16 unit tests, 13 runtime skill validations, package discovery,
  formatting, and OpenSpec validation passed

Commit chain:

```text
28ad922 fix: close filing CI review gaps
0e1281e docs: verify filing CI review corrections
```

## 1. Wins

- A fresh final reviewer compared the archived plan, reports, durable spec, and
  implementation rather than relying on the first verification report.
- The four missing scenarios passed without expanding or changing the public
  skill, confirming that the defect was evidence coverage rather than behavior.
- The corrective delta now preserves the two exact loopholes found during the
  original hard-finding GREEN runs.
- The correction remains entirely inside OpenSpec and `/private/tmp`; it creates
  no forbidden coordination folder or runtime dependency.

## 2. Misses

- 🔴 **Blocking**: The first archive marked all-scenario comparison complete
  even though four specified scenarios lacked recorded GREEN runs.
- 🔴 **Blocking**: The first durable requirement omitted the two behaviorally
  necessary edit-loop safeguards while verification reported no drift.
- 📌 **Nit**: OpenSpec generated a placeholder capability purpose that was not
  replaced before the first archive commit.

## 3. Plan Deviations

| Plan task               | What changed                                                                      | Why                                                                 |
| ----------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Public skill correction | No skill edit was needed.                                                         | All four missing scenarios passed the current skill.                |
| Durable purpose         | Updated the existing durable spec directly before applying the requirement delta. | OpenSpec requirement deltas do not replace capability purpose text. |

## 4. Skill / Workflow Compliance

| Skill                                                     | Used |
| --------------------------------------------------------- | ---- |
| `superpowers:brainstorming`                               | ✓    |
| `superpowers:writing-plans`                               | ✓    |
| `superpowers:using-git-worktrees`                         | ✓    |
| `superpowers:subagent-driven-development`                 | ✓    |
| `(transitive) superpowers:test-driven-development`        | ✓    |
| `(transitive) superpowers:requesting-code-review`         | ✓    |
| `superpowers:receiving-code-review`                       | ✓    |
| `superpowers:finishing-a-development-branch`              | ✓    |
| `(transitive) superpowers:verification-before-completion` | ✓    |

### Deliberately Skipped Skills

None.

## 5. Surprises

- A green skill and green structural validation did not establish that every
  requirement scenario had evidence.
- The archived delta accurately reflected the initial spec but not the later
  behavior-driven corrections to the skill.
- A final review after archive was necessary to expose both gaps.

## 6. Promote Candidates → Long-Term Learning

- [ ] 🔴 **Require an explicit requirement-scenario-to-evidence matrix before a
      behavioral task can be marked complete.** → **Promote to the
      superpowers-bridge verification schema**

  > **Why**: The original task and verification were green while four named
  > specification scenarios had no recorded run. **How to apply**: For
  > public-seam behavior changes, verify must list every requirement scenario
  > and its exact deterministic or fresh-context evidence before archive.

- [ ] 🔴 **Reconcile behavior-driven implementation corrections back into the
      delta spec before verification.** → **Promote to the superpowers-bridge
      apply workflow**
  > **Why**: Two GREEN fix commits changed the necessary behavioral contract
  > without updating the original delta requirement. **How to apply**: After
  > each RED-GREEN correction changes a contract boundary, compare the skill and
  > delta spec before marking the associated task complete.
