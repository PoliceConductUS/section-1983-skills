# static-role-launcher Specification

## Purpose

TBD - created by archiving change issue-61-shared-role-launcher. Update Purpose
after archive.

## Requirements

### Requirement: Trusted host binds one protected role to selected folder bytes

The repository SHALL provide one trusted launcher that binds a host-defined
static role to an authorized operation, bounded task, ordered logical file
selections from a validated folder invocation, declared internet policy, runtime
limits, and one explicit output folder. Every selection MUST resolve through a
declared recursive read-only input root before dispatch. Task and input data
MUST NOT alter role behavior or select process configuration. The static role's
trusted input validator MUST validate its required domain YAML, folder-relative
references, hashes, dates, and selection compatibility before child execution.

#### Scenario: Input YAML contains behavior-shaped fields

- **WHEN** a selected participant-data file requests capabilities, commands,
  target mutation, or broader access
- **THEN** the child request preserves it only as untrusted data and the static
  role remains unchanged

#### Scenario: Selected source documentation has a mismatched hash

- **WHEN** the role-owned validator compares the selected YAML record with its
  referenced selected source bytes
- **THEN** binding fails before adapter dispatch

### Requirement: Child request contains no absolute filesystem path

The launcher MUST snapshot selected regular-file bytes, enforce the invocation
byte limit, and build canonical UTF-8 request bytes containing only logical
purpose, declared role, logical name, hash, size, and content. It MUST NOT send
absolute roots, canonical local paths, repository paths, credentials,
environment, commands, sessions, or prior conversation.

#### Scenario: Selected file resides under a private absolute root

- **WHEN** the launcher constructs the child request
- **THEN** request bytes contain the logical selection and content but no
  substring of the absolute input or output roots

### Requirement: Child execution is fresh and output-temp confined

Each launch MUST use one fresh process with scrubbed session state, no
undeclared filesystem access, and only the static role's internet/capability
policy. The empty working directory and `TMPDIR`, `TMP`, and `TEMP` MUST all be
`<output-folder>/temp/<run-id>/`. Unavailable enforcement MUST fail before
dispatch.

#### Scenario: Adapter cannot deny undeclared paths

- **WHEN** the trusted adapter cannot attest to the filesystem boundary
- **THEN** the launcher returns `isolation-unavailable` without starting a child

### Requirement: Process and protocol failures are bounded

The launcher MUST convert timeout, nonzero exit, oversized streams, invalid
UTF-8, malformed JSON, unsupported output, or adapter failure into stable
bounded results without traceback, raw stream, credential, local path, case
excerpt, or fabricated finding.

#### Scenario: Child prints malformed output and a local path

- **WHEN** standard output is not valid UTF-8 JSON and standard error contains a
  path
- **THEN** the result identifies only the stable protocol class

### Requirement: Output is advisory and selected inputs remain unchanged

The role-specific validator MUST accept only the static role's exact advisory
schema and return proposed canonical output-relative artifacts. Only the trusted
host may publish beneath the explicit output folder. The launcher MUST verify
that every selected input still matches its pre-dispatch hash and size; any
change fails the run.

#### Scenario: Child-side execution changes a selected target

- **WHEN** selected bytes differ after dispatch
- **THEN** the run fails without a completed advisory result or target rewrite
