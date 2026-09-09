# planning-section-1983-monell-claims Specification

## Purpose

TBD - created by archiving change monell-claim-contract-v2. Update Purpose after
archive.

## Requirements

### Requirement: Source-bounded Monell planning

The skill SHALL plan municipal-liability claims from the operative pleading,
operative rulings, approved record, verified authorities, and any supplied
validated municipal profile or on-disk graph. It MUST keep allegations, record
facts, supported inferences, disputed interpretations, and discovery targets
distinct.

#### Scenario: Planner receives mixed source classifications

- **WHEN** the record contains a complaint allegation, an official policy, a
  disputed interpretation, and a discovery lead
- **THEN** the plan preserves all four classifications and does not describe the
  discovery lead as an established fact

### Requirement: Separate path recommendations

The skill SHALL evaluate formal policy, custom or practice, final-policymaker
decision, ratification, failure to train, and failure to supervise or discipline
as separate candidate paths. It SHALL return `include`,
`include-with-narrowing`, `preserve-internal`, or `omit` with reasons, contrary
material, missing connections, and consequences for every evaluated path.

#### Scenario: Multiple paths have different support

- **WHEN** custom evidence is stronger than final-policymaker evidence
- **THEN** the planner returns separate recommendations and does not merge both
  paths into one generic Monell theory

### Requirement: Litigation principal retains path selection

The skill MAY rank and recommend supported paths, but SHALL identify the result
as a recommendation and SHALL require the litigation principal's decision before
drafting inclusion, narrowing, or abandonment.

#### Scenario: Planner recommends omission

- **WHEN** the planner concludes that a path is likely insufficient
- **THEN** it explains that conclusion but does not silently remove or abandon
  the path

### Requirement: Mechanisms remain distinct from liability paths

The skill SHALL represent FTO transfer, complaint review, arrest review, jail
intake, supervisory review, and rubber-stamp review as mechanisms or evidence
within an authority-supported Monell path, not as freestanding paths merely
because the mechanism exists.

#### Scenario: FTO conduct supports a training theory

- **WHEN** similar conduct occurs in an FTO relationship
- **THEN** the planner evaluates whether it supports an approved
  failure-to-train or custom path and does not label FTO status itself a Monell
  path

### Requirement: Optional read-only graph evaluation

When an explicit on-disk CaseGraph path is supplied, the skill SHALL validate
and evaluate the claim-relevant graph slice directly from its files without
invoking a CaseGraph CLI or writing to the graph.

#### Scenario: Valid graph slice is available

- **WHEN** the relevant configuration, nodes, references, sources, authority
  posture, procedural context, and pleading fingerprint validate
- **THEN** the planner may use the graph to render a traceable path assessment

#### Scenario: Graph is missing or invalid

- **WHEN** the graph is absent, incompatible, stale, or invalid
- **THEN** the planner reports the exact assessment status, continues with
  source-bounded planning when possible, and does not invent graph connections

### Requirement: Authority use requires verified pinpoint text

When the planner relies on a graph authority proposition, it SHALL resolve the
proposition to the verified authority source, canonical opinion artifact and
hash, cited pinpoint, and exact matching text. If that chain is incomplete, the
planner SHALL report the authority connection as unresolved and SHALL NOT use
the graph label as verified support.

#### Scenario: Graph proposition has only a citation label

- **WHEN** a proposition node identifies a case and pinpoint but cannot resolve
  the verified opinion artifact and exact matching passage
- **THEN** the planner treats the authority connection as incomplete and states
  the missing artifact, provenance, pinpoint, or text link

### Requirement: Deterministic planning handoff

The planner SHALL return one stable record per candidate path with its path ID,
type, common Monell fields, path-specific fields, recommendation, source
locations, graph assessment status, missing connections, and a field for the
litigation principal's decision.

#### Scenario: Planning completes before user decision

- **WHEN** all candidate paths have been evaluated but the user has not selected
  them
- **THEN** the handoff is complete as a planning artifact and every decision
  field remains explicitly pending

### Requirement: Every Monell proposition has an explicit class

The planning skill MUST classify every proposed Monell proposition as a source-
documented fact, a supported inference drawn from identified pleaded facts, or
an expected-discovery proposition. It MUST include those proposition records in
each path record and preserve their stable IDs through the approved planning
handoff. It MUST preserve attribution, temporal limits, and the factual basis
for every supported inference. An expected-discovery proposition MUST NOT be
treated as a present fact or evidence.

#### Scenario: Municipality-controlled directive is unavailable

- **WHEN** the current sources document repeated implementation but the expected
  written directive has not been obtained
- **THEN** the planner classifies the implementation facts and supported
  inference separately and preserves the directive only as expected discovery

#### Scenario: Supported inference uses an information-and-belief basis

- **WHEN** known facts support a narrow inference and municipality-controlled
  records are expected to clarify it
- **THEN** the planner records the known facts, controller, inference, affected
  fields, and expected information separately without treating the expected
  contents as true

### Requirement: Supported but incomplete paths have staged-development records

The planning skill MUST recommend pleading every presently supportable Monell
path at the narrowest factually plausible level and MUST NOT recommend a
speculative placeholder merely to preserve a claim. Every `preserve-internal`
path MUST identify its missing connection, expected records or testimony,
information controller, request-specific independent relevance to a named live
claim or defense, anticipated discovery restrictions or stays, request and
production dates, first-reasonably-knowable date, diligence chronology,
pleading-amendment deadline, evidence threshold for recommending amendment,
reassessment triggers, and limitations or relation-back risk. It MUST preserve
unknown values without inventing dates or expected facts.

#### Scenario: Incomplete path is preserved for discovery

- **WHEN** the current record supports a concrete Monell lead but not a
  plausible complaint allegation
- **THEN** the planner keeps the path internal, records each required staged-
  development field, and does not draft a placeholder allegation

### Requirement: Discovery and amendment remain conditional

The planning skill MUST NOT assume discovery is available merely because an
individual claim survives. Each proposed request MUST state its own relevance to
a named live claim or defense and account for applicable restrictions or stays.
The plan MUST reassess a preserved path when responsive material arrives and
before the amendment deadline. After a scheduling-order deadline, it MUST apply
the applicable Rule 16 good-cause standard, including diligence and the
explanation for delay, before Rule 15. Any recommendation to amend MUST rest on
the developed record and remain subject to litigation-principal approval.

#### Scenario: Responsive municipal records arrive after the deadline

- **WHEN** responsive material may satisfy a preserved path's evidence threshold
  after the scheduling-order amendment deadline
- **THEN** the planner updates the diligence record, analyzes Rule 16 good cause
  before Rule 15, and seeks principal approval before any amendment is drafted
