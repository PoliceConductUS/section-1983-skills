# repository-skill-governance Delta

## ADDED Requirements

### Requirement: Participant profiles remain data rather than skills

The repository MUST keep judge-, attorney-, team-, court-, source-class-, and
assumption-specific information in validated immutable folder packages. It MUST
NOT publish real-participant skills, generate person-specific skills, or permit
profile package data to alter a protected static role contract.

#### Scenario: Maintainer adds a new participant profile

- **WHEN** the profile is intended for an agent simulating that participant's
  litigation role
- **THEN** the maintainer adds or regenerates a validated package while the
  reusable behavioral skill and static role contract remain unchanged
