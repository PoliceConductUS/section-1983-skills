# Design: explicit skill output persistence

## Context

`ValidatedInvocation` already carries canonical input roots and one canonical
output root. The new writer consumes that value and a previously computed
logical input manifest. It never discovers authority from the working directory
or from an ambient environment variable.

## Public API

`scripts/skill_output_writer.py` exposes:

```python
run = OutputRun.start(
    invocation,
    run_id="audit-20260824-001",
    skill_version="1.4.0",
    mode="append-immutable",
    input_manifest=logical_manifest,
)
artifact = run.write(
    "audits/report.md",
    contents_or_stream,
    internet_sources=(),
)
manifest = run.complete()
```

`contents_or_stream` accepts `str` encoded as UTF-8, bytes-like values, or a
binary stream whose `read()` returns bytes. Unsupported or mixed stream content
fails before publication.

`OutputRun.fail(code, phase)` publishes one bounded failure receipt. After
`complete()` or `fail()`, further writes or terminal transitions fail closed.

## Stable directory authority

At start, the writer opens the canonical output root as a directory handle. All
reserved-directory creation, parent traversal, staging, and publication remain
relative to that stable root. Each descendant component is opened or created as
a real directory without following symlinks. Absolute paths and noncanonical raw
segments are rejected before operating-system resolution.

The writer indexes regular input-file identities as `(device, inode)` before the
first write. An existing destination that aliases an input file reports
`input-alias`; every other existing destination reports `output-collision`.
Neither case mutates the destination.

## Atomic publication

For each artifact the writer:

1. creates a unique staging file beneath `.skill-runs/<run-id>/staging/` with
   exclusive creation;
2. copies the supplied content while computing SHA-256 and size;
3. flushes and syncs the staging file successfully;
4. creates missing real parent directories beneath the stable output root;
5. atomically creates the final name as a hard link to the staging inode;
6. syncs the final parent directory so the published name is durable;
7. unlinks the staging name only after publication succeeds.

The hard-link publication is same-filesystem because staging and destination
share the output root. It cannot replace an existing name. A failed copy never
publishes a final artifact. Temporary names remain confined to the run staging
directory; safe cleanup may remove only the current run's unlinked staging
files. If cleanup cannot finish, the failure receipt records an incomplete
staging condition without exposing the machine path.

## Collision and run modes

`append-immutable` permits pre-existing output content but never a destination
collision. The caller must choose a unique report and run ID.

`fresh-regenerable` checks that the canonical output root is empty before the
run directory is created. This is the express authorization for regenerable
outputs. It does not grant replacement authority; collisions still fail.

The reserved `.skill-runs` namespace is writer-owned. Artifact paths cannot
target it. A pre-existing non-directory, symlink, or malformed run namespace
fails closed.

## State and receipts

Run state lives at `.skill-runs/<run-id>/`:

- `incomplete.json` is create-exclusive and makes startup/interruption visible;
- `manifest.json` is the immutable terminal success receipt;
- `failure.json` is the immutable terminal failure receipt;
- `staging/` contains only current-run temporary files.

The incomplete record is authoritative non-success state, not a durable success
artifact. A terminal receipt never replaces another file. Consumers treat a run
as successful only when `manifest.json` exists and validates AND
`incomplete.json` is absent. Manifest presence while the incomplete record
remains is non-success. A failure receipt or only an incomplete record is never
durable success.

Terminal receipt publication follows the same staged, create-exclusive, file-
the manifest name visible, but the incomplete record remains and prevents a
success result. Successful completion publishes and syncs `manifest.json`, then
removes `incomplete.json`, then syncs the run directory again. If incomplete-
record removal fails, or if the directory sync after removal fails, completion
restores `incomplete.json` when necessary and syncs that restored non-success
state before returning `receipt-unavailable`. The writer never reports success
from manifest presence alone.

## Canonical manifest

The input-manifest fingerprint is SHA-256 over compact UTF-8 JSON with sorted
object keys and the logical manifest's already deterministic array order.
Terminal receipts use the same canonical encoding. Artifact entries are sorted
by relative path regardless of write order.

Internet use is explicit. An artifact that derives from internet content must
include source records containing stable identity or URL, UTC retrieval time,
bounded request context, and lowercase SHA-256. `used` is derived from the
presence of source records. Source records are rejected when the invocation's
internet policy is `disabled`.

## Error contract

Public errors expose stable codes and bounded phases only. They never include an
absolute path, raw exception, traceback, environment value, credential, stream
content, or case bytes. Expected codes include `invalid-output-path`,
`output-collision`, `input-alias`, `output-not-fresh`, `stream-failed`,
`internet-not-authorized`, `run-collision`, `run-terminal`, and
`receipt-unavailable`.

## Testing

Synthetic tests use temporary folders and controlled streams. They assert exact
bytes, hashes, sizes, canonical ordering, exclusive collision behavior, symlink
and traversal rejection, input inode/byte preservation, no final file after a
stream failure, visible interruption state, honest terminal status, retry
behavior, and complete internet provenance.
