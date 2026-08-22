# auditing-section-1983-privilege-logs Specification

## Purpose

Define source-bounded Section 1983 privilege-log requirements and entry audits
without invented metadata, exposed privileged substance, privilege adjudication,
or agent-selected waiver strategy.

## Requirements

### Requirement: Approved privilege-log requirements matrix

The privilege-log skill SHALL identify supplied approved rules, orders,
agreements, and request relationships governing a requirements checklist or
audit. It MUST record required fields and timing from those sources without
supplying a generic court rule or certifying an authority that has not passed
the authority gate.

#### Scenario: Requirements requested before a log arrives

- **WHEN** approved requirements are supplied but no privilege log has arrived
- **THEN** the skill returns a scoped requirements checklist and does not invent
  entries, withheld material, or a deficiency in a nonexistent log

#### Scenario: Governing requirement is absent

- **WHEN** a packet contains a log but no approved source defines a disputed
  requirement
- **THEN** the audit reports a scoped authority gap and does not invent or
  certify the requirement

### Requirement: Line-by-line source-bounded log audit

When a log exists, the skill SHALL review each supplied entry and stable request
or target ID for every approved required field, including only supplied
identifier, date, author, recipients, document type, nonprivileged subject,
asserted privilege or protection, stated basis, custodian, and family or
attachment relationship when applicable. It MUST identify missing fields and
request-matching gaps without inventing metadata or exposing privileged
substance.

#### Scenario: Entry omits a required author

- **WHEN** an approved requirement calls for an author and an entry has none
- **THEN** the audit identifies the missing field and does not infer an author
  from custodian, recipient, document type, or context

### Requirement: Privilege and waiver decisions remain reserved

The skill MUST NOT adjudicate privilege, declare waiver, select clawback
treatment, accept a categorical log, choose a waiver theory, or decide whether
to confer or move. A material choice SHALL use `PLAINTIFF DECISION REQUIRED`,
state choices and consequences, preserve the supplied material and position, and
select none.

#### Scenario: Entry may support a waiver challenge

- **WHEN** approved sources permit but do not compel a waiver argument
- **THEN** the audit reports the potential issue and routes the choice to the
  plaintiff without declaring waiver
