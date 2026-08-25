# Verification

## TDD evidence

- RED:
  `python3 -m unittest evaluations.tests.test_independent_legal_rag_supervision`
  failed for the absent stage-provenance schema, supervision classifier,
  independent-stage instructions, and versioned corpus.
- GREEN: the same command passed 7 tests after implementation.

## Focused verification

- `python3 -m unittest evaluations.tests.test_independent_legal_rag_supervision evaluations.tests.test_authority_grounding_contract evaluations.tests.test_verified_authority_audit evaluations.tests.test_non_mutating_quality_control evaluations.tests.test_repository_governance evaluations.tests.test_skill_folder_contracts`
  passed 74 tests.
- `npm run evaluations:corpus` passed.
- `python3 scripts/validate_governance.py` passed.
- `npx openspec validate issue-80-independent-rag-supervision --strict` passed.

## Full verification

`npm run validate` passed and included:

- 27 drafting-script tests;
- 631 evaluation tests;
- discovery of all 29 installed skills;
- 38 OpenSpec items with the active change;
- the complete existing evaluation corpus; and
- governance validation.

## Whole-story review

- Generation and audit stages have distinct identities, invocation identities,
  and output-folder fingerprints.
- The classifier fails closed on self-review, a missing stage, changed bytes,
  reused output, unavailable execution, malformed output, and every unresolved
  or failed proposition class.
- Fifteen versioned YAML fixtures cover the complete Issue #80 taxonomy and
  verify their embedded source SHA-256 values without network access.
- AI-only records cannot claim human approval, and prohibited provider secrets
  and continuation identifiers are rejected.
- The change adds no package, graph, CaseGraph, repository, persistence layer,
  Git dependency, datastore, or ambient workspace.
