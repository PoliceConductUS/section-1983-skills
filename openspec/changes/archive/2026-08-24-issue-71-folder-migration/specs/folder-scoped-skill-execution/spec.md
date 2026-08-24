# folder-scoped-skill-execution Delta Specification

## ADDED Requirements

### Requirement: Invocation conforms to the installed skill contract

Before root resolution, the trusted host MUST load the selected installed
skill's strict `references/folder-contract.json` and verify that the invocation
uses the same skill name, exact ordered input-role set, target policy and role,
internet policy, and `append-immutable` output mode. Contract validation MUST
NOT read case material, infer a role, merge roles from composed skills, or
invent a missing target.

#### Scenario: Invocation adds a convenient source folder

- **WHEN** an invocation contains an input role not listed in the selected
  skill's install-local contract
- **THEN** validation fails before any root is traversed or input manifest is
  created

### Requirement: Host enforcement and skill processing remain separate

The trusted host SHALL retain ownership of root descriptors, filesystem and
network enforcement, logical input manifests, and output-run publication. A
skill or helper MAY receive validated role-bound input access, canonical
relative targets, and in-memory data. It MUST NOT receive ambient filesystem
authority or an output-root path. The folder protocol MUST NOT require a
universal runner or duplicated persistence manager.

#### Scenario: Helper completes deterministic processing

- **WHEN** the helper returns an output-relative artifact plan
- **THEN** the trusted host independently validates and publishes the plan
  through the canonical output boundary
