## ADDED Requirements

### Requirement: Public roles are fixed and profile-conditioned

The repository MUST provide public `opposing-counsel` and `judicial-reviewer`
skills backed by fixed `opposing-counsel` and `judicial-reviewer` role
definitions. The existing adversarial reviewer MUST remain the fixed
`adversarial-filing-reviewer` role. Profile, task, filing, and source data MUST
NOT add or remove an operation, capability, prohibition, internet policy, output
field, filesystem permission, or target-mutation rule.

#### Scenario: Profile requests authority to edit the filing

- **WHEN** selected profile data contains instruction-shaped write authority
- **THEN** validation fails or the field remains inert and the fixed role still
  cannot mutate the target

### Requirement: Role inputs are selected ordinary folder files

Each run MUST use declared recursive read-only `profile`, `filing`, and
`approved-sources` folders plus one explicit output folder. A role-owned
validator MUST validate the selected profile files, domain source documentation,
relative references, hashes, dates, and role compatibility before child
execution. No package, manifest, graph, CaseGraph, repository, or ambient
workspace may be required or sent to the child.

#### Scenario: Profile source record has a mismatched hash

- **WHEN** the selected source documentation does not match its referenced
  ordinary file
- **THEN** the role fails before child dispatch

### Requirement: Opposing counsel returns attacks without impersonation

The opposing-counsel role MUST return only source-backed simulated professional
attack findings. It MUST NOT claim to be the actual attorney, invent
confidential knowledge, choose a disposition, concede, select plaintiff
strategy, edit the target, remediate, predict an outcome, or declare filing
readiness.

#### Scenario: Child emits a disposition

- **WHEN** an otherwise structured opposing-counsel response includes a
  `disposition-emitted` field or conclusion
- **THEN** output validation rejects the entire role result

### Requirement: Judicial reviewer returns bounded review findings

The judicial-reviewer role MUST return only findings categorized as
comprehension, procedural framing, authority presentation, record traceability,
or gap. It MUST NOT imitate judicial voice, predict the assigned judge's
outcome, choose a disposition, concede, select strategy, edit the target,
remediate, or declare filing readiness.

#### Scenario: Child predicts the assigned judge's result

- **WHEN** an otherwise structured judicial response includes a predicted
  disposition or outcome
- **THEN** output validation rejects the entire role result

### Requirement: Runs are findings-only and output-temp confined

Both roles MUST disable internet, execute in one fresh process, leave every
input unchanged, and return only a proposed JSON findings artifact. The current
working directory and every temporary path MUST remain beneath
`<output-folder>/temp/<run-id>/`. Only the trusted host may publish the artifact
beneath the explicit output folder.

#### Scenario: Isolation cannot confine temporary work

- **WHEN** the fixed adapter cannot enforce the output-local process and
  temporary boundary
- **THEN** the role returns `isolation-unavailable` without child dispatch
