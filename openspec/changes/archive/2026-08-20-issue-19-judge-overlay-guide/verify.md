# Verification

Verified on 2026-08-20 in the `codex/issue-19-judge-overlay-guide` worktree.

## TDD evidence

- RED: ten focused methods failed because the root guide and README route were
  absent. The reviewed suite rejected Markdown/HTML/autolink decoys, semantic
  inversions, unsourced conduct, invalid transfer cards, private paths, and
  judge-conclusion leakage.
- GREEN: eleven focused methods passed after adding the guide, README route, and
  a repository-root validator invocation.
- The command test executes the published argv against the canonical fictional
  valid corpus and requires exact paths, exit status, and output.

## Repository evidence

- `python3 -m unittest evaluations.tests.test_judge_overlay_guide -v`: 11
  passed.
- `npm run validate`: passed.
  - Prettier: passed.
  - Drafting tests: 16 passed.
  - Evaluation tests: 219 passed.
  - Skill discovery: 20 skills found.
  - OpenSpec: 15 items passed before archive.
  - Canonical evaluation corpus: passed with no regressions.
  - Governance validator: passed.
- The published corpus-validator command returned `corpus validation passed`
  from repository root.
- `python3 -m py_compile evaluations/tests/test_judge_overlay_guide.py`: passed.
- `git diff --check`: passed.

## Independent review

RED review successively hardened link forms, operative prose and headings,
conduct provenance, canonical card validation, inverse permissions, paired
fictional examples, structural-only Scholer treatment, and private-path checks.
Whole-story review found one broken validator invocation; a corrective RED test
then exposed it, and the published command was made directly executable. Final
review reported no Critical or Important findings at commit `f20cd4e`.

## Scope review

The branch adds one root guide, one README route, one standard-library test, and
the OpenSpec record. It adds no judge-specific overlay, court research, public
skill, dependency, workflow, executable product, private strategy, private path,
real case fact, root `docs` directory, `.superpowers` directory, or code
comment.
