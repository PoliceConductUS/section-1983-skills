# Tasks

## 1. Atomic output boundary RED

- [x] 1.1 Add synthetic tests for valid text/bytes/stream publication, path
      grammar, traversal, reserved paths, symlink escapes, collisions, input
      aliases, and input/prior-output preservation.
- [x] 1.2 Add failure-injection tests proving partial streams and sync or
      publication failures expose no final artifact.

## 2. Atomic output boundary GREEN

- [x] 2.1 Implement the standard-library invocation-bound `OutputRun` writer,
      stable output-root authority, confined staging, and create-exclusive
      atomic publication.
- [x] 2.2 Implement append-immutable and fresh-regenerable startup rules without
      deletion, replacement, chmod, or ambient path authority.

## 3. Run receipt RED

- [x] 3.1 Add tests for visible incomplete state, terminal success/failure,
      terminal immutability, interrupted runs, run-ID collision, and retry
      honesty.
- [x] 3.2 Add tests for canonical input fingerprinting, sorted artifact records,
      hashes, sizes, bounded failures, internet policy, and complete internet
      provenance.

## 4. Run receipt GREEN

- [x] 4.1 Implement canonical state and terminal receipts plus the manifest JSON
      schema and canonical public persistence protocol.
- [x] 4.2 Integrate the shared writer contract with the folder-scoped execution
      owner document without copying the full protocol into every skill.

## 5. Review and archive

- [x] 5.1 Independently review directory-handle confinement, race behavior,
      collision/alias classification, atomicity, retry honesty, receipt
      completeness, and bounded diagnostics.
- [x] 5.2 Correct accepted Critical or Important findings test-first and rerun
      review.
- [x] 5.3 Write verification and retrospective evidence, archive the OpenSpec
      change, validate durable specs, run `npm run validate`, push, and mark the
      draft PR ready while leaving Issue #65 and the PR open.
