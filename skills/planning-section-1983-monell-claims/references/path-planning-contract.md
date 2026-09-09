# Monell path-planning contract

## Common record

Evaluate each of the six recognized path types. Create one record for every
distinct candidate policy, custom, decision, or omission, allowing multiple
records of the same type, and an explicit `omit` record when a type has no
candidate. Use a stable `path_id` and one `path_type`. Record:

1. challenged policy, custom, decision, or omission;
2. supporting facts and source or pleading locations;
3. a `propositions` collection using the classification contract below;
4. inference classification and municipal inference;
5. attribution route;
6. implementation or transmission mechanism;
7. underlying constitutional violation;
8. particular injury;
9. moving-force chain;
10. `temporal_lanes`, mapping each supporting fact to every applicable lane;
11. information-and-belief basis, when used;
12. contrary material;
13. missing connections;
14. recommendation, reasons, and consequences;
15. `graph_assessment_status` for that path;
16. `principal_decision`, using the typed record below; and
17. `staged_development`, required when the recommendation is
    `preserve-internal`.

## Proposition classes

Every proposed Monell proposition must be classified as:

- `source_documented_fact`: a source-documented fact with its attribution,
  temporal limits, and source locations;
- `supported_inference`: a supported inference with its attribution, temporal
  limits, the identified pleaded facts from which it is drawn, and the reasoning
  connecting them; or
- `expected_discovery`: an expected-discovery proposition preserved in the
  discovery plan.

Every proposition record must have a stable `proposition_id`, its proposed text,
and exactly one of those classes. A source-documented fact identifies its
source. A supported inference identifies its pleaded factual premises. An
expected-discovery proposition identifies its discovery-plan location and is not
a present fact or evidence.

The fact that records are municipality-controlled may itself be documented. The
expected contents of unavailable records remain expected discovery. A proposed
information-and-belief allegation qualifies as a supported inference only when
its existing known facts and complete basis satisfy the information-and-belief
contract below; expected discovery alone cannot supply that basis.

Before selection, `principal_decision` is `{ "status": "pending" }`. Approval
replaces it with `status: approved`, approver identity, approval scope, approved
narrowing, decision-record path, and decision-record SHA-256. Rejection uses
`status: rejected` and its decision-record path and hash. A recommendation
cannot populate or change this record.

An FTO method, jail handoff, complaint review, classification practice, or
rubber-stamp review is a mechanism or supporting fact inside an authorized
Monell path unless verified authority establishes a separate path. Identify the
employee who implemented the mechanism and the source of the inference; do not
invent an unknown supervisor or policymaker.

When repeated employees implement the same stated policy, evaluate that evidence
under `formal_policy` as well as any supported `custom_or_practice` alternative.
The `formal_policy` record may use information-and-belief pleading for the text,
operative status, or adopting authority only when it identifies the repeated
implementation facts, the records expected to confirm the allegation, and the
municipality controlling those records. Do not invent a written policy or final
policymaker.

## Information and belief

When information-and-belief pleading is proposed, record an
`information_and_belief_basis` object with `used`, `known_facts`,
`expected_information`, `controller`, `inference`, and `affected_fields`. When
`used` is true, every other field is required. The known facts and controller
must be source-bounded. `expected_information` identifies discovery targets; it
does not establish their contents. The proposed allegation is a
`supported_inference` only when the known facts and stated reasoning support the
inference without assuming the expected information is true.

## Path-specific records

- `formal_policy`: policy source, operative status, adopting or promulgating
  authority, and application to the conduct.
- `custom_or_practice`: similar incidents, similarity rule, frequency, duration
  or persistence, and actual- or constructive-knowledge route.
- `final_policymaker_decision`: decision, decisionmaker, source of final
  authority, timing, and causal application.
- `ratification`: subordinate act and basis, policymaker knowledge, approval or
  adoption, timing, and an injury the ratification can legally cause.
