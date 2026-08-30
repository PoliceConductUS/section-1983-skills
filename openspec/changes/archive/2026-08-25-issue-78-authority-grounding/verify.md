# Verification

## TDD evidence

- RED: `python3 -m unittest evaluations.tests.test_authority_grounding_contract`
  failed with the missing schema, missing six fixture folders, and missing audit
  and drafting protocol terms.
- GREEN: the same command passed 3 tests after the schema, protocol, and fixture
  implementation.

## Focused verification

- `python3 -m unittest evaluations.tests.test_authority_grounding_contract evaluations.tests.test_verified_authority_audit evaluations.tests.test_repository_governance evaluations.tests.test_skill_folder_contracts`
  passed 61 tests.
- `npm run evaluations:corpus` passed with all permanent regressions detected.
- `python3 scripts/validate_governance.py` passed.

## Full verification

`npm run validate` passed after one clean rerun of an existing 50-millisecond
subprocess-startup timing test that passed in isolation. The successful run
included:

- 27 drafting-script tests;
- 618 evaluation tests;
- discovery of all 29 installed skills;
- 38 OpenSpec items with the active change;
- the complete synthetic evaluation corpus; and
- governance validation.

## Whole-story review

- Every Issue #78 failure class has a separate bounded, network-independent
  passing/regression fixture.
- The schema separates correctness from groundedness and records exact source
  support, source voice, applicability fields, and verification provenance.
- The skill and shared drafting protocol reject citation existence, links,
  lists, snippets, and treatment symbols as substitutes for exact support.
- Existing folder, non-mutation, source, authority, and human-decision gates
  remain intact.
- The change adds no package, graph, CaseGraph, repository, persistence layer,
  or ambient workspace dependency.
