# collecting-legal-authority-sources Specification

## ADDED Requirements

### Requirement: Collection uses exact declared folders

The installed skill MUST accept exactly the recursive read-only
`legal-question`, `jurisdiction`, `court-hierarchy`, `relevant-date`,
`seed-authority`, and `approved-source-system` roles, no target, expressly
authorized internet, and one explicit output folder. Temporary work MUST remain
under `<output-folder>/temp/`.

#### Scenario: Bounded source collection is authorized

- **WHEN** the trusted host validates the exact roles, source limits, and
  enforceable isolation
- **THEN** collection uses only declared inputs and expressly authorized network
  access

### Requirement: Every retrieved file has exact provenance

Each retrieved ordinary file MUST have adjacent strict domain YAML binding its
relative path, SHA-256, source URL, query, filters, checked and retrieval dates,
result identity, classification, decision-date evidence or gap, proposed
citation identity, limitations, and duplicate relationships.

#### Scenario: Retrieved bytes changed

- **WHEN** ordinary source bytes no longer match their documented SHA-256
- **THEN** validation fails before publication

### Requirement: Source types remain distinct

The collector MUST distinguish official text, authenticated opinions, docket
copies, mirrors, citator records, secondary material, and unverified references.

#### Scenario: Opinion comes from an unofficial mirror

- **WHEN** the retrieved file is not official or authenticated
- **THEN** it remains `mirror` or `unverified_reference` rather than official
  text

### Requirement: Search gaps remain explicit

The collector MUST preserve empty, incomplete, inaccessible, paid, ambiguous,
and out-of-scope search results as bounded gaps and MUST NOT establish that no
authority exists from those results.

#### Scenario: Approved source returns no accessible result

- **WHEN** the bounded query cannot retrieve an authority source
- **THEN** the collector returns a coverage gap with the exact query, filters,
  date, source-system identity, and limit

### Requirement: Collection never substitutes for authority audit

The collector MUST leave candidate identity, publication, binding
classification, treatment, proposition fit, quotation, pinpoint, and
fair-warning value unverified until a separate `audit-authorities` invocation.

#### Scenario: Candidate source is collected

- **WHEN** collection validates and publishes the ordinary file and source YAML
- **THEN** the candidate may become a later audit input but not a verified
  authority
