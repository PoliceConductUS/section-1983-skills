# Verification

## TDD evidence

- RED:
  `python3 -m unittest evaluations.tests.test_premise_aware_authority_retrieval`
  failed against the old frame-less planner API and missing premise-aware skill
  and fixture contracts.
- GREEN: focused premise-aware retrieval and existing source-collection tests
  passed 13 tests after implementation.

## Focused verification

- `python3 -m unittest evaluations.tests.test_premise_aware_authority_retrieval evaluations.tests.test_collecting_legal_authority_sources evaluations.tests.test_skill_folder_contracts evaluations.tests.test_repository_governance`
  passed 61 tests.
- `npm run evaluations:corpus` passed with every permanent retrieval regression
  detected.
- `python3 scripts/validate_governance.py` passed.

## Full verification

`npm run validate` passed and included:

- 27 drafting-script tests;
- 624 evaluation tests;
- discovery of all 29 installed skills;
- 38 OpenSpec items with the active change;
- the complete synthetic evaluation corpus; and
- governance validation.

## Whole-story review

- Every Issue #79 premise and retrieval failure class has a bounded,
  network-independent passing/regression fixture.
- Retrieval frames bind jurisdiction, hierarchy, date, posture, rule version,
  factual trigger, source universe, access limits, and checked-through date.
- Premises preserve verified, false, and unresolved states; sources preserve
  retrieval order, stable rejection reasons, and exact internet provenance.
- Empty and incomplete results remain known missingness rather than proof that
  no authority exists.
- The change adds no package, graph, CaseGraph, repository, persistence layer,
  or ambient workspace dependency.
