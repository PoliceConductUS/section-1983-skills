# Project 1 Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure this repository to run OpenSpec with the Superpowers bridge
and provide one reproducible validation command for subsequent backlog branches.

**Architecture:** Keep workflow configuration repository-local. Pin OpenSpec and
Prettier as development dependencies, vendor the same prompt-only bridge schema
used by the PoliceConductUS template repositories, and run current Python skill
tests plus OpenSpec and formatting checks through npm and GitHub Actions.

**Tech Stack:** Node.js 24 or newer, npm, `@fission-ai/openspec` 1.3.1, Prettier
3.8.3, Python standard-library `unittest`, Agent Skills CLI.

**Spec:** `docs/superpowers/specs/2026-08-20-project-1-backlog-design.md`

## Global Constraints

- Keep `.worktrees/` ignored at the repository root.
- Use the `superpowers-bridge` schema for every later OpenSpec change.
- Preserve the existing Python-standard-library-only rule for skill scripts.
- Run `git town sync` after every commit.
- Do not merge, close issues, or change GitHub Project status.

---

### Task 1: Add repository-local workflow configuration

**Files:**

- Create: `.nvmrc`
- Create: `package.json`
- Create: `openspec/config.yaml`
- Create: `AGENTS.md`
- Create: `.github/workflows/validate.yml`

**Interfaces:**

- Consumes: existing `skills/*/SKILL.md` packages and
  `skills/section-1983-drafting/scripts` unit tests.
- Produces: `npm run validate`, the public repository validation command used by
  developers and continuous integration.

- [ ] **Step 1: Add the Node and npm contract**

  Set `.nvmrc` to `24`. Create a private `package.json` with these pinned
  development dependencies:

  ```json
  {
    "@fission-ai/openspec": "1.3.1",
    "prettier": "3.8.3"
  }
  ```

  Define scripts for `format`, `format:check`, `test:unit`, `skills:list`,
  `openspec:status`, `openspec:validate`, and `validate`. The `validate` script
  must run formatting, the current unit suite, Agent Skills package discovery,
  and `openspec validate --all` in that order.

- [ ] **Step 2: Add OpenSpec project configuration**

  Create `openspec/config.yaml` with `schema: superpowers-bridge`. State that
  this repository owns public Section 1983 agent skills, that general-purpose
  executable tooling belongs in an owning repository behind thin skills, and
  that behavior changes require public-seam tests and skill validation.

- [ ] **Step 3: Add repository-local agent instructions**

  Create `AGENTS.md` that routes behavior changes through OpenSpec, requires
  Superpowers execution discipline, reserves litigation judgment to the user,
  preserves the thin-wrapper boundary, and identifies the exact validation
  command. Do not duplicate the bridge schema's artifact instructions.

- [ ] **Step 4: Add continuous validation**

  Create `.github/workflows/validate.yml` using `actions/checkout@v6` and
  `actions/setup-node@v6`, the checked-in `.nvmrc`, `npm ci`, and
  `npm run validate` for pull requests and pushes to `main`.

- [ ] **Step 5: Install pinned dependencies**

  Run: `npm install`

  Expected: `package-lock.json` records OpenSpec 1.3.1 and Prettier 3.8.3.

- [ ] **Step 6: Commit and synchronize**

  ```bash
  git add .nvmrc package.json package-lock.json openspec/config.yaml AGENTS.md \
    .github/workflows/validate.yml
  git commit -m "build: configure repository workflow"
  git town sync --non-interactive
  ```

### Task 2: Install and validate the Superpowers bridge

**Files:**

- Create: `openspec/schemas/superpowers-bridge/README.md`
- Create: `openspec/schemas/superpowers-bridge/schema.yaml`
- Create:
  `openspec/schemas/superpowers-bridge/templates/adopters/CLAUDE.md.fragment.md`
- Create:
  `openspec/schemas/superpowers-bridge/templates/adopters/CLAUDE.md.fragment.zh-TW.md`
- Create: `openspec/schemas/superpowers-bridge/templates/brainstorm.md`
- Create: `openspec/schemas/superpowers-bridge/templates/design.md`
- Create: `openspec/schemas/superpowers-bridge/templates/plan.md`
- Create: `openspec/schemas/superpowers-bridge/templates/proposal.md`
- Create: `openspec/schemas/superpowers-bridge/templates/retrospective.md`
- Create: `openspec/schemas/superpowers-bridge/templates/spec.md`
- Create: `openspec/schemas/superpowers-bridge/templates/tasks.md`
- Create: `openspec/schemas/superpowers-bridge/templates/verify.md`

**Interfaces:**

- Consumes: the bridge bundle already adopted at
  `/Users/dalelotts/dev/PoliceConductUS/intake/openspec/schemas/superpowers-bridge`.
- Produces: a repository-local `superpowers-bridge` OpenSpec schema discoverable
  and valid through the pinned OpenSpec CLI.

- [ ] **Step 1: Vendor the adopted bridge without modification**

  Copy the complete `superpowers-bridge` directory from the adopted local
  PoliceConductUS repository into `openspec/schemas/`. Do not modify the
  vendored schema or templates during bootstrap.

- [ ] **Step 2: Verify schema discovery**

  Run: `npx openspec schemas`

  Expected: output lists `superpowers-bridge`.

- [ ] **Step 3: Verify the schema**

  Run: `npx openspec schema validate superpowers-bridge`

  Expected: the schema is valid.

- [ ] **Step 4: Commit and synchronize**

  ```bash
  git add openspec/schemas/superpowers-bridge
  git commit -m "build: install superpowers bridge"
  git town sync --non-interactive
  ```

### Task 3: Prove the complete bootstrap

**Files:**

- Modify: `docs/superpowers/plans/2026-08-20-project-1-bootstrap.md`

**Interfaces:**

- Consumes: the repository configuration and vendored bridge from Tasks 1 and 2.
- Produces: current passing evidence for the bootstrap branch.

- [ ] **Step 1: Run complete validation**

  Run: `npm run validate`

  Expected: formatting, 16 existing Python tests, Agent Skills discovery, and
  all OpenSpec validation pass.

- [ ] **Step 2: Revalidate every skill with the runtime validator**

  Run the bundled `quick_validate.py` once for every `skills/*/SKILL.md`.

  Expected: all 12 skills report `Skill is valid!`.

- [ ] **Step 3: Mark this plan complete**

  Change each completed checkbox in this file from `[ ]` to `[x]`.

- [ ] **Step 4: Commit and synchronize**

  ```bash
  git add docs/superpowers/plans/2026-08-20-project-1-bootstrap.md
  git commit -m "docs: record bootstrap verification"
  git town sync --non-interactive
  ```
