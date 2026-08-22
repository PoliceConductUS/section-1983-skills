# Retrospective: issue-6-drafting-evaluations

> Written: 2026-08-20 after verification passed
>
> Commit range: `7b8b021..56b8a2b`
>
> Worktree: `.worktrees/issue-6-drafting-evaluations`

## 0. Evidence

- **Commit range**: `7b8b021..56b8a2b` (8 commits)
- **Diff size**: +5,058 / -2 lines across 44 files
- **Tasks done before archive**: 13/14; the archive operation completes 5.2
- **Active hours**: about 1.8 hours from design commit through final corrective
  commit
- **Subagent dispatches**: more than 20 RED, GREEN, fixture, and review turns
- **New external dependencies**: none
- **Bugs encountered post-merge**: none; the stacked branch remains unmerged
- **OpenSpec validate state before archive**: 2 passed, 0 failed
- **Test coverage signal**: 16 existing unit tests, 79 evaluation tests, 13
  runtime skill validators, canonical corpus, formatting, OpenSpec, range
  whitespace, and forbidden-folder checks passed

Commit chain:

```text
598da3b docs: design drafting skill evaluations
e6f69a9 test: define drafting evaluation contracts
e4a3383 feat: add drafting evaluation harness
ba84d1b test: add synthetic drafting regressions
db62d30 test: define drafting evaluation PR gate
181df85 ci: gate drafting skill evaluations
be0af7d test: cover drafting protocol byte boundaries
56b8a2b fix: contain drafting protocol decode failures
```

## 1. Wins

- The harness remained standard-library-only while covering fixture loading,
  deterministic grading, configured process isolation, repeated judgment,
  baseline comparison, safe reports, and CI publication.
- The three synthetic regressions became behavior-specific after adversarial
  review, so generic banned text cannot satisfy their permanent expectations.
- RED tests were committed before each implementation checkpoint, and every
  commit was synced to origin.
- The existing validation workflow was extended without adding a provider SDK,
  secret, extra coordination directory, or code comment.

## 2. Misses

- 🟡 **Painful**: The first fixture expectations were too generic; unrelated
  outputs could satisfy unavailable-checker and stale-result regressions.
- 🟡 **Painful**: The first RED integration test constrained workflow triggers
  and formatting beyond the approved contract before review corrected it.
- 🟡 **Painful**: The first whole-change review found two untested subprocess
  protocol escapes after the main harness was otherwise green.
- 📌 **Nit**: The CI gate initially ran the corpus first and published missing
  reports unconditionally; task review restored validation order and guarded
  publication.

## 3. Plan Deviations

| Plan area           | What changed                                | Why                                                         |
| ------------------- | ------------------------------------------- | ----------------------------------------------------------- |
| Corpus expectations | Added behavior-specific banned patterns     | Generic expectations did not prove the named failure mode   |
| PR workflow         | Extended the existing combined workflow     | This was narrower than creating or restructuring workflows  |
| Protocol coverage   | Added a final RED-GREEN byte-boundary cycle | Untrusted JSON and byte streams exposed uncaught exceptions |
| Artifact sequencing | Task 5.2 remains open until archive         | The task explicitly includes the archive operation          |

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

- Stable JSON parsing was not enough at a subprocess boundary; decoding itself
  had to be classified and bounded.
- A permanent regression can look specific by filename while remaining
  nondiscriminating unless an adversarial candidate is tried against it.
- Workflow assertions need behavioral YAML seams without dictating whether an
  existing workflow also serves push validation.

## 6. Promote Candidates → Long-Term Learning

- [ ] 🟡 **Adversarially test every permanent regression expectation against an
      unrelated candidate.** → **Promote to** superpowers-bridge verification

  > **Why**: Two initial fixtures passed while generic banned text satisfied
  > their expected-finding subsets. **How to apply**: When adding a permanent
  > regression, run at least one unrelated candidate that shares generic surface
  > violations and require it not to match the named regression.

- [ ] 🟡 **Treat decoding as part of every external command protocol.** →
      **Promote to** evaluation-harness design guidance

  > **Why**: Invalid UTF-8 escaped before malformed-response handling and report
  > generation. **How to apply**: Capture command streams as bytes, strictly
  > decode protocol payloads inside classification, and replacement-decode
  > bounded diagnostics.

- [ ] 📌 **Test CI workflow behavior without constraining unrelated triggers or
      harmless YAML layout.** → **Promote to** test-review checklist

  > **Why**: The first repository-integration test required a PR-only workflow
  > even though the specification allowed combined pull-request and push use.
  > **How to apply**: Assert one coherent workflow provides required behavior,
  > then permit additional workflows, triggers, step names, quoting, and layout.
