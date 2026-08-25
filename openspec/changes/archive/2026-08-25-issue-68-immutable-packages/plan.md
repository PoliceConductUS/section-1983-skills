# Issue #68 Immutable Folder Packages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans
> to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Add one immutable folder-package envelope, trusted-host loader and
publisher, and protected static-role/profile binding for future role stories.

**Architecture:** Domain artifacts remain unchanged inside complete manifest-
listed folders. A standard-library trusted-host module validates all filesystem
and integrity properties into frozen bytes and publishes regeneration through
`OutputRun`; a separate module validates static role contracts and returns a
non-merging role/profile binding.

**Tech stack:** Python standard library, JSON Schema Draft 2020-12 documents,
`unittest`, existing folder invocation validation, and `OutputRun`.

**Spec:** `openspec/changes/issue-68-immutable-packages/design.md`

## Global constraints

- No CaseGraph, Git, registry, launcher, real participant data, or new runtime
  dependency.
- Inputs remain recursively read-only; only the trusted host writes beneath the
  explicit output folder.
- Tests and fixtures are fictional and public-safe.
- Every behavior change follows RED, observed failure, minimal GREEN, and push
  after commit.

---

### Task 1: Public schemas and fictional packages

**Files:**

- Create: `governance/immutable-folder-package.schema.json`
- Create: `governance/static-role-contract.schema.json`
- Create: `evaluations/folder-package-fixtures/*`
- Create: `evaluations/tests/test_immutable_folder_packages.py`

**Interfaces:**

- Produces the exact manifest and role-contract shapes consumed by later tasks.

- [ ] Write schema/fixture tests with literal expected top-level fields and four
      complete fictional package kinds.
- [ ] Run
      `python3 -m unittest     evaluations.tests.test_immutable_folder_packages`
      and confirm failures are caused by the absent schemas and fixtures.
- [ ] Add the two strict schemas and the four canonical fixture packages.
- [ ] Run the focused test and confirm the structure/fixture slice passes.
- [ ] Commit and push the RED and GREEN changes in separate commits.

### Task 2: Immutable package loader

**Files:**

- Create: `scripts/immutable_folder_package.py`
- Modify: `evaluations/tests/test_immutable_folder_packages.py`

**Interfaces:**

- Produces `PackageError(code)`, frozen `PackageMember`, frozen
  `ValidatedFolderPackage`, and
  `load_folder_package(root, *, accepted_kinds, max_bytes)`.
- `ValidatedFolderPackage` exposes package identity, kind, freshness, producer,
  sources, exact manifest SHA-256/fingerprint, and immutable member bytes.

- [ ] Write loader tests for canonical success, versions, dates, complete
      membership, aliases, escapes, special files, hashes, receipt linkage,
      failed validation, byte limits, and mutation after load.
- [ ] Run the focused test and confirm the absent loader or missing behavior is
      the only failure cause.
- [ ] Implement the minimal strict loader with bounded stable error codes.
- [ ] Run focused tests and the existing FilingPacket/output-writer suites.
- [ ] Commit and push the RED and GREEN changes in separate commits.

### Task 3: Complete package publisher

**Files:**

- Modify: `scripts/immutable_folder_package.py`
- Modify: `evaluations/tests/test_immutable_folder_packages.py`

**Interfaces:**

- Produces
  `publish_folder_package(invocation, *, package_kind, package_id, created_at, freshness, sources, members, validation, operation, run_id, skill_version)`
  returning the terminal `OutputRun` receipt.
- Proposed members contain `id`, `role`, `classification`, `path`, `media_type`,
  and `contents`.

- [ ] Write publication tests using a real installed-contract invocation and
      literal expected manifest/provenance values.
- [ ] Confirm RED for unbound invocation, incomplete publication, or missing
      publisher while source bytes remain unchanged.
- [ ] Implement canonical manifest construction and one complete
      `fresh-regenerable` output run at `packages/<package-id>/`.
- [ ] Confirm published output reloads to the expected fingerprint and all
      source/context bytes remain unchanged.
- [ ] Commit and push the RED and GREEN changes in separate commits.

### Task 4: Protected static-role/profile binding

**Files:**

- Create: `scripts/static_role_binding.py`
- Modify: `evaluations/tests/test_immutable_folder_packages.py`

**Interfaces:**

- Produces `RoleBindingError(code)`, frozen `ValidatedStaticRoleContract`,
  frozen `RoleProfileBinding`, `validate_static_role_contract(value)`, and
  `bind_role_profile(contract, package, *, as_of)`.
- Binding retains canonical contract bytes and a validated package snapshot in
  separate fields; no profile object is merged into contract data.

- [ ] Write literal contract and hostile-profile tests that would fail if
      capabilities, prohibitions, network, target mutation, or output authority
      were copied from package data.
- [ ] Confirm RED for absent validation/binding and incompatible or stale
      packages.
- [ ] Implement strict contract validation and deterministic freshness binding.
- [ ] Confirm exact canonical role-contract bytes remain unchanged and package
      contents remain separate immutable bytes.
- [ ] Commit and push the RED and GREEN changes in separate commits.

### Task 5: Public migration and governance

**Files:**

- Create: `FOLDER_PACKAGES.md`
- Modify: `README.md`
- Modify: `GOVERNANCE.md`
- Modify: `scripts/validate_governance.py`
- Modify: `evaluations/tests/test_repository_governance.py`
- Modify: `skills/building-defense-counsel-overlays/SKILL.md`
- Modify: `skills/building-litigation-alignment-overlays/SKILL.md`
- Create in each affected skill: `references/immutable-folder-package.md`

**Interfaces:**

- Public and independently installed skills link to the shared package boundary
  while their current domain schemas and validators remain canonical.

- [ ] Write governance and isolated-package RED tests for missing, inverted, or
      escaping package-contract guidance.
- [ ] Add the shared guide, install-local references, governance matrix/rules,
      and README routing.
- [ ] Run focused governance, package, counsel, and alignment suites.
- [ ] Commit and push the RED and GREEN changes in separate commits.

### Task 6: Verification and archive

**Files:**

- Create: `openspec/changes/issue-68-immutable-packages/verify.md`
- Create: `openspec/changes/issue-68-immutable-packages/retrospective.md`
- Modify: `openspec/changes/issue-68-immutable-packages/tasks.md`

**Interfaces:**

- Produces durable OpenSpec requirements and exact-head readiness evidence.

- [ ] Run focused tests, `python3 -m py_compile` on modified Python,
      `npm run     validate`, and `git diff --check`.
- [ ] Review the entire stacked diff against live Issue #68 and correct every
      finding through a new RED/GREEN cycle.
- [ ] Record verification/retrospective evidence and archive with
      `npx openspec archive issue-68-immutable-packages -y`.
- [ ] Re-run `npm run validate`, commit/push the archive, require exact GitHub
      checks, mark the PR ready, and leave both PR and issue open.
