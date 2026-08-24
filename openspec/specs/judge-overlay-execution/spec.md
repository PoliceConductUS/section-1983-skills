# judge-overlay-execution Specification

## Purpose

TBD - created by archiving change issue-27-judge-overlay-receipts. Update
Purpose after archive.

## Requirements

### Requirement: Complete judge-overlay execution packet

The packaged processor SHALL accept the required canonical relative filing
target inside the declared `filing` role root and canonical relative artifacts
inside the declared `judge-corpus` and `court-conduct` role roots. The packet
SHALL contain the exact filing scope, source and artifact fingerprints, overlay
and corpus identity/version/fingerprint/check date/validation, official conduct
inputs and checked dates, neutral transfer cards, exact prohibited-inference
checks, and the requested drafting-change, no-change, or fail-closed result.

#### Scenario: Required declared input is unavailable

- **WHEN** the filing target, corpus, conduct input, or used transfer card is
  missing, stale, failed, out of role, or unavailable
- **THEN** the processor returns a stable fail-closed outcome with no drafting
  change and does not represent it as passing

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

The receipt SHALL identify the selected filing target, declared artifact roles
and paths, expected and actual fingerprints, quality-control kind, UTC run time,
run ID, scope, approved sources, overlay and corpus identities/versions/check
dates/validation, official conduct inputs, used neutral transfer-card IDs, all
anti-gaming checks, the normalized outcome, and every supported drafting change
or bounded no-change reason. Remediation SHALL remain advisory and separately
authorized.

#### Scenario: Reviewer inspects a no-change receipt

- **WHEN** a reviewer opens a host-published no-change receipt
- **THEN** the reviewer can distinguish validated execution from nonexecution
  without relying on filed judge-specific prose

### Requirement: Host-published immutable receipt

The packaged processor SHALL verify the declared target and artifacts and return
exactly one canonical output-relative Markdown receipt path with deterministic
bytes. It MUST reject traversal, symlink escape, an artifact under the output
namespace, or mismatched bytes. It MUST NOT accept or open an output root, write
a receipt, create a run marker, or edit any input. Only the trusted host MAY
publish the returned receipt append-immutably through `OutputRun`.

#### Scenario: Completed overlay returns a receipt plan

- **WHEN** a valid execution packet and matching immutable artifacts are
  supplied
- **THEN** the processor returns one receipt plan and every input remains
  byte-identical
