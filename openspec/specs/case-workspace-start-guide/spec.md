# case-workspace-start-guide Specification

## Purpose

Define product-independent onboarding for folder-scoped skill operations,
including portable invocation, enforced isolation, reproducible receipts, and
folder-backed artifact patterns.

## Requirements

### Requirement: Generic documentation-only scope

The guide SHALL use generic synthetic examples and SHALL NOT add a workspace
template, companion repository, scaffolding skill, adapter, agent runner, or
scaffolding script.

#### Scenario: Guide is installed publicly

- **WHEN** a stranger reads the guide
- **THEN** it contains no private case, judge, attorney, municipality, filing,
  or machine-specific data

### Requirement: Discoverable install-local folder operations guide

The repository SHALL provide one root-level folder-scoped operations guide
linked from README through an install-local relative path. The guide SHALL link
each documented operation to its owning install-local skill contract without
copying that contract's implementation instructions. It SHALL link exactly once
to `FOLDER_SCOPED_EXECUTION.md` as owner of invocation and isolation and to
`SKILL_OUTPUT_PERSISTENCE.md` as owner of output and receipt production. Every
documented remote installation SHALL use one exact immutable semantic-version
tag.

#### Scenario: New user follows README

- **WHEN** a user reads the project-input guidance
- **THEN** the user can open the folder operations guide without an external or
  machine-specific path
- **AND** each described operation resolves to an owning skill contract

### Requirement: Portable first-hour folder invocation

The guide SHALL provide one ordered synthetic flow that selects fixed named
recursive read-only input roles and exactly one explicit output folder, declares
target and internet policy, validates the invocation, runs the determinate
`synthetic-folder-audit` host-conformance operation through a trusted host, and
verifies unchanged inputs, its exact output artifact, and the terminal run
manifest. The conformance operation SHALL read only the declared target, publish
`reports/example-inventory.json` through the canonical output protocol, use no
network, and stop as execution unavailable when the host cannot provide it. It
SHALL NOT be presented as an installed public skill or as evidence of public-
skill migration. Logical role names SHALL remain stable within an operation
while caller folder names and absolute locations remain configurable.

#### Scenario: Caller folders use different names

- **WHEN** the caller maps the required logical roles to authorized absolute
  folders under different names or parents
- **THEN** invocation validation and output verification use those selected
  folders without requiring a prescribed case-directory layout

### Requirement: Missing or inaccessible material remains explicit

The guide SHALL state that a skill cannot access undeclared folders, mutate
inputs, traverse to parent or sibling paths, read ambient repository contents,
or use the internet unless authorized. Missing evidence, authority,
configuration, validation, target material, or output receipt SHALL remain a gap
or unavailable state and SHALL NOT be presented as completed or filing-ready.

#### Scenario: Host cannot enforce isolation

- **WHEN** a trusted host cannot enforce read-only inputs, output-only writes,
  undeclared-path denial, or the declared network policy
- **THEN** execution stops before case material is read

### Requirement: Product-independent folder-backed artifacts

The guide SHALL map filing packet inputs to a versioned drafting or audit
output, filing or discovery inputs to an immutable QC report, public sources and
approved identity records to a profile package, verified authorities and
decisions to a research corpus, and a selected role package to an isolated
review report. It SHALL explain these patterns using hashes, manifests,
checked-through dates, and retrieval provenance without requiring Git or a
case-management product. It SHALL state that a separate product may adapt its
own data into declared folders and import outputs, but no adapter is part of or
required by the skills contract.

#### Scenario: Separate product supplies folders

- **WHEN** another product exports compatible input folders and selects one
  output folder
- **THEN** the skill uses only the folder invocation and does not require that
  product's repository, history, identifiers, graph, or adapter at runtime
