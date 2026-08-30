# drafting-section-1983-complaints Delta Specification

## RENAMED Requirements

- FROM: `### Requirement: Deterministic external-checker handoff`
- TO: `### Requirement: Packaged mechanical complaint check`

## MODIFIED Requirements

### Requirement: Packaged mechanical complaint check

The complaint package SHALL ship a deterministic helper that reads the
install-local `complaint-structure-contract.json`, the declared `filing` input
root, and an optional canonical relative filing target. It SHALL implement only
the contract's section/order, numbering, identifier, tuple/cardinality,
cross-reference, incorporation, and required-field-presence checks. It MUST
return stable finding identifiers, nonzero failure status, one canonical
output-relative mechanical-report path, and deterministic report bytes for
trusted-host publication. It MUST NOT require or invoke an external configured
checker.

#### Scenario: Declared complaint target is checked

- **WHEN** the caller supplies an existing complaint target in the declared
  `filing` role
- **THEN** the packaged helper returns deterministic mechanical findings and the
  trusted host may publish the report append-immutably

#### Scenario: New complaint has no input target

- **WHEN** the operation drafts a new complaint and omits the optional filing
  target
- **THEN** drafting may produce a new output artifact, but a later mechanical
  check must consume that artifact through a new declared-input invocation
  before any check can be reported complete

#### Scenario: Requested check requires legal judgment

- **WHEN** a requested check concerns fact truth, legal sufficiency, authority
  fit, material analogy, strategy, or filing readiness
- **THEN** the packaged contract identifies that question as excluded and does
  not represent it as a mechanical finding

## ADDED Requirements

### Requirement: Complaint helper is install-local and input confined

The mechanical checker MUST ship inside the complaint skill package, work when
that package is installed alone, accept only declared input-root plus canonical
relative target or validated in-memory bytes, and emit deterministic results. It
MUST NOT import root scripts, accept an output root, mutate input, access an
undeclared path, use the internet, create a receipt, or dispatch a command.

#### Scenario: Complaint package is isolated

- **WHEN** the package is copied without repository-root files and supplied a
  valid declared filing root and target
- **THEN** the same mechanical finding bytes are produced without any external
  runtime dependency
