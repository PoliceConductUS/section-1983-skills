# Verification

## Branch and scope

- Branch: `codex/issue-31-municipal-profiles`.
- Parent: `codex/issue-60-authority-sources`.
- Pre-archive implementation HEAD: `748fb04`.
- Draft PR: `#92`; Issue `#31` remains open.
- The public boundary accepts only seven exact recursive read-only input
  folders, ordinary files with source YAML, one explicit output folder, and
  output-local temporary space.

## TDD and review evidence

- RED specified the exact offline folder contract, source-YAML/hash binding,
  upstream validation, input fingerprints, five domains, ten institutional
  evidence categories, support directions, cross-record references, gaps, and
  output confinement.
- GREEN added an installable skill and pure in-memory helper that returns four
  deterministic output-relative artifacts without opening folders or using the
  network.
- Review added a failing case for affirmative Monell-liability language. The
  helper now rejects that language before producing profile bytes.
- No source file, input folder, target filing, or litigation decision is mutated
  by the skill.

## Commands

- Focused five-suite run: 62 tests passed.
- `npm run skills:list`: 29 skills discovered.
- `npm run governance:validate`: passed.
- `npm run format:check`: passed.
- `npm run validate`: passed with 27 drafting tests, 609 evaluation tests, 29
  discovered skills, 36 OpenSpec items, corpus evaluation, and governance.
- `git diff --check`: passed.

## Remote state

Every commit through `748fb04` is present on
`origin/codex/issue-31-municipal-profiles`. The PR remains draft until the
archive commit and exact-head checks pass.

## Archive verification

The repository-local OpenSpec CLI archived the change as
`2026-08-25-issue-31-municipal-profiles` and created the durable
`building-municipal-monell-profiles` specification with a concrete purpose.
After archive, `npm run validate` again passed 27 drafting tests, 609 evaluation
tests, 29 discovered skills, all 36 OpenSpec items, corpus evaluation, and
governance.
