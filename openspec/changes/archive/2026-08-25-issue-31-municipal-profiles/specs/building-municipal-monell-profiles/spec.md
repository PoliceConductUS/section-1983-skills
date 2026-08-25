# building-municipal-monell-profiles Specification

## ADDED Requirements

### Requirement: Profile building uses exact declared folders

The installed skill MUST accept exactly the recursive read-only `municipality`,
`department`, `source`, `policy-catalog`, `policy-assessment`, `case-record`,
and `verified-authority` roles, no target, disabled internet, and one explicit
output folder. Temporary work MUST remain under `<output-folder>/temp/`.

#### Scenario: Complete offline profile inputs are supplied

- **WHEN** the trusted host validates the exact roles and enforceable isolation
- **THEN** profile building uses only selected ordinary files and YAML within
  those folders

### Requirement: Every evidence use has exact provenance

The builder MUST bind every evidence use to one declared input role,
folder-relative path, SHA-256, location, date, bounded proposition, support
direction, limitation list, and review state.

#### Scenario: Selected institutional source changed

- **WHEN** ordinary bytes no longer match the documented SHA-256
- **THEN** profile building fails before using that evidence

### Requirement: Institutional evidence types remain distinct

The builder MUST distinguish formal policy, custom evidence, training,
supervision, FTO transmission, complaints/internal affairs, ratification
candidates, litigation positions, institutional feedback, and institutional
learning while preserving favorable, unfavorable, disconfirming, and neutral
evidence.

#### Scenario: Complaint lacks corroborating institutional response

- **WHEN** a complaint is selected as a possible notice event
- **THEN** it remains a bounded complaint record with limitations rather than
  proof of custom, notice, or deliberate indifference

### Requirement: Five analysis domains remain nonconclusive

The builder MUST organize `Practice`, `Knowledge`, `Authority`, `Causation`, and
`Recurrence` as separate evidence, counterevidence, gaps, and bounded questions.
It MUST NOT represent a Monell element as satisfied or legally sufficient.

#### Scenario: Domain has favorable and disconfirming evidence

- **WHEN** evidence points in different directions
- **THEN** both directions and the unresolved question remain in the same domain

### Requirement: Profile output remains non-liability analysis

The builder MUST return deterministic profile YAML, gap YAML, Markdown, and
domain validation bytes for trusted-host publication. It MUST NOT decide Monell
liability, select a municipal theory, provide legal advice, or edit a filing.

#### Scenario: Profile validates

- **WHEN** every proposed record and gap passes the domain contract
- **THEN** the trusted host may publish the artifacts without treating the
  profile as proof or governing law
