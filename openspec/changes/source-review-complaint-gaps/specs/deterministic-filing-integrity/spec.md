# deterministic-filing-integrity Delta Specification

## ADDED Requirements

### Requirement: Filing CI preserves privacy-gate hard findings

The installed Filing CI complaint checker MUST validate the same `privacy_gate`
contract as the canonical installed complaint checker, using the same closed
vocabularies and the same three check identifiers. Its packaged checker contract
MUST remain identical to the canonical packaged block. Filing CI MUST preserve
every privacy-gate hard finding and MUST leave the filing gate open when the
gate is missing, malformed, unresolved, or blocked.

Filing CI MUST NOT decide whether an authorization basis satisfies Rule 5.2;
`redaction-authorization` is an excluded judgment.

#### Scenario: Filing CI receives a handoff without a privacy gate

- **WHEN** the selected complaint handoff omits the `privacy_gate` object
- **THEN** Filing CI reports the presence finding and leaves its filing gate open

#### Scenario: Identical documents reach both checkers

- **WHEN** the same handoff is checked by the canonical complaint checker and by
  Filing CI
- **THEN** both report the same privacy-gate check identifiers
