# drafting-section-1983-complaints Delta Specification

## ADDED Requirements

### Requirement: Unknown and new individual defendants trigger a limitations gate

The canonical complaint contract MUST apply a defendant-specific limitations
gate whenever a complaint amendment adds, identifies, or substitutes an
individual defendant after the calculated limitations deadline, or when the
supplied record, an opposing party, the court, or the caller raises a
limitations, relation-back, Rule 4(m) notice or service, diligence, concealment,
or tolling issue. The reusable contract MUST NOT invent a universal numeric
definition of "near limitations."

#### Scenario: Calculated deadline has passed

- **WHEN** an amendment adds, identifies, or substitutes an individual after the
  calculated limitations deadline
- **THEN** the complaint workflow applies the defendant-specific limitations
  gate before treating the amendment as filing-ready

#### Scenario: Record raises risk before the deadline

- **WHEN** the deadline has not passed but the supplied record, an opposing
  party, the court, or the caller raises a covered limitations-related issue
- **THEN** the complaint workflow applies the same defendant-specific gate
  without relying on a universal day-count threshold

### Requirement: Each affected defendant has a complete limitations record

For every affected individual, the complaint workflow MUST complete a separate
limitations record containing: the supported accrual date and applicable
limitations deadline; the original Doe designation or role description; a
same-transaction, conduct, or occurrence analysis; separate Rule 15(c)(1)(A) and
Rule 15(c)(1)(C) analyses; a supported mistake-versus-lack-of-knowledge
classification; Rule 4(m) notice and service facts and dates; the earliest
supported date on which the defendant's identity was knowable; concrete
pre-limitations diligence acts, dates, and sources; defendant-specific
concealment or tolling facts and supporting-authority status; and fallback
claims and severable relief if substitution or relation back fails.

#### Scenario: Amendment affects two individuals

- **WHEN** an amendment identifies or substitutes two affected individual
  defendants with different notice, diligence, or concealment histories
- **THEN** the workflow completes two separately supported limitations records
  rather than one collective analysis

#### Scenario: Rule 15 paths differ

- **WHEN** an affected defendant may implicate both state-law relation back and
  the federal notice-and-mistake route
- **THEN** the record separately analyzes Rule 15(c)(1)(A) and Rule 15(c)(1)(C)
  and separately classifies mistake versus lack of knowledge

### Requirement: An incomplete limitations record blocks filing-ready status

Every missing, unsupported, or unresolved required limitations-record entry MUST
create an internal filing-critical GAP and MUST block filing-ready status. The
complaint workflow MUST route the issue for a reserved litigation decision
without adding an adverse merits characterization to filed text.

#### Scenario: Identity-first-knowable date is unresolved

- **WHEN** the record does not establish the earliest supported date on which an
  affected defendant's identity was knowable
- **THEN** the workflow records a filing-critical GAP, blocks filing-ready
  status, and does not characterize the claim as time-barred in filed text

#### Scenario: Fallback relief is missing

- **WHEN** the record does not identify fallback claims and severable relief if
  substitution or relation back fails
- **THEN** the workflow records the same filing-critical and filing-readiness
  result

### Requirement: Regression evaluation protects the limitations gate

The repository SHALL retain deterministic synthetic evaluation for the
calculated-deadline trigger, identified pre-deadline risk, one record per
affected defendant, all required record entries, separate Rule 15 analyses,
mistake-versus-lack-of-knowledge classification, and fail-closed treatment of
every unresolved entry.

#### Scenario: Complaint guidance regresses

- **WHEN** the canonical complaint contract or completion audit omits a trigger,
  required entry, separate analysis, defendant-specific cardinality, or
  filing-critical result
- **THEN** focused repository evaluation fails before the skill is treated as
  complete
