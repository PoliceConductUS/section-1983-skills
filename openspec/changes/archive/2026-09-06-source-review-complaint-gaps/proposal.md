## Why

A source review on 2026-09-05 compared twenty public Section 1983 primers,
guides, and court forms against the installed skills. Four rules were absent:
claim-specific accrual and the _Heck_ bar, the pre-force events that _Barnes v.
Felix_ (2025) requires in a totality analysis, Rule 5.2 privacy redaction, and
the capacity rules that make an official-capacity count duplicative and bar
punitive damages against a municipality. A complaint can pass every installed
check while pleading a Heck-barred count, naming a minor in full, or demanding
punitive damages from a city.

## What Changes

**Criminal-proceeding posture and accrual**

- From: The limitations gate requires a supported accrual date but no skill
  states an accrual rule, the _Heck_ rule, or the criminal-case posture.
- To: The canonical contract requires the posture of every charge, a
  claim-specific accrual event with verified authority, and a per-count _Heck_
  comparison, with file, stay, alternative, and omission choices reserved to the
  user.
- Reason: False-arrest, fabricated-evidence, and malicious-prosecution claims
  accrue on different events, and a standing conviction can bar a count.
- Impact: Non-breaking prose and completion-audit change.

**Events preceding the force**

- From: The excessive-force contract lists Graham-style factors at the moment of
  force.
- To: The contract requires the events preceding the force and forbids confining
  the application to that moment, citing _Barnes v. Felix_.
- Reason: The Supreme Court rejected the moment-of-threat rule in 2025.
- Impact: Non-breaking prose change.

**Rule 5.2 privacy gate**

- From: No contract or checker addresses Rule 5.2 redaction.
- To: The contract states the four Rule 5.2(a) limits and the minor-initials
  rule, and the version-2 handoff carries a `privacy_gate` object that both
  installed checkers validate.
- Reason: The federal pro se complaint form leads with this notice, and a
  violation exposes a minor or an identifier in a public record.
- Impact: Every complaint handoff must declare a `privacy_gate`; three
  mechanical checks and one excluded judgment are added.

**Capacity and relief**

- From: Capacity is a required count field with no rule about duplication or
  relief.
- To: The contract states that an official-capacity claim runs against the
  entity, forbids a duplicative official-capacity count without a stated purpose
  or reserved decision, and limits punitive damages to individual-capacity
  defendants.
- Reason: _Kentucky v. Graham_ and _City of Newport_ control these points.
- Impact: Non-breaking prose and completion-audit change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drafting-section-1983-complaints`: Add criminal-posture and accrual,
  pre-force events, Rule 5.2 privacy gate, and capacity and relief requirements.
- `deterministic-filing-integrity`: Require Filing CI to validate the privacy
  gate and preserve its hard findings without deciding redaction authorization.

## Impact

The change touches the canonical complaint contract, claim-specific contracts,
completion audit, complaint skill routing, false-arrest delta, entry-skill case
map, the version-2 structure contract, both installed checkers and the Filing CI
contract copy, the governance provenance review dates, and tests. It adds no
dependency, network access, or automated litigation decision.
