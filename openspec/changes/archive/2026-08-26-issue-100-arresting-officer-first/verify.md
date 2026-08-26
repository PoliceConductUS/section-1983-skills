# Verification

## TDD evidence

- RED:
  `python3 -m unittest evaluations.tests.test_arresting_officer_defendant_order`
  ran five tests and failed three contract tests because the existing umbrella,
  complaint, and false-arrest instructions omitted the arrest audit and
  defendant-order rule. The synthetic passing candidates and permanent
  regressions already evaluated as expected.
- GREEN: the same command passed all five tests after the minimal instruction
  changes.
- Mutation: changing the umbrella trigger from `arrest` to `detention` caused
  the focused suite to fail one test. Restoring the trigger returned all five
  tests to passing.

## Focused verification

- `python3 -m unittest evaluations.tests.test_arresting_officer_defendant_order evaluations.tests.test_complaint_contract_composition evaluations.tests.test_complaint_candor_contract evaluations.tests.test_skill_folder_contracts evaluations.tests.test_skill_folder_guidance`
  passed 58 tests.
- The new repository-integration regression initially exposed that a bespoke
  multi-scenario corpus cannot live under the canonical `evaluations/fixtures/`
  loader. Moving it to `evaluations/arresting-officer-defendant-order/v1/` made
  the formerly failing integration test, focused tests, and
  `npm run evaluations:corpus` pass.
- `npx openspec validate issue-100-arresting-officer-first --strict` passed.

## Full verification

`npm run validate` passed and included:

- 27 drafting-script tests;
- 636 evaluation tests;
- discovery of all 29 installed skills;
- 38 OpenSpec items with the active change;
- the complete existing evaluation corpus; and
- governance validation.

## Delta spec sync state

- `arresting-officer-defendant-ordering`: needs sync through the owning branch's
  OpenSpec archive step.

## Whole-story review

- Every new or materially revised filing that names defendants audits declared
  inputs for an arrest and source-documented arresting officers.
- One arresting officer is primary. Several arresting officers require a
  caller-declared primary; without one, drafting stops and asks.
- The primary arresting officer leads captions, Parties sections, defendant
  lists or tables, and defendant-grouped claim presentations.
- Earlier filing order does not control, while factual chronology and
  substantive claim logic remain unchanged.
- Markham appears only as synthetic caller-designated fixture data and is not a
  public-skill default.
- The change adds no package, manifest runtime, graph, CaseGraph, repository,
  persistence layer, Git dependency, or ambient workspace scan.

## Implementation signal

All implementation changes are committed through `3e74e2f`, and the worktree is
clean before verification-artifact creation.

## Front-door routing leak detector

No Issue #100 design artifact was written beneath `docs/superpowers/specs/`.
