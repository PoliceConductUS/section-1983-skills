## ADDED Requirements

### Requirement: Integrated Monell text receives shared assertion validation

The Monell drafting skill MUST hand its approved-path deltas to the canonical
complaint owner and MUST require the integrated whole-document candidate to use
`validating-court-facing-assertions`. It MUST NOT describe an isolated delta as
whole-document validation or use validation findings to select, narrow, or omit
a Monell path without the plaintiff's decision.

#### Scenario: Monell delta is valid before integration

- **WHEN** an approved-path delta satisfies its local contract but has not been
  integrated into the complaint
- **THEN** the skill reports delta completion without claiming that complaint
  assertions, omissions, or rendered output have been validated
