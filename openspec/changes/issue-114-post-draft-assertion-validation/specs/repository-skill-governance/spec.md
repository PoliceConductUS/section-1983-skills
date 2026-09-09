## ADDED Requirements

### Requirement: Post-draft assertion validation has one semantic owner

The repository MUST define the complete post-draft assertion-validation workflow
in `validating-court-facing-assertions`. Applicable drafting and review skills
MUST reference that owner and MUST NOT duplicate or independently alter its
proposition model, status taxonomy, freshness rules, omission rules, or stopping
criteria. Existing compact install-local non-mutation, filesystem, and
immutable-report safeguards MUST remain present where repository governance
requires them.

#### Scenario: Consumer needs the shared contract

- **WHEN** an applicable skill cannot load `validating-court-facing-assertions`
- **THEN** it reports `assertion validation contract unavailable` and does not
  reconstruct a local substitute or claim validation completion

### Requirement: Semantic tests do not overclaim deterministic proof

Repository tests MUST distinguish contract-shape and behavior-pressure evidence
from human or agent substantive legal and factual judgment. No deterministic
test result MUST be described as deciding evidentiary support, legal
sufficiency, or filing readiness.

#### Scenario: Acceptance fixture receives expected classifications

- **WHEN** a deterministic fixture confirms required report fields and statuses
- **THEN** the test reports contract conformance without claiming that arbitrary
  real-world assertions will be assessed correctly
