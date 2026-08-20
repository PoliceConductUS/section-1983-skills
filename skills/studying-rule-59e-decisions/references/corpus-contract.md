# Rule 59(e) corpus contract

Use this contract for a reproducible study of Rule 59(e) dispositions and
postjudgment amendment practice.

CSV, YAML, and databases may be used while researching. Publication and
downstream transfer require a versioned canonical JSON export that conforms to
[decision-corpus.schema.json](decision-corpus.schema.json) and passes
`python3 ../scripts/validate_corpus.py <corpus.json>` from this directory. Use
[transfer-card.schema.json](transfer-card.schema.json) when transferring a card
without the corpus. These schemas document the public format; the validator is
skill-specific and does not certify legal accuracy or implement a general JSON
Schema engine.

## Study manifest

Record:

- study identifier and version;
- research question;
- governing circuit and district;
- governing Supreme Court, circuit, former-circuit, rule, statutory, and any
  controlling state-law sources within scope;
- decisionmakers;
- date range;
- included motion types and case categories;
- excluded categories and reasons;
- databases and sites searched;
- exact queries or docket filters;
- search and retrieval dates;
- deduplication method;
- known unavailable sources; and
- the denominator definition.

## Evidence-ledger fields

Use the canonical schema fields in JSON exports. A working CSV, YAML file, or
database may use equivalent columns or relations:

| Group              | Fields                                                                                                                                  |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Identity           | `row_id`, `case_name`, `case_number`, `court`, `filed_date`, `decision_date`                                                            |
| Judges             | `assigned_judge`, `reasoning_author`, `recommendation_author`, `adopting_judge`, `consent_authority`, `independent_reasoning`           |
| Motion             | `rule_subsection`, `motion_type`, `claimed_ground`, `postjudgment_amendment`, `case_category`, `representation_status`                  |
| Procedural history | `challenged_disposition`, `prior_leave_request`, `prior_amendments`, `proposed_pleading_status`, `response_reviewed`, `reply_reviewed`  |
| Result             | `disposition_code`, `relief_granted`, `judgment_changed`, `stated_reasons`, `outcome_changing_reason`                                   |
| Ground child       | `ground_id`, `parent_row_id`, `asserted_ground`, `court_treatment`, `ground_result`, `supporting_pinpoint`                              |
| Amendment          | `rule15_applied`, `futility_test`, `claim_specific_review`, `leave_scope`, `new_judgment_entered`                                       |
| Appeal             | `appeal_taken`, `review_standard`, `appellate_result`, `later_history_checked_through`                                                  |
| Sources            | `docket_index_source`, `motion_source`, `response_source`, `reply_source`, `proposed_pleading_source`, `ruling_source`, `appeal_source` |
| Quality            | `retrieval_status`, `missing_documents`, `coding_confidence`, `notes`                                                                   |

Each canonical decision record represents one motion-disposition pair or a
linked judicial stage. Use the same stable `motion_id` for related stages and a
different `record_id` for each stage. Code `decision_type` as one of:

- `recommendation`;
- `adoption-only-order`;
- `independently-reasoned-final-decision`;
- `consent-final-decision`; or
- `outcome-only-order`.

A recommendation uses `recommendation-only`, identifies a distinct
recommendation author, and does not attribute final district-court reasoning. An
adoption-only order uses `adopts-without-additional-reasoning`, identifies the
adopting judge, and does not claim an independent reasoning author. An
independently reasoned final decision uses `independent` and identifies its
reasoning author. Every canonical decision record also requires one controlled
`retrieval_status` and `coding_confidence` value from the lists below. Every
stated reason uses a code from the reason-coding list.

## Controlled values

### `independent_reasoning`

- `independent`
- `adopts-with-additional-reasoning`
- `adopts-without-additional-reasoning`
- `recommendation-only`
- `docket-outcome-only`
- `unclear`

### `proposed_pleading_status`

- `complete-attached`
- `complete-tendered-separately`
- `cure-explanation-only`
- `neither`
- `not-applicable`
- `unknown`

### `disposition_code`

- `grant-full`
- `grant-partial`
- `correction-without-relief`
- `deny`
- `procedural-disposition`
- `administrative-only`
- `withdrawn`
- `unresolved`

### `retrieval_status`

- `complete-pair`: motion, ruling, and documents needed for the coded research
  question reviewed
- `ruling-complete`: full ruling reviewed but motion-side materials incomplete
- `index-only`: docket or metadata identifies the event but the ruling is
  unavailable
- `lead-only`: search result not yet tied to a verified docket artifact

### `coding_confidence`

- `high`: primary documents resolve the coded field
- `medium`: primary record is incomplete but the field is supported by an
  identified artifact
- `low`: field remains provisional and may not support a finding

## Reason coding

Code the court's stated reasons without converting them into broader holdings:

- `manifest-error-not-shown`
- `new-evidence-not-shown`
- `intervening-law-not-shown`
- `rehash-or-available-before-judgment`
- `vehicle-or-timing-defect`
- `rule15-factors`
- `futility`
- `delay-bad-faith-or-prejudice`
- `prior-failure-to-cure`
- `record-or-inference-error`
- `correction-does-not-change-result`
- `other-stated-reason`

Quote only verified language. Otherwise summarize and cite the page or docket
paragraph.

## Neutral transfer card

Every finding transferred downstream must use this neutral shape:

```yaml
card_id: R59-CARD-001
proposition: ""
universe: ""
numerator: 0
denominator: 0
date_range: ""
source_row_ids: []
evidence_level: example
missingness: ""
disconfirming_row_ids: []
permitted_use: ""
prohibited_inference: ""
checked_through: "YYYY-MM-DD"
actual_source_identity: ""
source_checked_date: "YYYY-MM-DD"
metric_type: descriptive
```

`evidence_level` is `example`, `documented-cluster`, or `tendency`.
`metric_type` is `descriptive` or `success-rate`. A `tendency` or `success-rate`
card requires a complete attempted census with zero unresolved relevant
missingness. A convenience or incomplete corpus may transfer only an `example`
or `documented-cluster` with explicit limits. A card communicates evidence and
limits; it does not select litigation strategy or turn association into
causation or prediction.

## Motion-design comparison

Compare document design only for `complete-pair` rows. Code observable features
rather than impressions:

- requested outcome in the first paragraph;
- Rule 59 ground named in the application;
- separate or integrated Rule 15 analysis;
- complete proposed pleading supplied;
- ruling-to-cure crosswalk;
- claim-specific alternative relief;
- appendix support for procedural quotations;
- response and reply treatment; and
- page count and local-rule compliance.

An association is not causation. Report whether the court referred to the
feature. Do not call a feature successful merely because it appeared in a
granted motion.

## Completeness statement

End every study with:

1. number of candidate dockets located;
2. number of motion-disposition pairs coded;
3. number complete for the research question;
4. missing motion, response, ruling, pleading, and appellate artifacts;
5. excluded cases by reason; and
6. whether the defined universe supports examples, a cluster, or a tendency.

Every retrieval gap carries a stable `candidate_id`. A document gap uses
`unavailable`, `unresolved`, or `not-found`, identifies a non-null `record_id`,
and matches one missing-document object's `gap_id`, record, and document type.
An unresolved candidate uses `unresolved-candidate` with a null `record_id` and
does not create a decision record. The denominator's unresolved relevant
missingness count equals the retrieval-gap inventory. Report the defined
universe, sampling method, located candidate count, coded motion-disposition
pair count, research-question-complete count, completeness status, and explicit
limits in the canonical denominator.
