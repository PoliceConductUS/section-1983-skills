# Retrospective: issue-9-declaration-evidence

> Written: 2026-08-20 after verification passed
>
> Parent: `4f56696`
>
> Worktree: `.worktrees/issue-9-declaration-evidence`

## Evidence

- **Implementation head before archive**: `1b06baf`
- **Diff before archive**: 51 files, +2,535 / -43 lines
- **Tasks done before archive**: 11/12; archive completes 4.2
- **New external dependencies**: none
- **Test signal**: 16 existing drafting tests, 128 evaluation tests, 20 runtime
  skill validators, canonical corpus, formatting, OpenSpec, range whitespace,
  and forbidden-folder checks passed

## Wins

- One self-contained public skill keeps statement classification, factual
  declaration drafting, exhibit-foundation prompts, and human declarant approval
  in one observable contract.
- Both statutory execution forms are complete and selected only from the actual
  execution location.
- Five fixture families and seven isolated permanent regressions cover knowledge
  laundering, retained analysis, unsupported foundation, form selection, stale
  approval, and premature readiness.
- Fresh contexts reproduced both statutory forms exactly and kept all approval,
  execution, authentication, and admissibility boundaries intact.

## Misses and corrections

- The initial design paraphrased Rule 56(c)(4) with the separate Rule 56(c)(2)
  formulation; review replaced it with the correct personal-knowledge,
  admissible-facts, and competency standard.
- The first outside-United-States requirement named only the distinguishing
  phrase; review required the complete statutory form.
- The first execution regression required three defects at once; review split it
  into independently firing readiness, form-selection, and stale-approval cases.
- Early passing and regression candidates were grader-clean but omitted
  unrelated contract fields; review made every baseline complete and every
  regression differ only at its target behavior.
- The first approval-status table treated `revised` as a durable state; a
  focused RED test now preserves revision as an action that resets status to
  `pending`.

## Plan deviations

| Area             | Change                                                              | Reason                                                                                       |
| ---------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Regression count | Five fixture families contain seven isolated permanent regressions. | Three execution failures need independent signals rather than one compound pattern.          |
| Approval actor   | Approval is expressly the human declarant's approval.               | A lawyer, user, or other reviewer cannot approve execution testimony for the signer.         |
| Derived analysis | It remains in `Excluded or Separate Material` for v1.               | The narrow factual-declaration contract does not add an analyst or expert foundation system. |
| Git Town         | Used as an available workflow convenience, not a public contract.   | Branch stacking remains operational and tool-agnostic to installed skills.                   |

## Long-term learning candidates

- Derive every permanent regression from a complete passing baseline and alter
  only the target behavior.
- Test complete statutory alternatives as whole strings and verify that each
  fresh output contains one selected form and not the other.
- Treat approval actions and approval states as different public concepts.
