# repository-skill-governance Specification

## ADDED Requirements

### Requirement: Independent quality-control stages are non-mutating

Independent quality-control stages MUST be non-mutating. This includes every
independent audit, verification, review, evaluation, Filing CI run, or
behaviorally equivalent quality-control stage. The stage MAY read designated
artifacts and write its designated report or result. It MUST NOT edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review.

#### Scenario: Combined audit-and-fix request

- **WHEN** a user asks an independent quality-control stage to audit and fix the
  same artifact
- **THEN** the stage preserves the artifact bytes, writes only its report or
  result, and does not treat the combined instruction as remediation authority

#### Scenario: Pressure conflicts with the quality-control boundary

- **WHEN** deadline pressure, sunk cost, claimed prior approval, or a contrary
  workflow instruction directs the independent stage to mutate the artifact
- **THEN** the quality-control boundary controls and the artifact remains
  unchanged

### Requirement: Quality-control recommendations are advisory

Quality-control output MUST remain advisory. Recommendations, proposed language,
corrections, and copy-ready replacements from an independent quality-control
stage MUST NOT authorize implementation.

#### Scenario: Report supplies copy-ready replacement text

- **WHEN** an independent report contains complete replacement language
- **THEN** the reviewed artifact remains unchanged until a separately authorized
  drafting or revision stage applies a selected correction

### Requirement: Remediation and re-verification are separate stages

Remediation MUST occur in a separately authorized drafting or revision stage and
MUST create a new version when repository or project versioning applies. A new
read-only quality-control stage MUST verify the remediated artifact.

#### Scenario: User authorizes remediation after review

- **WHEN** a user separately authorizes a supported correction
- **THEN** the drafting stage creates the applicable new version and a later
  independent quality-control stage assesses that version without modifying it

### Requirement: Authorized drafting self-checks remain distinct

Authorized drafting self-checks MUST remain distinct from independent quality
control. An internal self-check inside an explicitly authorized drafting or
revision stage MAY guide edits within that stage. It MUST NOT be represented as
an independent audit, verification, review, evaluation, or quality-control
result.

#### Scenario: Drafter checks its work while revising

- **WHEN** an authorized drafting stage performs an internal completion check
- **THEN** it may use the result to revise the working artifact but does not
  label that self-check as an independent quality-control stage

### Requirement: Independently installable quality-control contract

Each affected public skill MUST carry the compact contract within its own
installable package. An affected skill is one whose trigger permits an
independent quality-control stage. The compact contract covers non-mutation,
advisory output, separate remediation, versioning, and fresh verification.

#### Scenario: Quality-control skill is installed alone

- **WHEN** an agent loads the skill without repository-root governance files
- **THEN** the skill still prohibits same-stage artifact mutation and routes
  remediation and re-verification to separate stages

### Requirement: Deterministic quality-control contract validation

Repository governance validation MUST identify current public quality-control
entrypoints from their trigger language and fail with a stable skill-specific
finding when the compact contract is absent or inverted. Deterministic
validation MUST NOT claim to prove agent behavior or evaluate subjective prose
quality.

#### Scenario: Audit-capable skill permits same-stage correction

- **WHEN** an affected public skill omits the contract or permits an independent
  audit to edit the reviewed artifact
- **THEN** repository governance validation exits nonzero and identifies the
  affected skill through the stable quality-control contract finding
