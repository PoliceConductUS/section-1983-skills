# Implementation plan: Issue #67 invocation-owned QC reports

> Execute test-first on the isolated Issue #67 worktree. Push every commit, keep
> the stacked pull request draft until fresh full verification succeeds, and
> leave the issue and pull request open for later merge.

## Task 1: OpenSpec and draft PR

- [x] Record the selected trusted-host report-envelope design and durable spec
      deltas.
- [x] Validate the change, commit, push, and open a draft PR against the Issue
      #71 branch.

## Task 2: QC publisher RED/GREEN

- [x] Add RED tests for required primary targets, canonical unique report paths,
      complete metadata, exact target hashes, and default prior-report
      exclusion.
- [x] Add RED filesystem tests for input/prior-report preservation, output
      confinement, collision refusal, write/receipt failure honesty, and
      advisory-only recommendations.
- [x] Implement the narrow trusted-host report builder/publisher on top of
      `build_input_manifest()` and `OutputRun`.
- [x] Run focused tests and commit/push RED and GREEN separately.

## Task 3: Governance and entrypoints

- [x] Make every QC-only folder contract require exactly one target; preserve
      optional targets for mixed drafting behavior while requiring a target at
      the QC publisher.
- [x] Update governance and every QC `SKILL.md` with the exact shared report
      metadata, filtering, receipt, and advisory-remediation contract.
- [x] Extend deterministic governance tests and stable findings without claiming
      to prove subjective report quality.
- [x] Run focused tests, commit, and push.

## Task 4: Verify and archive

- [ ] Run focused QC/persistence/governance suites, strict OpenSpec, formatting,
      `git diff --check`, and fresh `npm run validate`.
- [ ] Review the whole Issue #67 diff for contract drift, unsafe writes,
      incorrect fingerprints, output-success ambiguity, and legal-behavior
      changes; correct accepted findings test-first.
- [ ] Write verification and retrospective artifacts, archive the OpenSpec
      change, validate durable specs, commit, push, rerun fresh verification,
      and mark the PR ready while leaving it and Issue #67 open.
