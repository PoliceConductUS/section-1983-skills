# Verification

Verified on 2026-08-20 in the `codex/issue-16-versioned-releases` worktree.

## TDD evidence

- RED: five focused tests failed only for moving README install sources,
  push-to-main publishing guidance, and the absent release workflow.
- GREEN: eight focused tests passed, including mutation probes for leading-zero
  versions, incomplete clean-tree checks, force flags, force refspecs, tag
  deletion, and deletion refspecs.

## Repository evidence

- `python3 -m unittest evaluations.tests.test_release_discipline -v`: 8 passed.
- `npm run validate`: passed.
  - Prettier: passed.
  - Drafting tests: 16 passed.
  - Evaluation tests: 195 passed.
  - Skill discovery: 20 skills found.
  - OpenSpec: 12 items passed before archive.
  - Canonical evaluation corpus: passed with no regressions.
  - Governance validator: passed.
- Workflow YAML parsing and every embedded Bash block syntax check: passed.
- Canonical SemVer shell probes accepted `v0.1.0` and `v10.20.30` and rejected a
  leading zero in each numeric component.
- `python3 -m py_compile evaluations/tests/test_release_discipline.py`: passed.
- Branch and working-tree `git diff --check`: passed.
- Root `docs` and `.superpowers` directory checks: passed.

## Independent review

The initial review found permissive leading-zero validation, an incomplete
clean-tree check, and a force-push test blind spot. A second mutation review
found destructive refspec, untracked-file suppression, and README-pin seams.
After test-first corrections, the final independent review reported no Critical
or Important findings at commit `c4aca28`.

## Scope review

The change adds one manual release workflow, one focused test module, and
release/install documentation. It creates no tag, GitHub release, stable branch,
registry package, pull request, or automatic publication trigger.
