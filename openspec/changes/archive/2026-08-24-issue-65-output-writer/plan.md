# Implementation plan: Issue #65 explicit output persistence

> Execute with subagent-driven development, strict RED/GREEN task reviews,
> OpenSpec verification and retrospective artifacts, immediate push after every
> commit, and fresh whole-branch verification before PR readiness.

## Task 1: Atomic output boundary RED

**Files:**

- Create: `evaluations/tests/test_skill_output_writer.py`

**Interfaces:**

- Specify `OutputRun.start(...)` and
  `OutputRun.write(relative_path, contents_or_stream, internet_sources=())`.

- [ ] Write valid text, bytes, and binary-stream cases with exact bytes,
      SHA-256, and size expectations.
- [ ] Write output-relative grammar, reserved namespace, traversal, NUL,
      backslash, drive-prefix, and symlink-escape cases.
- [ ] Write existing-output and input-hardlink-alias cases that assert inode,
      metadata, and byte preservation.
- [ ] Write stream, sync, and publication failure cases that assert no final
      artifact and confined staging.
- [ ] Run focused tests and record the expected missing-interface RED.
- [ ] Commit with `test: define atomic skill output boundary` and push.

## Task 2: Atomic output boundary GREEN

**Files:**

- Create: `scripts/skill_output_writer.py`
- Modify only invalid Task 1 assumptions if a platform fact is proved and
  documented.

**Interfaces:**

- `OutputRun.start(invocation, *, run_id, skill_version, mode, input_manifest)`
- `OutputRun.write(relative_path, contents_or_stream, *, internet_sources=())`

- [ ] Bind all filesystem operations to the canonical output root and reject
      descendant symlinks without ambient working-directory authority.
- [ ] Index input file identities for explicit alias rejection.
- [ ] Stage, hash, size, flush, sync, and publish create-exclusively without
      replacement.
- [ ] Enforce append-immutable and expressly empty fresh-regenerable startup.
- [ ] Make Task 1 and existing folder-boundary tests green.
- [ ] Commit with `feat: add atomic skill output writer` and push.

## Task 3: Run receipt RED

**Files:**

- Modify: `evaluations/tests/test_skill_output_writer.py`

**Interfaces:**

- `OutputRun.complete()`
- `OutputRun.fail(code, phase)`

- [ ] Write incomplete, success, failure, interruption, terminal immutability,
      duplicate-run, and retry cases.
- [ ] Write exact canonical input fingerprint and artifact ordering fixtures.
- [ ] Write disabled/authorized internet cases and required provenance fields.
- [ ] Write bounded failure and machine-path exclusion cases.
- [ ] Run focused tests and record receipt RED evidence.
- [ ] Commit with `test: define reproducible output receipts` and push.

## Task 4: Run receipt GREEN

**Files:**

- Modify: `scripts/skill_output_writer.py`
- Create: `governance/skill-run-manifest.schema.json`
- Create: `SKILL_OUTPUT_PERSISTENCE.md`
- Modify: `FOLDER_SCOPED_EXECUTION.md`

**Interfaces:**

- Canonical `.skill-runs/<run-id>/` state and terminal receipts.

- [ ] Implement canonical compact JSON fingerprinting and terminal receipts.
- [ ] Derive internet-use status from validated source records and reject
      undeclared internet use before publication.
- [ ] Publish success only after all recorded bytes are durable; publish bounded
      failure without raw exception or path leakage.
- [ ] Document one canonical protocol and link it from the folder owner.
- [ ] Make focused, full evaluation, governance, and OpenSpec checks green.
- [ ] Commit with `feat: record reproducible skill output runs` and push.

## Task 5: Whole-story review and archive

**Files:**

- Modify implementation/tests only for accepted test-first corrections.
- Create: `openspec/changes/issue-65-output-writer/verify.md`
- Create: `openspec/changes/issue-65-output-writer/retrospective.md`
- Archive into: `openspec/changes/archive/2026-08-24-issue-65-output-writer/`
- Create durable spec:
  `openspec/specs/explicit-skill-output-persistence/spec.md`
- Modify durable spec: `openspec/specs/folder-scoped-skill-execution/spec.md`

- [ ] Review stable-directory authority, symlink swaps, hard-link availability,
      alias/collision races, atomic publication, partial failures, manifests,
      retries, and diagnostics.
- [ ] Correct accepted Critical or Important findings through new failing tests
      and rerun review.
- [ ] Complete all task checkboxes and write fresh verification evidence.
- [ ] Write the retrospective, archive with the repository-local OpenSpec CLI,
      and validate durable specs.
- [ ] Remove ignored SDD scratch after review, run `npm run validate`,
      `git diff --check`, forbidden dependency searches, branch/origin parity,
      and live GitHub checks.
- [ ] Commit with `docs: archive explicit output persistence`, push, mark the
      draft PR ready, and leave Issue #65 and its PR open.
