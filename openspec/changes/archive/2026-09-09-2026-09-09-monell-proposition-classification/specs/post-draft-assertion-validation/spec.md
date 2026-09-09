## ADDED Requirements

### Requirement: Expected Monell discovery is not validated as an existing fact

The assertion validator MUST identify any expected-discovery Monell proposition
presented as an existing fact or evidence. It MUST also identify when a
supporting brief is needed to supply a factual basis absent from the complaint.
This review is semantic and MUST NOT claim that deterministic checks decide
evidentiary support or legal sufficiency.

#### Scenario: Complaint predicts contents of unavailable municipal records

- **WHEN** a Monell allegation states what unavailable training, discipline, or
  complaint-history records are expected to show as an existing fact
- **THEN** the validator records the unsupported proposition and does not treat
  the expectation as present support

#### Scenario: Brief supplies the only factual basis

- **WHEN** a brief supplies the factual basis for a Monell inference that the
  complaint itself does not plead
- **THEN** the validator records the missing complaint-level factual basis
