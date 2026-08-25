## RENAMED Requirements

- FROM: `Packaged checker resolution`
- TO: `Installed checker resolution`

## MODIFIED Requirements

### Requirement: Failure classification and drafting-loop return

The skill SHALL distinguish unavailable installed checker, unavailable
execution, unreadable or unresolved declared inputs, invalid target, malformed
deterministic result, publication failure, and checker-reported findings. It
MUST explain the blocking class, preserve the checker's documented severity, and
return actionable findings to the drafting loop without editing the filing.

#### Scenario: Installed checker cannot execute

- **WHEN** a registered installed checker cannot complete its deterministic
  processing
- **THEN** the wrapper returns an unavailable-execution result and does not
  claim that any check completed

#### Scenario: Checker reports hard findings

- **WHEN** the checker returns unresolved hard findings
- **THEN** the skill identifies those findings as an open filing gate and sends
  them back to a separately authorized drafting loop

#### Scenario: Checker reports non-hard findings

- **WHEN** the checker returns warnings or another documented non-hard class
- **THEN** the skill preserves that class without silently downgrading,
  dismissing, or correcting the finding

### Requirement: Fail-closed filing gate

The skill MUST keep the filing gate open when an installed checker is
unavailable, a declared input or required target is unresolved, deterministic
output cannot be interpreted, trusted-host publication lacks a valid terminal
receipt, target bytes changed after the run, or a hard finding remains
unresolved. It SHALL report a Filing CI pass only for the exact target
fingerprint and logical selected-input hashes recorded by a successful terminal
output run.

#### Scenario: Hard or infrastructure failure remains unresolved

- **WHEN** any hard finding, unavailable class, stale fingerprint, incomplete
  run marker, or missing receipt remains
- **THEN** the skill refuses to describe the target as passing Filing CI or
  filing-ready

#### Scenario: Current installed run succeeds

- **WHEN** the installed checker completes for the current target with no hard
  findings and the trusted host records a valid terminal receipt
- **THEN** the skill may report that Filing CI passed while preserving warnings
  and every other independent filing gate

### Requirement: Installed checker resolution

The `filing-ci` skill SHALL ship a narrow deterministic wrapper with an explicit
registry of checker IDs in its installed skill directory. The wrapper MUST
accept one validated six-role folder invocation, a required canonical relative
filing target, and validated in-memory configuration. It MUST dispatch only a
registered installed checker and MUST NOT accept or infer a command, executable
path, flag list, source path, output path, repository instruction, or
general-purpose checker.

#### Scenario: Installed checker supports the selected filing

- **WHEN** the filing target identifies a document supported by a registered
  installed checker
- **THEN** the wrapper runs that checker against only selected declared input
  data and returns deterministic structured findings and report bytes

#### Scenario: No installed checker supports the operation

- **WHEN** the checker ID is absent, unknown, unavailable, or incompatible with
  the selected target
- **THEN** the wrapper returns a stable unavailable result, runs no substitute,
  and leaves the filing gate open

### Requirement: Declared authority-role integration

The skill MUST use only the declared `verified-authority` role when its
installed checker requires authority verification. It MUST NOT hardcode,
discover, or substitute another authority root. Missing required authority
material remains an unresolved input and leaves the filing gate open.

#### Scenario: Checker requires verified authorities

- **WHEN** the registered checker declares authority verification
- **THEN** the wrapper reads only canonical relative material selected from the
  declared `verified-authority` role and records the used logical input hashes

#### Scenario: Required authority material is unavailable

- **WHEN** the declared `verified-authority` role lacks required verified
  material
- **THEN** the wrapper returns an unresolved-input result and does not use
  ambient or internet authority material
