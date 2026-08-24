# Implementation plan: Issue #69 folder-scoped operations documentation

> Execute with subagent-driven development, strict documentation RED/GREEN
> reviews, OpenSpec verification and retrospective artifacts, immediate push
> after every commit, and fresh whole-branch verification before PR readiness.

## Task 1: Documentation contract RED

**Files:**

- Rename/modify: `evaluations/tests/test_case_workspace_guide.py` to
  `evaluations/tests/test_folder_operations_guide.py`

- [x] Specify one repository-relative README guide link and confined operation
      owner links.
- [x] Specify the ordered first-hour flow and parse the canonical invocation
      fixture after replacing caller-selected root tokens.
- [x] Specify stable logical roles, exactly one reused output root, target and
      internet/isolation fields, inaccessible paths, and receipt verification.
- [x] Specify synthetic-only examples and ban obsolete product-specific terms
      from current public documents.
- [x] Run the focused test and record RED.
- [x] Commit with `test: define folder operations documentation` and push.

## Task 2: Folder-native documentation GREEN

**Files:**

- Rename: `CASE_WORKSPACE.md` to `FOLDER_OPERATIONS.md`
- Modify: `FOLDER_OPERATIONS.md`
- Modify: `README.md`

- [x] Write one canonical invocation and ordered first-hour flow without a
      prescribed case directory or universal runner.
- [x] Explain recursive read-only inputs, one output, target selection, internet
      policy, trusted-host isolation, inaccessible paths, hashes, manifests,
      checked-through dates, and retrieval provenance.
- [x] Explain portable folder-backed artifact patterns and the separate-product
      adapter boundary.
- [x] Link each described operation to its owning skill contract.
- [x] Make focused and full tests green.
- [x] Commit with `docs: explain folder-scoped skill operations` and push.

## Task 3: Whole-story review and archive

**Files:**

- Create: `openspec/changes/issue-69-folder-scoped-docs/verify.md`
- Create: `openspec/changes/issue-69-folder-scoped-docs/retrospective.md`
- Archive into:
  `openspec/changes/archive/2026-08-24-issue-69-folder-scoped-docs/`
- Modify durable spec: `openspec/specs/case-workspace-start-guide/spec.md`

- [x] Review links, terminology, flow order, invocation consistency, operation
      ownership, synthetic scope, and Issue #71 boundary.
- [x] Correct accepted Critical or Important findings test-first and rerun
      review.
- [x] Write evidence, archive with repository-local OpenSpec, and run
      `npm run validate` with ignored SDD scratch temporarily isolated.
- [x] Commit with `docs: archive folder operations guide` and push.
- [x] Complete the final independent review, remove ignored SDD scratch, and
      rerun fresh `npm run validate`.

After the final evidence commit is pushed and freshly verified, the controller
marks the draft PR ready while leaving Issue #69 and its PR open. That external
PR-state transition is not a tracked repository change.
