# folder-scoped-skill-execution Delta

## MODIFIED Requirements

### Requirement: Invocation conforms to the installed skill contract

Before root resolution, the trusted host MUST load the selected installed
skill's strict `references/folder-contract.json` and verify that the invocation
uses the same skill name, exact ordered input-role set, target policy and role,
an expressly allowed internet policy, and the declared output mode. A contract
MAY declare either one exact internet-policy string or, for a multi-operation
skill, a nonempty unique array containing every and only permitted invocation
policies. Each invocation MUST still declare exactly one internet policy.
Contract validation MUST NOT read case material, infer a role, merge roles from
composed skills, or invent a missing target.

#### Scenario: One skill has acquisition and compilation operations

- **WHEN** its contract permits `authorized` and `disabled` internet policies
- **THEN** an authorized acquisition invocation and a disabled compilation
  invocation each validate independently
- **AND** any other internet policy fails before input traversal
