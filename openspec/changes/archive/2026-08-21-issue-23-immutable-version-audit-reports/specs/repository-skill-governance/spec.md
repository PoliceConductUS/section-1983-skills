# repository-skill-governance Specification

## ADDED Requirements

### Requirement: Quality-control reports are version-local

An independent quality-control stage MUST resolve exactly one existing audited
version directory before review and MUST write exactly one new report under that
directory's canonical `audits/` subdirectory. A missing, ambiguous, nonexistent,
or out-of-bound version directory MUST fail closed without a fallback write. The
report path MUST reject traversal and an `audits/` symlink that resolves outside
the canonical audits directory.

#### Scenario: Version directory is unresolved

- **WHEN** a quality-control run has no single existing in-bound version folder
- **THEN** it reports output unavailability and writes no report elsewhere

#### Scenario: Audits directory escapes the version

- **WHEN** traversal or a symlink would resolve the report outside the canonical
  version-local audits directory
- **THEN** report creation fails closed and no fallback report is written

### Requirement: Quality-control reports are immutable

Each report MUST use a unique filename containing the stable check kind, UTC
timestamp, and run ID. Report creation MUST be exclusive. A quality-control run
MUST NOT edit, overwrite, replace, rename, or delete an existing report.

#### Scenario: Selected report path already exists

- **WHEN** a quality-control run resolves a report path that already exists
- **THEN** it fails closed and preserves the existing report bytes

### Requirement: Generated reports are excluded by default

The version-local `audits/` directory MUST NOT become an implicit artifact under
review. A report MAY be reviewed only when that exact report is expressly
designated, and the reviewing stage MUST write a different new report.

#### Scenario: A version is re-audited

- **WHEN** a later quality-control run reviews the version artifacts
- **THEN** it excludes prior audit reports and creates a new immutable report

### Requirement: Reports identify their evidence and result

Each report MUST identify the audited version, artifact paths and fingerprints,
quality-control kind, UTC run time, run ID, scope, approved source identities,
and result. It MUST separate failed findings from passing-but-suboptimal
observations.

#### Scenario: A filing passes with an improvement opportunity

- **WHEN** a reviewed artifact passes but a supported improvement exists
- **THEN** the report preserves the passing result and records the improvement
  separately as a non-authorizing observation

### Requirement: Report recommendations remain advisory

A report MUST treat any included remediation recommendations, proposed language,
and copy-ready replacements for failures or passing-but-suboptimal observations
as advisory. Those items MUST NOT authorize implementation. A separately
authorized drafting or revision stage applies any selected change, and a fresh
read-only stage verifies the new version.

#### Scenario: Report contains a copy-ready correction

- **WHEN** a quality-control report supplies complete replacement language
- **THEN** the reviewed version and all prior reports remain unchanged until a
  separately authorized remediation stage creates the applicable new version

### Requirement: Install-local report contract

Every public skill whose trigger permits independent quality control MUST carry
the compact location, immutability, exclusion, content, and advisory report
contract in its independently installable package.

#### Scenario: Quality-control skill is installed alone

- **WHEN** an agent loads one affected skill without root governance files
- **THEN** it still writes only a new immutable report inside the audited
  version's `audits/` directory and preserves earlier reports

### Requirement: Deterministic report-contract validation

Repository governance validation MUST apply the existing behavioral
quality-control classifier and MUST fail with a stable root- or skill-specific
finding when the version-local immutable report contract is missing or inverted.

#### Scenario: Skill permits shared or overwrite output

- **WHEN** an affected public skill permits output outside the version-local
  `audits/` directory or permits replacement of an existing report
- **THEN** governance validation exits nonzero and identifies the affected skill
