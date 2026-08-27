# drafting-section-1983-complaints Specification

## Purpose

Define one complete install-local Section 1983 complaint contract, explicit
fail-closed routing and specialization boundaries, and a bounded mechanical
handoff for external structural checking.

## Requirements

### Requirement: Canonical complete complaint owner

The `drafting-section-1983-complaints` package SHALL be the only canonical owner
of the complete general Section 1983 complaint skeleton and detailed count
contract. It MUST provide both contracts through install-local references and
MUST require them for complaint drafting, revision, and audit.

#### Scenario: General complaint package is installed alone

- **WHEN** an agent receives only the `drafting-section-1983-complaints` package
  for a complaint task
- **THEN** the package supplies the ordered whole-document skeleton and the
  complete detailed count contract without relying on another skill package

#### Scenario: Canonical reference is unavailable

- **WHEN** either canonical complaint reference cannot be read
- **THEN** the package reports the complaint contract unavailable and does not
  invent or reconstruct the missing requirements

### Requirement: Ordered whole-document contract

The canonical complaint contract MUST define caption, optional introduction,
jurisdiction and venue, parties and capacities, chronological numbered facts,
separate counts, prayer for relief, jury demand, and signature block in that
order, subject only to a verified governing-court requirement.

#### Scenario: Agent constructs a complaint checklist

- **WHEN** an agent derives a complaint checklist from the canonical package
- **THEN** every required section appears once in canonical order and the
  introduction remains expressly optional

### Requirement: One detailed record per count tuple

The canonical complaint contract MUST require one count mapping for every
claim-defendant-challenged-act tuple. Each mapping SHALL identify the count,
constitutional source, defendant, capacity, challenged act, event stage,
governing standard and pinpoint, decisive-fact and incorporated paragraph
references, relevant-time knowledge, application, qualified-immunity material
when applicable, injury, relief, and result.

#### Scenario: One claim names two individual defendants

- **WHEN** the same legal claim is asserted against two individual defendants
- **THEN** the complaint contract requires two separately complete mappings
  rather than one collective count record

#### Scenario: One defendant performs two challenged acts

- **WHEN** the same legal claim challenges two legally distinct acts by one
  defendant
- **THEN** the complaint contract requires two separately complete mappings
  rather than one collective act record

#### Scenario: Qualified immunity does not apply

- **WHEN** a count is against a defendant or capacity that cannot assert
  qualified immunity
- **THEN** the qualified-immunity fields are inapplicable without relaxing any
  other required count field

### Requirement: Umbrella routing without fallback

The `section-1983-drafting` package MUST route every complaint, amended
complaint, and amendment proffer to `drafting-section-1983-complaints`. It MUST
NOT maintain or use a competing general complaint skeleton or count contract.

#### Scenario: Umbrella is installed without the canonical owner

- **WHEN** a complaint task reaches the umbrella package but the canonical
  complaint package is unavailable
- **THEN** the umbrella reports the complaint contract unavailable and does not
  draft or audit from a local fallback

### Requirement: Specialization contains only deltas

The `drafting-false-arrest-complaints` package MUST load the canonical general
complaint package first and SHALL add only false-arrest-specific requirements.
It MUST NOT restate or replace the generic whole-document skeleton or detailed
general count contract.

#### Scenario: False-arrest stack is complete

- **WHEN** all three packages are installed for a false-arrest complaint
- **THEN** the general package supplies the one complete general contract and
  the false-arrest package supplies only its seizure, offense, actor,
  chronology, incorporated-material, and compression deltas

#### Scenario: General complaint owner is unavailable

- **WHEN** the false-arrest package is installed without the canonical general
  complaint package
- **THEN** it reports the complaint contract unavailable and does not promote
  its delta into a replacement general contract

### Requirement: Install-local and behavioral verification

The repository MUST verify that each package's live local links remain confined
to that package and that realistic isolated compositions either supply the one
complete contract or fail closed. Instruction behavior MUST be pressure-tested
in fresh contexts before and after the change.

