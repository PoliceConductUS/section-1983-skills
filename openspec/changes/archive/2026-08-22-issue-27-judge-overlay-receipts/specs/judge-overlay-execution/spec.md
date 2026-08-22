## ADDED Requirements

### Requirement: Complete judge-overlay execution packet

The system SHALL accept one exact, versioned judge-overlay execution packet
containing the audited version and scope, approved sources, artifact paths and
fingerprints, overlay and corpus identity/version/fingerprint/check date/
validation, official court-conduct inputs and checked dates, neutral transfer
cards, exact prohibited-inference checks, and the requested drafting-change,
no-change, or fail-closed result.

#### Scenario: Required overlay input is unavailable

- **WHEN** the packet marks the overlay, corpus, conduct input, or used transfer
  card as missing, stale, failed, or unavailable
- **THEN** the system records a stable fail-closed outcome with no drafting
  change and does not represent it as passing

### Requirement: Immutable version-local receipt

The system SHALL verify the designated artifacts and write exactly one new
Markdown receipt under the audited version's canonical `audits/` directory. It
MUST reject an unresolved or out-of-bound version, artifact traversal, an
artifact under `audits/`, an escaping audits symlink, or an existing report
path. It MUST NOT edit the filing, any designated artifact, or any prior report.

#### Scenario: Completed overlay writes a receipt

- **WHEN** a valid execution packet and matching immutable artifacts are
  supplied
- **THEN** the system creates one exclusive version-local receipt and every
  preexisting file remains byte-identical

### Requirement: No-change execution is explicit

A completed overlay that produces no supported change SHALL record the exact
outcome `no judge-specific drafting change` and a nonempty bounded reason. The
absence of judge-specific filing prose or absence of a receipt MUST NOT be
treated as proof that the overlay ran.

#### Scenario: Valid corpus supplies no qualifying support

- **WHEN** the overlay and inputs pass but no neutral card supports a permitted
  drafting change
- **THEN** the immutable receipt proves execution and records no judge-specific
  drafting change with the bounded reason

### Requirement: Anti-gaming checks fail closed

The packet SHALL contain each required assignment, preference, desired-outcome,
adverse-authority, record, personalization, outcome-prediction, and unsupported-
conclusion check exactly once. A missing, duplicate, unknown, or failed check
MUST produce a fail-closed result and no drafting change.

#### Scenario: Outcome prediction check fails

- **WHEN** the outcome-or-behavior-prediction check is absent or false
- **THEN** the receipt records the anti-gaming failure and cannot record a
  completed or passing result

### Requirement: Receipt preserves execution provenance

The receipt SHALL identify the audited version, artifact paths and expected and
actual fingerprints, quality-control kind, UTC run time, run ID, scope, approved
sources, overlay and corpus identities/versions/check dates/validation, official
conduct inputs, used neutral transfer-card IDs, all anti-gaming checks, the
normalized outcome, and every supported drafting change or bounded no-change
reason. It SHALL preserve the repository's advisory-remediation contract.

#### Scenario: Reviewer inspects a degraded receipt

- **WHEN** a reviewer opens a no-change receipt
- **THEN** the reviewer can distinguish validated execution from nonexecution
  without relying on filed judge-specific prose
