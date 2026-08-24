# filing-ci-orchestration Delta Specification

## RENAMED Requirements

- FROM: `### Requirement: Configured checker resolution`
- TO: `### Requirement: Packaged checker resolution`
- FROM: `### Requirement: Verified-authority root integration`
- TO: `### Requirement: Declared authority-role integration`

## MODIFIED Requirements

### Requirement: Packaged checker resolution

The `filing-ci` package SHALL ship a narrow deterministic wrapper with an
explicit registry of checker IDs packaged inside the installed distribution. The
wrapper MUST accept the declared `filing` input root, the required canonical
relative filing target, the declared `authorities` input root, and validated
in-memory configuration. It MUST dispatch only a registered packaged checker and
MUST NOT accept or infer a command, executable path, flag list, source path,
output path, repository instruction, or general-purpose checker.

#### Scenario: Packaged checker supports the selected filing

- **WHEN** the filing target identifies a document supported by a registered
  packaged checker
- **THEN** the wrapper runs that checker against only declared input data and
  returns deterministic structured findings and report bytes

#### Scenario: No packaged checker supports the operation

- **WHEN** the checker ID is absent, unknown, unavailable, or incompatible with
  the selected target
- **THEN** the wrapper returns a stable unavailable result, runs no substitute,
  and leaves the filing gate open

### Requirement: Declared authority-role integration

The skill MUST use only the declared `authorities` role when its packaged
checker requires authority verification. It MUST NOT hardcode, discover, or
substitute another authority root. Missing required authority material remains
an unresolved input and leaves the filing gate open.

#### Scenario: Checker requires verified authorities

- **WHEN** the registered checker declares authority verification
- **THEN** the wrapper reads only canonical relative material from the declared
  `authorities` role and records the used logical input hashes

#### Scenario: Required authority material is unavailable

- **WHEN** the declared authority role lacks required verified material
- **THEN** the wrapper returns an unresolved-input result and does not use
  ambient or internet authority material

### Requirement: Failure classification and drafting-loop return

The skill SHALL distinguish unavailable packaged checker, unavailable execution,
unreadable or unresolved declared inputs, invalid target, malformed
deterministic result, publication failure, and checker-reported findings. It
MUST explain the blocking class, preserve the checker's documented severity, and
return actionable findings to the drafting loop without editing the filing.

#### Scenario: Packaged checker cannot execute

- **WHEN** a registered checker cannot complete its deterministic processing
- **THEN** the wrapper returns an unavailable-execution result and does not
  claim that any check completed

#### Scenario: Checker reports hard findings

- **WHEN** the checker returns unresolved hard findings
- **THEN** the skill identifies those findings as an open filing gate and sends
  them back to a separately authorized drafting loop

#### Scenario: Checker reports non-hard findings

- **WHEN** the checker returns warnings or another documented non-hard class
- **THEN** the skill preserves that class without silently downgrading,
  dismissing, or correcting the finding

### Requirement: Read-only orchestration

The skill MUST treat declared input processing and result reporting as
non-mutating. The wrapper MUST NOT modify any input, create directories, open an
output root, rewrite checker bytes, or represent a correction as user-approved.
It SHALL return one canonical output-relative report path and deterministic
bytes for trusted-host append-immutable publication. A response with findings
MUST stop after reporting; remediation remains a separate authorized drafting
operation followed by a fresh Filing CI invocation against the new target bytes.

#### Scenario: Checker identifies a correctable defect

- **WHEN** a finding could be corrected in the filing
- **THEN** the Filing CI operation returns the attacked location and supported
  correction information without changing any input byte

#### Scenario: Drafting operation changes the filing

- **WHEN** a later authorized drafting operation produces a materially changed
  filing artifact
- **THEN** a new Filing CI invocation with new logical input hashes is required
  before the filing gate can pass

### Requirement: Fail-closed filing gate

The skill MUST keep the filing gate open when a packaged checker is unavailable,
a declared input or required target is unresolved, deterministic output cannot
be interpreted, trusted-host publication lacks a valid terminal receipt, target
bytes changed after the run, or a hard finding remains unresolved. It SHALL
report a Filing CI pass only for the exact target fingerprint and logical input
manifest recorded by a successful terminal output run.

#### Scenario: Hard or infrastructure failure remains unresolved

- **WHEN** any hard finding, unavailable class, stale fingerprint, incomplete
  run marker, or missing manifest remains
- **THEN** the skill refuses to describe the target as passing Filing CI or
  filing-ready

#### Scenario: Current packaged run succeeds

- **WHEN** the packaged checker completes for the current target with no hard
  findings and the trusted host records a valid terminal manifest
- **THEN** the skill may report that Filing CI passed while preserving warnings
  and every other independent filing gate
