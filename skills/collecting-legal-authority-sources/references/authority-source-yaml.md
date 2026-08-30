# Legal-authority source YAML contract

Every retrieved ordinary file has one adjacent domain
`<source-name>.SOURCE.yaml`. The strict version-1 mapping contains only:

- stable `source_id`, output-relative `artifact_path`, and exact `sha256`;
- stable `frame_id`, `source_system_id`, and nullable `provider_or_product_id`;
- canonical `source_url`, exact `query`, ordered `filters`, `execution_date`,
  `checked_date`, UTC `retrieved_at`, stable `result_identity`, and positive
  `retrieval_order`;
- bounded `proposed_legal_role` and nullable `rejection_reason`;
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

`rejection_reason` is null for a candidate. A rejected source uses exactly one
of `wrong-issue`, `wrong-jurisdiction`, `wrong-court`, `wrong-date`,
`wrong-statute`, `wrong-rule-version`, `wrong-posture`, `wrong-authority-level`,
`wrong-treatment`, or `wrong-factual-trigger`.

`authority-retrieval-frame.yaml` records the stable frame ID, exact legal
question, governing jurisdiction, ordered court hierarchy, operative date,
procedural posture, statute or rule version, material factual trigger, ordered
source universe, access and cost limits, and checked-through date.

`authority-retrieval-premises.yaml` contains ordered premise records. Each has a
stable ID, premise type, exact statement, and `verified`, `false`, or
`unresolved` status. Verified requires evidence. False requires evidence and a
correction. Unresolved requires a gap.

`authority-source-candidates.yaml` contains the checked-through date and ordered
candidate records with source/documentation paths, hash, source type, identity
status, verification state, review state, original retrieval order, proposed
legal role, and rejection reason.

`authority-source-gaps.yaml` contains ordered gaps with `gap_id`, `gap_type`,
`frame_id`, `source_system_id`, `query`, `filters`, `checked_date`,
`known_missingness`, and `coverage_limit`. Gap type is `empty`, `incomplete`,
`inaccessible`, `paid`, `ambiguous`, or `out_of_scope`.

A real citation, working link, source list, snippet, or positive treatment
symbol remains a retrieval lead. These records do not establish source
applicability or proposition support.

These files cannot contain verified publication, binding, treatment,
proposition-fit, quotation, pinpoint, or fair-warning findings.
