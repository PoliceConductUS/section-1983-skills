# Design

## Context

`drafting-section-1983-complaints` is the canonical owner of the general
complaint and count contract. Its current machine handoff records generic count
fields and conditional qualified-immunity fields, while Monell requirements
remain prose-only. The repository has no separate Monell planning or drafting
skill. `building-municipal-monell-profiles` is deliberately neutral: it
organizes municipal evidence but does not choose a path, render liability
conclusions, or draft allegations.

The user approved separate Monell planning and drafting skills, a strict
contract-version migration, individual-capacity and Monell typed validation, and
optional legal assessment from a CaseGraph stored on disk. The CaseGraph CLI and
codebase are not dependencies. The supplied matter graph uses a `CaseHomeConfig`
in `casegraph/config.yaml` and typed nodes in `casegraph/<uid>/root.yaml`; the
evaluator must consume that representation directly and read-only.

## Goals

- Give Monell planning and drafting separate, independently installable owners.
- Permit supported recommendations without taking the litigation decision from
  the user.
- Require typed individual-capacity, qualified-immunity, and Monell analysis in
  every applicable complaint handoff.
- Fail closed on version-1 handoffs.
- Validate path-specific Monell differences without collapsing alternatives.
- Separate deterministic contract validation from reasoned legal assessment.
- Use a valid on-disk CaseGraph when available and expose exact fallback states
  when it is unavailable or unusable.
- Produce traceable opinions under an identified procedural lens without
  presenting them as court findings or historical adjudications.

## Non-goals

- Editing the active motion or proposed complaint in this change.
- Modifying the CaseGraph repository or adding a CaseGraph command.
- Requiring the CaseGraph CLI, a CaseGraph release, or a running service.
- Turning FTO, review, or jail-intake mechanisms into freestanding Monell paths
  without approved authority.
- Selecting claims, abandoning claims, filing, or making the user's final legal
  strategy decision.
- Treating a numerical score as an adjudication of truth or success probability.

## Decisions

### Separate planning and drafting owners

`planning-section-1983-monell-claims` consumes the record, verified authority,
the operative pleading and rulings, and an optional validated municipal profile
or on-disk graph. It inventories supported Monell paths, identifies missing
connections, and returns one of four recommendations for each path: `include`,
`include-with-narrowing`, `preserve-internal`, or `omit`. Every recommendation
states reasons, contrary material, missing connections, and consequences. The
skill does not silently convert a recommendation into the user's claim-selection
decision.

`drafting-section-1983-monell-claims` requires the approved planning record. It
drafts only approved paths and returns complaint deltas to the canonical general
complaint owner. It does not become a second whole-document owner.

### Monell path model

One complaint count may plead alternative Monell paths. The version-2 handoff
therefore retains the existing claim-defendant-capacity-challenged-act count
unit and adds a `monell_paths` collection. Every path has a stable `path_id` and
exactly one `path_type`. A path cannot merge multiple types into one omnibus
object.

All paths require:

- the challenged policy, custom, decision, or omission;
- concrete supporting facts and complaint locations;
- the municipal inference drawn from those facts;
- the attribution route;
- the implementation or transmission mechanism, when alleged;
- the underlying constitutional violation;
- the particular injury;
- the moving-force chain;
- the temporal lane; and
- a complete information-and-belief basis when that pleading form is used.

The path-specific fields are:

| Path type                            | Additional required analysis                                                                                                                    |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `formal_policy`                      | policy source and operative status; promulgating or adopting authority; application to the challenged conduct                                   |
| `custom_or_practice`                 | similar incidents; similarity rule; frequency, duration, or persistence; actual- or constructive-knowledge route                                |
| `final_policymaker_decision`         | decision, decisionmaker, source of final authority, timing, and causal application                                                              |
| `ratification`                       | subordinate act and basis, policymaker knowledge, approval or adoption, timing, and an injury the ratification can legally cause                |
| `failure_to_train`                   | precise task and deficiency, responsible authority, pattern-notice or approved single-incident basis, deliberate indifference, and causal chain |
| `failure_to_supervise_or_discipline` | precise supervisory or disciplinary deficiency, responsible authority, notice, deliberate indifference, and causal chain                        |

FTO instruction, review practices, jail handoffs, complaint review, and
rubber-stamp review are represented as mechanisms or supporting facts within an
approved path. Post-event material is assigned to a notice, ratification,
recurrence, later-injury, or corroboration lane and cannot silently supply
pre-event causation.