#### Scenario: Package is installed independently

- **WHEN** any affected package is copied without the repository root
- **THEN** every live local link resolves within that package and no dependency
  is represented by a broken cross-package file link

#### Scenario: Agent faces pressure to fill a missing contract

- **WHEN** deadline, authority, or sunk-cost pressure encourages an agent to
  draft from an incomplete or conflicting composition
- **THEN** the agent uses the canonical owner or reports the contract
  unavailable without inventing or silently reconciling requirements

### Requirement: Filed complaint does not assess its own legal weakness

The canonical complaint contract MUST distinguish accurate factual/source
qualification from an adverse legal merits assessment. Filed text MUST NOT
volunteer that a pleaded claim, element, fair-warning path, or
qualified-immunity position is weak, likely to fail, likely barred, or otherwise
legally deficient. Legal risk assessment MUST be routed to versioned strategy or
internal audit work without concealing adverse evidence or authority.

#### Scenario: Source leaves an event fact unresolved

- **WHEN** the available source does not resolve a material event fact
- **THEN** the complaint may identify the source limitation and supported
  alternatives without characterizing the claim itself as weak

#### Scenario: Drafter doubts prong two

- **WHEN** the drafter believes the clearly-established-law path may fail
- **THEN** the assessment is recorded internally and the filed complaint either
  states a supportable fair-warning path or reports a filing-critical GAP for a
  reserved strategy decision

#### Scenario: Alternative pleading is authorized

- **WHEN** supported facts permit alternative or conditional pleading
- **THEN** the complaint may plead those alternatives without treating the
  procedural qualification as an adverse concession

### Requirement: Complaint-level fair-warning analysis remains bounded

Each distinct complaint-level fair-warning proposition MUST ordinarily use one
verified lead binding pre-event authority and the decisive factual comparison.
Any additional complaint-level authority MUST perform a separately identified
job. Full comparison matrices, competing case discussions, later history, and
string cites MUST remain in internal work product or a brief unless needed for a
separately identified complaint-level proposition.

#### Scenario: One case supplies the fair-warning proposition

- **WHEN** one verified binding pre-event case supplies the relevant rule and
  decisive factual comparison
- **THEN** the complaint uses that lead authority without reproducing the
  internal multi-case matrix

#### Scenario: A second case performs a distinct job

- **WHEN** another authority is necessary for a separate controlling proposition
  or precedential link
- **THEN** the complaint identifies that distinct job rather than adding an
  unexplained string cite

### Requirement: One canonical tuple checklist governs count completion

The complaint contract MUST define one canonical checklist for every
claim–defendant–challenged-act tuple. The universal fields MUST be the claim,
defendant, challenged act and event stage, governing element or standard,
decisive facts, facts known to the defendant at the legally relevant time,
resulting element-specific legal application, and result. For every
qualified-immunity-eligible individual-capacity tuple, the same checklist MUST
also require the event date; conduct-specific right or rule; verified binding
pre-event authority; authority-audit status; materially similar facts; material
differences; defendant-specific fair warning; rule-of-orderliness and later-
history review status; and separate prong-one and prong-two results.

The complaint contract MUST own these field names and the completion rule, but
MUST NOT duplicate the detailed authority-verification procedure owned by
`audit-authorities`. A missing or unverified universal field makes the tuple
incomplete. A missing or unverified qualified-immunity field creates an internal
filing-critical GAP, blocks filing-ready status, and routes the issue for a
reserved strategy decision without adding an adverse merits assessment to filed
text.

The install-local mechanical handoff MUST use the same tuple cardinality and
machine-readable field names. Capacity remains a required tuple field, but it
MUST NOT replace challenged act in the tuple cardinality. The handoff remains a
non-executable interface and MUST NOT claim to perform the authority audit.

#### Scenario: Universal application bridge is incomplete

- **WHEN** a count states decisive facts but omits the defendant's relevant-time
  knowledge or the resulting element-specific application
- **THEN** the tuple remains incomplete and the complaint cannot be marked
  filing-ready

