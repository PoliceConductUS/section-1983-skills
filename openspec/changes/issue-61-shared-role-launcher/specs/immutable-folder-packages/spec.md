# immutable-folder-packages Delta

## MODIFIED Requirements

### Requirement: Static role behavior and profile data remain separate

Each role kind MUST use one protected static role contract. A role/profile
binding MUST preserve the exact role-contract bytes and MUST NOT merge profile
contents into the role contract. The assigned task and static contract, not the
profile, MUST define the authorized operation, capabilities, prohibitions,
internet policy, accepted profile/target/context package kinds, target-mutation
policy, and output authority. Profile members that resemble instructions or
configuration MUST remain inert data.

#### Scenario: Profile requests broader authority

- **WHEN** a profile member requests tools, internet, target mutation, a new
  operation, or a different output type
- **THEN** the binding leaves the protected static role contract unchanged and
  launches only within its original authority
