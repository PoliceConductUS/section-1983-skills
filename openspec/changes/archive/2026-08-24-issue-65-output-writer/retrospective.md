# Retrospective

## Outcome

Issue #65 adds one explicit, invocation-bound persistence boundary for skill
artifacts. It publishes complete bytes without replacement, records honest
incomplete and terminal run state, and produces reproducible receipts without
CaseGraph or another external runtime.

## Evidence

- Pre-archive range: `28d0754..7b19d80` (16 commits; 14 files; +3,364 / -0).
- Tasks before archive: 11 of 11 checked.
- External dependencies: none.
- Focused result: 57 output-writer tests and 17 folder-boundary tests passed.
- Full result: 26 drafting tests and 433 evaluation tests passed; 22 skills were
  discovered; all 22 OpenSpec items, the evaluation corpus, and governance
  validation passed.
- Implementation work used four task-sized RED/GREEN dispatches, one initial
  Task 1 review correction, one Task 2 review correction, three Task 3 review
  refinements, and three Task 4 test-first correction rounds.

Commit chain:

```text
7e32fd1 docs: plan explicit output persistence
dbf2861 test: define atomic skill output boundary
ea95e2d test: strengthen atomic output boundary red
af95001 feat: add atomic skill output writer
3978ef8 fix: preserve atomic output failure state
adf7c6f test: define reproducible output receipts
3d51ee0 test: strengthen reproducible receipt red
592a202 test: close receipt false-success gaps
c724dbc test: require durable incomplete recovery
feaa6b0 feat: record reproducible skill output runs
451275d test: close output receipt review gaps
3e21385 fix: seal output run terminal receipts
7eeeaf8 test: expose terminal publication cleanup gaps
f20e160 fix: harden terminal publication cleanup
678f022 test: seal removed linked terminal receipts
7b19d80 fix: seal linked terminal receipt races
```

## What worked

- Directory-relative operations kept output authority attached to opened root
  and run directory identities even after visible path replacement.
- Same-filesystem staging plus create-exclusive hard-link publication gave the
  tests an observable whole-file, no-replacement boundary.
- Separate `incomplete.json`, `manifest.json`, and `failure.json` names made
  crash-window semantics testable. Success requires both a valid manifest and
  the durable absence of the incomplete marker.
- Canonical compact JSON fixtures exposed ordering and machine-path drift while
  keeping input fingerprints reproducible across relocated roots.
- Failure injection at file sync, directory sync, link, unlink, cleanup, and
  receipt publication boundaries found real state-machine defects before
  archive.
- Repeated independent reviews found subtle races that ordinary success-path
  tests missed, especially receipt names that became visible and were then
  removed before an injected sync failure.

## Misses and surprises

- Pushing every RED commit made draft-PR CI intentionally fail during the
  missing-interface and missing-receipt phases. Commit context is required to
  distinguish those expected failures from regressions.
- Initial cleanup treated staging unlink as cosmetic. Directory durability
  requires syncing the staging directory after every unlink, including
  pre-publication error cleanup.
- Checking whether a terminal name still existed was insufficient. A successful
  exclusive link must seal the run even if another actor removes that name
  before later failure handling observes it.
- Internet-use derivation initially considered only durable artifacts. Honest
  failure receipts must also derive it from incomplete artifacts that retain
  validated source provenance.
- Repository Prettier scans ignored Superpowers coordination files, so final
  aggregate validation requires temporarily isolating or finally removing the
  task-owned scratch workspace.

## Plan deviations

- Task 1 added one review-strengthening RED commit for stable-root swaps, run-ID
  confinement, full input preservation, invalid modes, and no-follow failure
  observation.
- Task 2 added one test-first review correction for namespace casing, post-link
  honesty, bounded recursion and modes, and symlink alias classification.
- Task 3 required three review refinements to specify exact receipts, the
  two-file success rule, and durable incomplete-state recovery before GREEN.
- Task 4 required three test-first correction rounds covering ten Important
  findings and one Minor documentation defect.
- The Task 5 worker leaves PR #73 draft despite the plan's final transition
  wording because the controller reserved readiness until after independent
  whole-branch review. No product behavior changes.
- The controller's post-archive whole-branch review found four additional
  Important state, detachment, and timestamp-grammar defects. RED commit
  `06c2292` proved them before a narrow correction updated runtime behavior and
  both archived and durable contracts without unarchiving the change.

## Boundaries preserved

- The shared writer consumes the folder-scoped validated invocation; it does not
  own sandbox creation, legal analysis, or skill-specific output meaning.
- Inputs and prior outputs remain immutable. Neither run mode permits replace,
  delete, chmod, or ambient path authority.
- Internet provenance records use only expressly authorized, validated source
  metadata. They do not grant network access.
- The implementation uses only Python's standard library and checked-in schemas,
  tests, and public protocol documentation.

## Reusable lessons

- Durable success is a state predicate over all authoritative marker names, not
  merely the presence of a success receipt.
- A terminal state machine must remember completed publication operations, not
  infer their history only from names that can later disappear.
- Every staging unlink is a filesystem state transition whose parent directory
  needs durability treatment.
- Failure receipts must account for provenance attached to uncertain artifacts,
  not only artifacts already accepted into the success set.
- A handled artifact-write exception still belongs to the run state machine;
  success eligibility cannot be inferred only from durable and incomplete
  artifact lists.
- Returning a shallow copy of a record that contains nested provenance still
  exposes receipt state to caller mutation.
- General ISO 8601 parsing is wider than an RFC 3339 receipt contract and needs
  an explicit grammar before semantic date validation.
