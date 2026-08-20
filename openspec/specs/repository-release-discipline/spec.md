# repository-release-discipline Specification

## Purpose

TBD - created by archiving change issue-16-versioned-releases. Update Purpose
after archive.

## Requirements

### Requirement: Immutable tagged release identity

Every published repository version MUST be identified by one immutable
semantic-version tag in `vMAJOR.MINOR.PATCH` form. A push or merge to `main`
MUST NOT constitute publication, and the repository MUST NOT use a stable branch
or another movable ref as a release identity. An existing release tag MUST NOT
be moved or reused; a correction SHALL receive a new version.

#### Scenario: Change reaches main

- **WHEN** a reviewed feature stack is merged to `main`
- **THEN** the commit remains unreleased until the release workflow validates
  and tags that exact commit

#### Scenario: Released version needs correction

- **WHEN** a defect is found after a release tag exists
- **THEN** maintainers preserve the existing tag and publish the correction
  under a new semantic version

### Requirement: Validation precedes tag creation

The repository MUST provide a manually dispatched release workflow that runs
only from `main`, rejects malformed or existing version tags, installs locked
dependencies, and runs the complete repository validation command before any tag
or GitHub release is created. The workflow SHALL create an annotated tag for the
validated commit and generated release notes only after validation succeeds. It
MUST NOT use a tag-push trigger as the release gate.

#### Scenario: Validation fails

- **WHEN** any repository validation command fails during a release run
- **THEN** the workflow exits before creating or pushing a tag

#### Scenario: Version tag already exists

- **WHEN** a maintainer dispatches a release using an existing remote tag
- **THEN** the workflow rejects the request without moving or replacing the tag

#### Scenario: Workflow runs from a feature branch

- **WHEN** the release workflow is dispatched from a ref other than `main`
- **THEN** the job rejects the run before publication

### Requirement: Pinned consumer installation

Every documented remote skills installation MUST identify one exact immutable
semantic-version tag. The README SHALL explain how to choose the published tag
and how to upgrade deliberately by reinstalling from a different tagged source.
It MUST NOT describe generic default-branch installation or `skills update` as
equivalent to selecting a released version.

#### Scenario: Consumer installs a release

- **WHEN** a consumer follows a README installation command
- **THEN** the skills CLI resolves a GitHub tree URL containing one exact
  semantic-version tag

#### Scenario: Consumer upgrades

- **WHEN** a consumer chooses a newer published version
- **THEN** the consumer replaces the pinned tag and reruns the install command
  rather than silently following a moving branch
