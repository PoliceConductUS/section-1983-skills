# repository-skill-governance Delta

## ADDED Requirements

### Requirement: Every quality-control invocation has one primary target

Every public quality-control skill MUST require exactly one primary target
within its approved declared input roles. This applies when its trigger permits
an independent audit, validation, verification, review, evaluation, Filing CI
run, or behaviorally equivalent quality-control stage. Missing, ambiguous,
directory, or out-of-role targets MUST fail closed.

#### Scenario: A QC-capable drafting skill is invoked without a filing target

- **WHEN** an invocation selects the independent quality-control behavior but
  supplies no primary target
- **THEN** the quality-control stage publishes no report and does not choose a
  target from the input tree

#### Scenario: The host receives only a generic validated invocation

- **WHEN** a quality-control publisher receives an invocation that was not bound
  to the installed skill's target policy and approved target roles
- **THEN** it publishes no report and fails closed

### Requirement: Quality-control report metadata is complete and receipt-bound

Every independent quality-control report MUST record the skill and version,
quality-control kind, UTC run time, run ID, filtered logical input roles and
reviewed artifact hashes, primary target role/path/hash/size, scope, result,
failed findings, passing-but-suboptimal recommendations, and the terminal
run-manifest identity. Findings and recommendations remain advisory and MUST NOT
authorize same-stage remediation.

#### Scenario: A passing run has a supported improvement

- **WHEN** a quality-control run passes but identifies a suboptimal choice
- **THEN** its report preserves the passing result, records the recommendation
  separately, and leaves the target bytes unchanged

### Requirement: Generated QC reports are excluded from reviewed fingerprints

The trusted host MUST exclude files beneath the reserved
`quality-control-reports/` output prefix and files identified by the canonical
quality-control metadata envelope from a quality-control run's reviewed-input
manifest unless one exact report is itself the explicit primary target.
Selecting one report MUST NOT implicitly include sibling or older reports.

#### Scenario: A prior report folder is declared as an input role

- **WHEN** a later quality-control invocation targets an ordinary artifact
- **THEN** prior generated reports do not contribute to the reviewed-input
  manifest or its fingerprint

#### Scenario: The declared input role is the report directory itself

- **WHEN** generated report relative paths omit the reserved prefix because the
  declared role is rooted directly at `quality-control-reports/`
- **THEN** the canonical metadata envelope still identifies and excludes every
  non-target generated report

#### Scenario: One prior report is the primary target

- **WHEN** the caller expressly selects one report beneath the reserved prefix
- **THEN** that report alone remains in the reviewed-input manifest and other
  generated reports remain excluded

### Requirement: Installed QC packages carry the shared report contract

Every behaviorally detected QC skill MUST carry the compact target, metadata,
report-exclusion, immutable publication, receipt-success, and advisory-only
remediation contract in its independently installable package. Deterministic
governance validation MUST fail with a stable skill-specific finding when that
contract is missing or inverted.

#### Scenario: A QC skill omits run-manifest identity

- **WHEN** an independently installed QC skill no longer requires its report to
  identify the terminal run manifest
- **THEN** repository validation exits nonzero and identifies that skill
