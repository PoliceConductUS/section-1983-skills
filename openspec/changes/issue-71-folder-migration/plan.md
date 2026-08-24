# Implementation plan: Issue #71 implemented-skill folder migration

> Execute with subagent-driven development, one reviewed RED/GREEN slice at a
> time, immediate push after every commit, and fresh whole-branch verification
> before PR readiness. Preserve the live legal-behavior suite throughout.

## Global constraints

- Every public skill ships exact `references/folder-contract.json` version 1.
- Every output mode is `append-immutable`.
- The trusted host owns absolute-root validation, logical input manifests,
  filesystem/network enforcement, and every `OutputRun` call.
- Standalone helpers work from an isolated skill package, accept only declared
  input roots plus canonical relative targets or in-memory/stdin data, and emit
  deterministic bytes/results.
- No helper imports repository-root validator/writer modules, receives an
  output-root path, dispatches an arbitrary command, or creates a receipt.
- Do not add a universal runner, duplicate persistence manager, CaseGraph
  bridge, graph adapter, or external general-purpose checker.
- Preserve approved legal behavior, source gates, human decisions, immutable
  provenance, and historical archived OpenSpec changes.

## Task 1: Exact install-local contract registry

**Files:**

- Create: `governance/skill-folder-contract.schema.json`
- Create: `skills/*/references/folder-contract.json` for all 22 skills
- Modify: `scripts/validate_governance.py`
- Modify: `evaluations/tests/test_repository_governance.py`
- Create: `evaluations/tests/test_skill_folder_contracts.py`
- Modify: `GOVERNANCE.md`

- [ ] Write RED tests that enumerate exactly the live public skill names and
      compare each contract to the approved role/target/internet/output matrix.
- [ ] Add mutation cases for unknown fields, wrong version/skill, missing,
      duplicate, reordered or unsafe roles, invalid target policy/roles, wrong
      internet value, and non-append output.
- [ ] Copy each package to a temporary isolated directory and prove its contract
      and live local links require no repository-root file.
- [ ] Run focused RED and record only intended failures.
- [ ] Add the strict schema, 22 exact contracts, compact install-local contract
      references, and stable governance findings.
- [ ] Run focused GREEN, full governance, strict Issue #71 OpenSpec, formatting,
      and `git diff --check`.
- [ ] Commit `feat: define exact skill folder contracts` and push.

## Task 2: Explicit-output quality-control governance

**Files:**

- Modify: `GOVERNANCE.md`
- Modify: `scripts/validate_governance.py`
- Modify: `evaluations/tests/test_repository_governance.py`
- Modify: `evaluations/tests/test_non_mutating_quality_control.py`
- Modify: the nine quality-control `skills/*/SKILL.md` files
- Modify: `openspec/specs/repository-skill-governance/spec.md` through this
  change's delta

- [ ] Replace version/project/audits matcher fixtures with one selected declared
      target and a unique append-immutable output-relative report.
- [ ] Mutation-test fallback writes, direct output writes, overwrites, prior-
      report implicit input, input edits, and same-stage remediation.
- [ ] Preserve advisory output, separate remediation, fresh re-verification,
      evidence fingerprints, source identities, scope, result, and observation
      separation.
- [ ] Run RED, implement the narrow prose/validator/spec migration, and rerun
      governance plus all QC tests GREEN.
- [ ] Commit `feat: route quality control through explicit output` and push.

## Task 3: Packaged complaint checker and Filing CI wrapper

**Files:**

- Create: `skills/drafting-section-1983-complaints/scripts/check_complaint.py`
- Create: `skills/filing-ci/scripts/run_filing_ci.py`
- Create/modify: focused complaint and Filing CI tests
- Modify: `skills/drafting-section-1983-complaints/SKILL.md`
- Modify: `skills/filing-ci/SKILL.md`
- Modify: `README.md`
- Modify: checker-related evaluation fixtures

- [ ] RED-test isolated installation and deterministic complaint mechanical
      findings derived only from `complaint-structure-contract.json`.
- [ ] RED-test Filing CI dispatch of explicitly registered packaged checker IDs,
      rejection of commands/executables, stable unavailable classes, required
      filing target, read-only inputs, and deterministic result bytes.
- [ ] Implement only section/order, numbering, identifier, tuple/cardinality,
      cross-reference, incorporation, and field-presence checks; keep every
      legal-judgment exclusion.
- [ ] Make the wrapper return artifact path/bytes/source metadata for host
      publication and never write directly.
- [ ] Migrate unavailable-checker, stale-result, and hard-finding fixtures and
      rerun the complete corpus to prove legal behavior remains stable.
- [ ] Commit `feat: package folder-based filing checks` and push.

## Task 4: Adversarial-review processor

**Files:**

