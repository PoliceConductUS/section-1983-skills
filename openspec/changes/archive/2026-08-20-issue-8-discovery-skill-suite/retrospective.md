# Retrospective: issue-8-discovery-skill-suite

> Written: 2026-08-20 after verification passed
>
> Parent: `dd6a866`
>
> Worktree: `.worktrees/issue-8-discovery-suite`

## Evidence

- **Implementation head before archive**: `1926884`
- **Diff before archive**: 61 files, +2,585 / -32 lines
- **Tasks done before archive**: 12/13; archive completes 4.2
- **New external dependencies**: none
- **Test signal**: 16 existing drafting tests, 114 evaluation tests, 19 runtime
  skill validators, canonical corpus, formatting, OpenSpec, range whitespace,
  and forbidden-folder checks passed

## Wins

- Five peer skills remain independently installable while sharing one compact
  traceability vocabulary through the existing umbrella router.
- The target map keeps claims, defendants, elements, factual gaps, likely
  custodians, expected native sources, and approved source IDs distinct.
- Written, audit, conference, privilege, and deposition work have explicit
  handoff boundaries instead of one monolithic discovery workflow.
- Five behavior-specific permanent regressions reject unrelated generic
  failures, and fresh contexts exercised every public skill.

## Misses and corrections

- Early capability names differed from the proposed public skill names; design
  review aligned durable capability IDs with package names before RED.
- An initial cross-cutting JSON fixture would have imposed an unapproved public
  schema; review removed it and kept human-facing Markdown outputs.
- The meet-and-confer date contract initially conflicted with the reserved-
  decision boundary; it now uses only a user-supplied or approved date.
- The deposition delta spec in the design commit missed repository formatting; a
  focused formatting commit corrected it before implementation validation.

## Plan deviations

| Area                     | Change                                                                                            | Reason                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Shared ownership         | Five peer specs jointly own the portable minimum while the existing umbrella hosts the reference. | This preserves exactly five new public skills and durable standalone contracts.           |
| Cross-cutting evaluation | No sixth JSON mapping fixture was added.                                                          | The repository has no approved machine-output schema for these human discovery artifacts. |
| Privilege-log scope      | The skill covers requirements before receipt and entry audit after receipt.                       | The issue requested both privilege-log requirements and auditing behavior.                |

## Long-term learning candidates

- Make positive-output contract tests distinguish affirmative requirements from
  negative disclaimers.
- Test one behavior-specific regression per public skill and mutate an unrelated
  rule to prove discrimination.
- Keep shared coordination references non-public when an existing router can own
  composition without creating an extra public capability.
