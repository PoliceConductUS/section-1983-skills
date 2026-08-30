# Brainstorm: explicit output persistence

## Starting point

Issue #64 gives a trusted host canonical read-only input roots and one canonical
writable output root. Issue #65 must ensure that every durable skill artifact is
published only beneath that output root, never overwrites an input or prior
output, and has an honest machine-readable run receipt.

The user-approved API direction is a writer bound to the invocation, with a
small call such as `run.write("reports/result.md", contents_or_stream)`.

## Constraints

- Accept only output-relative logical paths.
- Reject absolute paths, raw dot or empty segments, NUL, backslashes, drive
  prefixes, symlink escapes, and input-file aliases.
- Never edit, rename, delete, chmod, truncate, or replace an input or a prior
  durable output.
- Stage bytes inside the output root and publish atomically without replacement.
- Leave interrupted or failed runs visibly non-successful.
- Record logical input fingerprints, output hashes and sizes, internet use, and
  bounded failures without machine-path leakage.
- Remain independently installable and standard-library only.

## Options considered

### Write directly to the final path

Rejected. A stream failure exposes partial bytes, and create-versus-replace
flags do not make a multi-write stream atomic.

### Stage and call `os.replace`

Rejected. `os.replace` silently overwrites an existing destination. A separate
existence check is racy and violates the immutable-output rule.

### Stage, sync, then create an exclusive hard link

Selected. The writer stages a regular file under its run directory, flushes and
syncs it, and atomically publishes it with a same-filesystem create-exclusive
link. An existing destination fails closed. Stable output-directory handles and
no-follow traversal keep path resolution bound to the declared output tree.

## Run lifecycle

Each run has a caller-supplied unique run ID and one mode:

- `append-immutable`: add new uniquely named immutable artifacts beneath an
  existing output root; every collision fails.
- `fresh-regenerable`: require an expressly authorized empty output root before
  the run directory is created; every collision still fails.

The writer exclusively creates `.skill-runs/<run-id>/` and an incomplete state
record before accepting artifact bytes. Each successful `write` publishes one
whole artifact and records its logical path, SHA-256, size, and optional
internet source records in memory. `complete()` atomically publishes the
terminal success manifest. `fail(code, phase)` publishes a bounded failure
receipt. A crash that publishes neither terminal receipt leaves the incomplete
record visible.

Retrying the same run ID fails. A retry uses a new run ID and new artifact
paths; the writer never treats existing bytes as success.

## Manifest boundary

The terminal manifest contains:

- schema version, run ID, skill name and version, mode, and status;
- the SHA-256 fingerprint of the canonical logical input-role manifest;
- generated output-relative paths, hashes, and sizes;
- internet policy, whether internet was used, and source identity, retrieval
  time, request context, and content hash for internet-derived artifacts;
- a bounded failure code and phase for failed runs.

It contains no absolute source or output path, traceback, exception text,
environment value, credential, or case-material excerpt.

## Non-goals

- No CaseGraph, Git, branch, worktree, resource-URI, or external service.
- No deletion, cleanup, overwrite, chmod, or mutable latest-file convention.
- No content-type inference, artifact interpretation, or legal judgment.
- No claim that this Python helper establishes the host sandbox from Issue #64.
