# Rule 59(e) corpus contract

Use this contract for a reproducible study of Rule 59(e) dispositions and
postjudgment amendment practice.

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

Use CSV, YAML, or a database with these fields:

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

## Finding card

Every finding transferred to a drafting skill or case strategy must state:

```yaml
finding_id: R59-F-001
proposition: ""
universe: ""
numerator: 0
denominator: 0
date_range: ""
source_rows: []
evidence_level: example
missingness: ""
disconfirming_rows: []
permitted_use: ""
prohibited_inference: ""
checked_through: "YYYY-MM-DD"
```

`evidence_level` is `example`, `documented-cluster`, `tendency`,
`express-requirement`, or `binding-rule`.

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
