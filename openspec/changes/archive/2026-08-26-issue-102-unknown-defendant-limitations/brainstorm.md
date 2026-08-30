## Design Summary

The canonical Section 1983 complaint skill adds a defendant-specific limitations
gate when an amendment adds, identifies, or substitutes an individual defendant
after the calculated limitations deadline or when the supplied record, an
opposing party, the court, or the caller raises a limitations, relation-back,
notice, diligence, concealment, or tolling issue. The reusable skill does not
invent a universal number of days for "near limitations."

For every affected individual, the skill completes a separate internal record
covering the supported accrual date and limitations deadline; the original Doe
or role description; same-transaction analysis; separate Rule 15(c)(1)(A) and
(C) analyses; mistake versus lack of knowledge; Rule 4(m) notice and service;
the identity-first-knowable date; pre-limitations diligence; defendant-specific
concealment or tolling; and fallback claims and severable relief.

Every missing or unresolved required entry is an internal filing-critical GAP
that blocks filing-ready status. The rule does not add an adverse concession to
filed text and does not alter the false-arrest seizure-point or general
actor-causation contracts.

## Alternatives Considered

### Fold the gate into Issue #100

- **Benefit:** No additional story in the stack.
- **Cost:** Reopens an implemented, verified, and archived OpenSpec change.
- **Why not selected:** A distinct story preserves Issue #100's completed
  arrest-order contract and gives the new legal gate its own review history.

### Add the gate to several specialized skills

- **Benefit:** The requirement would appear near several amendment workflows.
- **Cost:** Duplicated requirements could drift, and the false-arrest and
  actor-causation contracts already cover their intended concerns.
- **Why not selected:** The canonical complaint skill already owns complete
  complaint composition and completion review.

### Add one canonical complaint gate

- **Approach:** Add the substantive checklist to the complaint contract, its
  fail-closed result to the completion audit, and a focused synthetic regression
  evaluation.
- **Benefit:** One authoritative contract covers every complaint amendment
  without changing unrelated skill boundaries.
- **Cost:** Other filing types do not independently own the gate.
- **Why selected:** The approved behavior concerns adding, naming, or
  substituting defendants in complaints and amendments.

## Agreed Approach

Use one canonical complaint gate with separate defendant-specific records,
fail-closed completion treatment, and deterministic regression coverage.

## Key Decisions

- The trigger is record-driven; it has no universal numeric "near limitations"
  threshold.
- Rule 15(c)(1)(A) and Rule 15(c)(1)(C) receive separate analyses.
- Mistake and lack of knowledge are classified rather than collapsed.
- Every required entry is defendant-specific where the subject permits.
- An unresolved entry blocks filing-ready status internally without creating a
  filed-text concession.
- No false-arrest or general actor-causation rule changes.

## Open Questions

None.
