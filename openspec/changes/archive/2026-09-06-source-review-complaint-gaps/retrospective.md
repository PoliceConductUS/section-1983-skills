# Retrospective: source-review-complaint-gaps

> Written: 2026-09-05 (after verify passed) Commit range: `0911efa..4248a37`
> Worktree: main checkout, branch `codex/source-review-complaint-gaps`

---

## 0. Evidence

- **Commit range**: `0911efa..4248a37` (1 implementation commit before archive)
- **Diff size**: +1214 / -41 lines across 23 files
- **Tasks done**: 13/13
- **Active hours**: about 2
- **Subagent dispatches**: 0
- **New external dependencies**: none
- **Bugs encountered post-merge**: none (not merged)
- **OpenSpec validate state at archive**: pass (40 items, strict pass)
- **Test coverage signal**: 705 evaluation tests, 27 unit tests, 19 new tests

Commit chain:

```
0911efa Add Monell planning, drafting, and complaint contract v2 (#112)
4248a37 Add criminal posture, pre-force, Rule 5.2, and capacity complaint rules
```

---

## 1. Wins

- The source review separated the one gap with a declarable structure (Rule 5.2)
  from three that need legal judgment, so only one mechanical gate was added and
  it excludes `redaction-authorization` (see §0 test count).
- Both installed checkers received identical native validation and the tests run
  the same documents through each, so the copies cannot drift silently.
- Every filing, stay, alternative, omission, and unredacted-identifier choice is
  routed to the user, consistent with GOVERNANCE.md.

## 2. Misses

- 🟡 [painful | evidence: verify.md §5] One completion-audit sentence collided
  with an existing candor regex because the checklist is one giant clause. The
  fix was wording, not logic, but the collision cost a validate cycle.
- 📌 [nit | evidence: design.md] _McDonough v. Smith_ is cited without a
  pinpoint because the U.S. Reports page for the holding was not verified from a
  primary source in session. `audit-authorities` covers this before filing.

## 3. Plan deviations

| Plan task | What changed                                 | Why                             |
| --------- | -------------------------------------------- | ------------------------------- |
| 3.3       | Reworded the duplicative-capacity audit item | Existing candor regex collision |

## 4. Skill / workflow compliance

| Skill                                            | Used |
| ------------------------------------------------ | ---- |
| superpowers:brainstorming                        | ✗    |
| superpowers:writing-plans                        | ✗    |
| superpowers:using-git-worktrees                  | ✗    |
| superpowers:subagent-driven-development          | ✗    |
| (transitive) superpowers:test-driven-development | ✓    |
| (transitive) superpowers:requesting-code-review  | ✗    |
| superpowers:finishing-a-development-branch       | ✗    |

### Deliberately Skipped Skills

- **`superpowers:brainstorming`, `superpowers:writing-plans`**
  - **What was skipped**: the interactive skill invocations; brainstorm.md and
    plan.md were written manually from the completed source review.
  - **Why this cycle**: the user had already reviewed the four findings and said
    "proceed with those changes", and the session ran autonomously without a
    user available for one-question-at-a-time brainstorming.
  - **How to prevent recurrence**: scope-judgment rule — when the user approves
    an itemized finding list, write brainstorm.md from that list and note the
    approval; invoke the interactive skill only when design choices remain open.
- **`superpowers:using-git-worktrees`,
  `superpowers:subagent-driven-development`,
  `superpowers:requesting-code-review`,
  `superpowers:finishing-a-development-branch`**
  - **What was skipped**: worktree isolation, per-task subagents, subagent code
    review, and the branch-finishing skill.
  - **Why this cycle**: the session's operating instructions forbade subagents
    unless the user, CLAUDE.md, or a skill requested them, and the user had just
    asked to remove the repository's stale worktrees; the working tree was
    clean, so an in-place branch was used. Push and PR are reserved to the user.
  - **How to prevent recurrence**: CLAUDE.md trigger — AGENTS.md could state
    whether the OpenSpec apply phase's subagent and worktree steps are required
    in autonomous sessions, so the next cycle does not have to reconcile the
    schema with the session rule.

## 5. Surprises

- The candor test treats the whole completion-audit checklist as one clause, so
  any new item can trigger a cross-item regex match.
- Six of the twenty sources were blocked to plain fetches (402/403) and needed
  browser user agents, PDF extraction, or a mirror; one (Institute for Justice)
  was never readable.

## 6. Promote candidates → long-term learning

- [ ] 🟡 **Split the completion-audit checklist assertions by item** → **Promote
      to skill** (`evaluations/tests/test_complaint_candor_contract.py`)
  > **Why**: one-clause checklists make every new audit item a regex hazard.
  > **How to apply**: when adding audit items, run the candor suite before
  > `npm run validate` and prefer wording that avoids "job", "function", and
  > "filed text" in the same item.
- [ ] 📌 **Cite the U.S. Reports pinpoint only when read from a primary source**
      → **One-off**
  > **Why**: the contract's own rule requires verified pinpoints. **How to
  > apply**: when a pinpoint is uncertain, cite the case without one and leave
  > verification to `audit-authorities`.
