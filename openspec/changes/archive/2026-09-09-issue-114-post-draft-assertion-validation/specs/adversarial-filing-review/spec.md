## ADDED Requirements

### Requirement: Adversarial review remains downstream from assertion validation

Adversarial filing review MUST remain a separate read-only defense attack on a
validation-complete candidate and MUST NOT substitute for original-source
assertion validation. A material adversarial finding accepted for correction
MUST return to a separately authorized drafting stage and then through affected-
assertion and dependency revalidation before another downstream review.

#### Scenario: Defense attack exposes a source defect

- **WHEN** adversarial review identifies a credible attack that the principal
  authorizes for correction
- **THEN** the review preserves the target and routes the finding to separate
  correction followed by shared revalidation
