## ADDED Requirements

### Requirement: Complete complaint candidates use shared assertion validation

The canonical complaint owner MUST supply its complete claim, Defendant,
challenged-act, limitations, qualified-immunity, Monell, relief, and completion-
audit requirements to `validating-court-facing-assertions`. It MUST route
reported drafting defects to a separate authorized correction stage and MUST
submit the corrected complete complaint to affected-assertion revalidation and
final coverage reconciliation.

#### Scenario: Complaint completion audit passes but an approved claim is absent

- **WHEN** structural complaint checks pass but shared validation finds an
  approved claim omitted from the draft
- **THEN** the complaint remains incomplete until the principal authorizes the
  omission or a separate drafting stage corrects and revalidates it
