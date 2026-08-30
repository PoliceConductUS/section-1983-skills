## MODIFIED Requirements

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

## ADDED Requirements

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
