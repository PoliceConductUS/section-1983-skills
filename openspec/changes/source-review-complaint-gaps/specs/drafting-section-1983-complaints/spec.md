# drafting-section-1983-complaints Delta Specification

## ADDED Requirements

### Requirement: Criminal-proceeding posture and claim accrual are recorded before filing

The canonical complaint contract MUST require the posture of every criminal
charge that arose from the pleaded events, with charge, court, current status,
disposition date, and source. For every count the workflow MUST state the
accrual event and the verified authority that fixes it, distinguishing
false-arrest accrual at detention under legal process, fabricated-evidence
accrual at favorable termination, and malicious-prosecution termination without
a conviction. For every count the workflow MUST state whether success would
necessarily imply the invalidity of an outstanding conviction. The workflow MUST
present file, stay, alternative-pleading, and omission choices to the user as
reserved decisions and MUST NOT select one or describe a count as Heck-barred in
filed text.

#### Scenario: Charges are pending at drafting

- **WHEN** a criminal charge from the arrest remains pending
- **THEN** the workflow records the pending status, states that the false-arrest
  claim accrued at detention under legal process, and presents filing now or
  requesting a stay as reserved user choices

#### Scenario: A conviction stands

- **WHEN** the plaintiff was convicted of an offense arising from the events
- **THEN** the workflow states for each count whether success would necessarily
  imply the invalidity of that conviction and routes the omission or
  alternative-pleading choice to the user without a Heck characterization in
  filed text

### Requirement: Excessive-force counts plead the events preceding the force

The claim-specific excessive-force contract MUST require the events preceding
the force, including each officer's conduct that created, raised, or reduced
the risk and the timing between each event and the force. The contract MUST
forbid confining the application to the moment force was used and MUST cite
_Barnes v. Felix_ (2025). The qualified-immunity comparison MUST include
pre-force events among the compared facts.

#### Scenario: Officer conduct created the risk

- **WHEN** an officer's pre-force conduct created or raised the risk that the
  force answered
- **THEN** the count pleads that conduct and its timing as part of the totality
  rather than starting the application at the moment of force

### Requirement: Rule 5.2 privacy redaction is gated in the handoff

The canonical complaint contract MUST state the Rule 5.2(a) limits: last four
digits of a social-security or taxpayer-identification number, year of birth,
minor's initials, and last four digits of a financial-account number. The
version-2 mechanical handoff MUST contain a `privacy_gate` object declaring
every minor party with its name form and one entry per Rule 5.2(a) category with
a status of absent, redacted, unredacted-authorized, or unresolved. The
installed complaint checker MUST report a missing gate, a malformed entry, a
missing or duplicated category, a location that names a missing paragraph, or a
missing authorization basis as a hard finding, and MUST treat an unresolved
entry or a blocked gate as filing-critical. The checker MUST NOT decide whether
an authorization basis suffices; `redaction-authorization` is an excluded
judgment. Any unredacted identifier MUST be routed to the user as a reserved
decision.

#### Scenario: Handoff omits the privacy gate

- **WHEN** a complaint handoff has no `privacy_gate` object
- **THEN** the installed checker returns a stable hard finding and a nonzero
  status

#### Scenario: Minor is named in full without a basis

- **WHEN** a minor party is declared with a full-name form and an empty
  authorization basis
- **THEN** the installed checker reports a structure finding without deciding
  whether any basis would suffice

#### Scenario: Identifier status is unresolved

- **WHEN** a Rule 5.2(a) category entry is marked unresolved
- **THEN** the installed checker reports the gate as filing-critical

### Requirement: Capacity governs duplicative counts and punitive relief

The canonical complaint contract MUST state that an official-capacity claim
against an officer is a claim against the entity, MUST forbid an
official-capacity count that duplicates a municipal count on the same claim and
challenged act unless the draft states the distinct purpose of each count or
records a reserved user decision, and MUST limit punitive damages to defendants
sued in an individual capacity because a municipality is immune from punitive
damages under Section 1983.

#### Scenario: Draft seeks punitive damages from the city

- **WHEN** the prayer for relief requests punitive damages from a municipality
  or an official-capacity defendant
- **THEN** the completion audit fails until the request is limited to
  individual-capacity defendants

#### Scenario: Officer is sued in both capacities on one claim

- **WHEN** a claim names an officer in an official capacity and also names the
  municipality on the same challenged act
- **THEN** the draft states the distinct purpose of each count or records the
  duplication as a reserved user decision
