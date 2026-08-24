# explicit-skill-output-persistence Delta Specification

## ADDED Requirements

### Requirement: Output-relative atomic publication

Every skill-produced durable artifact MUST be written through a shared writer
bound to the validated invocation's canonical output root. The writer MUST
accept only canonical output-relative paths, stage bytes beneath that root,
flush and sync successfully, publish the whole file atomically without replacing
an existing destination, and sync the destination directory before reporting
durable success. It MUST reject absolute paths, traversal, noncanonical
segments, reserved run paths, symlink escapes, and destinations outside the
output root.

#### Scenario: Complete artifact is published

- **WHEN** a caller supplies a valid relative path and complete supported
  content to an open output run
- **THEN** the final name appears atomically beneath the canonical output root
  with exactly the supplied bytes

#### Scenario: Content production fails

- **WHEN** a stream fails before staging completes or sync succeeds
- **THEN** no final artifact is published and the run cannot report success

### Requirement: Inputs and prior outputs remain immutable

The writer MUST NOT edit, rename, delete, chmod, truncate, replace, or otherwise
mutate an input file or a prior durable output. It MUST reject an existing
destination and MUST distinguish a destination that aliases an input file.

#### Scenario: Destination already exists

- **WHEN** publication targets a prior output name
- **THEN** the writer reports an output collision and preserves the existing
  inode and bytes

#### Scenario: Destination aliases an input

- **WHEN** an existing destination resolves to the same file identity as a
  declared input file
- **THEN** the writer reports an input alias and preserves both names and bytes

### Requirement: Collision policy is explicit

Each run MUST declare either `append-immutable` or `fresh-regenerable` mode.
Append-immutable mode MUST require unique artifact and receipt paths.
Fresh-regenerable mode MUST require an expressly authorized empty output root at
run start and MUST NOT gain overwrite authority. Reusing a run ID MUST fail.

#### Scenario: Regenerable output folder is not fresh

- **WHEN** a fresh-regenerable run starts with any pre-existing output entry
- **THEN** startup fails before creating run state or changing the output folder

#### Scenario: Failed run is retried

- **WHEN** a caller retries after a failed or interrupted run
- **THEN** it must use a new run ID and new artifact paths and cannot claim that
  prior missing bytes were written

### Requirement: Run status remains honest

The writer MUST create visible incomplete state before accepting artifact bytes.
It MUST publish a terminal success manifest only after all recorded artifact
bytes are durably published. A failure or interruption MUST remain visibly
incomplete or failed and MUST NOT be interpreted as durable success. Temporary
files MUST remain beneath the output root and be safely removed or recorded as
incomplete. A run is successful only when `manifest.json` exists and validates
and `incomplete.json` is absent. Completion MUST publish and sync the manifest,
remove the incomplete record, and sync the run directory in that order. If
incomplete-record removal or the following directory sync fails, the writer MUST
leave or restore and re-sync `incomplete.json` before returning a bounded
failure.

#### Scenario: Process stops before completion

- **WHEN** a run has started but no terminal receipt was published
- **THEN** its incomplete state remains visible and no success manifest exists

#### Scenario: Failure is recorded

- **WHEN** the writer publishes a terminal failure receipt
- **THEN** it contains only bounded failure information and the run rejects any
  later write or success transition

#### Scenario: Manifest is visible while the run remains incomplete

- **WHEN** terminal manifest publication or incomplete-state cleanup stops with
  both `manifest.json` and `incomplete.json` visible
- **THEN** consumers treat the run as non-success regardless of manifest
  validity

#### Scenario: Incomplete-state removal is not durably synced

- **WHEN** `incomplete.json` is removed after the manifest is synced but the
  following run-directory sync fails
- **THEN** the writer restores and re-syncs `incomplete.json` before reporting
  `receipt-unavailable`, and manifest presence alone does not report success

### Requirement: Run manifests are reproducible

A terminal run receipt MUST record schema version, run ID, skill name and
version, status, run mode, logical input-manifest fingerprint, generated
relative paths, output hashes and sizes, internet-use status, and bounded
failure information when applicable. It MUST use canonical logical JSON and MUST
NOT contain absolute machine paths, tracebacks, credentials, environment values,
or case-material excerpts.

#### Scenario: Equivalent runs write in different call order

- **WHEN** equivalent inputs and artifact bytes are written in different call
  order under different machine roots
- **THEN** their logical artifact entries and input-manifest fingerprint are
  identical

#### Scenario: A run fails

- **WHEN** a failure receipt is created
- **THEN** it records a stable code and bounded phase without raw exception text
  or machine paths

### Requirement: Internet provenance is consumption-ready

Every internet-derived artifact MUST record source URL or stable identity, UTC
retrieval time, bounded query or request context when applicable, and lowercase
content SHA-256 before a later skill may consume it as a read-only input.
Internet source records MUST be rejected when the invocation policy is
`disabled`.

#### Scenario: Authorized internet artifact is written

- **WHEN** an authorized invocation writes an artifact with complete internet
  source records
- **THEN** the terminal manifest records those sources and marks internet as
  used

#### Scenario: Internet use is undeclared

- **WHEN** a disabled invocation supplies an internet source record
- **THEN** the writer rejects the write and publishes no final artifact