#### Scenario: Fair-warning verification is incomplete

- **WHEN** a qualified-immunity-eligible tuple lacks verified authority status
  or completed rule-of-orderliness and later-history review
- **THEN** the internal record contains a filing-critical GAP, filing-ready
  status is blocked, and the filed complaint does not volunteer an adverse
  merits assessment

### Requirement: Uncertain factual paragraphs perform a pleaded function

The completion audit MUST inventory every factual paragraph the draft labels
unresolved, unknown, unrelated, or non-establishing. Each retained paragraph
MUST identify at least one function: an element, an actual defense premise, a
material chronology function, or a candor/preservation function. A paragraph
with no such function MUST be removed from filed text or moved to internal
chronology.

#### Scenario: Unresolved detail serves no pleaded job

- **WHEN** a paragraph says a detail is unresolved but maps to no element,
  defense premise, chronology need, or candor/preservation duty
- **THEN** the completion audit directs that paragraph out of filed text

#### Scenario: Unresolved detail preserves a material source limit

- **WHEN** an unresolved fact is material and the source limitation must be
  disclosed accurately
- **THEN** the audit records the candor/preservation function and retains only
  the bounded necessary statement

### Requirement: Material incorporated-record ambiguity completes the offense analysis

The false-arrest specialization SHALL, for each alternative offense actually
raised by the defense, a controlling ruling, or governing law, identify any
incorporated-record fact left unresolved that is material to an offense element.
Without admitting the fact occurred, the count MUST either state the supported
element-level reason the unresolved fact does not supply probable or arguable
probable cause or record a filing-critical GAP for reserved strategy decision.
The specialization MUST NOT inventory merely conceivable offenses.

#### Scenario: Recording leaves possible conduct unresolved

- **WHEN** a recording leaves possible conduct unresolved and the conduct is
  material to an element of an actually raised alternative offense
- **THEN** the count identifies the disputed fact and element and either
  completes the supported probable-cause analysis without an admission or logs a
  filing-critical GAP

#### Scenario: Offense is merely conceivable

- **WHEN** no defense, controlling ruling, or governing law has made an offense
  material
- **THEN** the skill does not add that offense to the pleading or matrix

### Requirement: Packaged mechanical complaint check

The complaint package SHALL ship a deterministic helper that reads the
install-local `complaint-structure-contract.json`, the declared `filing` input
root, and an optional canonical relative filing target. It SHALL implement only
the contract's section/order, numbering, identifier, tuple/cardinality,
cross-reference, incorporation, and required-field-presence checks. It MUST
return stable finding identifiers, nonzero failure status, one canonical
output-relative mechanical-report path, and deterministic report bytes for
trusted-host publication. It MUST NOT require or invoke an external configured
checker.

#### Scenario: Declared complaint target is checked

- **WHEN** the caller supplies an existing complaint target in the declared
  `filing` role
- **THEN** the packaged helper returns deterministic mechanical findings and the
  trusted host may publish the report append-immutably

#### Scenario: New complaint has no input target

- **WHEN** the operation drafts a new complaint and omits the optional filing
  target
- **THEN** drafting may produce a new output artifact, but a later mechanical
  check must consume that artifact through a new declared-input invocation
  before any check can be reported complete

#### Scenario: Requested check requires legal judgment

- **WHEN** a requested check concerns fact truth, legal sufficiency, authority
  fit, material analogy, strategy, or filing readiness
- **THEN** the packaged contract identifies that question as excluded and does
  not represent it as a mechanical finding

### Requirement: Complaint helper is install-local and input confined

The mechanical checker MUST ship inside the complaint skill package, work when
that package is installed alone, accept only declared input-root plus canonical
relative target or validated in-memory bytes, and emit deterministic results. It
MUST NOT import root scripts, accept an output root, mutate input, access an
undeclared path, use the internet, create a receipt, or dispatch a command.

#### Scenario: Complaint package is isolated

- **WHEN** the package is copied without repository-root files and supplied a
  valid declared filing root and target
