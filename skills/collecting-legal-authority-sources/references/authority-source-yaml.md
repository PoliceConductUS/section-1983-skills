# Legal-authority source YAML contract

Every retrieved ordinary file has one adjacent domain
`<source-name>.SOURCE.yaml`. The strict version-1 mapping contains only:

- stable `source_id`, output-relative `artifact_path`, and exact `sha256`;
- `source_url`, exact `query`, ordered `filters`, `checked_date`, UTC
  `retrieved_at`, and stable `result_identity`;
- `source_type`: `official_text`, `authenticated_opinion`, `docket_copy`,
  `mirror`, `citator_record`, `secondary_material`, or `unverified_reference`;
- `decision_date`: strict `status`, `date`, `evidence`, and `gap` mapping;
- `citation_identity`: strict `status`, `case_name`, `court`, `citation`, and
  `docket_number` mapping, where status is `proposed` or `mistaken`;
- `verification_state`: always `unverified`;
- `review_state`: `candidate` or `rejected`;
- `retrieval_result`: always `retrieved`;
- ordered bounded `limitations`; and
- ordered `duplicate_of` source IDs from the same proposed collection.

`authority-source-candidates.yaml` contains the checked-through date and ordered
candidate records with source/documentation paths, hash, source type, identity
status, verification state, and review state.

`authority-source-gaps.yaml` contains ordered gaps with `gap_id`, `gap_type`,
`source_system_id`, `query`, `filters`, `checked_date`, and `coverage_limit`.
Gap type is `empty`, `incomplete`, `inaccessible`, `paid`, `ambiguous`, or
`out_of_scope`.

These files cannot contain verified publication, binding, treatment,
proposition-fit, quotation, pinpoint, or fair-warning findings.
