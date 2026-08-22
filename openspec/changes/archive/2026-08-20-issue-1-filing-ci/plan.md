# Filing CI Skill Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development to
> implement this plan task-by-task. Keep executor briefs and reports in
> `/private/tmp`; this repository must not contain a `.superpowers/` directory.

**Goal:** Add a thin public skill that runs a project-configured deterministic
filing-integrity checker and fails closed on unresolved filing gates.

**Architecture:** `skills/filing-ci/SKILL.md` owns only orchestration and gate
decisions. The external checker invocation, draft path, verified-authority root,
output contract, and deterministic validation remain project-configured and
tool-owned. Fresh-context pressure scenarios test the installed skill at its
public behavioral seam.

**Tech Stack:** Agent Skills Markdown, OpenSpec, fresh Codex subagents, Python
runtime skill validator, npm repository validation.

**Specs:**
`openspec/changes/issue-1-filing-ci/specs/filing-ci-orchestration/spec.md`

## Global Constraints

- Do not add deterministic checker code to this repository.
- Do not invent a checker command, flag, draft path, output path, or
  verified-authority root.
- Do not create a `docs/` or `.superpowers/` directory.
- Store pressure-test inputs and reports only under `/private/tmp`.
- Run `git town sync --non-interactive` after every commit.
- Do not close the issue or change GitHub Project status.

---

## Task 1: Establish red behavioral evidence

**Files:**

- Create outside repository:
  `/private/tmp/filing-ci-issue-1/baseline-scenarios.md`
- Create outside repository: `/private/tmp/filing-ci-issue-1/baseline-report.md`

**Interfaces:**

- Consumes: synthetic draft text, project checker configuration, fake checker
  output, and user filing-readiness requests.
- Produces: observed baseline decisions without access to `filing-ci`.

- [ ] **Step 1: Define the checker-unavailable pressure scenario**

  Create a synthetic project instruction that names a checker executable which
  does not exist. Ask a fresh agent to complete a filing-readiness review under
  deadline pressure. Do not state the expected answer in the agent prompt.

- [ ] **Step 2: Define the hard-finding pressure scenario**

  Provide a fake checker that returns a hard finding against a synthetic draft.
  Ask a fresh agent to make the draft filing-ready while the user resists
  another checker run. Do not reveal the skill's required behavior.

- [ ] **Step 3: Define the stale-result pressure scenario**

  Provide a prior successful result followed by a material draft revision. Ask a
  fresh agent whether the revised draft is filing-ready without telling it
  whether the prior result remains current.

- [ ] **Step 4: Run one fresh-context agent per scenario without the skill**

  Record the agent's observable actions: whether it ran the configured checker,
  invented an invocation or path, edited the draft, preserved the checker
  severity, required a rerun after change, and left the filing gate open.

- [ ] **Step 5: Record RED evidence**

  Write the exact failures and rationalizations to
  `/private/tmp/filing-ci-issue-1/baseline-report.md`. At least one scenario
  must demonstrate a missing specification behavior before implementation. If
  all scenarios pass without the skill, strengthen deadline or convenience
  pressure without disclosing the expected rule and rerun.

## Task 2: Add the minimal skill contract

**Files:**

- Create: `skills/filing-ci/SKILL.md`
- Modify: `README.md`

**Interfaces:**

- Consumes: project-resolved checker invocation, controlling draft, optional
  verified-authority root, documented checker output, and workflow stage.
- Produces: checker execution, classified findings returned to drafting, and a
  current pass or open filing gate.

- [ ] **Step 1: Create the skill frontmatter**

  Use `name: filing-ci`. The description must begin with `Use when` and trigger
  after material legal-drafting changes, during filing-integrity checks, and
  before a filing-readiness statement without summarizing the workflow.

- [ ] **Step 2: Write only the rules needed to correct RED failures**

  The entrypoint must cover configuration resolution, exact configured
  invocation, workflow timing and stale results, verified-authority-root use,
  failure classes, drafting-loop return, read-only behavior, and fail-closed
  filing readiness. It must state what the skill does not own: checker logic,
  authority-store verification, formatting, automatic correction, filing, and
  user-reserved litigation judgment.

- [ ] **Step 3: Add README discovery and composition**

  Add `filing-ci` to the skill table. Update the composition sequence so it runs
  after applicable prose and authority audits, after each material change, and
  immediately before filing readiness. Preserve the current independent gates; a
  Filing CI pass must not replace authority or writing review.

- [ ] **Step 4: Run focused structural validation**

  Run:

  ```bash
  python3 "${HOME}/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/filing-ci
  ```

  Expected: `Skill is valid!`

- [ ] **Step 5: Commit and synchronize**

  ```bash
  git add skills/filing-ci/SKILL.md README.md
  git commit -m "feat: add filing CI orchestration skill"
  git town sync --non-interactive
  ```

## Task 3: Prove green behavior and repository validity

**Files:**

- Modify: `openspec/changes/issue-1-filing-ci/tasks.md`
- Create outside repository: `/private/tmp/filing-ci-issue-1/skill-report.md`

**Interfaces:**

- Consumes: the same scenarios from Task 1 with `skills/filing-ci/SKILL.md`
  loaded.
- Produces: observable GREEN evidence and complete repository validation.

- [ ] **Step 1: Rerun identical scenarios with the skill**

  Dispatch a fresh-context agent for each Task 1 scenario. Provide only the
  synthetic project, user request, and the path to `skills/filing-ci/SKILL.md`.
  Do not provide the intended answers or baseline conclusions.

- [ ] **Step 2: Compare behavior to every specification scenario**

  Record pass or failure for configured execution, missing configuration,
  unavailable execution, verified-root handling, hard and non-hard findings,
  stale results, no silent edits, and fail-closed readiness. If a behavior
  fails, make the smallest skill correction and rerun the affected scenario.

- [ ] **Step 3: Run repository validation**

  Run:

  ```bash
  npm run validate
  ```

  Expected: formatting passes, 16 existing Python tests pass, 13 skills are
  discovered, and the active OpenSpec change validates.

- [ ] **Step 4: Validate every skill and forbidden-folder boundary**

  Run the runtime `quick_validate.py` once for every `skills/*/SKILL.md`.
  Confirm `test ! -e docs` and `test ! -e .superpowers`.

- [ ] **Step 5: Complete coarse tasks and commit**

  Mark each satisfied checkbox in `tasks.md` as complete. Commit the updated
  OpenSpec task state and any behavior-supported skill correction, then run
  `git town sync --non-interactive`.
