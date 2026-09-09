## ADDED Requirements

### Requirement: Filing CI contributes only deterministic validation signals

Filing CI MUST expose applicable deterministic findings and artifact freshness
signals to the shared post-draft workflow. It MUST NOT decide whether evidence
substantively supports an assertion, whether authority supports a legal
proposition, whether a document is legally sufficient, or whether a semantic
validation finding is closed.

#### Scenario: Every deterministic checker passes

- **WHEN** Filing CI reports no mechanical defect but substantive assertion
  validation remains incomplete
- **THEN** the document remains validation-incomplete and Filing CI does not
  upgrade the semantic result
