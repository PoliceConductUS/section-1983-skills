# deterministic-filing-integrity Specification

## Purpose

TBD - created by archiving change issue-2-filing-integrity. Update Purpose after
archive.

## Requirements

### Requirement: Checker behavior is fixed and folder scoped

The repository MUST provide one fixed installed filing-integrity checker
registry. A run MUST read only selected ordinary files from declared recursive
read-only `filing-source`, `filing-index`, `record-reference`, `exhibit`,
`docket-to-appendix`, and `verified-authority` folders. Case data MUST NOT add a
checker, command, executable, capability, permission, path, or output rule.

#### Scenario: Input YAML names an executable

- **WHEN** a selected case-data YAML record contains instruction-shaped
  executable or capability fields
- **THEN** strict validation rejects it before any checker runs

### Requirement: Domain YAML binds ordinary source bytes

The checker MUST strictly validate bounded versioned domain YAML, relative
paths, stable source IDs, SHA-256 values, ISO dates, exact fields, and
referenced ordinary file bytes before semantic checks. YAML MUST NOT grant
access outside its declared input folder.

#### Scenario: Documented source hash differs

- **WHEN** a selected YAML record's hash does not match its referenced ordinary
  file
- **THEN** the run returns an invalid-input result and performs no filing check

### Requirement: Initial checks are deterministic and mechanical

The installed initial check set MUST validate declared section ownership and
order, paragraph continuity and bounds, exhibit paragraph ranges, supported
internal short forms, docket-to-appendix consistency, persistent citation-ID
uniqueness and resolution state, and open filing-gate markers. It MUST NOT
decide fact truth, legal sufficiency, authority quality, strategy, or filing
readiness.

#### Scenario: Open filing gate remains in the selected index

- **WHEN** the selected filing index contains an unresolved hard gate
- **THEN** the checker returns the stable open-gate finding and cannot pass

### Requirement: Persistent citation identity preserves visible text

Persistent citation markup MUST preserve ordinary visible citation text while
providing stable citation identity, citation type, and a logical source or
record target. Manual markup MUST NOT bypass quotation, pinpoint, source, or
authority verification.

#### Scenario: Citation identifier is duplicated

- **WHEN** two selected citation instances use the same persistent ID
- **THEN** the checker returns a stable duplicate-citation-ID finding

### Requirement: Outputs are explicit and output-temp confined

The trusted host MUST publish deterministic JSON findings, Markdown findings,
and `run-receipt.yaml` only beneath the caller's full absolute output folder.
Every transient byte, staging file, process working directory, `TMPDIR`, `TMP`,
and `TEMP` MUST remain beneath `<output-folder>/temp/`. Every selected input
MUST remain byte-identical.

#### Scenario: Output-local isolation is unavailable

- **WHEN** the host cannot enforce the output-local working and temporary
  boundary
- **THEN** the checker returns unavailable without reading case material

### Requirement: Exit classes are stable and fail closed

The checker MUST return only documented `passed`, `findings`, `unavailable`, or
`invalid` classes. Missing required folders or selected YAML MUST be
unavailable; malformed or mismatched selected input MUST be invalid; and
unresolved hard findings MUST keep the Filing CI gate open.

#### Scenario: Required source documentation is missing

- **WHEN** the selected check set requires source documentation that is absent
- **THEN** the run returns unavailable and never reports a pass
