# Monell path-planning contract

## Common record

Evaluate each of the six recognized path types. Create one record for every
distinct candidate policy, custom, decision, or omission, allowing multiple
records of the same type, and an explicit `omit` record when a type has no
candidate. Use a stable `path_id` and one `path_type`. Record:

1. challenged policy, custom, decision, or omission;
2. supporting facts and source or pleading locations;
3. inference classification and municipal inference;
4. attribution route;
5. implementation or transmission mechanism;
6. underlying constitutional violation;
7. particular injury;
8. moving-force chain;
9. `temporal_lanes`, mapping each supporting fact to every applicable lane;
10. information-and-belief basis, when used;
11. contrary material;
12. missing connections;
13. recommendation, reasons, and consequences.
14. `graph_assessment_status` for that path; and
15. `principal_decision`, using the typed record below.

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
