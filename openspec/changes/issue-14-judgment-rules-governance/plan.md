# Repository Skill Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add test-enforced judgment routing, rules freshness and provenance,
protected-gate review, and thin-wrapper governance for every public skill.

**Architecture:** A public Markdown policy defines human behavior, while one
JSON registry classifies every public skill and normalizes authoritative rule
sources. A small standard-library validator compares that registry with the
repository tree and checks the policy and pull-request review surfaces without
network access.

**Tech Stack:** Markdown, JSON, Python 3 standard library, `unittest`, npm
scripts, OpenSpec 1.3.1.

**Spec:**
`openspec/changes/issue-14-judgment-rules-governance/specs/repository-skill-governance/spec.md`

## Global Constraints

- Public skills reserve litigation judgment and select no material strategy.
- Jurisdiction-specific propositions live only in verified references.
- Every public skill has exactly one registry classification.
- The validator performs no network retrieval and uses only the Python standard
  library.
- General-purpose executable tooling remains outside this repository.
- Do not create `docs/` or `.superpowers/` directories.
- Add no code comments; prefer self-documenting names.
- Commit and run `git town sync` after every commit.

---

### Task 1: RED governance contract tests

**Files:**

- Create: `evaluations/tests/test_repository_governance.py`

**Interfaces:**

- Consumes: repository files and a future CLI
  `python3 scripts/validate_governance.py [repository_root]`.
- Produces: public-seam and temporary-repository tests for the validator
  contract.

- [ ] **Step 1: Add public-seam tests**

  Assert that `GOVERNANCE.md` reserves the named user decisions, requires
  choices and consequences without selection, confines jurisdiction
  propositions, protects all seven gate categories, and states the thin-wrapper
  boundary. Assert that `.github/pull_request_template.md` requests an affected
  gate, rationale, and explicit review. Assert `package.json` makes the
  governance validator reachable from `validate`.

- [ ] **Step 2: Add registry and validator tests**

  Build temporary repositories with `skills/<name>/SKILL.md`, policy, checklist,
  and a minimal registry. Execute the validator and assert stable nonzero
  messages for: `skill-entry-mismatch`, `invalid-rules-mode`, `invalid-date`,
  `bundled-source-required`, `unknown-source-id`, `insecure-source-url`,
  `jurisdiction-reference-required`, and `protected-review-language-missing`.
  Assert a complete temporary repository exits zero.

- [ ] **Step 3: Run RED**

  Run:

  ```bash
  python3 -m unittest evaluations.tests.test_repository_governance -v
  ```

  Expected: failures because the policy, registry, checklist, validator, and npm
  wiring do not exist.

- [ ] **Step 4: Commit and sync the RED seam**

  ```bash
  git add evaluations/tests/test_repository_governance.py
  git commit -m "test: define repository governance contracts"
  git town sync
  ```

### Task 2: GREEN policy, registry, and validator

**Files:**

- Create: `GOVERNANCE.md`
- Create: `governance/rules-provenance.json`
- Create: `.github/pull_request_template.md`
- Create: `scripts/validate_governance.py`
- Modify: `CONTRIBUTING.md`
- Modify: `package.json`
- Modify: `skills/drafting-for-judge-scholer/SKILL.md`
- Modify: `skills/drafting-for-judge-scholer/REFERENCE.md`

**Interfaces:**

- Consumes: repository root containing policy, checklist, registry, and public
  skills.
- Produces: `validate_repository(root: pathlib.Path) -> list[str]` and CLI exit
  zero only when the returned error list is empty.

- [ ] **Step 1: Add public policy and review checklist**

  Write the spec's exact user-decision, jurisdiction-reference, provenance,
  protected-gate, and thin-wrapper contracts in `GOVERNANCE.md`. Link it from
  `CONTRIBUTING.md`. Add pull-request fields for affected gate, rationale, and
  explicit review.

- [ ] **Step 2: Add the complete provenance registry**

  Add top-level `version`, `sources`, and `skills`. Give every actual public
  skill one entry with `rules_mode`, `reviewed_on`, `rationale`, and the
  mode-specific source or runtime-exposure fields. Use official HTTPS source
  URLs and the concrete `2026-08-20` checked date for bundled sources reviewed
  for this change.

- [ ] **Step 3: Implement the minimal validator**

  Implement:

  ```python
  def validate_repository(repository_root: Path) -> list[str]:
      errors = []
      errors.extend(validate_registry(repository_root))
      errors.extend(validate_policy(repository_root))
      errors.extend(validate_pull_request_template(repository_root))
      return errors
  ```

  Use `json.loads`, `datetime.date.fromisoformat`, `urllib.parse.urlparse`,
  exact skill directory enumeration, and stable error IDs. Print one error per
  line and return exit 1 when any error exists.

- [ ] **Step 4: Normalize the jurisdiction overlay**

  Add jurisdiction, official page URL, and checked date to `REFERENCE.md`. Move
  any current Judge Scholer-specific procedural or legal proposition out of
  `SKILL.md` and preserve only its source-gated workflow and reference route
  there.

- [ ] **Step 5: Wire validation and run GREEN**

  Add `governance:validate` and make `validate` reach it. Run:

  ```bash
  python3 -m unittest evaluations.tests.test_repository_governance -v
  npm run governance:validate
  ```

  Expected: all focused tests pass and the live validator exits zero.

- [ ] **Step 6: Commit and sync implementation**

  ```bash
  git add GOVERNANCE.md governance/rules-provenance.json .github/pull_request_template.md scripts/validate_governance.py CONTRIBUTING.md package.json skills/drafting-for-judge-scholer/SKILL.md skills/drafting-for-judge-scholer/REFERENCE.md
  git commit -m "feat: enforce repository skill governance"
  git town sync
  ```

### Task 3: Full verification, review, and archive

**Files:**

- Modify: `openspec/changes/issue-14-judgment-rules-governance/tasks.md`
- Create: `openspec/changes/issue-14-judgment-rules-governance/verify.md`
- Create: `openspec/changes/issue-14-judgment-rules-governance/retrospective.md`
- Archive through OpenSpec after all checks pass.

**Interfaces:**

- Consumes: complete Issue #14 diff and all repository validation commands.
- Produces: verified archived durable spec `repository-skill-governance`.

- [ ] **Step 1: Run complete validation**

  Run `npm run validate`, all quick validators for `skills/*/SKILL.md`,
  `python3 -m compileall scripts evaluations`, `git diff --check`, and root
  checks for forbidden `docs` and `.superpowers` directories. Preserve exact
  output under `/private/tmp/issue-14-governance/`.

- [ ] **Step 2: Review against the spec**

  Verify every requirement and scenario has a public test seam, the registry
  exactly matches actual skills, source URLs are authoritative, runtime exposure
  is explicit, and no general-purpose tool or code comment entered the diff.
  Correct and rerun any failing gate.

- [ ] **Step 3: Complete OpenSpec artifacts**

  Mark completed task checkboxes, write `verify.md` with command evidence and
  requirement coverage, and write `retrospective.md` with what worked, what
  changed, and no unresolved follow-up.

- [ ] **Step 4: Commit verification and sync**

  ```bash
  git add openspec/changes/issue-14-judgment-rules-governance
  git commit -m "docs: verify repository skill governance"
  git town sync
  ```

- [ ] **Step 5: Archive, validate, commit, and sync**

  Run:

  ```bash
  npx openspec archive issue-14-judgment-rules-governance --yes
  npm run validate
  git add openspec
  git commit -m "docs: archive repository skill governance change"
  git town sync
  ```
