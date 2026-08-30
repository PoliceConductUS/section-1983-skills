# deterministic-filing-integrity Delta Specification

## ADDED Requirements

### Requirement: Filing CI preserves limitations-record hard findings

The installed Filing CI complaint checker MUST validate the same
machine-readable limitations-gate contract as the canonical installed complaint
checker. Its packaged limitations schema MUST remain aligned with the canonical
schema. Filing CI MUST preserve every limitations-record hard finding and MUST
leave the filing gate open when the record is missing, malformed, or unresolved.

Filing CI MUST NOT decide fact truth, relation back, tolling, mistake, notice or
service sufficiency, authority fit, strategy, requested relief, or filing
readiness.

#### Scenario: Filing CI receives an unresolved limitations record

- **WHEN** the selected complaint handoff contains an unresolved required
  limitations entry and declares a filing-critical gap
- **THEN** Filing CI preserves the hard finding and leaves its filing gate open

#### Scenario: Installed schemas drift

- **WHEN** the Filing CI copy of the limitations schema differs from the
  canonical complaint-skill schema
- **THEN** repository validation fails before either installed skill is treated
  as complete
