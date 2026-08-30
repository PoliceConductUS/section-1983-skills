# filing-ci-orchestration Specification

## Purpose

Define thin, project-configured Filing CI orchestration that runs deterministic
filing-integrity checks at the required workflow stages, preserves checker
findings, and fails closed without taking ownership of checker logic or
drafting.

## Requirements

### Requirement: Configured checker resolution

The `filing-ci` skill SHALL resolve the controlling draft and checker invocation
from the canonical complaint contract, repository instructions, project
configuration, or explicit user input. For a version-2 complaint handoff, the
canonical package's declared install-local validator is a complete approved
invocation. Filing CI MUST run the resolved invocation rather than describe or
reproduce checks in prose. It MUST NOT invent executable paths, flags, source
paths, or output locations.

#### Scenario: Canonical version-2 validator is installed

- **WHEN** the canonical complaint package declares its install-local validator
  and the controlling draft and handoff are identified
- **THEN** Filing CI runs that exact validator invocation without requiring a
  separate project-defined command

#### Scenario: Project supplies a complete checker invocation

- **WHEN** a project identifies the controlling draft and a complete compatible
  filing-integrity checker invocation
- **THEN** Filing CI runs that invocation without substituting an inferred
  command

#### Scenario: Checker invocation is unavailable

- **WHEN** neither the canonical version-2 validator nor repository
  instructions, project configuration, or explicit user input supplies a
  complete checker invocation
- **THEN** Filing CI reports unavailable checker configuration and leaves the
  filing gate open without inventing a command

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

- **WHEN** the installed configured checker completes successfully for the
  current target with no unresolved hard findings and the trusted host records a
  valid terminal receipt
- **THEN** the skill may report that Filing CI passed while preserving warnings
  and every other independent filing gate

### Requirement: Drafting and filing assessment modes

Filing CI SHALL expose drafting and filing modes. Drafting mode SHALL require
version-2 structural validation and MAY continue with an explicit non-completed
graph-assessment state. Filing mode SHALL require a current graph assessment
that ran across every included claim unit.

#### Scenario: Graph is missing in drafting mode

- **WHEN** structure passes and graph assessment is `not_run_missing`
- **THEN** drafting mode reports the unassessed state without calling the filing
  ready

#### Scenario: Graph is stale in filing mode

- **WHEN** graph assessment is `not_run_stale`
- **THEN** filing mode exits nonzero and identifies the fingerprint mismatch

### Requirement: No CaseGraph CLI dependency

Filing CI SHALL consume the version-2 result and any assessment produced from
the on-disk graph. It SHALL NOT require or invoke a CaseGraph CLI to establish
graph availability or validity.

#### Scenario: Graph files exist and no CLI is installed

- **WHEN** the on-disk graph validates and assessment completes
- **THEN** Filing CI may accept the assessment without testing for a CaseGraph
  executable

### Requirement: No silent assessment downgrade

Filing CI SHALL preserve structural and graph-assessment status separately in
machine and human output. A missing, invalid, incompatible, stale, or partial
assessment SHALL NOT be converted into an unqualified pass.

#### Scenario: Structure passes and graph is invalid

- **WHEN** the structural result passes but graph assessment is
  `not_run_invalid`
- **THEN** both states remain visible and filing mode exits nonzero

### Requirement: Authority resolution remains visible

Filing CI SHALL preserve every authority-resolution status supplied by the graph
assessment. It SHALL NOT treat a citation or pinpoint string as resolved unless
the assessment identifies the verified opinion artifact and hash and an exact
matching passage at the cited pinpoint.

#### Scenario: Used authority has no exact source match

- **WHEN** an assessed component relies on an authority proposition whose
  pinpoint or exact-text resolution is missing, ambiguous, or nonmatching
- **THEN** Filing CI reports the unresolved authority connection and preserves
  the affected component as incomplete or indeterminate

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
