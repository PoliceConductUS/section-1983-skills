## Context

The canonical complaint contract states pleading rules as prose with verified
authority and mirrors each rule in a completion-audit checklist. Structural
rules that a handoff can declare are enforced by two independently installed
Python checkers that share a contract JSON and validate only structure. The
source review found four doctrinal gaps. Three are prose rules that require
legal judgment. One, Rule 5.2 redaction, has a declarable structure.

## Goals / Non-Goals

**Goals:**

- State the accrual event for false-arrest, fabricated-evidence, and
  malicious-prosecution claims and the _Heck_ comparison for every count.
- Require the events preceding a use of force in the excessive-force contract.
- Enforce a declared Rule 5.2 `privacy_gate` at both installed checker seams.
- State the official-capacity and municipal punitive-damages rules.
- Reserve every file, stay, alternative, omission, and unredacted-identifier
  choice to the user.

**Non-Goals:**

- No mechanical Heck, accrual, capacity-duplication, or punitive-relief check.
- No decision on whether an authorization basis satisfies Rule 5.2.
- No state-law companion claims or qualified-immunity reform content.
- No change to the limitations-record schema or folder boundaries.

## Decisions

### Prose rules cite verified Supreme Court authority

_Wallace v. Kato_, _McDonough v. Smith_, _Thompson v. Clark_, _Heck v.
Humphrey_, _Barnes v. Felix_, _Kentucky v. Graham_, and _City of Newport v.
Fact Concerts_ are cited in the contract the way the existing contract cites
_Johnson v. City of Shelby_. The existing rule that `audit-authorities` verifies
every pinpoint before filing is unchanged. _Barnes_ is cited by docket number
and date because the U.S. Reports page is not yet assigned.

### One privacy gate, native validation, no schema file

The `privacy_gate` object is small enough that both checkers validate it with
native code and a closed vocabulary rather than a second JSON Schema copy. It
declares every minor party with its name form and, for each of the four Rule
5.2(a) categories, whether the identifier is absent, redacted, unredacted with a
stated basis, or unresolved. The checkers report presence, structure, and
unresolved status as hard findings. `redaction-authorization` joins the excluded
judgments so that a stated basis is never adjudicated mechanically.

### Capacity and relief stay in prose

Relief is free text and capacity is not a closed vocabulary in the version-2
handoff. A text scan for "punitive" would misfire on a sentence that disclaims
punitive damages. The rule lives in the contract and the completion audit.

## Risks / Trade-offs

- **A drafter treats the accrual section as legal advice** → Every choice is
  routed to the user as a reserved decision, and the filed text may not carry a
  Heck characterization.
- **The two checker copies drift** → Tests run identical documents through both
  checkers and compare the Filing CI contract copy to the canonical packaged
  block.
- **A pinpoint is wrong** → `audit-authorities` remains mandatory before filing.

## Migration Plan

1. RED tests for the prose, the completion audit, the contracts, and both
   checkers.
2. Contract prose, completion audit, routing, and case-map edits.
3. Checker validation and contract JSON updates.
4. Format, full test suite, strict OpenSpec validation, and `npm run validate`.

Rollback is the reversal of this branch.

## Open Questions

None.
