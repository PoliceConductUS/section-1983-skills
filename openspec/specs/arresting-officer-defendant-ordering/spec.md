# arresting-officer-defendant-ordering Specification

## Purpose

TBD - created by archiving change issue-100-arresting-officer-first. Update
Purpose after archive.

## Requirements

### Requirement: Arrest involvement is audited before defendant presentation

The drafting stack MUST audit arrest involvement before defendant presentation.
Before generating or materially revising a filing that names defendants, it must
examine the caller-declared read-only inputs to determine whether an arrest
occurred and identify every source-documented arresting officer. It MUST report
a gap instead of inventing an arrest or officer identity.

#### Scenario: Record documents an arrest by one officer

- **WHEN** the declared inputs document an arrest and identify one arresting
  officer
- **THEN** the drafting operation treats that officer as the primary arresting
  officer for defendant presentation

#### Scenario: Record does not establish an arrest

- **WHEN** the declared inputs do not establish that an arrest occurred
- **THEN** the drafting operation does not infer an arrest or arresting officer

### Requirement: The primary arresting officer leads ordered defendant presentations

Each covered filing MUST put the primary arresting officer first. When an arrest
occurred and one primary arresting officer is identified, every new or
materially revised filing must list that officer first in each ordered defendant
presentation that the filing contains, including its caption, Parties section,
defendant list or table, and defendant-grouped claim presentation. A different
order in an earlier filing MUST NOT control the new or revised output.

#### Scenario: Existing complaint lists another defendant first

- **WHEN** a complaint naming an identified primary arresting officer is
  materially revised and its prior caption or Parties section lists another
  defendant first
- **THEN** the revised caption, Parties section, defendant list, and
  defendant-grouped claim presentation place the primary arresting officer first

#### Scenario: Current matter designates Markham

- **WHEN** the caller designates Markham as the primary arresting officer
- **THEN** each ordered defendant presentation in the requested new or revised
  filing lists Markham first without making Markham a reusable default

### Requirement: Multiple arresting officers require a caller designation

Multiple arresting officers MUST require a caller designation. When the declared
inputs identify more than one arresting officer, the drafting operation must use
a primary arresting officer expressly declared by the caller. If the caller has
not declared one, the operation MUST stop and ask for the designation and MUST
NOT infer one from rank, chronology, report authorship, physical contact, or
prior filing order.

#### Scenario: Caller designates one of several arresting officers

- **WHEN** several arresting officers are source-documented and the caller
  declares one as primary
- **THEN** the filing uses that officer first in every ordered defendant
  presentation

#### Scenario: Several officers exist without a primary designation

- **WHEN** several arresting officers are source-documented and no primary is
  declared
- **THEN** drafting stops with a focused request for the primary designation and
  does not produce a reordered filing

### Requirement: Defendant order does not reorder facts or merits

The defendant-presentation rule MUST NOT reorder factual chronology,
claim-specific allegations, event stages, or merits analysis merely to place an
officer first. When no arrest occurred, the operation MUST preserve the caller's
defendant order unless another approved contract expressly controls it.

#### Scenario: Chronology begins with another officer

- **WHEN** another officer acted before the primary arresting officer in the
  supported event sequence
- **THEN** the facts retain that chronological order while ordered defendant
  presentations still list the primary arresting officer first

#### Scenario: Matter contains no arrest

- **WHEN** the declared inputs establish no arrest
- **THEN** the new or revised filing preserves the caller's defendant order

### Requirement: Regression evaluation covers every decision branch

The repository SHALL retain deterministic synthetic evaluations for one
arresting officer, correction of legacy defendant order, a caller-designated
primary among several arresting officers, missing-primary clarification, and a
no-arrest matter. The evaluations MUST distinguish defendant presentation from
factual chronology and MUST NOT require a case-specific reusable default.

#### Scenario: Ordering guidance regresses

- **WHEN** an affected instruction omits arrest auditing, first-defendant
  placement, clarification for an undesignated primary, or the chronology
  boundary
- **THEN** focused repository evaluation fails before the skill is treated as
  complete
