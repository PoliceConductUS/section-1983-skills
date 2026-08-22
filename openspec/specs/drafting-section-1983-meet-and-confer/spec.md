# drafting-section-1983-meet-and-confer Specification

## Purpose

Define neutral Section 1983 meet-and-confer correspondence that consumes a
completed response audit, preserves a factual conference record, and reserves
narrowing, deadlines, and escalation for the plaintiff.

## Requirements

### Requirement: Audit-driven correspondence

The meet-and-confer skill SHALL consume a completed request-by-request audit and
organize neutral correspondence by request number and stable target ID. Each
issue MUST identify the exact response or objection, concrete deficiency,
approved rule or order source IDs, requested cure, proposed response date, and
reservation. An actual date MUST appear only when the user supplied or approved
it; otherwise date options MUST remain under `PLAINTIFF DECISION REQUIRED`. The
skill MUST NOT silently redo the audit.

#### Scenario: Audit identifies a curable omission

- **WHEN** an approved audit identifies an exact omitted answer and an approved
  requirement supplies the cure
- **THEN** the correspondence states that omission and cure without adding a new
  deficiency or unsupported accusation

### Requirement: Conference record remains factual

The skill SHALL return a conference or certification record separately from the
draft correspondence and MUST include only supplied dates, participants,
methods, positions, agreements, and unresolved issues. It MUST NOT infer consent
or agreement from silence or invent a conference event.

#### Scenario: Opponent position is not supplied

- **WHEN** no approved source supplies the opponent's position
- **THEN** the record marks the position unknown and does not state consent,
  opposition, or agreement

### Requirement: Escalation and compromise remain reserved

The skill MUST NOT decide whether or when to send correspondence, compromise,
narrow a request, select an unapproved response date, move to compel, assert
waiver, or seek fees or sanctions. It MUST NOT threaten automatic relief. Each
material choice SHALL use `PLAINTIFF DECISION REQUIRED`, state choices and
consequences, preserve the current request and draft, and select none.

#### Scenario: Narrowing could resolve the dispute

- **WHEN** the audit supports preserving the request and proposing narrower
  scope
- **THEN** the output presents both options and consequences without silently
  narrowing the request or sending the proposal
