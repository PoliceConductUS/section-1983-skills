# Policy assessment YAML contract

`policy-assessments.yaml` is a strict version-1 mapping with `scope` and an
ordered `assessments` array. Each assessment records stable assessment,
requirement, actor, event, and phase IDs; policy and event dates; applicability,
violation, and evidence states; supporting and contrary source references;
missing predicates; conflicts; bounded explanation; review state; and exact
input-folder fingerprints.

Each source reference records `source_id`, `input_role`, folder-relative
`source_path`, exact `source_sha256`, and `location`.

Applicability is exactly `applies`, `not_applicable`, or `uncertain`. Violation
is exactly `yes`, `likely`, `unlikely`, `no`, or `indeterminate`. Evidence is
exactly `complete`, `incomplete`, `disputed`, or `unavailable`. `no` requires
`applies`, complete affirmative support, no missing predicates, and no
unresolved conflict. `not_applicable` and `uncertain` require `indeterminate`.

`policy-assessment-gaps.yaml` contains ordered strict records with `gap_id`,
`assessment_id`, `gap_type`, and `description`. Gap type is `missing_predicate`,
`missing_source`, `disputed_source`, `uncertain_applicability`,
`unavailable_source`, or `conflicting_evidence`.

`policy-assessment-validation.json` records the deterministic catalog hash,
assessment IDs, gap IDs, selected source IDs and hashes, input fingerprints, and
`valid` state. None of these files records a constitutional, Monell, negligence,
admissibility, strategy, allegation, or filing-readiness conclusion.
