# Case Workspace Starting Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:test-driven-development.

**Goal:** Give a new user a portable, source-bounded first-hour workspace guide
without creating a template or scaffolder.

**Architecture:** A root Markdown guide owns the documentation. README links it
relatively. A standard-library `unittest` module verifies observable guide
content, link confinement, release pinning, and generic-only examples.

**Tech Stack:** Markdown, Python 3 standard library, `unittest`, OpenSpec 1.3.1.

## Global Constraints

- Add documentation only, plus its focused test and OpenSpec artifacts.
- Add no template, repository, skill, script, dependency, workflow, root `docs`,
  or `.superpowers` directory.
- Use no private case material or machine-specific paths.
- Commit and run `git town sync` after every commit.

### Task 1: RED public guide tests

- Create: `evaluations/tests/test_case_workspace_guide.py`
- [ ] Require README to link `CASE_WORKSPACE.md` relatively.
- [ ] Require every first-hour role and the renameable role contract.
- [ ] Require a canonical pinned remote install and explicit unavailable/gap
      behavior.
- [ ] Reject private paths, case identifiers, and template/scaffolder claims.
- [ ] Run focused RED, commit, and sync.

### Task 2: GREEN documentation

- Create: `CASE_WORKSPACE.md`
- Modify: `README.md`
- [ ] Add the minimal generic guide and one README route.
- [ ] Run focused GREEN and full repository validation.
- [ ] Commit and sync.

### Task 3: Review and archive

- [ ] Run independent scope/content review.
- [ ] Record verification and retrospective artifacts.
- [ ] Archive, run post-archive validation, commit, and sync.
