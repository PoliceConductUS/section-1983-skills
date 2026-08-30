# verified-authority-audit Specification

## Purpose

TBD - created by archiving change issue-3-verified-authorities. Update Purpose
after archive.

## Requirements

### Requirement: Authority audit is folder scoped

The skill MUST read only one required target inside `filing-source` and selected
ordinary files inside `verified-authority`. It MUST publish only beneath one
explicit output folder and MUST use its `temp/` directory for all transient
work. It MUST NOT require a case-data package, manifest-based input format,
graph, CaseGraph, repository, Git, global datastore, or ambient workspace.

#### Scenario: Authority YAML names another root

- **WHEN** selected YAML attempts to add or escape to another folder
- **THEN** validation rejects it before citation analysis

### Requirement: Authority YAML binds exact ordinary bytes

Selected corpus, authority, and source YAML MUST use strict bounded schemas,
canonical relative paths, stable IDs, hashes, ISO dates, exact fields, and
deterministic ordering. Authority and source YAML MUST independently agree on
the selected ordinary opinion bytes.

#### Scenario: Opinion hash differs

- **WHEN** selected YAML does not match the authority document bytes
- **THEN** the audit returns invalid and performs no citation verification

### Requirement: Eyecite is extraction only

The audit MUST use eyecite for candidate extraction and antecedent resolution
without treating its output as proof of identity, binding status, proposition,
pinpoint, quotation, later history, or good law.

#### Scenario: Eyecite extracts an absent case

- **WHEN** an extracted citation has no selected verified-authority record
- **THEN** the audit returns a missing-authority hard finding

### Requirement: Quotation and authority gates fail closed

The audit MUST verify required authority identity and status fields and MUST
require each asserted direct quotation to occur verbatim in the exact selected
document. An unusable text layer MUST remain pending visual review rather than
pass.

#### Scenario: Quotation is absent

- **WHEN** an asserted quotation does not occur verbatim in the selected
  authority document
- **THEN** the audit returns a stable hard quotation finding

### Requirement: Ordinary audit is deterministic and offline

The `audit` operation MUST disable internet and produce deterministic findings
for identical logical input bytes. A separately authorized `freshness-research`
operation MAY retrieve candidate material but MUST NOT certify good law or
mutate inputs.

#### Scenario: Ordinary audit lacks internet

- **WHEN** an ordinary authority audit runs with all selected files present
- **THEN** it completes without network access

### Requirement: Results are explicit and read only

The host MUST publish deterministic JSON and Markdown findings plus
`run-receipt.yaml` beneath the explicit output folder. Exit classes MUST be
`passed`, `findings`, `unavailable`, or `invalid`, and all selected inputs MUST
remain byte-identical.

#### Scenario: Required authority YAML is absent

- **WHEN** selected authority documentation is missing
- **THEN** the result is unavailable and never verified