- Modify: `skills/adversarial-filing-review/scripts/launch_review.py`
- Modify: `skills/adversarial-filing-review/SKILL.md`
- Modify: adversarial structure, launcher, runtime, fixture, and non-mutation
  tests
- Modify: `README.md`

- [ ] RED-test removal of project-boundary/version-folder/output-path APIs and
      acceptance only of declared filing/source input data plus required target.
- [ ] Use a network trap for disabled invocations and prove provider dispatch
      occurs only for the contract's authorized policy.
- [ ] Make the launcher emit the existing report bytes and bounded structured
      result; use a host test double to publish through shared `OutputRun`.
- [ ] Preserve strict packet/response validation, empty capabilities, provider
      secrecy, failure classes, fingerprints, categorized findings, and
      plaintiff decisions.
- [ ] Run focused and parent-stack GREEN, then commit
      `feat: adapt adversarial review to folder output` and push.

## Task 5: Judge-overlay receipt processor

**Files:**

- Modify: `skills/section-1983-drafting/scripts/judge_overlay_receipt.py`
- Modify: `skills/section-1983-drafting/SKILL.md`
- Modify: `skills/drafting-for-judge-scholer/SKILL.md`
- Modify: judge guide, structure, and runtime tests

- [ ] RED-test declared filing/corpus/conduct roots, required filing target,
      canonical relative artifacts, and deterministic receipt bytes.
- [ ] Reject project/version/output arguments, absolute paths, traversal,
      symlink escapes, implicit audits input, collisions, and direct writes.
- [ ] Preserve packet schema, fingerprints, anti-gaming checks,
      supported-change, no-change, failure, and advisory-remediation semantics.
- [ ] Publish only through a host test double and prove all declared input bytes
      remain unchanged.
- [ ] Commit `feat: adapt judge receipts to folder output` and push.

## Task 6: Packaged validator adapters

**Files:**

- Modify: litigation and counsel overlay validators and their tests
- Modify: Rule 59 corpus validator and alignment tests
- Modify: drafting linter and its contract tests
- Modify: affected skill instructions and README command examples

- [ ] RED-test one declared input root plus canonical relative targets for every
      helper and isolated package execution without root imports.
- [ ] Add traversal, absolute path, symlink escape, unsupported entry, oversized
      input, network trap, stdout determinism, and input-hash cases.
- [ ] Replace arbitrary positional paths with confined helper interfaces and
      return structured results/artifact bytes without direct publication.
- [ ] Preserve every existing schema, finding identifier, validation rule,
      provenance field, checked date, fingerprint, and non-gating linter limit.
- [ ] Commit `feat: confine packaged validators to input roles` and push.

## Task 7: Remaining skill contracts and current documentation

**Files:**

- Modify: remaining public `skills/*/SKILL.md` files
- Modify: applicable current references and `README.md`
- Modify: relevant structure/fixture tests
- Modify: applicable durable specs through this change's deltas

- [ ] Add exact role meanings, target behavior, internet policy, output artifact
      semantics, gap behavior, and host/publication boundary to each remaining
      independently installed skill.
- [ ] Test composition variants: each skill invocation uses its own exact
      contract; a stack does not silently union roles or enlarge authority.
- [ ] Remove positive external-checker, project/version/audits, repository-path,
      CaseGraph, CaseHome, Git-runtime, graph, and persistence-manager language
      from current public docs/specs while retaining foundation prohibitions and
      repository release/evaluation Git.
- [ ] Run every affected legal-behavior fixture unchanged.
- [ ] Commit `docs: complete implemented skill folder contracts` and push.

## Task 8: Whole-story review, verification, and archive

**Files:**

- Create: `openspec/changes/issue-71-folder-migration/verify.md`
- Create: `openspec/changes/issue-71-folder-migration/retrospective.md`
- Archive into: `openspec/changes/archive/2026-08-24-issue-71-folder-migration/`
- Update all durable specifications changed by this OpenSpec delta

- [ ] Run exact contract tests for all 22 skills, every helper-focused suite,
      all evaluations, governance, strict OpenSpec, tracked formatting,
      terminology searches, and `git diff --check`.
- [ ] Independently review matrix/schema agreement, isolated installation,
      target confinement, helper purity, direct writes/imports, packaged checker
      scope, input hashes, output receipts, internet traps, and legal
      regression.
- [ ] Correct accepted Critical or Important findings through new RED/GREEN
      commits and rerun review.
- [ ] Write exact RED/GREEN/review evidence and retrospective lessons, archive
      with the repository-local CLI, and validate every updated durable spec.
- [ ] Remove ignored review scratch only after controller consumption, run fresh
      `npm run validate`, commit `docs: archive implemented skill migration`,
      push, and complete final independent review before PR readiness.

After final verification, mark the draft PR ready while leaving Issue #71 and
its PR open for later merge.
