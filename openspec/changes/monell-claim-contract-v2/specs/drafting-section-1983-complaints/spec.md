## MODIFIED Requirements

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

### Requirement: Deterministic complaint-contract validation

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

## ADDED Requirements

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

### Requirement: Stable graph fallback states

Graph assessment SHALL return exactly one of `completed`, `partial`,
`not_run_missing`, `not_run_invalid`, `not_run_incompatible`, or
`not_run_stale`, with bounded diagnostics for every non-completed state.

#### Scenario: Pleading fingerprint differs

- **WHEN** the graph references a different pleading fingerprint from the draft
  under review
- **THEN** assessment is `not_run_stale` and graph conclusions are not reused
