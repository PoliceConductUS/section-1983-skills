## ADDED Requirements

### Requirement: Complete declarations use shared assertion validation

The declaration skill MUST submit each complete generated declaration as one
filing target to `validating-court-facing-assertions` after every retained
statement has exact human approval. Any changed statement MUST return to pending
human approval before a new validation invocation.

#### Scenario: Source-supported correction changes approved text

- **WHEN** validation identifies a correction and a separate authorized drafting
  stage changes an approved declaration statement
- **THEN** the statement returns to pending, receives new exact human approval,
  and the complete declaration receives a new validation invocation
