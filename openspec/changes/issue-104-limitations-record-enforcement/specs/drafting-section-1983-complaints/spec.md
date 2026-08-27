# drafting-section-1983-complaints Delta Specification

## MODIFIED Requirements

### Requirement: Unknown and new individual defendants trigger a limitations gate

The canonical complaint contract MUST apply a defendant-specific limitations
gate whenever a proposed complaint or amendment includes an intended individual
defendant who remains unnamed, role-only, misnamed, or not serviceable. The gate
MUST also apply when an amendment adds, identifies, or substitutes an individual
after the calculated limitations deadline, when the deadline remains unresolved,
or when the supplied record, an opposing party, the court, or the caller raises
a limitations, relation-back, Rule 4(m), diligence, concealment, or tolling
issue. An unidentified witness or other person who is not an intended defendant
MUST NOT activate the gate. The reusable contract MUST NOT invent a universal
numeric definition of "near limitations."

#### Scenario: Intended Doe has no express limitations warning

- **WHEN** a proposed complaint includes a role-only intended individual
  defendant and no caller, court, opponent, or supplied record expressly raises
  limitations
- **THEN** the complaint workflow applies the defendant-specific gate before
  treating the complaint as filing-ready

#### Scenario: Unidentified witness is not a defendant

- **WHEN** a complaint describes an unidentified witness who is not an intended
  defendant and no other trigger applies
- **THEN** that witness does not activate the defendant-specific limitations
  gate

### Requirement: Each affected defendant has a complete limitations record

For every affected individual, the complaint workflow MUST complete a separate
limitations record. The record MUST preserve separate sourced facts for source
first availability, source first possession, objective ascertainability with its
basis, and actual identification with its source and method. No one of those
facts may imply another.

The record MUST separately contain pre-limitations,
post-filing/pre-identification, and post-identification/pre-service diligence;
record-control and withholding provenance; municipal, custodian, and individual
attribution; Rule 15(c)(1)(C) notice; service; Rule 4(m) deadline and extension
facts; and authority-route analysis. Every relied-on authority route MUST state
the controlling jurisdiction, governing authority, pinpoint,
binding/precedential/current status, supported proposition, defendant-specific
application, sources, and unresolved status.

The record MUST continue to contain accrual and limitations dates, original Doe
or role description, same-transaction analysis, separate Rule 15(c)(1)(A) and
Rule 15(c)(1)(C) analyses, mistake-versus-lack-of-knowledge classification,
defendant-specific concealment or tolling facts, fallback claims, and severable
relief.

#### Scenario: Identity dates differ

- **WHEN** an identifying source was available or possessed before the plaintiff
  objectively could identify the defendant and actual identification occurred
  later
- **THEN** the record preserves each date and basis separately without treating
  one as proof of another

#### Scenario: Municipal custodian withheld a source

- **WHEN** a municipality or custodian controlled an identity source but the
  record does not support individual-defendant involvement
- **THEN** the record identifies the controller and request history without
  imputing that conduct to the individual defendant

#### Scenario: Notice differs from service

- **WHEN** the record supports Rule 15(c)(1)(C) notice but formal service
  occurred later or remains incomplete
- **THEN** notice facts and service facts remain separately complete entries

### Requirement: An incomplete limitations record blocks filing-ready status

The complaint workflow SHALL treat every missing, unsupported, malformed, or
unresolved required limitations-record entry as an internal filing-critical GAP
and MUST block filing-ready status. A structurally complete sourced entry may
state that notice, service, concealment, tolling, or another favorable fact was
not found; the deterministic checker MUST NOT decide the legal effect of that
fact. The workflow MUST route legal judgment to the agent and user without
adding an adverse merits characterization to filed text.

#### Scenario: Actual identification remains unresolved

- **WHEN** the plaintiff has not yet identified an intended individual defendant
- **THEN** the record preserves that distinct unresolved event, declares the
  filing-critical GAP, and blocks filing-ready status

#### Scenario: Supported record shows no notice

- **WHEN** the sources support a complete record stating that qualifying notice
  was not found
- **THEN** the validator accepts the record's structure without deciding whether
  relation back succeeds

### Requirement: Regression evaluation protects the limitations gate

The repository SHALL retain public-seam tests of the machine-readable record and
fresh-context behavioral pressure tests. Pressure scenarios MUST include an
unidentified intended defendant without an express warning, conflicting
availability/possession/identification dates, multiple Does, incomplete
authority application, deadline pressure, and an instruction to file
immediately. Verification MUST preserve the exact prompts and scored baseline
and corrected outputs.

#### Scenario: Agent is pressed to file with unresolved Does

- **WHEN** a fresh-context agent receives incomplete identity and authority
  facts plus an instruction to file immediately
- **THEN** the corrected skill preserves the separate facts, creates the
  defendant-specific filing-critical gaps, and does not claim filing-ready
  status

## ADDED Requirements

### Requirement: Installed complaint checker enforces limitations-record structure

The install-local complaint mechanical handoff MUST contain a machine-readable
`limitations_gate` object. It MUST declare intended-individual trigger facts and
one schema-conforming record for every affected individual. The installed
checker MUST deterministically validate trigger derivation, unique defendant and
record IDs, per-defendant cardinality, required fields and types, supported
status vocabularies, ISO dates, source-reference presence, and filing-critical
treatment of unresolved material.

The checker MUST retain fact truth, legal sufficiency, authority fit, relation
back, tolling, mistake, notice sufficiency, service sufficiency, strategy, and
filing readiness as excluded judgments.

#### Scenario: Applicable handoff omits the record

- **WHEN** the handoff declares a role-only intended defendant but supplies no
  matching limitations record
- **THEN** the installed checker returns a stable hard finding and a nonzero
  status

#### Scenario: Handoff supplies one record for two affected defendants

- **WHEN** two intended individual defendants are affected but only one record
  exists
- **THEN** the installed checker reports the missing defendant-specific record

#### Scenario: No intended individual is affected

- **WHEN** the handoff declares no affected intended individual and the empty
  limitations gate is structurally valid
- **THEN** limitations-record validation adds no finding
