# Verification

Verified on 2026-08-20 in the `codex/issue-18-case-workspace-guide` worktree.

## TDD evidence

- RED: the focused suite failed because the root guide and README route were
  absent.
- GREEN: nine focused tests passed for discovery, install-local confinement,
  ordered first-hour roles, source boundaries, protected decisions, immutable
  inputs, configured validation, release pinning, and no-scaffolding scope.
- Mutation review rejected reversed evidence classifications, approval,
  immutability, validation, and readiness semantics; a traversal link hidden by
  a fenced decoy; and a version-tag prefix with a moving suffix.

## Repository evidence

- `python3 -m unittest evaluations.tests.test_case_workspace_guide -v`: 9
  passed.
- `npm run validate`: passed.
  - Prettier: passed.
  - Drafting tests: 16 passed.
  - Evaluation tests: 208 passed.
  - Skill discovery: 20 skills found.
  - OpenSpec: 14 items passed before archive.
  - Canonical evaluation corpus: passed with no regressions.
  - Governance validator: passed.
- `python3 -m py_compile evaluations/tests/test_case_workspace_guide.py`:
  passed.
- `git diff --check`: passed.

## Independent review

Review first found that the future `v0.1.0` tag was not yet published, semantic
presence checks accepted inverted duties, README discovery accepted a traversal
link plus a fenced decoy, and the version matcher accepted tag suffixes. The
guide now keeps the exact future tag, prohibits substituting `main`, and offers
the verified local-checkout command until that release exists. The final review
reported no Critical or Important findings at commit `19847a7`.

## Scope review

The branch adds one concise root guide, one README link, one standard-library
test, and the OpenSpec record. It adds no workspace template, companion
repository, scaffolder, dependency, workflow, private path, case-specific fact,
root `docs` directory, `.superpowers` directory, or code comment.
