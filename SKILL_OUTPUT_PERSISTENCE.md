# Skill Output Persistence

Artifact-producing skills persist bytes only through
`scripts/skill_output_writer.py`. A trusted host first validates the folder
invocation, builds its logical input manifest, and starts one output run with a
unique lower-kebab run ID, skill version, and one mode:

- `append-immutable` adds unique artifacts to an existing output folder.
- `fresh-regenerable` requires the output folder to be empty at startup.

Neither mode permits replacement. The skill version is validated before
run-state mutation and contains 1–64 ASCII characters matching
`[A-Za-z0-9][A-Za-z0-9._+-]{0,63}`.
`OutputRun.write(relative_path, contents, internet_sources=())` accepts one
canonical output-relative path and text, bytes, or a binary stream. It rejects
absolute, traversing, noncanonical, reserved, and symlink-escaping paths;
existing outputs; and destinations that alias an input. Publication stages and
syncs the complete file under the output root, creates the final name without
replacement, and syncs its parent directory. After removing the staging name, it
syncs the staging directory; failure is recorded as incomplete staging cleanup.

## Run state

Writer-owned state is stored under `.skill-runs/<run-id>/`:

- `incomplete.json` is created and synced before the run accepts artifact bytes.
- `manifest.json` is the immutable terminal success receipt.
- `failure.json` is the immutable terminal failure receipt.
- `staging/` contains only current-run temporary files.

A run is successful only when `manifest.json` validates against
`governance/skill-run-manifest.schema.json` and `incomplete.json` is absent.
Completion publishes and syncs the manifest, removes the incomplete marker, and
syncs the run directory. If the final cleanup cannot be made durable, the writer
leaves or restores and syncs `incomplete.json` and reports
`receipt-unavailable`. A failed or interrupted run is never success. A terminal
receipt name seals the run even when a later sync or cleanup is uncertain. A
sealed run closes its retained directory handles and rejects every later write
or state transition. Retry uses a new run ID and new artifact paths.

## Reproducibility and internet provenance

Receipts use compact UTF-8 JSON with sorted object keys. The input fingerprint
is SHA-256 over that canonical encoding of the logical input manifest. Artifact
records are sorted by relative path and contain the artifact SHA-256 and byte
size.

An internet-derived artifact supplies one or more source records before its
bytes are published. Each source has exactly one nonempty `url` or `identity`, a
valid UTC `retrieved_at` value normalized to `Z`, a lowercase SHA-256, and an
optional nonempty `request_context` of at most 1024 characters. Source records
include URLs of at most 2048 printable ASCII characters using an absolute
lowercase `http://` or `https://` scheme with a nonempty host and no whitespace,
control character, backslash, embedded username/password, or invalid port.
Source records are rejected when internet is disabled. Receipt `internet.used`
is derived from validated sources on both durable and incomplete artifacts.

Failure receipts accept only a lower-kebab code and phase of at most 64
characters. Receipts never include absolute machine paths, raw exceptions,
tracebacks, environment values, credentials, or case-material excerpts.