- **THEN** the same mechanical finding bytes are produced without any external
  runtime dependency

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

### Requirement: Each actor unit contains its own decisive application bridge

Every claim–Defendant–challenged-act unit MUST identify its own incorporated
factual paragraphs and MUST directly state the Defendant's challenged act and
event time, decisive facts known to that Defendant then, disputed claim or
offense element, application of those then-known facts to that element, personal
causal role, resulting injury, and Defendant-specific application of
qualified-immunity prongs one and two when qualified immunity applies. A
paragraph range plus a conclusion does not perform the application.

Functional closure controls. The contract MUST NOT impose a fixed paragraph
count or require needless repetition. A supporting brief MAY expand authority
comparisons or competing record interpretations but MUST NOT supply a missing
complaint-level factual bridge.

#### Scenario: Different actors share omnibus incorporation

- **WHEN** Defendants acted at different stages or possessed different
  information and their units use one omnibus incorporation qualified by “to the
  extent applicable”
- **THEN** each unit remains incomplete until it identifies its own incorporated
  paragraphs and directly performs the actor-specific application

#### Scenario: Actor unit supplies only a paragraph range

- **WHEN** a unit states that the relevant facts appear in a paragraph range and
  then states an element or qualified-immunity conclusion
- **THEN** the unit remains incomplete because the court must construct the
  decisive fact-to-element bridge

#### Scenario: Supporting brief expands a complete unit

- **WHEN** the complaint contains the compact decisive bridge and a supporting
  brief adds fuller authority comparisons
- **THEN** the unit may be complete without duplicating the entire brief

### Requirement: Later facts in an arrest-time unit have an express limited function

The canonical complaint contract MUST require an express limited-use statement
when an arrest-time actor unit incorporates a report, prosecution, suppression,
dismissal, identification, resistance, or other fact occurring after the
challenged act. The unit MUST state that fact's limited later function and that
the fact is not part of the Defendant's earlier relevant-time knowledge. A
later-only fact MUST NOT enter the earlier knowledge set by incorporation.

#### Scenario: Arrest unit incorporates a later report

- **WHEN** an arrest-time actor unit incorporates paragraphs describing a later
  report or prosecution
- **THEN** the unit identifies the later function and excludes those facts from
  the officer's arrest-time knowledge

### Requirement: False-arrest units close officer-specific offense analysis

The false-arrest specialization MUST require one closed application for every
officer whose seizure or continued seizure is challenged. That application MUST
identify the seizure point; suspected offense and every alternative offense
actually raised by an opponent, controlling ruling, or governing law; facts
known to that officer then; the missing or disputed element of each material
offense; exclusion or limited later function of post-seizure facts;
probable-cause and arguable-probable-cause application; personal participation
and causal stage; resulting injury; and conduct-specific fair warning and
QI-prong results.

#### Scenario: Officers acted with different knowledge

- **WHEN** one officer initiates a seizure and another continues it after
  receiving different information
- **THEN** each officer's unit separately applies that officer's relevant-time
  facts to every material offense, causation, injury, and both QI prongs

#### Scenario: Merely conceivable offense

- **WHEN** no opponent, controlling ruling, or governing law has made an
  alternative offense material
- **THEN** the closed-unit requirement does not add that offense to the pleading

### Requirement: Completion audit rejects open actor units

The completion audit MUST fail when the court must search several factual
sections and construct the fact-to-element analysis; actors with different acts,
stages, or knowledge share broad incorporation without closed individual
applications; a QI paragraph gives only a paragraph range and conclusion;
later-only facts enter an earlier knowledge set without an express statement
excluding them from that earlier knowledge set; or a supporting brief is needed
to cure a missing complaint-level application. Every unresolved required
component MUST be filing-critical.

#### Scenario: Brief is the only source of application

- **WHEN** the complaint lists facts and conclusions but only the supporting
  brief connects them for a particular Defendant and challenged act
- **THEN** the complaint audit fails and records a filing-critical gap
