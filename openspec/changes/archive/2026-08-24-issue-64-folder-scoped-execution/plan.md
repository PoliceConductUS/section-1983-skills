# Folder-Scoped Skill Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development`
> to implement this plan task-by-task. Follow `test-driven-development`,
> `requesting-code-review`, and the OpenSpec/Superpowers bridge. Push every
> commit before continuing.

**Goal:** Establish a folder-native invocation and governance contract that all
public Section 1983 skills can preserve without CaseGraph or another persistence
dependency.

**Architecture:** A versioned JSON schema defines the public envelope. A
standard-library repository conformance module validates exact shapes,
canonicalizes roots and child paths, and builds logical input manifests; the
trusted host, not skill prose or the validator, enforces OS and network
isolation. The full protocol has one owner document while each independently
installable skill carries a compact boundary checked by governance validation.

**Tech Stack:** Python 3 standard library, JSON Schema document, `unittest`,
OpenSpec superpowers-bridge, existing governance validator.

**Spec:**
`openspec/changes/issue-64-folder-scoped-execution/specs/folder-scoped-skill-execution/spec.md`

## Global constraints

- No CaseGraph, CaseHome, Git, MCP, resource URI, virtual filesystem, bridge,
  output writer, or external runtime dependency.
- Inputs are recursively read-only; only the declared output folder is writable.
- Internet is disabled unless the invoked skill expressly authorizes it.
- Prompt text does not establish filesystem or network isolation.
- Python standard library only.
- One story branch and one draft PR; leave Issue #64 and the PR open.

## Task 1: Folder invocation and manifest RED

**Files:**

- Create: `evaluations/tests/test_folder_scoped_execution.py`

**Interfaces:**

- Produces failing expectations for `validate_invocation(envelope)`,
  `build_input_manifest(invocation)`, `resolve_input_path(...)`, and
  `resolve_output_path(...)` from `scripts.validate_folder_invocation`.

- [ ] Write a valid two-role fixture with literal expected canonical roots and a
      hand-derived manifest containing relative paths, sizes, and SHA-256.
- [ ] Add table-driven invalid envelopes for missing fields, extra fields,
      duplicate roles, relative roots, missing/non-directory roots, invalid
      isolation values, and invalid internet/runtime values.
- [ ] Add separate cases for output-inside-input, input-inside-output, absolute
      child path, parent traversal, missing target, and target symlink escape.
- [ ] Add manifest cases for deterministic output at different absolute roots,
      internal file symlink handling, external file/directory symlink rejection,
      and directory-symlink cycle rejection.
- [ ] Run
      `python3 -m unittest evaluations.tests.test_folder_scoped_execution -v`.
      Expected: import failure because the conformance module does not exist.
- [ ] Commit with `test: define folder invocation boundary` and push.

## Task 2: Folder invocation and manifest GREEN

**Files:**

- Create: `governance/folder-invocation.schema.json`
- Create: `scripts/validate_folder_invocation.py`
- Create: `FOLDER_SCOPED_EXECUTION.md`
- Modify: `evaluations/tests/test_folder_scoped_execution.py` only to correct a
  proven invalid RED assumption.

**Interfaces:**

- `InvocationError(code: str)` exposes one stable `code`.
- `validate_invocation(envelope: dict) -> ValidatedInvocation` returns canonical
  `Path` roots, target data, runtime limits, and internet policy.
- `resolve_input_path(invocation, role, relative_path) -> Path` permits only an
  existing child confined to that input role.
- `resolve_output_path(invocation, relative_path) -> Path` permits only a
  confined output child and follows no escaping existing symlink component.
- `build_input_manifest(invocation) -> dict` returns only logical role/file
  data.

- [ ] Add the exact JSON schema with `additionalProperties: false` at every
      envelope object and literal isolation values.
- [ ] Implement strict type/shape validation and stable error codes before path
      access.
- [ ] Implement canonical root, target, child-path, containment, and symlink
      checks using `pathlib` and `os.scandir`.
