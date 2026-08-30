# drafting-linter-signals Specification

## Purpose

Define backward-compatible, location-bearing mechanical prose findings, proven
controlling-term exemptions, non-gating paragraph-density warnings, and an
exhaustive source-bounded reconciliation workflow for the Section 1983 drafting
linter.

## Requirements

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

### Requirement: Proven controlling terms of art

The linter SHALL exempt `active resistance`, `materially similar`, and
`reasonably trustworthy` from banned-word counts and SHALL expose their exact
locations as `controlling_term_of_art` exemption records. It MUST NOT add an
exemption that does not correspond to a phrase currently matched by a mechanical
banned-word check.

#### Scenario: Legal analysis uses controlling wording and rhetoric

- **WHEN** one paragraph uses a proven controlling phrase and another says
  `unbearably` or `almost immediately`
- **THEN** the controlling phrase is an exemption and the rhetoric remains a
  location-bearing unexempted violation

### Requirement: Non-gating paragraph heuristics

The linter SHALL emit `review_heuristic` warnings when one paragraph has at
least two sentences longer than twenty-five words or at least four bounded
reporter-form case citations. Warnings MUST remain outside violation counts,
normalized scores, exit status, legal-sufficiency conclusions, and filing-
readiness conclusions.

#### Scenario: Dense legal analysis triggers review

- **WHEN** a paragraph reaches either documented density threshold
- **THEN** the report identifies the paragraph and observed threshold but does
  not increase the violation score or declare the filing deficient

### Requirement: Exhaustive residual reconciliation

The drafting workflow SHALL target zero unexempted violations and account for
every residual location-bearing finding exactly once as an unexempted violation,
an accurate quotation verified against an approved source, or a controlling term
of art supported by an exemption record. The linter MUST NOT call a quotation
accurate without source verification. Warnings SHALL be reviewed separately.

#### Scenario: A quoted banned phrase remains

- **WHEN** the linter locates a banned phrase inside quoted text
- **THEN** it remains an unexempted finding until the drafting stage verifies
  the source and records the accurate-quotation disposition

### Requirement: Score deltas remain feedback

The linter and drafting workflow SHALL describe the difference between two
scores as editing feedback only. No score, finding count, or warning MAY be
represented as a merits verdict, legal-sufficiency decision, or filing-
readiness decision.

#### Scenario: The revised score improves

- **WHEN** a second lint run has fewer violations
- **THEN** the workflow reports the improvement as feedback and performs the
  residual reconciliation without declaring the filing meritorious or ready
