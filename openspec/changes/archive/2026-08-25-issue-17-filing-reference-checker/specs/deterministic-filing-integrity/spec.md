# deterministic-filing-integrity Specification

## MODIFIED Requirements

### Requirement: Domain YAML binds ordinary source bytes

The checker MUST strictly validate bounded versioned domain YAML, canonical ISO
dates, relative paths, stable source IDs, exact source roles and
classifications, SHA-256 values, exact fields, and referenced ordinary file
bytes before semantic checks. YAML MUST NOT grant access outside its declared
input folder or supply a command, executable, capability, permission, output
rule, or persistence instruction.

#### Scenario: Documented source date is parseable but noncanonical

- **WHEN** selected YAML supplies a date spelling that parses but is not exact
  `YYYY-MM-DD`
- **THEN** the run returns an invalid-input result before the checker runs
- **AND** no output is published

#### Scenario: Documented source hash differs

- **WHEN** a selected YAML record's hash does not match its referenced ordinary
  file
- **THEN** the run returns an invalid-input result and performs no filing check

## ADDED Requirements

### Requirement: First installed reference-checker milestone remains complete

The installed checker MUST preserve its fixed initial checks for section
ownership and order, paragraph continuity and bounds, exhibit paragraph ranges,
internal short forms, docket-to-appendix consistency, persistent citation
identity and resolution, and open filing gates. The trusted host MUST preserve
deterministic JSON and Markdown reports, a run receipt, stable `passed`,
`findings`, `unavailable`, and `invalid` classes, byte-identical inputs,
explicit output confinement, output-local temporary work, disabled internet, and
isolated installed-skill execution.

#### Scenario: Installed checker is copied without the repository

- **WHEN** the Filing CI skill is copied into an isolated installation with its
  declared input folders
- **THEN** its checker and fixed contract remain available without a repository
  path, external executable, persistence service, or network access
