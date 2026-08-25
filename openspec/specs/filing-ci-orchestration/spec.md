# filing-ci-orchestration Specification

## Purpose

Define thin, project-configured Filing CI orchestration that runs deterministic
filing-integrity checks at the required workflow stages, preserves checker
findings, and fails closed without taking ownership of checker logic or
drafting.

## Requirements

### Requirement: Workflow-stage execution

The skill MUST run Filing CI after every material drafting change and again
immediately before describing the document as filing-ready. A material change
MUST invalidate an earlier successful result.

#### Scenario: Draft changes after a successful run

- **WHEN** the controlling draft changes materially after Filing CI succeeds
- **THEN** the skill treats the prior result as stale and requires a new run
  before filing readiness

#### Scenario: Filing-readiness review begins

- **WHEN** the workflow reaches a filing-readiness decision
- **THEN** the skill requires a current successful Filing CI result for the
  controlling draft

### Requirement: Failure classification and drafting-loop return

The skill SHALL distinguish unavailable installed checker, unavailable
execution, unreadable or unresolved declared inputs, invalid target, malformed
deterministic result, publication failure, and checker-reported findings. It
MUST explain the blocking class, preserve the checker's documented severity, and
return actionable findings to the drafting loop without editing the filing.

#### Scenario: Installed checker cannot execute

- **WHEN** a registered installed checker cannot complete its deterministic
  processing
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

The skill MUST keep the filing gate open when an installed checker is
unavailable, a declared input or required target is unresolved, deterministic
output cannot be interpreted, trusted-host publication lacks a valid terminal
receipt, target bytes changed after the run, or a hard finding remains
unresolved. It SHALL report a Filing CI pass only for the exact target
fingerprint and logical selected-input hashes recorded by a successful terminal
output run.

#### Scenario: Hard or infrastructure failure remains unresolved

- **WHEN** any hard finding, unavailable class, stale fingerprint, incomplete
  run marker, or missing receipt remains
- **THEN** the skill refuses to describe the target as passing Filing CI or
  filing-ready

#### Scenario: Current installed run succeeds

- **WHEN** the installed checker completes for the current target with no hard
  findings and the trusted host records a valid terminal receipt
- **THEN** the skill may report that Filing CI passed while preserving warnings
  and every other independent filing gate

### Requirement: Packaged checker resolution

The `filing-ci` skill SHALL ship a narrow deterministic wrapper with an explicit
registry of checker IDs in its installed skill directory. The wrapper MUST
accept one validated six-role folder invocation, a required canonical relative
filing target, and validated in-memory configuration. It MUST dispatch only a
registered installed checker and MUST NOT accept or infer a command, executable
path, flag list, source path, output path, repository instruction, or
general-purpose checker.

#### Scenario: Installed checker supports the selected filing

- **WHEN** the filing target identifies a document supported by a registered
  installed checker
- **THEN** the wrapper runs that checker against only selected declared input
  data and returns deterministic structured findings and report bytes

#### Scenario: No installed checker supports the operation

- **WHEN** the checker ID is absent, unknown, unavailable, or incompatible with
  the selected target
- **THEN** the wrapper returns a stable unavailable result, runs no substitute,
  and leaves the filing gate open

### Requirement: Declared authority-role integration

The skill MUST use only the declared `verified-authority` role when its
installed checker requires authority verification. It MUST NOT hardcode,
discover, or substitute another authority root. Missing required authority
material remains an unresolved input and leaves the filing gate open.

#### Scenario: Checker requires verified authorities

- **WHEN** the registered checker declares authority verification
- **THEN** the wrapper reads only canonical relative material selected from the
  declared `verified-authority` role and records the used logical input hashes

#### Scenario: Required authority material is unavailable

- **WHEN** the declared `verified-authority` role lacks required verified
  material
- **THEN** the wrapper returns an unresolved-input result and does not use
  ambient or internet authority material
