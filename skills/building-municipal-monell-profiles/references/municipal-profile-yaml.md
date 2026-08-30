# Municipal profile YAML contract

`municipal-profile.yaml` is a strict version-1 mapping containing profile,
municipality, and department identity; checked-through date; upstream validation
hashes; input fingerprints; evidence; entities; institutional events; chains;
comparisons; contradictions; similarity features; and five ordered domains.

Every evidence record contains `evidence_id`, `domain`, `category`, `source_id`,
`input_role`, folder-relative `source_path`, exact `source_sha256`, `location`,
`date`, bounded `proposition`, `support_direction`, `limitations`, and
`review_state`.

The five domains are exactly `Practice`, `Knowledge`, `Authority`, `Causation`,
and `Recurrence`. Each records only `evidence_ids`, `counterevidence_ids`,
`gap_ids`, and bounded `questions`. No field records an element conclusion,
liability conclusion, legal sufficiency, or selected theory.

`municipal-profile-gaps.yaml` contains strict ordered `gap_id`, `domain`, and
`description` records. `municipal-profile-validation.json` records deterministic
source hashes, upstream hashes, input fingerprints, and every output record ID.
