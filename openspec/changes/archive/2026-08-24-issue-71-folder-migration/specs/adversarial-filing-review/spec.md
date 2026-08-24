# adversarial-filing-review Delta Specification

## RENAMED Requirements

- FROM: `### Requirement: Immutable execution report`
- TO: `### Requirement: Host-published immutable execution report`

## MODIFIED Requirements

### Requirement: Independent review packet

The adversarial-review processor SHALL accept the required canonical relative
filing target within the declared `filing` role root and approved sources only
from the declared `approved-sources` role root. It SHALL validate and embed the
exact target and source bytes, stable identities, roles, and SHA-256
fingerprints in a bounded packet before dispatch. Paths and URLs MUST NOT appear
in the provider packet. The reviewer capability set MUST exclude filesystem,
repository, browser, tool, storage, and conversation access. Missing,
out-of-role, malformed, or fingerprint-mismatched content MUST produce a scoped
gap before dispatch without an undeclared or internet-sourced substitute.

#### Scenario: Declared source is missing

- **WHEN** an approved source target is absent from `approved-sources` or its
  bytes do not match its fingerprint
- **THEN** processing reports a scoped source gap before provider dispatch and
  does not read another folder

### Requirement: Host-published immutable execution report

The input-confined processor SHALL return one canonical output-relative report
path, deterministic report bytes, and validated internet-source records. It MUST
NOT accept a project, version, artifact, or output-root path; open an output
folder; write a report; create a receipt; or mutate any declared input. Only the
trusted host MAY publish the returned result append-immutably through
`OutputRun`. The report SHALL preserve the runtime type, explicit model, local
run identity, document family, packet and artifact fingerprints, source
identities, time, outcome, and stable failure class without credentials or
provider-session continuation state.

#### Scenario: Completed review is returned

- **WHEN** the trusted runtime returns a valid categorized review
- **THEN** the processor returns one complete report plan and only the trusted
  host may publish it append-immutably

#### Scenario: Review is unavailable

- **WHEN** the provider cannot complete a valid review
- **THEN** the processor returns an honest bounded unavailable result without
  writing, synthesizing findings, or labeling the review complete