- `failure_to_train`: precise task and deficiency, responsible authority,
  pattern-notice or verified single-incident basis, deliberate indifference, and
  causal chain.
- `failure_to_supervise_or_discipline`: precise deficiency, responsible
  authority, notice, deliberate indifference, and causal chain.

## Temporal lanes

Assign each fact to the legally relevant lane. Pre-event material may address
notice, adoption, knowledge, mechanism, or causation. Post-event material may
address later notice, ratification, recurrence, later-injury, or corroboration.
Post-event material cannot supply pre-event causation or pre-event notice merely
because it resembles the earlier event. It may support that an already-existing
FTO or review mechanism transmitted a practice only if the sources and inference
support that distinct proposition.

## Recommendations

Use exactly one:

- `include`: the current record supports pleading the path without a
  load-bearing unresolved connection.
- `include-with-narrowing`: a narrower formulation is supported and the
  limitation is identified.
- `preserve-internal`: the path is a supported discovery or strategy lead but is
  not approved for filed allegations on the present record.
- `omit`: identified authority or record defects make the path unsuitable for
  the proposed pleading.

A recommendation is advice, not selection. Identify the consequences and await
the litigation principal's approval before drafting.

## Staged development

Plead each presently supportable Monell path at the narrowest factually
plausible level. Do not recommend boilerplate, the underlying incident alone, or
a speculative placeholder merely to preserve a claim. A supported but incomplete
path remains an internal discovery lead through
`recommendation: preserve-internal`.

Every preserved path must include a `staged_development` object with:

- `missing_connection`: the exact unresolved connection preventing a presently
  supportable allegation;
- `expected_records_or_testimony`: the identified material expected to resolve
  that connection, without predicting its contents as fact;
- `information_controller`: who controls each identified item;
- `discovery_requests`: one record per proposed or served request, each with a
  stable request ID, target material, independent relevance to a named live
  claim or defense, anticipated discovery restrictions or stays, `requested_at`,
  `produced_at`, and `first_reasonably_knowable_at`;
- `diligence_record`: the dated requests, responses, objections, rulings,
  follow-ups, productions, and review steps relevant to later amendment;
- `pleading_amendment_deadline`: the exact deadline and source, or an explicit
  unknown with the step needed to resolve it;
- `evidence_threshold_for_amendment`: the path-specific connection and support
  that must be established before recommending amendment;
- `reassessment_triggers`: responsive material arriving and a review before the
  amendment deadline, plus any path-specific trigger; and
- `limitations_or_relation_back_risk`: the current path-specific risk and
  governing dates or an explicit unresolved status.

Use explicit `not_requested`, `not_produced`, `unknown`, or `not_applicable`
values where a date or status does not exist. Never invent a date, the expected
contents of unavailable material, or a discovery outcome.

A relative deadline interval such as “21 days away” is not an exact date. Do not
calculate or derive an exact deadline from a relative interval unless the
controlling order and a source-backed as-of date are both identified. Otherwise,
record the exact date as `unknown`, preserve the relative statement with its
source, and obtain the order.

### Discovery conditions

Do not assume that surviving individual claims guarantee municipal discovery.
For each request, explain its independent relevance to a named live claim or
defense rather than assigning a general “qualified immunity,” “punitive
damages,” or “Monell” label. Record anticipated discovery restrictions or stays
and the request-specific scope needed under the current procedural posture.

### Amendment conditions

Reassess each preserved path when responsive material arrives and before the
pleading amendment deadline. Compare the material to the recorded evidence
threshold; production alone does not establish the path.

Before the scheduling-order deadline, record the governing amendment standard
and current diligence posture. After the deadline, analyze the applicable Rule
16 good-cause standard, including diligence and the explanation for delay,
before applying Rule 15. Do not assume amendment will be permitted. Any
recommendation to amend must be supported by what the record actually
establishes and remains subject to the litigation principal's approval.