### Individual-capacity and qualified-immunity model

Every individual-capacity unit records the defendant's personal act or causal
role, event stage, relevant time, facts then known, underlying constitutional
violation, application, injury, and causation. Group pleading cannot satisfy a
missing actor-specific record.

When qualified immunity applies, the same unit records the incident date,
precise right, jurisdiction, each QI prong, pre-event authority, authority-audit
status, material similarities and differences, fair-warning application, and the
treatment of later authority. These fields are structural requirements; their
legal quality is evaluated only by the optional assessment layer or a human
reviewer.

### Strict version-2 migration

The canonical contract version changes from 1 to 2. The install-local validator
accepts only version 2. A version-1 handoff returns a stable
`unsupported_contract_version` failure with migration guidance. Historical
artifacts remain untouched, but they cannot be represented as passing current
validation.

The narrow validator lives with the canonical complaint skill because it
validates that skill's own handoff. This intentionally replaces the prior
external-checker-only boundary for the version-2 contract. It may verify JSON
shape, identifiers, cardinality, conditional fields, referenced paragraph
locations, and supplied fingerprints. It does not become a general graph engine
or a legal analysis tool. Project-configured checkers may consume the same
contract without displacing the canonical validator.

### Two-layer result model

Every check result separates:

1. `structural_validation`: deterministic version-2 contract findings; and
2. `casegraph_assessment`: optional reasoned evaluation from the on-disk graph.

The structural layer reports `pass` or `fail`. It never reports that facts are
true, authority is controlling, an analogy is persuasive, or a claim is legally
sufficient.

The assessment layer may render those judgments under a declared procedural
lens. Its statuses are:

- `completed`;
- `partial`;
- `not_run_missing`;
- `not_run_invalid`;
- `not_run_incompatible`; and
- `not_run_stale`.

No overall label may collapse an absent assessment into an unqualified pass.

### Direct on-disk CaseGraph adapter

The evaluator accepts an explicit graph-directory path. It does not search the
entire filesystem and does not invoke a binary. It reads `config.yaml` and
`<uid>/root.yaml` files directly. The adapter maintains an install-local list of
supported on-disk API versions and envelope requirements. The initial profile
supports the supplied `casegraph.policeconduct.org/v1alpha1` representation
without assuming that the current public CaseGraph `main` or CLI implements it.

Graph validation is claim-slice-specific. Before using a graph conclusion, the
evaluator verifies:

- the configuration and relevant node files parse;
- every relevant node has a recognized API version and kind-bearing envelope;
- every relevant directory name and `metadata.uid` agree;
- relevant UIDs are unique;
- every reference traversed for the assessment resolves;
- source paths and hashes are present where the conclusion depends on source
  content;
- the evaluated pleading or draft fingerprint matches;
- authority propositions identify their authority and case-specific posture;
- procedural context, relevant date, and governing jurisdiction are present; and
- the traversal can be reproduced from recorded node IDs and fields.

A parse failure, duplicate or mismatched relevant UID, unresolved relevant
reference, path escape, or pleading-fingerprint mismatch prevents use of the
affected graph slice. Unrelated graph defects are reported but do not invalidate
an otherwise independent slice. A structurally valid slice with missing
substantive nodes is incomplete, not invalid.

The evaluator never edits graph files, follows an unresolved write instruction,
or treats graph labels as self-proving. Each proposition retains its graph
classification, source treatment, review status, and contrary links.

### Legal assessment model

For each claim-defendant-capacity-challenged-act unit, the evaluator selects an
explicit lens such as Rule 12(b)(6). It then connects the claim to elements,
tests, defenses, authority propositions, allegations, incorporated material,
rulings, contrary paths, injury, and requested relief.

At Rule 12, the evaluator distinguishes allegations assumed true from
source-supported facts, reasonable inferences, disputed propositions,
contradicted propositions, judicial-notice candidates, and material outside the
permitted pleading universe. A court ruling is represented as a ruling in this
case, not as universal factual truth.

Each element or path component receives:

- `element_coverage`: `satisfied`, `partial`, `missing`, or `not_applicable`;
- `connection_quality`: `direct`, `strong_supported_inference`,
  `plausible_inference`, `weak_inference`, `unsupported`, or `contradicted`;
