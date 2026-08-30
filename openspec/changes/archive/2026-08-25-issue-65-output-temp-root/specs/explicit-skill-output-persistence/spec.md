# explicit-skill-output-persistence Specification Delta

## ADDED Requirements

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

## MODIFIED Requirements

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
