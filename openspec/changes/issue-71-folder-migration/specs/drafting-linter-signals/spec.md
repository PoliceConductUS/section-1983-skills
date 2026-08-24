# drafting-linter-signals Delta Specification

## MODIFIED Requirements

### Requirement: Location-bearing mechanical findings

The linter SHALL accept one declared `filing` input root and one required
canonical relative filing target, or bounded validated filing bytes on standard
input. It SHALL preserve aggregate counts and score while emitting bounded
records that identify the selected artifact, one-based paragraph, one-based line
range, check, count, excerpt, stable finding ID, and `unexempted_violation`
classification for every paragraph containing a counted mechanical hit. The
per-check record counts MUST reconcile exactly with the aggregate counts. It
MUST reject arbitrary second paths, absolute or traversing targets, symlink
escapes, directories, and oversized input, and MUST NOT write or accept an
output root.

#### Scenario: Declared filing contains violations

- **WHEN** the selected target inside `filing` contains violations in different
  paragraphs
- **THEN** every finding identifies the correct target and paragraph line range
  and the aggregate score remains backward compatible

#### Scenario: A second arbitrary path is supplied

- **WHEN** a caller attempts to add another filesystem path outside the one
  declared filing target
- **THEN** the linter rejects the invocation without reading that path
