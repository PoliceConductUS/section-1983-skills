## ADDED Requirements

### Requirement: Discoverable install-local workspace guide

The repository SHALL provide a root-level case-workspace starting guide linked
from README through an install-local relative path. Every documented remote
installation SHALL use one exact immutable semantic-version tag.

#### Scenario: New user follows README

- **WHEN** a user reads the project-input guidance
- **THEN** the user can open the case-workspace guide without an external or
  machine-specific path
- **AND** the installation example identifies one exact tagged release

### Requirement: Portable first-hour artifact roles

The guide SHALL cover choosing a workspace root, recording approved source IDs,
adding a source-bounded chronology entry, recording a protected decision,
separating immutable inputs from generated artifacts, and running only available
validation. Each example path SHALL identify its role and SHALL be renameable
when project configuration identifies the equivalent location.

#### Scenario: Project uses different filenames

- **WHEN** a project already stores the required roles under different names
- **THEN** the user keeps those paths and configures or identifies their
  equivalent roles rather than copying the example layout

### Requirement: Missing material remains explicit

The guide SHALL treat missing evidence, authority, configuration, or validation
as a gap or unavailable state and SHALL NOT instruct the user to fabricate a
path, source, fact, decision, authority, or passing result.

#### Scenario: Optional validator is absent

- **WHEN** the project has no configured validation command
- **THEN** the user records validation as unavailable
- **AND** the guide does not present the workspace as validated or filing-ready

### Requirement: Generic documentation-only scope

The guide SHALL use generic synthetic examples and SHALL NOT add a workspace
template, companion repository, scaffolding skill, or scaffolding script.

#### Scenario: Guide is installed publicly

- **WHEN** a stranger reads the guide
- **THEN** it contains no private case material or machine-specific path
