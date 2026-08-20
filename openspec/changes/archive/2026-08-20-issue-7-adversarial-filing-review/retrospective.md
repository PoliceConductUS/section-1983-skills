# Retrospective: issue-7-adversarial-filing-review

> Written: 2026-08-20 after verification passed
>
> Parent: `52a0a4d`
>
> Worktree: `.worktrees/issue-7-adversarial-filing-review`

## Evidence

- **Implementation head before archive**: `3401ee8`
- **Diff before archive**: 36 files, +2,410 / -1 lines
- **Tasks done before archive**: 12/13; archive completes 4.2
- **New external dependencies**: none
- **Test signal**: 16 existing drafting tests, 100 evaluation tests, 14 runtime
  skill validators, canonical corpus, formatting, OpenSpec, range whitespace,
  and forbidden-folder checks passed

## Wins

- The public skill keeps independence, categorization, corrections, and
  plaintiff-reserved strategy in one bounded read-only contract.
- The launcher remains standard-library-only and makes packet validation,
  capability isolation, process isolation, and failure classes observable.
- Three behavior-specific permanent regressions reject unrelated generic
  failures.
- A fresh clean-room reviewer produced all five categories, a supported complete
  correction, and reserved choices without changing the canonical draft.

## Misses and corrections

- The first public wording treated path and URL provenance as packet content;
  review corrected it to an absolute packet prohibition.
- The first child environment used a narrow denylist that leaked drafting and
  control state; a RED test forced an explicit minimal allowlist.
- The first packet validator accepted whitespace-only metadata and unpaired
  surrogates in non-content fields; focused RED cases now reject both before
  execution while preserving exact untrimmed content hashes.

## Plan deviations

| Area                     | Change                                                 | Reason                                                                        |
| ------------------------ | ------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Parent verification base | Updated from `8020676` to `52a0a4d`                    | The user updated `main`, and Git Town propagated it through the parent stack. |
| Environment isolation    | Replaced context-key denylist with a minimal allowlist | Arbitrary inherited variables could contain forbidden review state.           |
| Packet strings           | Added meaningful-text and UTF-8 validation             | Serialization errors and blank identifiers escaped initial preflight.         |

## Long-term learning candidates

- Test clean-room subprocess environments with unrelated sentinels, not only
  names that match known conversation or session patterns.
- Validate every untrusted protocol string before serialization and preserve
  immutable content exactly rather than trimming it for convenience.
- Treat provenance resolution and reviewer-packet construction as separate
  boundaries; provenance paths and URLs never belong in the clean-room packet.
