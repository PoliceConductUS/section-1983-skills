## ADDED Requirements

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
