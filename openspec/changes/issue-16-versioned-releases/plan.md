# Immutable Versioned Releases Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:test-driven-development for the RED/GREEN implementation and
> superpowers:verification-before-completion before every completion claim.

**Goal:** Make an immutable, validated semantic-version tag the only published
skills version and make every documented consumer install resolve that tag.

**Architecture:** A manual GitHub Actions workflow validates the exact `main`
commit before creating its annotated tag and release record. Standard-library
repository tests protect workflow ordering and pinned README commands. Human
release documentation uses the same contract.

**Tech Stack:** GitHub Actions YAML, Markdown, Python 3 standard library,
`unittest`, OpenSpec 1.3.1.

## Global Constraints

- Do not create or document a stable branch.
- Do not create a tag before `npm run validate` succeeds.
- Do not trigger the release gate from tag pushes.
- Do not publish a package-registry artifact.
- Do not change skill behavior or dependencies.
- Add no root `docs` or `.superpowers` directory.
- Add no code comments; prefer self-documenting names.
- Commit and run `git town sync` after every commit.

### Task 1: RED release integration tests

**Files:**

- Create: `evaluations/tests/test_release_discipline.py`

- [ ] Parse all remote `npx skills add` commands in README and require the same
      literal `vMAJOR.MINOR.PATCH` GitHub tree source.
- [ ] Reject default-branch install and generic update instructions.
- [ ] Require publishing and contribution guidance to describe `main` as
      integration history and immutable tags as releases.
- [ ] Require a manual workflow with `contents: write`, a `main` ref guard, full
      checkout, semantic-version and duplicate-tag rejection, and this order:
      `npm ci` → `npm run validate` → annotated tag → tag push → GitHub release.
- [ ] Verify RED, commit only the test, and run `git town sync`.

### Task 2: GREEN release workflow and public guidance

**Files:**

- Create: `.github/workflows/release.yml`
- Modify: `README.md`
- Modify: `PUBLISHING.md`
- Modify: `CONTRIBUTING.md`

- [ ] Implement the workflow with `workflow_dispatch`, version input,
      least-privilege write permission, non-main rejection, full checkout,
      semantic-version and remote-tag preflight, locked install, complete
      validation, annotated tag push, and generated GitHub release notes.
- [ ] Pin README sources to `v0.1.0`, remove generic update instructions, and
      explain deliberate upgrades.
- [ ] Replace every release statement that calls `main` stable or treats a push
      as publication.
- [ ] Verify focused GREEN and the full repository gate.
- [ ] Commit and run `git town sync`.

### Task 3: Review, verify, and archive

**Files:**

- Modify: `openspec/changes/issue-16-versioned-releases/tasks.md`
- Create: `openspec/changes/issue-16-versioned-releases/verify.md`
- Create: `openspec/changes/issue-16-versioned-releases/retrospective.md`

- [ ] Review the branch from its Story 15 parent and correct every blocking or
      important finding.
- [ ] Run focused tests, all evaluations, `npm run validate`, strict OpenSpec,
      compile, diff, forbidden-folder, and comment checks.
- [ ] Record evidence, archive through OpenSpec, commit, and sync.
