# Police-policy source YAML contract

Every retrieved ordinary file has one adjacent domain
`<source-name>.SOURCE.yaml`. The source record is a strict version-1 mapping
with only these fields:

- `version`: integer `1`.
- `source_id`: stable lowercase hyphenated identifier.
- `artifact_path`: canonical output-relative path beneath `sources/`.
- `sha256`: lowercase SHA-256 of the exact ordinary file bytes.
- `source_url`: bounded HTTP or HTTPS retrieval URL without credentials.
- `query`: exact bounded query.
- `filters`: ordered exact filter strings.
- `checked_date`: ISO `YYYY-MM-DD` date no later than the invocation's
  checked-through date.
- `retrieved_at`: UTC timestamp ending in `Z`.
- `result_identity`: stable identity returned by the source system.
- `classification`: one classification listed in the skill entrypoint.
- `adoption_relationship`: `documented`, `uncertain`, `rejected`, or
  `not_applicable`.
- `review_state`: `candidate` or `rejected`; collection never records approval.
- `retrieval_result`: `retrieved`.
- `effective_date`: strict mapping of `status`, `date`, `evidence`, and `gap`.
  `documented` requires a date and evidence. `uncertain` or `missing` requires a
  bounded gap.
- `limitations`: ordered bounded strings.
- `duplicate_of`: ordered source IDs within the same proposed collection.

`policy-source-candidates.yaml` is a strict version-1 mapping containing the
checked-through date and an ordered `sources` array. Each entry records only
`source_id`, `source_documentation_path`, `artifact_path`, `sha256`,
`classification`, and `review_state`.

`policy-source-gaps.yaml` is a strict version-1 mapping containing the
checked-through date and an ordered `gaps` array. Each gap contains exactly:
`gap_id`, `gap_type`, `source_system_id`, `query`, `filters`, `checked_date`,
and `coverage_limit`. Gap type is `empty`, `incomplete`, `inaccessible`, `paid`,
`ambiguous`, or `out_of_scope`.

These records cannot contain analysis requirements, compliance findings,
commands, executable fields, output roots, or alternate capabilities.
