## Design Summary

A review of twenty public Section 1983 primers, guides, and forms on 2026-09-05
found four rules the canonical complaint contract did not state. The skills
already encode everything else those sources describe, usually more strictly.

1. No skill mentions the _Heck_ bar, favorable termination, or the plaintiff's
   criminal-case posture. The limitations gate demands an accrual date but
   states no accrual rule, and false-arrest, fabricated-evidence, and
   malicious-prosecution claims accrue on different events.
2. The excessive-force contract lists offense severity, threat, resistance,
   flight, force, duration, and injury but not the events preceding the force.
   _Barnes v. Felix_ (2025) rejected the moment-of-threat rule.
3. Nothing enforces Rule 5.2 redaction of minors' names, birth dates,
   social-security numbers, and account numbers, even though the federal pro se
   form leads with that notice.
4. The contract requires a capacity per count but never states that an
   official-capacity claim is a claim against the entity or that a municipality
   is immune from punitive damages.

## Approach chosen

Add the four rules to the canonical complaint contract as prose with verified
Supreme Court authority, mirror each in the completion audit, and add one
machine-readable `privacy_gate` object to the version-2 handoff that both
installed checkers validate for presence, structure, and unresolved status.
Route every file, stay, alternative-pleading, omission, or unredacted-identifier
choice to the user as a reserved decision.

## Alternatives rejected

- A mechanical Heck or accrual check. Accrual and Heck comparison require
  element-level legal judgment that the deterministic checkers exclude.
- A mechanical punitive-damages or duplicate-capacity check. Relief is free text
  and capacity values are not a closed vocabulary; a text scan would misfire.
- Adding state-law companion claims without qualified immunity. That is a scope
  expansion beyond federal Section 1983 contracts.
