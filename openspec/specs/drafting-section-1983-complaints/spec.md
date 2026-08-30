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
claim-defendant-capacity-challenged-act tuple. Each mapping SHALL identify the
count, constitutional source, defendant, capacity, challenged act, event stage,
governing standard and pinpoint, decisive-fact and incorporated paragraph
references, relevant-time knowledge, application, typed individual-capacity and
qualified-immunity material when applicable, typed Monell paths when applicable,
injury, relief, and result.

#### Scenario: One claim names two individual defendants

- **WHEN** the same legal claim is asserted against two individual defendants
- **THEN** the complaint contract requires two separately complete mappings
  rather than one collective count record

#### Scenario: One claim names one defendant in two capacities

- **WHEN** the same legal claim is asserted against one defendant in individual
  and official capacities
- **THEN** the complaint contract requires two separately complete mappings and
  applies the correct individual or municipal conditional fields to each

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

### Requirement: Deterministic external-checker handoff

The canonical package SHALL publish one machine-readable contract identifying
the owner, version, ordered sections, count cardinality, required fields,
conditional individual-capacity, qualified-immunity, and Monell fields,
mechanical checks, structural exclusions, graph-assessment interface, and stable
finding shape. The package SHALL include a narrow install-local validator for
that handoff. The validator MUST NOT become a general graph engine or represent
reasoned legal judgments as deterministic findings. A project-configured
external checker MAY consume the same contract.

#### Scenario: Install-local validator reads the handoff

- **WHEN** the canonical package validates a version-2 handoff
- **THEN** it checks section and order, numbering, identifiers, tuple
  cardinality, cross-references, incorporation, conditional field presence, and
  supplied fingerprints with stable finding identifiers and nonzero structural
  failure status

#### Scenario: External checker reads the handoff

- **WHEN** a project-configured checker consumes the machine-readable contract
- **THEN** it derives the same deterministic structural requirements without
  weakening the canonical validator

#### Scenario: Requested deterministic check requires legal judgment

- **WHEN** a requested structural check concerns fact truth, legal sufficiency,
  authority fit, material analogy, strategy, or filing readiness
- **THEN** structural validation identifies that question as excluded rather
  than representing it as deterministic, while a separately labeled on-disk
  graph assessment MAY render a traceable reasoned opinion

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

### Requirement: Strict complaint contract version 2

The canonical complaint owner SHALL publish and validate contract version 2. The
validator MUST reject version-1 handoffs as `unsupported_contract_version`; it
MUST NOT accept a legacy mode that can be reported as a current pass.

#### Scenario: Historical handoff uses version 1

- **WHEN** the validator receives a version-1 handoff
- **THEN** it returns a deterministic failure with migration guidance and does
  not alter the historical artifact

### Requirement: Typed individual-capacity units

Every individual-capacity claim-defendant-challenged-act unit SHALL record the
defendant's personal act or causal role, event stage, relevant time, facts then
known, underlying constitutional violation, application, injury, and causation.

#### Scenario: Generic group allegation lacks personal role

- **WHEN** a handoff names several officers but omits one officer's personal act
  or causal role
- **THEN** structural validation fails for that officer's unit

### Requirement: Typed qualified-immunity units

When qualified immunity applies, the individual unit SHALL additionally record
the incident date, precise right, governing jurisdiction, both QI prongs,
pre-event authority, authority-audit status, material similarities and
differences, fair-warning application, and later-authority treatment.

#### Scenario: QI unit lacks pre-event authority treatment

- **WHEN** qualified immunity applies and the handoff omits pre-event authority
  or an approved obvious-case analysis
- **THEN** structural validation fails without purporting to decide the quality
  of any authority supplied

### Requirement: Typed Monell path units

Every municipal claim unit SHALL contain one or more `monell_paths`. Every path
SHALL have a stable path ID, exactly one approved path type, all common Monell
fields, and all fields conditional on that path type. Alternative paths MAY
share a count but SHALL remain separate path objects.

#### Scenario: Municipal count has no typed path

- **WHEN** a municipal count contains only generic count fields
- **THEN** structural validation fails

#### Scenario: One path object merges two types

- **WHEN** one object identifies both custom and failure to train as its type
- **THEN** structural validation fails and identifies the omnibus object