- `source_quality`;
- `procedural_usability`;
- `confidence`: `high`, `medium`, or `low`;
- `opinion`: `likely_sufficient`, `plausibly_sufficient_but_vulnerable`,
  `likely_insufficient`, or `indeterminate`; and
- an explanation citing the supporting path, contrary path, and missing
  connection.

The report may include transparent coverage counts, but no opaque composite
percentage or unstated weighting controls the opinion.

### Missing, invalid, stale, and incomplete graphs

If no graph path is supplied or the path does not exist, structural validation
continues and the assessment is `not_run_missing`. If the relevant files fail
validation, the assessment is `not_run_invalid` and lists the exact failures. An
unsupported on-disk API version produces `not_run_incompatible`. A pleading
fingerprint mismatch produces `not_run_stale`.

A valid graph with missing substantive connections produces `partial` and
`indeterminate` component opinions. The evaluator inventories missing
connections and does not infer absent nodes or edges. Structural success remains
visible, but it is never described as a merits or filing-readiness success.

### Drafting and filing modes

Drafting mode always runs the version-2 structural validator. When the graph is
missing or unusable, drafting may continue with the explicit unassessed status.

Filing mode requires a current graph assessment that ran across every included
claim unit. The assessment may contain reasoned `indeterminate` opinions, but it
cannot be missing, invalid, incompatible, stale, or skipped. Filing CI returns a
nonzero status when that requirement is unmet. Neither mode files a document or
overrides the litigation principal's approval.

## Data flow

1. The Monell planner builds typed candidate paths from approved sources and
   optional municipal-profile material.
2. If an on-disk graph is supplied, the planner validates and reads only the
   claim-relevant graph slice and attaches a traceable assessment.
3. The user approves, narrows, preserves, or rejects each recommended path.
4. The Monell drafter converts approved paths into complaint deltas.
5. The canonical complaint owner incorporates those deltas and emits a version-2
   handoff.
6. The install-local validator checks the handoff and fingerprints.
7. Filing CI reports structural and graph-assessment states separately and
   applies the selected drafting or filing mode.

## Verification strategy

Tests begin with synthetic handoffs that currently pass generic checks but omit
individual-capacity, QI, or Monell path structure. Version-2 validation must
reject them. Positive fixtures cover every Monell path type and QI unit.

On-disk graph fixtures cover a complete synthetic graph, missing graph,
malformed YAML, unsupported API version, UID mismatch, duplicate UID, unresolved
relevant reference, irrelevant broken reference, stale complaint hash, and
valid-but-incomplete claim slice. Behavioral evaluations test that the planner
recommends without deciding, the drafter uses only approved paths, and the
evaluator does not invent missing connections.

Repository validation includes focused tests, all skill validators, governance
classification, OpenSpec validation, the evaluation corpus, formatting, and
`npm run validate`.

## Risks and trade-offs

- **Graph labels may encode earlier analysis rather than verified facts.** →
  Preserve source classification, review status, contrary links, and procedural
  use in every conclusion.
- **A global graph error could make useful independent material unavailable.** →
  Validate the claim-relevant traversal slice and report unrelated defects
  separately.
- **A partial graph could be mistaken for an adverse merits conclusion.** → Use
  `partial` and `indeterminate`; inventory missing connections.
- **A structural pass could be mistaken for legal sufficiency.** → Keep the two
  result layers and labels separate in machine and human output.
- **Alternative Monell paths could be collapsed.** → Require stable path IDs and
  one type per path object.
- **Post-event evidence could be used to cause a completed injury.** → Require a
  temporal lane and path-specific causation analysis.
- **Version 2 breaks historical handoffs.** → Preserve files but reject them as
  current results with explicit migration guidance.

## Migration plan

1. Add RED contract, validator, graph-adapter, and behavioral fixtures.
2. Add the two public skill packages and governance entries.
3. Publish the version-2 complaint contract, validator, and result schema.
4. Update canonical complaint, specialization, umbrella, and Filing CI routing.
5. Migrate repository-owned synthetic fixtures to version 2.
6. Run focused and full validation.
7. Do not rewrite frozen case artifacts automatically; regenerate their handoffs
   only during an authorized drafting event.

Rollback reverts the branch before merge. After merge, rollback requires a new
change because accepting version 1 again would restore the known false-pass
condition.

## Open questions

None.
