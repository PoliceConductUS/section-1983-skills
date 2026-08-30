# folder-scoped-role-orchestration Specification

## Purpose

TBD - created by archiving change issue-63-role-sweeps. Update Purpose after
archive.

## Requirements

### Requirement: Sweeps repeat one fixed role over explicit profile selections

A sweep MUST accept a nonempty explicit set of already validated profile-file
selections bound to one fixed role and operation. Every variant MUST use the
same exact selected filing target bytes and hash. Profile data MUST NOT select
or alter role behavior, adapters, permissions, output validation, or publication
policy.

#### Scenario: Two variants target different filing bytes

- **WHEN** two otherwise valid sweep variants bind different target hashes
- **THEN** the sweep fails before any child dispatch

### Requirement: Every variant receives a fresh output-confined process

Each variant MUST launch exactly once through the shared launcher in a fresh
isolated process. It MUST have a distinct full absolute output folder, and its
working directory and all temporary paths MUST remain under that output folder's
`temp/` directory.

#### Scenario: Three variants are selected

- **WHEN** a valid sweep selects three variants
- **THEN** three fresh child processes run and no variant shares a process,
  output folder, temporary folder, or hidden state

### Requirement: Runs publish ordinary artifacts and bounded receipts

The trusted host MUST publish a successful run's validated findings and
`run-receipt.yaml` through the existing output writer. The receipt MUST record
the fixed role and operation, variant ID, selected logical profile, source-YAML,
and target paths and hashes, launcher and producer versions, terminal status,
and output-relative paths and hashes. It MUST NOT contain absolute paths or case
excerpts. Failed runs MUST publish only bounded failure state and MUST NOT
publish findings.

#### Scenario: A child is unavailable

- **WHEN** one role launch returns a bounded unavailable failure
- **THEN** that run remains visibly failed and has no successful findings
  artifact

### Requirement: Sweep comparison is deterministic and failure-aware

When every selected run succeeds, the comparison MUST deterministically report
stable, subset, and flipped findings using exact normalized finding content and
sorted variant support. Profile input order MUST NOT change the comparison
bytes. When any run fails or is unavailable, the comparison MUST be marked
`incomplete`, list successful and failed variants, and emit no stable, subset,
or flipped conclusion.

#### Scenario: Variant order changes

- **WHEN** the same complete successful variants are supplied in a different
  order
- **THEN** the comparison bytes are identical

### Requirement: Role sequences cross only persisted ordinary files

A later role hop MUST run as a new invocation with a fresh process, declared
read-only input folders, and its own full absolute output folder. A prior role's
work may cross the boundary only as one selected persisted ordinary file whose
relative path and hash match the prior trusted-host publication. No
conversation, hidden context, or in-memory child result may cross between roles.

#### Scenario: Later hop names an unpersisted in-memory result

- **WHEN** a later hop does not select the prior persisted artifact from a
  declared read-only input folder
- **THEN** the sequence fails before launching that hop

### Requirement: Sweep and sequence inputs remain unchanged

A sweep or sequence MUST NOT mutate a filing target, profile file,
source-documentation YAML, approved source, or prior output. The coordinator's
own transient work MUST remain under `<sweep-output-folder>/temp/`.

#### Scenario: A prior output changes during a later hop

- **WHEN** the selected prior output's hash changes during the later invocation
- **THEN** the later run fails and the sequence cannot report success
