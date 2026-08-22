# Verification

## Branch and scope

- Branch: `codex/issue-27-judge-overlay-receipts`
- Parent: `codex/issue-26-linter-signals`
- Pre-archive reviewed HEAD: `b25f4de`
- Commits: design `5f3d756`, RED `7d289b9`, and GREEN `b25f4de`.
- No dependency-version, workflow, root `docs/`, `.superpowers/`, case-specific
  data, filing edit, PR, or issue closure was added.

## Public result

- The generic drafting package owns one exact Draft 2020-12 execution packet and
  one standard-library receipt writer.
- The writer verifies one existing version folder, every designated artifact
  path, and every expected and actual SHA-256 value before creating output.
- A completed run records either supported card-linked changes or the exact
  result `no judge-specific drafting change` with a bounded reason.
- Nonpassing required inputs, fingerprint mismatch, unsupported changes, and
  missing, duplicate, unknown, or failed anti-gaming checks produce one stable
  fail-closed receipt with no drafting change.
- The writer creates only one exclusive immutable Markdown receipt under the
  audited version's canonical `audits/` directory and never edits an artifact.

## TDD and review evidence

- Initial runtime RED ran 10 methods with 19 expected missing-feature failures
  and zero errors. Initial structure RED ran three methods with four expected
  failures and zero errors.
- Minimal GREEN initially passed 12 of 13 focused methods. The remaining test
  exposed a formatter that removed the required internal hyphens from the
  no-change phrase.
- The formatter correction preserved the normalized API value and rendered the
  exact required phrase. The final focused suite passed 13 of 13 methods.
- Whole-story pressure rechecked packet immutability, artifact byte
  preservation, path confinement, audits-symlink rejection, exclusive collision
  handling, exact anti-gaming cardinality, unsupported changes, and CLI-only
  creation.

## Commands

- `python3 -m unittest evaluations.tests.test_judge_overlay_receipt_runtime evaluations.tests.test_judge_overlay_receipt_structure -v`
  — 13 focused methods passed.
- `python3 -m compileall -q skills/section-1983-drafting/scripts/judge_overlay_receipt.py`
  — compilation passed.
- `npm run validate` — formatting; 26 drafting tests; 356 evaluation tests; 22
  discovered skills; 20 OpenSpec items; corpus evaluation; and governance
  passed.
- Targeted Prettier, strict change validation, forbidden-directory,
  private-marker, code-comment, and diff checks passed.

## Remote state

Every design, RED, and implementation commit was pushed with `git town sync`. No
PR was created and Issue 27 remains open.

## Archive verification

- The archive creates the durable `judge-overlay-execution` capability and
  updates the durable `judge-overlay-authoring` capability.
- Both durable capabilities pass strict OpenSpec validation.
- The focused suite, standalone skill validators, full repository validation,
  compilation, scope checks, and diff checks pass before the archive commit is
  synced.
