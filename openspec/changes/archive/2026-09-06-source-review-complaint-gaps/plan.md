# Plan

Each task in tasks.md maps to one RED test group followed by one GREEN edit.

1. Tests: `evaluations/tests/test_source_review_contract_gaps.py` holds every
   new assertion. `test_installed_filing_checks.py` gains `clear_privacy_gate()`
   and `test_complaint_contract_composition.py` gains the three checks and the
   excluded judgment. Run
   `python3 -m unittest evaluations.tests.test_source_review_contract_gaps` and
   confirm failures.
2. Prose: edit `complaint-contract.md`, `claim-specific-contracts.md`,
   `completion-audit.md`, `false-arrest-complaint-delta.md`, both `SKILL.md`
   files, and `case-map.md`. Rerun the test module.
3. Checkers: add `_privacy_findings` to `check_complaint.py` and
   `run_filing_ci.py`, call it after the limitations findings, and update both
   contract JSON files. Rerun the module and `test_installed_filing_checks`.
4. Repository: `npx prettier --write` on changed files, then `npm run validate`,
   then `npx openspec validate source-review-complaint-gaps --strict`.
5. Close: verify.md, retrospective.md, `npx openspec archive -y`, commit.
