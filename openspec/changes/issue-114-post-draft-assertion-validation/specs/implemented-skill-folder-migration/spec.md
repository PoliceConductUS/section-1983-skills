## ADDED Requirements

### Requirement: Assertion validation has a fixed folder contract

`validating-court-facing-assertions` MUST declare ordered required input roles
`filing`, `record`, `authorities`, and `strategy`; optional input role
`prior-reports`; one required target in `filing`; disabled internet; and append-
immutable output.

#### Scenario: Validation invocation receives an undeclared folder

- **WHEN** the invocation attempts to add an undeclared source, graph,
  repository, or ambient workspace role
- **THEN** folder-contract validation fails before case material is reviewed or
  a report is published
