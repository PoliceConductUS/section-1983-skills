# repository-skill-governance Delta Specification

## RENAMED Requirements

- FROM: `### Requirement: Quality-control reports are version-local`
- TO: `### Requirement: Quality-control reports use explicit output`

## MODIFIED Requirements

### Requirement: Quality-control reports use explicit output

An independent quality-control stage MUST select exactly one artifact through
its declared input roles and target policy and MUST propose exactly one unique
append-immutable output-relative report beneath the caller-declared output
folder. A missing, ambiguous, nonexistent, or out-of-role target MUST fail
closed without a fallback write. The report path MUST reject absolute paths,
traversal, symlink escapes, and existing destinations. Only the trusted host MAY
publish the report through the shared output boundary.

#### Scenario: Quality-control target is unresolved

- **WHEN** a quality-control run has no single valid target required by its
  install-local folder contract
- **THEN** it reports output unavailability and the trusted host publishes no
  completed report

#### Scenario: Proposed report escapes output

- **WHEN** a helper returns an absolute, traversing, escaping, or colliding
  output-relative report path
- **THEN** publication fails closed and every existing input and output byte is
  preserved

### Requirement: Generated reports are excluded by default

Prior quality-control reports MUST NOT become implicit input. A report MAY be
reviewed only when that exact report is expressly present in a declared input
role and selected consistently with the reviewing skill's target policy. The
reviewing stage MUST propose a different new append-immutable report for trusted
host publication.

#### Scenario: An output folder contains earlier reports

- **WHEN** a later quality-control run begins
- **THEN** those outputs remain unavailable as input unless the caller declares
  them under an authorized input role in a separate invocation

### Requirement: Install-local report contract

Every public skill whose trigger permits independent quality control MUST carry
the compact non-mutation, target, append-immutable report, input exclusion,
content, receipt, and advisory-remediation contract in its independently
installable package. It MUST identify its exact
`references/folder-contract.json` without copying the full shared persistence
protocol.

#### Scenario: Quality-control skill is installed alone

- **WHEN** an agent loads one affected skill without root governance files
- **THEN** the package still selects only a declared target, returns one new
  output-relative report, preserves every input and prior output, and leaves
  publication to the trusted host

### Requirement: Deterministic report-contract validation

Repository governance validation MUST apply the behavioral quality-control
classifier and MUST fail with a stable root- or skill-specific finding when the
explicit-output immutable report contract is missing or inverted. It MUST reject
project-boundary, version-folder, implicit `audits/`, fallback output, direct
helper write, and overwrite permissions in current public contracts.

#### Scenario: Skill permits project-shaped or direct output

- **WHEN** an affected skill permits a report outside the trusted host's
  caller-declared output boundary or permits replacement of an existing report
- **THEN** governance validation exits nonzero and identifies the affected skill

### Requirement: Independently installable folder boundary

Every public `SKILL.md` MUST link to a schema-valid install-local
`references/folder-contract.json` that states the exact ordered input roles,
target policy and roles, internet policy, and `append-immutable` output mode.
The skill MUST also carry the compact recursive input-read-only, output-only,
internet, and host-enforcement boundary. The full protocol SHALL remain in the
repository's canonical execution owner and MUST NOT be copied into every skill.

#### Scenario: Skill is installed alone

- **WHEN** an agent loads one public skill without repository-root governance
  files
- **THEN** the package still exposes its complete exact invocation authority and
  preserves the compact enforcement boundary

### Requirement: Deterministic folder-contract validation

Repository governance validation MUST inspect every public skill package and
fail with a stable skill-specific finding when its folder contract is missing,
unreadable, malformed, noncanonical, mismatched to the public skill name, or
different from the approved role/target/internet/output matrix. Deterministic
validation MUST NOT claim to prove host isolation or subjective agent behavior.

#### Scenario: Public skill changes one role or policy

- **WHEN** a public contract adds, removes, duplicates, reorders, or renames a
  role or changes its target, internet, or output policy
- **THEN** repository validation exits nonzero and identifies that skill before
  any invocation uses the broadened authority

## ADDED Requirements

### Requirement: Standalone helper ownership is deterministic

Repository governance validation MUST identify every helper named by a public
folder contract and verify that the file exists inside that skill package. A
helper MUST NOT import repository-root validator/writer modules, accept an
output-root argument, perform arbitrary command dispatch, or directly create an
output artifact or receipt.

#### Scenario: Installed helper depends on repository root

- **WHEN** a helper imports or references a required executable outside its
  isolated skill package
- **THEN** governance validation fails with a stable skill-specific helper
  ownership finding
