# Policy requirement YAML contract

`policy-requirements.yaml` is a strict version-1 mapping with `scope` and an
ordered `requirements` array. Each requirement records stable requirement,
department, policy, and source IDs; effective dates or gaps; exact quotation and
pinpoint; source-relative ordinary-file path and SHA-256; actor; triggers; type;
action; exceptions; definitions; dependencies; cross-references; documentation
or review steps; gaps; and operative-marker booleans.

Requirement type is exactly `mandatory`, `prohibited`, `permitted`, or
`discretionary`. A true marker requires its corresponding structured content.
A false marker prohibits invented corresponding content. A discretionary marker
requires the discretionary type. The effective start cannot precede the
documented policy effective date.

`policy-analysis-gaps.yaml` contains ordered strict gap records with `gap_id`,
`gap_type`, `source_id`, `location`, and `description`. Supported gaps are
`missing_page`, `illegible_text`, `unresolved_history`, `uncertain_adoption`,
`ambiguous_cross_reference`, and `uncertain_effective_date`.

`policy-analysis-validation.json` records the deterministic selected source
IDs and hashes, requirement IDs, gap IDs, and `valid` state. None of these files
records compliance or a legal conclusion.
