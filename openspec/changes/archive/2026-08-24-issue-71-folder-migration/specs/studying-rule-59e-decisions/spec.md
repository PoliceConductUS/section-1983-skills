# studying-rule-59e-decisions Delta Specification

## MODIFIED Requirements

### Requirement: Install-local deterministic validation

The public skill MUST include a standard-library validator that accepts the
declared `decisions` input root plus an optional canonical relative corpus
target, or bounded validated corpus JSON on standard input. It SHALL perform
shape, controlled-value, unique-ID, reference, authorship, gap, denominator, and
transfer-strength checks without network access and return deterministic
validation results. It MUST reject an absolute or traversing target, symlink
escape, directory target, malformed JSON, malformed field type, or oversized
input with a stable finding and no traceback. It MUST NOT accept an arbitrary
corpus path, output root, or direct-write destination.

#### Scenario: Valid declared corpus target

- **WHEN** a canonical corpus target inside `decisions` satisfies all shape and
  semantic invariants
- **THEN** the validator exits zero and reports validation success

#### Scenario: Valid bounded standard input

- **WHEN** no target is supplied and validated corpus JSON is provided on
  standard input within the documented bound
- **THEN** the validator applies the same checks without filesystem access