- [ ] Implement sorted SHA-256 manifest traversal with real-directory cycle
      detection and no absolute persisted paths.
- [ ] Add a stdin JSON CLI that emits the logical manifest on success and a
      bounded JSON error on failure; it performs no writes.
- [ ] Write the canonical owner document and state exactly what the helper
      proves and what only the host can enforce.
- [ ] Run the focused module until GREEN, then
      `python3 -m unittest evaluations.tests.test_folder_scoped_execution -v`.
- [ ] Commit with `feat: establish folder-scoped invocation contract` and push.

## Task 3: Independently installable governance RED

**Files:**

- Modify: `evaluations/tests/test_repository_governance.py`

**Interfaces:**

- Produces failing expectations for `validate_folder_scope_contracts(root)` in
  `scripts/validate_governance.py` and for every public skill package.

- [ ] Define the four compact affirmative rules and literal semantic inversions
      in the test module.
- [ ] Extend the temporary repository fixture with a valid compact skill
      contract and protected folder-gate policy.
- [ ] Add mutation cases for each missing/inverted rule and assert the stable
      `folder-scope-contract-language-missing: <skill>` finding.
- [ ] Add a real-repository test that iterates every public `SKILL.md` and
      applies the same compact assertion.
- [ ] Extend protected-gate expectations for folder scope, input non-mutation,
      output confinement, and internet policy.
- [ ] Run `python3 -m unittest evaluations.tests.test_repository_governance -v`.
      Expected: failures because governance and public skills lack the contract.
- [ ] Commit with `test: protect folder-scoped skill execution` and push.

## Task 4: Independently installable governance GREEN

**Files:**

- Modify: `scripts/validate_governance.py`
- Modify: `GOVERNANCE.md`
- Modify: `CONTRIBUTING.md`
- Modify: `.github/pull_request_template.md`
- Modify: every `skills/*/SKILL.md`
- Modify: `openspec/changes/issue-64-folder-scoped-execution/tasks.md`

**Interfaces:**

- `validate_folder_scope_contracts(root) -> list[str]` returns stable
  skill-specific findings and is called by `validate_repository`.

- [ ] Add the compact rules and deterministic validator without claiming to
      prove host behavior.
- [ ] Add the canonical protected boundary to governance and link it from
      contribution guidance without copying the full protocol.
- [ ] Add the compact four-sentence boundary to every public skill exactly once.
- [ ] Run the governance module until GREEN, then run discovery, formatting,
      OpenSpec validation, and the full evaluation suite.
- [ ] Mark Tasks 1 through 3 complete in `tasks.md` using verified evidence.
- [ ] Commit with `docs: apply folder boundary to public skills` and push.

## Task 5: Whole-story review and archive

**Files:**

- Modify implementation/tests only for accepted review corrections.
- Create: `openspec/changes/issue-64-folder-scoped-execution/verify.md`
- Create: `openspec/changes/issue-64-folder-scoped-execution/retrospective.md`
- Archive into:
  `openspec/changes/archive/2026-08-24-issue-64-folder-scoped-execution/`
- Create durable spec: `openspec/specs/folder-scoped-skill-execution/spec.md`
- Modify durable spec: `openspec/specs/repository-skill-governance/spec.md`

**Interfaces:**

- Produces one complete Issue #64 branch ready to parent Issue #65.

- [ ] Review schema and validator false greens, path/symlink handling, manifest
      determinism, bounded diagnostics, host-enforcement honesty, and complete
      public-skill coverage.
- [ ] Correct accepted Critical or Important findings through a new failing test
      and rerun review.
- [ ] Complete all task checkboxes and write verification evidence from fresh
      focused and full commands.
- [ ] Write the evidence-first retrospective, archive with the repository-local
      OpenSpec CLI, and validate durable specs.
- [ ] Run `npm run validate`, `git diff --check`, forbidden dependency searches,
      branch/origin parity, and clean-status checks.
- [ ] Commit with `docs: archive folder-scoped execution contract`, push, mark
      the draft PR ready for review, and leave Issue #64 and the PR open.
