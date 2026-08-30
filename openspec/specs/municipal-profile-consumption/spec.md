# municipal-profile-consumption Specification

## Purpose

Define how named Section 1983 consumers optionally use validated municipal
profile folders while preserving ordinary file inputs, existing non-profile
behavior, explicit output roots, and evidence-bounded legal judgment.

## Requirements

### Requirement: Applicable consumers declare the profile folder

Each applicable consumer MUST declare exactly one optional recursive read-only
`municipal-profile` role while retaining its existing required roles, target
policy, and internet policy. The applicable consumers are complaint, city Rule
12, written-discovery, deposition-outline, and adversarial-review skills. A task
that requests profile use MUST supply the role and pass validation; omission
preserves only the consumer's existing non-profile behavior.

#### Scenario: A consumer is invoked with the exact roles

- **WHEN** the trusted host validates the skill's required roles and supplied
  optional profile role
- **THEN** the consumer may inspect the ordinary municipal-profile files without
  acquiring access to any undeclared path

### Requirement: Profile validation fails closed

Each consumer MUST validate the four Issue #31 files, version, passing result,
identity, checked-through date, hashes, folder fingerprint, and exact linked
record IDs before specialized work.

#### Scenario: Profile data is missing or inconsistent

- **WHEN** a required file, hash, ID, date, or passing result is absent, stale,
  changed, or inconsistent
- **THEN** the consumer returns a visible bounded failure and no specialized
  drafting or review artifact

### Requirement: Consumer uses remain bounded

Consumers MUST use the profile only for their named theory map, motion-attack
map, gap-directed discovery, gap-directed examination, or independent attack.
They MUST NOT turn the profile into proof, law, an assumed fact, an automatic
Monell element, or a selected litigation strategy.

#### Scenario: Profile contains a favorable institutional record

- **WHEN** the consumer encounters favorable evidence without complete record
  and authority support
- **THEN** it preserves the evidence, counterevidence, limitation, and gap
  without declaring the corresponding element complete

### Requirement: Inputs remain unchanged and output remains explicit

Each consumer MUST preserve every input byte, write durable output only beneath
the caller-declared output folder, and confine temporary work to
`<output-folder>/temp/`.

#### Scenario: A prior output is needed for a later audit

- **WHEN** a fresh audit needs a prior proposed artifact
- **THEN** the caller supplies the prior output folder as a declared read-only
  input to a new invocation
