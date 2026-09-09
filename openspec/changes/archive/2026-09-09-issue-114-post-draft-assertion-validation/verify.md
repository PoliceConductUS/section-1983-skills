# Verification

## Required repository validation

`npm run validate` completed successfully against the working-tree bytes after
the complete pressure-test evidence was added:

- Prettier found all files formatted.
- 27 drafting-script unit tests passed.
- 716 evaluation tests passed.
- the repository listed all 32 skills, including
  `validating-court-facing-assertions`;
- all 41 OpenSpec specs and changes passed;
- the complete evaluation corpus passed; and
- governance validation passed.

## Focused checks

- `python3 -m unittest evaluations.tests.test_post_draft_assertion_validation`
- `python3 -m unittest evaluations.tests.test_skill_folder_contracts evaluations.tests.test_skill_folder_guidance evaluations.tests.test_repository_governance`
- `npm exec -- openspec validate issue-114-post-draft-assertion-validation --strict`
- `npm run evaluations:corpus`

## Independent review

An independent branch review identified corpus-ID, governance-fixture,
multi-result, cross-skill role, multi-document target, declaration-routing,
issue-register, fixture completeness, and OpenSpec coverage defects. The final
review confirmed those architecture defects were corrected. The remaining
positive-fixture and pressure-evidence findings were addressed by the permanent
positive-path assertions and reproducible pressure-test artifacts. A final
read-only review then found that the reference report still collapsed compound
propositions and that the verbatim pressure transcript closed its outer fence
early. The report now inventories all nine atomic propositions, its test asserts
the complete expected inventory and counts, and the transcript fence is fixed.
The reviewer reported no additional defects in the approved party-document
source rule, ownership, consumer routing, folder boundary, or CaseGraph
independence.

## Result

The focused regression suite passed 11 tests after the final review corrections,
and strict validation passed for the Issue #114 OpenSpec change. After archive
and formatting, a complete `npm run validate` passed again: 27 drafting-script
unit tests, 716 evaluation tests, 32 listed skills, 42 OpenSpec specifications,
the complete evaluation corpus, and governance validation. Live PR-head and
check reconciliation occurs after the push.
