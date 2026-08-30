## Design Summary

Before a Section 1983 skill drafts or materially revises a filing that names
defendants, it audits the declared inputs to determine whether an arrest
occurred and identifies the arresting officer or officers. If one primary
arresting officer is established, that officer appears first in every ordered
defendant presentation. A prior filing's different order does not control.

If several arresting officers are identified, the skill uses a primary officer
declared by the caller. Without that declaration, it stops and asks rather than
guessing. In the user's current matter, Markham is the caller-designated primary
officer, but the reusable public skills do not hard-code that name.

The ordering rule applies to captions, Parties sections, defendant lists or
tables, and defendant-grouped claim presentation. It does not reorder factual
chronology, claim-specific allegations, or merits analysis merely to move a
defendant.

## Alternatives Considered

### Dedicated new skill

- **Approach:** Add a separate defendant-ordering skill to every drafting stack.
- **Benefit:** One isolated package would own the rule.
- **Cost:** Callers could omit it, and the small rule would add another routing
  dependency.
- **Why not selected:** Existing general and complaint drafting contracts
  already own document composition and completion review.

### Complaint-only rule

- **Approach:** Add the rule only to the canonical complaint contract.
- **Benefit:** Captions, Parties sections, and complaint counts have one owner.
- **Cost:** Motions, responses, and other revised filings that present
  defendants would remain uncovered.
- **Why not selected:** The approved rule applies to future filings generally.

### Shared drafting rule with complaint specialization

- **Approach:** Put the cross-document trigger in `section-1983-drafting`, put
  the detailed complaint presentation and completion check in the canonical
  complaint references, and make the false-arrest actor audit supply the
  required officer identification.
- **Benefit:** All filing routes receive the rule while standalone complaint and
  false-arrest compositions remain complete.
- **Cost:** The same invariant appears at two intentional composition seams.
- **Why selected:** It is the smallest approach that covers both general filing
  revision and canonical complaint drafting.

## Agreed Approach

Use the shared drafting rule with complaint specialization. Add deterministic
regression scenarios for one arresting officer, legacy wrong order, a declared
primary among several officers, a missing primary that requires clarification,
and a no-arrest matter.

## Key Decisions

- Arrest involvement and officer identity come only from caller-declared input
  folders and caller instructions.
- A case-specific designation such as Markham belongs to the invocation or case
  materials, never the public skill.
- The order changes defendant presentation, not chronology or substantive claim
  logic.
- The skill never selects a primary officer from several candidates.

## Open Questions

None.
