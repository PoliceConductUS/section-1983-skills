# Verification

## Branch and live scope

- Branch: `codex/issue-71-folder-migration`.
- Stacked base: `codex/issue-69-folder-docs` at
  `a41001e538eb41530ca18a0808425bd47393d81d`.
- Pre-archive reviewed HEAD: `58ec69402f74eab89c4de8ee7d43646152059e1a`.
- Live Issue #71 was open and retained the folder-native corrective-migration
  acceptance criteria.
- Live PR #75 was open and draft at that exact HEAD with the expected stacked
  base. Its new validation run was in progress when archival work began.
- Local HEAD and `origin/codex/issue-71-folder-migration` matched exactly.

## RED and GREEN history

- `398f4f4` planned the corrective migration through OpenSpec.
- `b0d0db3`, `a31701c`, and `e3f10fd` established and hardened the RED exact
  22-skill contract matrix before `e2975c9` supplied the GREEN contracts and
  governance validation.
- `b890070` and `367539b` rejected direct and legacy quality-control output;
  `46f370c` routed non-mutating QC reports through explicit host publication.
- `618ce0f`, `486a7b2`, `7c666a3`, and `6a41e36` established packaged-checker
  RED coverage before `d9e3476` supplied the complaint checker and Filing CI
  wrapper.
- `702c0ea`, `b6e27d4`, `a7823f0`, and `a960250` established adversarial-review
  input, command-removal, target, and failure-provenance RED coverage before
  `475da9f` supplied the input-confined processor.
- `72768ac` and `7f28277` established judge-receipt RED coverage before
  `f3ffe9b` supplied deterministic receipt bytes and host-only publication.
- `ec1d07b` established confined helper RED coverage before `ae04800` adapted
  overlay, corpus, and linter validators.
- `87b8a58` established complete folder-native public guidance RED coverage.
- `daf96fa` made the root validation helpers an explicit Python package after
  GitHub Actions exposed Linux import shadowing.
- Independent review found that prose-only checks did not prove each installed
  contract controlled an invocation. `afa174e` added the executable RED matrix;
  `2aac1ac` loads the bounded install-local contract and rejects skill, ordered
  role, internet, and target mismatches before resolving input roots.
- `58ec694` completed all public guidance, durable deltas, current terminology,
  QC host-publication wording, and regression tests.

## Independent review

The first whole-Task-7 review found two Important blockers:

1. generic RRD, Rule 12 RRD, and Rule 59 study instructions still contained
   direct-persistence language; and
2. the contract tests proved JSON presence but did not execute each installed
   contract against missing, extra, reordered, wrong-target, or internet-
   mismatched invocations.

Both findings were accepted and corrected test-first. The fresh re-review
approved the corrected Task 7 diff with no Critical or Important finding. Its
independent focused run passed 82 tests, strict OpenSpec validation, and
`git diff --check`.

## Pre-archive verification

- `npm run validate` passed formatting, 27 drafting tests, 484 evaluation tests,
  discovery of all 22 public skills, 23 OpenSpec items, corpus evaluation, and
  governance validation.
- `npx openspec validate --all --strict` passed 23 items and failed 0.
- The exact installed-contract matrix copied and exercised all 22 skill
  packages, including missing, extra, and reordered roles; internet-policy
  mismatch; missing required target; and wrong target role.
- Focused folder, governance, QC, contract, and guidance suites passed 72 tests
  after the final governance-language correction.
- Current-public terminology searches found no remaining positive CaseGraph,
  CaseHome, Git-runtime, worktree, graph, persistence-manager, external-checker,
  version-folder, `audits/`, or direct-report-write requirement. Repository
  release links, negative capability prohibitions, and contributor validation
  commands remain intentionally present.
- `git diff --check` passed and the tracked worktree was clean before this
  evidence update.

## Archive and final readiness

The repository-local OpenSpec CLI archived the complete change into
`openspec/changes/archive/2026-08-24-issue-71-folder-migration/` and applied 10
added, 20 modified, and 6 renamed requirement operations across 11 durable
specifications. OpenSpec reported no deletion and created the durable
`implemented-skill-folder-migration` specification.

- `npx openspec validate --all --strict` passed all 23 durable specifications.
- The OpenSpec merge output was formatted, and `npm run validate` then passed
  formatting, 27 drafting tests, 484 evaluation tests, discovery of all 22
  public skills, all 23 durable specifications, corpus evaluation, and
  governance validation.
- The final independent archive review repeated full validation, strict OpenSpec
  validation, archive-fidelity comparison, and `git diff --check`. It found one
  Important current-public wording defect: README still advertised an
  `external-checker handoff` even though the implementation is packaged and
  install-local.
- A new `external[-\s]+checker\s+handoff` regression failed on the hyphenated
  wording before README changed and passed after README described the packaged
  install-local mechanical check.
- The final independent re-review approved that correction and found no
  remaining Critical or Important code or specification issue.
- A fresh controller `npm run validate` after that correction again passed 27
  drafting tests, 484 evaluations, 22 skills, 23 specs, corpus evaluation, and
  governance validation. `git diff --check` remained clean.

PR readiness follows only after this archive commit is pushed and the exact
remote head and GitHub validation are freshly verified. PR #75 and Issue #71
remain open under the requested close-on-merge policy.
