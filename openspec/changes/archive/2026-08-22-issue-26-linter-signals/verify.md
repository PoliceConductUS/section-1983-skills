# Verification

## Branch and scope

- Branch: `codex/issue-26-linter-signals`
- Parent: `codex/issue-30-defense-counsel-overlays`
- Pre-archive reviewed HEAD: `761d294`
- Commits: design `803c79a`, RED `f0a8a57`, and GREEN/review correction
  `761d294`.
- No dependency, workflow, root `docs/`, `.superpowers/`, case-specific data,
  filing edit, PR, or issue closure was added.

## Public result

- The existing aggregate violation counts, normalized score, and score-delta
  workflow remain available.
- Every counted check now has a stable paragraph-level finding with the supplied
  artifact, one-based paragraph and line range, bounded excerpt, count, and
  unexempted classification.
- `active resistance`, `materially similar`, and `reasonably trustworthy` are
  the only new exemptions because RED proved only those requested phrases
  currently misfired. Four already-clean suggestions remain outside the
  exemption inventory.
- Long-sentence density at two and reporter-citation density at four produce
  paragraph warnings outside counts and scores.
- The drafting workflow targets zero unexempted violations and reconciles every
  residual finding as a violation, a source-verified accurate quotation, or a
  linter-supported controlling term of art.

## TDD and review evidence

- Initial RED kept existing/control behavior green while ten linter assertions
  and two drafting-contract assertions failed on absent Issue 26 behavior.
- Minimal GREEN passed 22 linter tests and two contract tests.
- Whole-story pressure found duplicate exemption IDs when the same controlling
  phrase appeared twice in one paragraph. The focused regression failed before
  the occurrence ordinal correction and passed after it.
- The final focused result was 23 linter tests and two contract tests.

## Commands

- `python3 -m unittest discover -s skills/section-1983-drafting/scripts -p 'test_draft_lint.py' -q`
  — 23 focused linter tests passed.
- `python3 -m unittest evaluations.tests.test_draft_linter_contract -q` — two
  drafting-contract tests passed.
- `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/section-1983-drafting`
  — `Skill is valid!`.
- `npm run validate` — formatting; 26 drafting tests; 343 evaluation tests; 22
  discovered skills; 19 OpenSpec items; corpus evaluation; and governance
  passed.
- Python compilation, strict change validation, forbidden-directory,
  private-marker, code-comment, and diff checks passed.

## Remote state

Every design, RED, and implementation commit was pushed with `git town sync`. No
PR was created and Issue 26 remains open.

## Archive verification

- The archive created the durable `drafting-linter-signals` specification.
- The durable specification passed strict OpenSpec validation.
- The focused suite, standalone skill validator, full repository validation,
  compilation, scope checks, and diff checks passed before the archive commit
  was synced.
