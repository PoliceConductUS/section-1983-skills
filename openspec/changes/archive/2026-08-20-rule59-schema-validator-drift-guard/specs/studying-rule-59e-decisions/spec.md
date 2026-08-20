## ADDED Requirements

### Requirement: Automatic schema-validator alignment guard

The repository test suite MUST compare every public Rule 59 schema required
field set and controlled enum with the corresponding validator constant. The
guard SHALL fail when either side adds, removes, or changes a mapped field or
value without the other side and SHALL inventory the schemas so an unmapped
required-field or enum node also fails. Semantic and cross-field behavior MUST
remain covered by the real validator CLI and synthetic fixture tests.

#### Scenario: Required field drifts

- **WHEN** a required field exists in a mapped schema object but not in the
  corresponding validator required-field constant, or vice versa
- **THEN** the alignment test fails and identifies the contract plus the
  one-sided field

#### Scenario: Controlled value drifts

- **WHEN** an enum value exists in a mapped schema node but not in the
  corresponding validator allowed-value constant, or vice versa
- **THEN** the alignment test fails and identifies the contract plus the
  one-sided value

#### Scenario: Schema contract node is not mapped

- **WHEN** a public schema contains a required-field or enum node absent from
  the alignment inventory
- **THEN** the alignment test fails instead of silently omitting that node

#### Scenario: Semantic validator behavior changes

- **WHEN** validator logic changes without changing required fields or enums
- **THEN** the existing real-CLI and fixture tests, not the structural guard,
  remain responsible for accepting or rejecting the behavior
