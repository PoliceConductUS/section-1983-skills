# drafting-section-1983-monell-claims Specification

## Purpose

TBD - created by archiving change monell-claim-contract-v2. Update Purpose after
archive.

## Requirements

### Requirement: Approved-path drafting gate

The skill SHALL draft only from a Monell planning handoff that records the
litigation principal's decision for every included path. It SHALL fail closed
when a requested path remains pending or when the planning contract is absent.

#### Scenario: Path remains pending

- **WHEN** a planning record recommends inclusion but has no user decision
- **THEN** the drafter reports the gate and does not draft that path

### Requirement: Path-specific complaint deltas

The skill SHALL draft each approved Monell path separately with its common and
path-specific fields, supporting complaint paragraphs, authority, attribution,
injury, and moving-force application. It SHALL NOT merge different path types
into an omnibus path object.

#### Scenario: Custom and failure-to-train paths are approved

- **WHEN** both paths are approved for one municipal count
- **THEN** the drafter returns two separately identified alternatives under the
  count rather than one blended allegation

### Requirement: Information-and-belief foundation

Every information-and-belief allegation SHALL identify the known facts, the
specific information controlled by the municipality, the municipal controller,
and the inference drawn. A promise that discovery will supply the theory SHALL
NOT satisfy this requirement.

#### Scenario: Municipality controls review records

- **WHEN** the allegation depends on nonpublic review records
- **THEN** the draft states the known external facts, identifies the controlled
  records and controller, and explains the resulting inference

### Requirement: Temporal and causal separation

The skill SHALL assign pre-event notice, event implementation, post-event
ratification, recurrence, later injury, and corroboration to separate temporal
lanes. It SHALL connect each fact only to an injury it can legally be alleged to
cause under the approved path.

#### Scenario: Review occurs after a completed arrest

- **WHEN** a post-arrest review is offered as support
- **THEN** the draft does not use that review as pre-arrest notice or as a cause
  of the already completed arrest unless approved authority and a distinct
  legally cognizable causal theory support that use

### Requirement: Canonical-owner handoff

The skill SHALL return complaint deltas and version-2 Monell path records to
`drafting-section-1983-complaints`. It SHALL NOT independently own the full
complaint skeleton, final integration, or filing decision.

#### Scenario: Approved drafting completes

- **WHEN** all approved paths have been drafted
- **THEN** the output identifies insertion targets, supporting paragraphs, path
  records, and unresolved gates for the canonical complaint owner

### Requirement: Integrated Monell text receives shared assertion validation

The Monell drafting skill MUST hand its approved-path deltas to the canonical
complaint owner and MUST require the integrated whole-document candidate to use
`validating-court-facing-assertions`. It MUST NOT describe an isolated delta as
whole-document validation or use validation findings to select, narrow, or omit
a Monell path without the plaintiff's decision.

#### Scenario: Monell delta is valid before integration

- **WHEN** an approved-path delta satisfies its local contract but has not been
  integrated into the complaint
- **THEN** the skill reports delta completion without claiming that complaint
  assertions, omissions, or rendered output have been validated

### Requirement: Monell proposition placement follows classification

The drafting skill MUST limit complaint allegations to source-documented facts
and supported inferences whose identified factual basis, attribution, and
temporal limits are pleaded. It MUST carry every classified proposition from the
approved planning handoff into the typed delta and map it to an integrated
complaint paragraph or discovery-plan location. Expected-discovery propositions
MUST remain in the discovery plan and MUST NOT appear in the complaint as
present facts or evidence. A supporting brief MAY explain why pleaded facts
support a reasonable inference, but it MUST NOT supply a missing complaint-level
factual basis.

#### Scenario: Expected records have not been obtained

- **WHEN** a proposed complaint expects municipal training or complaint-history
  records to support a path but the present sources do not contain those records
- **THEN** the complaint omits those expectations as present support, the
  discovery plan preserves them, and any brief relies only on the complaint's
  pleaded factual basis

### Requirement: Drafting does not use a placeholder to preserve a Monell path

The drafting skill MUST NOT draft boilerplate, the underlying incident alone, or
expected-discovery propositions as a Monell allegation merely to preserve a
path. A previously preserved internal path MUST enter drafting only when its
recorded evidence threshold is met, current support is sufficient under the
approved planning record, the applicable amendment gate is satisfied, and the
litigation principal approves amendment.

#### Scenario: Preserved path remains below its evidence threshold

- **WHEN** discovery has not established the missing connection identified in
  the staged-development record
- **THEN** the drafter leaves the path out of complaint prose and returns it for
  continued internal planning
