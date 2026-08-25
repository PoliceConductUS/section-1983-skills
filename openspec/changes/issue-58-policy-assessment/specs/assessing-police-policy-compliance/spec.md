# assessing-police-policy-compliance Specification

## ADDED Requirements

### Requirement: Assessment uses exact declared folders

The installed skill MUST accept exactly the recursive read-only
`policy-catalog`, `actor`, `event`, `phase`, `case-record`, and
`assessment-scope` roles, no target, disabled internet, and one explicit output
folder. Temporary work MUST remain under `<output-folder>/temp/`.

#### Scenario: Complete offline assessment is supplied

- **WHEN** the trusted host validates the exact roles and enforceable isolation
- **THEN** assessment uses only selected ordinary files and YAML within those
  folders

### Requirement: Catalog and case-source bytes are strictly bound

The assessor MUST validate the catalog result, selected requirement IDs, source
hashes, and every selected case-source YAML, adjacent ordinary file, relative
path, and SHA-256 before assessment.

#### Scenario: Selected evidence bytes changed

- **WHEN** an ordinary case-record file no longer matches its documented SHA-256
- **THEN** assessment fails before producing a finding from that evidence

### Requirement: Each actor and phase is assessed separately

Each assessment MUST preserve one requirement, one actor, one event, and one
event-or-phase unit with policy and event dates, source references, missing
predicates, conflicts, explanation, review state, and input fingerprints.

#### Scenario: Two actors appear in one event phase

- **WHEN** the same requirement may apply differently to two actors
- **THEN** the assessor returns separate records rather than one collective
  finding

### Requirement: Status combinations preserve uncertainty

Applicability MUST be `applies`, `not_applicable`, or `uncertain`; violation
MUST be `yes`, `likely`, `unlikely`, `no`, or `indeterminate`; and evidence MUST
be `complete`, `incomplete`, `disputed`, or `unavailable`. Missing, incomplete,
disputed, unavailable, or silent evidence MUST NOT become `no`.

#### Scenario: Record lacks affirmative nonviolation evidence

- **WHEN** available material does not show a violation but is incomplete
- **THEN** violation is `indeterminate`, not `no`

### Requirement: Assessment output remains non-liability analysis

The assessor MUST return deterministic assessment YAML, gap YAML, Markdown, and
domain validation bytes for trusted-host publication. It MUST NOT decide
constitutional or Monell liability, negligence, admissibility, litigation
strategy, allegations, or filing readiness.

#### Scenario: Assessment validates

- **WHEN** every proposed assessment and gap passes the domain contract
- **THEN** the trusted host may publish the artifacts without treating them as a
  legal conclusion
