# Proposal: Put the arresting officer first among defendants

## Why

An arrest-centered Section 1983 filing should consistently identify the officer
responsible for the arrest before other defendants. Existing filings may use a
different order, and the current skills do not require correction during later
drafting or revision.

## What changes

- Audit declared inputs to determine whether an arrest occurred and identify the
  arresting officer or officers.
- Put the caller-designated primary arresting officer first in each ordered
  defendant presentation in new or materially revised filings.
- Stop and ask when several arresting officers exist without a declared primary.
- Preserve caller order when no arrest occurred and preserve factual chronology
  in every matter.
- Add deterministic regression scenarios for all branches of the rule.

## Capability

- New capability: `arresting-officer-defendant-ordering`

## Impact

The change affects the shared Section 1983 drafting workflow, the canonical
complaint composition and completion contracts, the false-arrest actor audit,
and evaluation fixtures. It adds no runtime dependency or persistence layer.
