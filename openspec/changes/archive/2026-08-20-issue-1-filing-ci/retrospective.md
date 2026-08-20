# Retrospective: issue-1-filing-ci

> Written: 2026-08-20 (after verification passed)  
> Commit range: `5f271d2..7a04be4`  
> Worktree: `.worktrees/issue-1-filing-ci`

---

## 0. Evidence

- **Commit range**: `5f271d2..7a04be4` (6 commits)
- **Diff size**: +643 / -1 lines across 9 files
- **Tasks done**: 6/6
- **Active hours**: approximately 0.4 hours from the first proposal commit to
  the verification commit
- **Subagent dispatches**: 8 measured fresh-context behavioral scenario runs,
  plus implementation and review assignments
- **New external dependencies**: none
- **Bugs encountered post-merge**: none; the branch is intentionally unmerged
- **OpenSpec validate state at archive**: pass before archive; 1 item passed and
  0 failed
- **Test coverage signal**: 16 deterministic unit tests passed; 8 fresh-context
  behavioral runs exercised 3 RED baselines, 3 initial GREEN cases, and 2
  focused hard-finding reruns; all 13 skills passed runtime validation and
  package discovery

Commit chain:

```text
eb7f070 docs: propose filing CI skill
cfaef37 feat: add filing CI orchestration skill
e026870 fix: guard filing CI against draft edits
9535ae3 fix: separate filing CI findings from drafting
320f4c7 docs: record filing CI verification work
7a04be4 docs: verify filing CI change
```

---

## 1. Wins

- The three RED baselines under `/private/tmp/filing-ci-issue-1` exposed
  distinct failure modes before implementation: substituting prose for an
  unavailable checker, editing through a hard finding, and relying on a stale
  result.
- The public-seam tests forced two narrow corrections in `e026870` and `9535ae3`
  instead of allowing an apparently reasonable but unsafe first draft of
  `skills/filing-ci/SKILL.md` to stand.
- The final skill remains a thin orchestrator: it resolves and runs project
  configuration but does not absorb checker logic, authority verification,
  formatting, filing, or litigation strategy.
- `npm run validate` passed formatting, all 16 unit tests, discovery of 13
  skills, and OpenSpec validation. Runtime validation also passed for every
  skill.
- The worktree contains neither a `docs/` directory nor a `.superpowers/`
  directory, and the repository artifacts contain no machine-specific project
  path.

## 2. Misses

- 🟡 **Painful**: The first GREEN hard-finding run treated “read-only” as
  permitting an immediate drafting handoff in the same response. Commit
  `e026870` had to prohibit edits while Filing CI is active.
- 🟡 **Painful**: The next hard-finding run inferred replacement language from a
  checker finding. Commit `9535ae3` had to separate the later drafting workflow
  and define checker-supplied correction text narrowly.
- 📌 **Nit**: The initial plan anticipated one GREEN run per scenario, but the
  hard-finding seam required two additional fresh-context reruns before it was
  stable.

## 3. Plan Deviations

| Plan task | What changed                                                                                                            | Why                                                                                                      |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Task 3.1  | The hard-finding scenario ran three GREEN iterations rather than one.                                                   | The first two iterations exposed distinct edit loopholes that were not visible in structural validation. |
| Task 3.2  | Comparison included the agent's inferred drafting handoff and replacement language, not only command and gate behavior. | Those observable actions violated the no-silent-edit requirement even though the gate remained open.     |

No capability was added outside the approved thin-skill scope.

## 4. Skill / Workflow Compliance

| Skill                                                     | Used |
| --------------------------------------------------------- | ---- |
| `superpowers:brainstorming`                               | ✓    |
| `superpowers:writing-plans`                               | ✓    |
| `superpowers:using-git-worktrees`                         | ✓    |
| `superpowers:subagent-driven-development`                 | ✓    |
| `(transitive) superpowers:test-driven-development`        | ✓    |
| `(transitive) superpowers:requesting-code-review`         | ✓    |
| `superpowers:finishing-a-development-branch`              | ✓    |
| `(transitive) superpowers:verification-before-completion` | ✓    |

### Deliberately Skipped Skills

None.

## 5. Surprises

- A plain “do not edit” rule was not enough to prevent a capable agent from
  reframing the same-response edit as a drafting handoff.
- Even after edits were barred, a checker finding could be misread as supplying
  approved replacement text. The contract had to distinguish exact
  checker-provided text from inferred language.
- Fresh-context behavioral runs found these defects while format, discovery,
  runtime, and OpenSpec validation were already green.

## 6. Promote Candidates → Long-Term Learning

- [ ] 🟡 **Turn every observed behavioral failure into a permanent synthetic
      regression fixture.** → **Promote to the Issue #6 evaluation suite**

  > **Why**: Three RED failures and two later hard-finding loopholes were
  > observable only at the installed-skill seam, not through structural
  > validation. **How to apply**: When Issue #6 adds drafting-skill evaluations,
  > encode these five synthetic cases with deterministic outcome checks and
  > repeated fresh-context judgment runs.

- [ ] 📌 **Make the bridge's forbidden-output check cover both legacy
      `docs/superpowers` output and standalone `.superpowers` coordination
      state.** → **Promote to the superpowers-bridge schema**
  > **Why**: This repository's approved layout permits bridge artifacts only
  > inside OpenSpec, while the current verification template explicitly detects
  > only the legacy docs path. **How to apply**: When the shared bridge schema
  > is next revised, add a non-blocking detector for `.superpowers/` and
  > document repository-specific exceptions.
