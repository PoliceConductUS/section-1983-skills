# static-role-launcher Delta

## ADDED Requirements

### Requirement: Trusted host binds one protected role to immutable packages

The repository SHALL provide one trusted launcher that binds a protected static
role contract to one validated profile package, one validated target package,
exact declared context packages, an authorized operation, a bounded task, and
one explicit output folder. Every package and role compatibility rule MUST pass
before child dispatch. Profile, target, context, task, and child data MUST NOT
alter role behavior or select executable process configuration.

#### Scenario: Profile contains behavior-shaped fields

- **WHEN** a valid immutable profile member contains capabilities, commands, or
  instruction-shaped data
- **THEN** the child request preserves those bytes only as profile data and the
  protected role contract remains unchanged

### Requirement: Child execution is fresh, isolated, and path-free

Each launch MUST use one fresh process with scrubbed session state, no
undeclared filesystem access, and only the static role's internet and capability
policy. The child MUST receive canonical request bytes rather than filesystem
paths. Its empty working directory and `TMPDIR`, `TMP`, and `TEMP` MUST all be
inside the selected `<output-folder>/temp/<run-id>/` tree. Unavailable isolation
or capability enforcement MUST fail before dispatch.

#### Scenario: Adapter cannot deny undeclared paths

- **WHEN** the trusted adapter cannot attest to the required filesystem boundary
- **THEN** the launcher returns `isolation-unavailable` without starting a child

### Requirement: Process and protocol failures are bounded

The launcher MUST convert timeout, nonzero exit, oversized standard streams,
invalid UTF-8, malformed JSON, unsupported output, or adapter failure into a
stable bounded failure report without traceback, credentials, local paths, case
excerpts, or fabricated findings.

#### Scenario: Child prints malformed output and a case path

- **WHEN** standard output is not valid UTF-8 JSON and standard error contains a
  local path
- **THEN** the returned failure identifies only the stable protocol class and
  contains neither raw stream nor path

### Requirement: Output is advisory and inputs remain immutable

The role-specific validator MUST accept only the static role's exact advisory
output schema and return proposed canonical output-relative artifacts. Only the
trusted host may publish beneath the explicit output folder. The launcher MUST
verify that profile, target, context, and public-reference bytes remain
unchanged; any mutation fails the run.

#### Scenario: Child attempts to change the target

- **WHEN** target bytes differ after execution or output requests a target path
- **THEN** the run fails without a completed advisory result or target rewrite