### Requirement: Path-specific conditional fields

The version-2 contract SHALL define distinct conditional fields for formal
policy, custom or practice, final-policymaker decision, ratification, failure to
train, and failure to supervise or discipline.

#### Scenario: Custom path omits recurrence and knowledge

- **WHEN** a custom path omits similar incidents, persistence, or its
  policymaker-knowledge route
- **THEN** structural validation fails only the missing custom requirements

#### Scenario: Formal-policy path has no custom pattern

- **WHEN** a formal-policy path otherwise identifies the operative policy,
  attribution, and application but has no recurring-incident pattern
- **THEN** the validator does not impose custom-only recurrence fields

### Requirement: Separate structural and graph-assessment results

Every result SHALL expose `structural_validation` separately from
`casegraph_assessment`. Structural success MUST NOT be labeled merits success or
filing readiness when graph assessment did not run.

#### Scenario: Structure passes without a graph

- **WHEN** version-2 structure passes and no graph path is supplied
- **THEN** the result reports structural pass and
  `casegraph_assessment: not_run_missing`

### Requirement: Direct read-only on-disk graph assessment

When an explicit graph path is supplied, assessment SHALL read the recognized
configuration and node files directly, validate the claim-relevant traversal
slice, and remain read-only. It SHALL NOT invoke or require a CaseGraph CLI.

#### Scenario: Relevant graph slice validates

- **WHEN** all relevant envelopes, UIDs, references, provenance, procedural
  context, and pleading fingerprints validate
- **THEN** the evaluator may render a traceable legal assessment

#### Scenario: Unrelated reference is broken

- **WHEN** an unrelated graph node has a broken reference but the evaluated
  claim slice is independent and valid
- **THEN** the evaluator reports the unrelated defect without invalidating the
  claim slice

### Requirement: Traceable legal opinion

Graph assessment SHALL identify its procedural lens and report element coverage,
connection quality, source quality, procedural usability, confidence, opinion,
supporting paths, contrary paths, and missing connections for every assessed
unit. It SHALL NOT use an opaque composite percentage as the opinion.

#### Scenario: Rule 12 graph assessment is incomplete

- **WHEN** a valid graph lacks a required policymaker-attribution connection
- **THEN** the affected component is `indeterminate` or incomplete, the missing
  connection is identified, and no edge is invented

### Requirement: Verified authority pinpoint and exact-text resolution

Every authority proposition used in a graph assessment SHALL resolve from the
proposition node through its authority reference to a verified authority unit,
that unit's source metadata, the canonical opinion artifact and matching hash,
the cited pinpoint, and an exact matching passage in a provenance-linked text
representation. The assessment SHALL record the matched text and stable source
locator. A citation string, reporter pinpoint, graph label, or semantic near
match alone SHALL NOT satisfy this requirement.

#### Scenario: Pinpoint and exact passage resolve

- **WHEN** the authority reference, verified source metadata, canonical opinion
  hash, provenance-linked text, pinpoint, and exact passage all resolve
- **THEN** the authority connection is `resolved` and the assessment records the
  artifact identities, hashes, pinpoint, exact text, locator, and any
  deterministic normalization applied

#### Scenario: Citation exists but source text does not match

- **WHEN** an authority proposition supplies a citation and pinpoint but the
  verified source has no exact matching passage at that pinpoint
- **THEN** the authority connection is `text_mismatch` or `pinpoint_unresolved`,
  the dependent component is incomplete, and the evaluator does not substitute a
  semantic or fuzzy match

#### Scenario: Derived opinion text lacks provenance

- **WHEN** exact text appears in a derived representation that is not linked by
  verified provenance to the hashed canonical opinion
- **THEN** the representation is unusable for authority resolution and the
  dependent component remains incomplete

### Requirement: Stable graph fallback states

Graph assessment SHALL return exactly one of `completed`, `partial`,
`not_run_missing`, `not_run_invalid`, `not_run_incompatible`, or
`not_run_stale`, with bounded diagnostics for every non-completed state.

#### Scenario: Pleading fingerprint differs

- **WHEN** the graph references a different pleading fingerprint from the draft
  under review
- **THEN** assessment is `not_run_stale` and graph conclusions are not reused
