# explicit-skill-output-persistence Specification

## Purpose

Define invocation-bound, create-exclusive artifact publication, honest run
state, reproducible receipts, and internet provenance for folder-scoped public
skills without an external persistence runtime.

## Requirements

### Requirement: Output-relative atomic publication

Every skill-produced durable artifact MUST be written through a shared writer
bound to the validated invocation's canonical output root. The writer MUST
accept only canonical output-relative paths, stage bytes beneath
`<output-folder>/temp/<run-id>/`, flush and sync successfully, publish the whole
file atomically without replacing an existing destination, and sync the
destination directory before reporting durable success. It MUST reject absolute
paths, traversal, noncanonical segments, reserved `temp/` and `.skill-runs/`
paths, symlink escapes, and destinations outside the output root.

#### Scenario: Complete artifact is published

- **WHEN** a caller supplies a valid relative path and complete supported
  content to an open output run
- **THEN** the final name appears atomically beneath the canonical output root
  with exactly the supplied bytes and no transient bytes exist outside the
  reserved output temp folder

#### Scenario: Content production fails

- **WHEN** a stream fails before staging completes or sync succeeds
- **THEN** no final artifact is published, the run cannot report success, and
  the caller can still publish a bounded failure receipt

#### Scenario: Validation fails before an artifact attempt

- **WHEN** path, provenance, or authorization validation rejects a write before
  staging begins
- **THEN** no artifact attempt has begun and the validation error alone does not
  make the run ineligible for success

#### Scenario: Caller mutates a returned artifact record

- **WHEN** a caller mutates any nested value in the artifact record returned by
  a successful write
- **THEN** later receipts and internet-use derivation remain unchanged

### Requirement: Invocation temporary work uses the reserved output temp folder

Every invocation MUST use `<output-folder>/temp/` as its only temporary
workspace. Trusted-host staging, intermediate files, scratch files, process
temporary files, and semantic-work working-directory files MUST be confined
beneath that folder. The host MUST configure the launched process working
directory and `TMPDIR`, `TMP`, and `TEMP` to that folder and MUST rely on the
folder isolation boundary to deny use of system temporary directories,
repository worktrees, current working directories, input folders, and undeclared
paths. `temp/` MUST be reserved against public artifact writes.

#### Scenario: A run stages an artifact

- **WHEN** the output writer stages bytes before atomic publication
- **THEN** the staging name exists only beneath `<output-folder>/temp/<run-id>/`
  and never beneath an input, system temporary directory, repository directory,
  or durable receipt directory

#### Scenario: A host prepares semantic work

- **WHEN** a trusted host prepares the process configuration for an invocation
- **THEN** its working directory and `TMPDIR`, `TMP`, and `TEMP` all select the
  canonical `<output-folder>/temp/` path

#### Scenario: A skill proposes a temp artifact

- **WHEN** a public artifact path begins with `temp/`
- **THEN** the writer rejects it before creating or changing filesystem state

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
files MUST remain beneath `<output-folder>/temp/` and be safely removed or
recorded as incomplete. A run is successful only when `manifest.json` exists and
validates and `incomplete.json` is absent. Completion MUST publish and sync the
manifest, remove the incomplete record, and sync the run directory in that
order. If incomplete-record removal or the following directory sync fails, the
writer MUST leave or restore and re-sync `incomplete.json` before returning a
bounded failure. As soon as a terminal receipt name may be visible, including
after an uncertain post-link sync or staging-cleanup failure, the writer MUST
seal the run, close its retained directory handles, and reject every later
operation as `run-terminal`.

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

The skill version MUST be validated before run-state mutation and MUST match
`[A-Za-z0-9][A-Za-z0-9._+-]{0,63}` so it is bounded and cannot contain a path,
control character, whitespace-delimited excerpt, or other free-form receipt
content.

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

A source URL MUST be 1–2048 printable ASCII characters whose raw value begins
with literal lowercase `http://` or `https://` and has a nonempty host. It MUST
NOT contain whitespace, a control character, a backslash, an embedded username
or password, or an invalid port. A retrieval time MUST use
`YYYY-MM-DDTHH:MM:SS[.fraction]Z` or the same form ending in `+00:00`; the
writer MUST normalize the offset form to literal `Z` and MUST reject alternate
ISO 8601 forms. Internet-use status MUST be derived from validated source
records on both durable and incomplete artifact records.

#### Scenario: Authorized internet artifact is written

- **WHEN** an authorized invocation writes an artifact with complete internet
  source records
- **THEN** the terminal manifest records those sources and marks internet as
  used

#### Scenario: Internet use is undeclared

- **WHEN** a disabled invocation supplies an internet source record
- **THEN** the writer rejects the write and publishes no final artifact

### Requirement: Staging cleanup is durable

The writer MUST sync the staging directory after every staging-entry unlink for
an artifact or receipt, including cleanup after a pre-publication failure. An
artifact staging-sync failure after publication MUST record the artifact as
incomplete at phase `staging-cleanup`. Cleanup failure after an earlier bounded
stream or publication failure MUST NOT replace that more fundamental failure
code. A receipt staging-sync failure after the receipt name may be visible MUST
leave honest incomplete state, seal the run, and report `receipt-unavailable`.

#### Scenario: Staging unlink is not durably synced

- **WHEN** a staging entry is unlinked but the staging-directory sync fails
- **THEN** the writer reports a bounded incomplete or unavailable result and
  does not permit the run to claim a later conflicting terminal state

### Requirement: Only the trusted host publishes helper results

Standalone skill helpers SHALL return deterministic output-relative artifact
paths, bytes or streams, and validated source metadata to the trusted host. They
MUST NOT open the output root, stage artifacts, create run-state files, or call
the output writer. The trusted host MUST validate every returned path and source
record and SHALL remain the sole caller of output-run start, write, complete,
and fail operations.

#### Scenario: Helper returns report bytes

- **WHEN** a packaged checker returns one report path and complete report bytes
- **THEN** the trusted host publishes them append-immutably and derives the
  terminal artifact and internet status from the accepted write

### Requirement: Quality-control publication is one receipt-bound report

The trusted host MUST publish an independent quality-control result as exactly
one append-immutable report through the shared output writer. The report path
MUST contain the quality-control kind, UTC run time, and a canonical lowercase
UUIDv4 run ID. Report bytes MUST identify the terminal run-manifest path that
the same output run will publish. The host MUST NOT report completion unless
both the report and terminal success manifest are durable and incomplete state
is absent.

#### Scenario: Report write succeeds but terminal completion fails

- **WHEN** report bytes are published but the terminal success manifest cannot
  be completed durably
- **THEN** the quality-control run does not report completion and visible run
  state remains failed or incomplete

#### Scenario: A report name already exists

- **WHEN** a quality-control publication selects an existing report path
- **THEN** the writer preserves the existing bytes, rejects the collision, and
  the run cannot report successful completion

#### Scenario: A weak or malformed run identity is supplied

- **WHEN** quality-control publication receives a run ID that is not a canonical
  lowercase UUIDv4
- **THEN** publication fails before creating report or run-state bytes
