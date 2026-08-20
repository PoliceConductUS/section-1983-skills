## Context

The complaint completion audit contains the controlling recorded-evidence
boundary. The claim-specific complaint reference has a shorter recording rule,
and the Rule 59(e) final gate has no equivalent checkpoint. Two intended prose
edits currently exist only in the dirty `main` checkout because they were made
in the wrong workspace.

## Goals / Non-Goals

**Goals:**

- Preserve the intended prose on one dedicated stacked branch.
- Keep complaint claim drafting, complaint completion review, and Rule 59(e)
  packet review aligned.
- Make a dropped evidence route or broken Rule 59(e) list number fail CI.

**Non-Goals:**

- Change the already-approved evidence rule.
- Decide whether a particular allegation is true.
- Add a transcript generator, video analyzer, source verifier, or filing
  checker.
- Rewrite unrelated skill guidance.

## Decisions

### Test semantic obligations, not exact prose

The focused test checks each public contract for the complete obligations: a
recorded event must be visible before the recording establishes it; a recorded
statement must appear in a verified transcript; quotations remain exact;
paraphrases add no content; uncertain speaker attribution remains uncertain; and
the alternative allegation route states present recollection, unresolved
recordings, correction if more recordings appear, and a fail-closed gap result.

### Keep the three public contracts aligned

The completion audit remains the existing public source. The complaint
claim-specific reference receives the complete rule where drafters first shape
claim allegations. The Rule 59(e) final-review list receives one packet-level
gate rather than duplicating the full paragraph.

### Preserve ordered-list continuity

The Rule 59(e) gate is a numbered acceptance list. The focused test extracts
that section and requires a continuous sequence so inserting the new checkpoint
cannot silently duplicate or skip a number.

## Risks / Trade-offs

- **[Semantic wording varies]** → Accept bounded wording alternatives while
  requiring every obligation in every contract.
- **[The short Rule 59(e) checkpoint depends on another section]** → Require it
  to name the recorded-evidence gate and fail when the gate does not pass.
- **[The accidental prose is lost during cleanup]** → Restore `main` only after
  branch/origin parity and full verification.

## Migration Plan

1. Commit OpenSpec design and sync the child branch.
2. Add and run the focused RED test against the clean child branch.
3. Transfer the exact intended two-file patch from `main`.
4. Run focused and full GREEN verification, review, and archive.
5. Confirm branch/origin parity, then restore only those two files on `main`.

## Open Questions

None.
