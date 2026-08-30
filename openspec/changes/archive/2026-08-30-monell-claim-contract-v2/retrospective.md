# Retrospective

## What changed from the initial design

Forward evaluation exposed three false-pass risks that lexical structure checks
did not catch:

1. one record per path type would merge distinct police and jail customs;
2. prose approval could reach drafting without a verifiable principal decision;
3. temporal lane names did not prove that every supporting fact was mapped.

The implementation now permits multiple distinct records of the same type,
requires a typed and hashed principal-decision record, assigns stable fact IDs,
rejects dangling temporal references, and rejects unmapped supporting facts.

## CaseGraph lesson

Keeping the public CaseGraph CLI out of the dependency chain did not require
accepting an unverifiable legal opinion. The reasoned layer reads supported YAML
directly, and the standard-library validator independently checks the receipt:
document fingerprint, graph API identity, every used graph-file hash, claim
coverage, component enums, authority artifacts, pinpoints, and exact text.

## Evidence-boundary lesson

Repeated policy statements can support a narrow direct-policy inference without
inventing a written policy or policymaker. FTO, review, and jail handoff remain
implementation or transmission mechanisms inside recognized Monell paths.
Post-event material remains in later-notice, ratification, recurrence,
later-injury, or corroboration lanes and cannot retroactively create pre-event
notice or causation.
