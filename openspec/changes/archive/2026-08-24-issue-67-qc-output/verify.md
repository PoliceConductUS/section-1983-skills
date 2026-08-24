# Verification

## Branch and scope

- Branch: `codex/issue-67-qc-output`.
- Stacked base: `codex/issue-71-folder-migration` at
  `f6f02437fb3b66737620c24e72a6fcc0b08464a2`.
- Pre-archive reviewed HEAD: `0aa3539ddd308f35babf239b3148a62867ba035f`.
- Pre-archive range: 6 commits; 36 files; +1,940 / -225.
- Issue #67 and draft PR #76 remain open. The PR stays draft through archive and
  final verification.
- No CaseGraph or other external persistence dependency was added.

## Behavior verified

- Every independent quality-control publication is bound to the installed
  skill's target policy and approved target roles.
- The host derives one append-immutable path containing the check kind, UTC run
  time, and canonical lowercase UUIDv4 run ID.
- A complete canonical metadata envelope records the selected target, filtered
  logical manifest, skill identity, findings, recommendations, approved sources,
  result, scope, and terminal run-manifest identity.
- Prior generated reports are excluded unless one exact report is targeted. A
  direct report-folder input is classified by a complete schema-valid canonical
  envelope; a malformed fence-only file remains reviewed.
- Quality-control processors return report bytes or content and structured
  findings without selecting paths or writing output. The judge-overlay
  integration publishes through the shared quality-control publisher.
- Inputs and prior reports remain unchanged. Completion requires durable report
  bytes and a terminal success manifest with no incomplete state.

## TDD and review trace

- `01fa0fd` established the missing publisher and immutable-report RED.
- `541cb2e` supplied the trusted-host publisher and receipt binding.
- `8e6b343` standardized installed skill contracts and governance.
- Independent review found unbound target authority, direct-root report
  classification, weak run IDs, and residual processor path ownership.
- `321c0a8` bound publication to installed contracts, required UUIDv4
  identities, and removed several processor-selected paths.
- Re-review found one remaining judge-overlay path and an unsafe marker-only
  report classifier.
- `0aa3539` removed the remaining output path and required a complete canonical
  envelope before direct-root exclusion. Exact-SHA re-review approved with no
  Critical or Important finding.

## Fresh pre-archive evidence

- Focused contract and review suites passed 106 tests after the first correction
  and 69 tests after the final correction.
- Independent final review passed 86 focused tests.
- `python3 -m py_compile` passed for every modified Python runtime and
  processor.
- `npx openspec validate issue-67-qc-output --strict` passed.
- `npm run validate` passed formatting, 27 drafting tests, 495 evaluation tests,
  discovery of 22 skills, all 24 OpenSpec items, corpus evaluation, and
  governance validation.
- `git diff --check` passed and the tracked worktree was clean at reviewed HEAD.
- GitHub Actions `Validate` passed at exact pushed SHA `0aa3539`.

## Decision

PASS for archive. Final readiness requires the archived durable specifications,
fresh repository validation, a pushed archive commit, and exact remote/check
verification. PR #76 and Issue #67 remain open.

## Archive verification

The first archive probe aborted without changing files because Issue #71 had
renamed the durable implemented-skill contract requirement. The active delta was
updated to that current header, strict change validation passed, and the retry
archived the change as `2026-08-24-issue-67-qc-output`. It added five durable
requirements and modified the exact installed-skill contract matrix without a
deletion.

- `npx openspec validate --all --strict` passed all 23 durable specifications.
- Post-archive `npm run validate` passed formatting, 27 drafting tests, 495
  evaluation tests, discovery of 22 skills, all 23 durable OpenSpec items,
  corpus evaluation, and governance validation.
- `git diff --check` passed after archive.

The archive commit, exact remote parity, GitHub validation, and draft-to-ready
transition remain controller-owned final steps. PR #76 and Issue #67 remain
open.
