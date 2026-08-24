# folder-scoped-skill-execution Specification

## Purpose

Define folder-native public skill invocation, canonical path confinement,
deterministic logical input manifests, and the boundary between conformance
validation and trusted-host filesystem and network enforcement.

## Requirements

### Requirement: Explicit folder-native invocation

Every public skill invocation MUST declare a fixed set of named absolute input
folders, exactly one absolute output folder, bounded runtime limits, and an
internet policy of `disabled` or `authorized`. It MAY select one target by input
role and relative path. The invocation MUST NOT require CaseGraph, CaseHome,
Git, resource identifiers, graph traversal, repository history, or an external
persistence service.

#### Scenario: Complete invocation is supplied

- **WHEN** a trusted host supplies valid named input folders, one output folder,
  runtime limits, internet policy, and its isolation declaration
- **THEN** the invocation can be validated without consulting an ambient working
  directory, repository, or external service

#### Scenario: Required invocation state is unavailable

- **WHEN** an input, output, runtime field, internet policy, or host isolation
  declaration is missing or invalid
- **THEN** validation fails with a stable bounded result before case material is
  read

### Requirement: Canonical path confinement

The invocation validator MUST canonicalize every declared root before semantic
work. It MUST reject missing or non-directory roots, duplicate input role names,
an output contained by an input, an input contained by the output, absolute
child paths, parent traversal, and any child or symlink resolution outside its
declared root.

#### Scenario: Roots are separate and valid

- **WHEN** all declared roots resolve to existing directories and no input and
  output contain one another
- **THEN** validation returns canonical roots for bounded host use

#### Scenario: A path escapes its role

- **WHEN** a target, input child, output child, or symlink resolves outside its
  declared root
- **THEN** validation fails before the escaped path is read or written

### Requirement: Logical input manifest

The validator MUST produce a deterministic logical manifest for every declared
input role. Each regular file entry MUST contain its slash-separated relative
path, byte size, and lowercase SHA-256 hash. The persisted manifest MUST NOT
contain an absolute source path.

#### Scenario: Equivalent inputs live at different machine paths

- **WHEN** two invocations use the same role names, relative file paths, and
  bytes under different absolute roots
- **THEN** their logical input manifests are identical

#### Scenario: Input tree contains an escaping symlink

- **WHEN** manifest traversal encounters a symlink whose target is outside the
  declared input root
- **THEN** manifest construction fails and does not include external bytes

### Requirement: Trusted host enforcement

Every public skill MUST treat declared inputs as recursively read-only, the
declared output as its only writable folder, undeclared filesystem paths as
unavailable, and internet access as unavailable unless its own contract
expressly authorizes it. If the host cannot enforce those filesystem and network
capabilities, the skill MUST stop before reading case material. Prompt
instructions alone MUST NOT be represented as enforcement.

#### Scenario: Host establishes the boundary

- **WHEN** the trusted host provides read-only input mounts, one writable output
  mount, no undeclared filesystem access, and the declared network policy
- **THEN** the skill may process only the declared invocation

#### Scenario: Host cannot establish the boundary

- **WHEN** the host cannot deny input mutation, undeclared filesystem access, or
  unauthorized internet access
- **THEN** the skill reports the execution boundary unavailable and performs no
  case-material work
