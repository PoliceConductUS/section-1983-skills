# folder-scoped-skill-execution Delta Specification

## ADDED Requirements

### Requirement: Durable writes use the shared output boundary

An artifact-producing public skill MUST route durable writes through the shared
output writer bound to its validated invocation. A skill MUST NOT treat a path,
file object, shell command, repository, graph, or external service as alternate
write authority.

#### Scenario: Skill produces an artifact

- **WHEN** a folder-scoped skill needs to persist a report, receipt, or
  regenerable artifact
- **THEN** it writes through the invocation-bound output writer using one
  output-relative path

#### Scenario: Writer is unavailable

- **WHEN** the trusted host cannot provide the shared output writer for an
  artifact-producing invocation
- **THEN** the skill reports output persistence unavailable and does not write
  through an ambient filesystem path
