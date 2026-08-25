# Design: Folder-native police-policy assessment

## Invocation boundary

The installed contract accepts exactly six recursive read-only roles:
`policy-catalog`, `actor`, `event`, `phase`, `case-record`, and
`assessment-scope`. Target is none and internet is disabled. The caller supplies
one full absolute output folder. The trusted host confines cwd, extraction,
cache, staging, and temporary environment variables to `<output-folder>/temp/`.

## Catalog and evidence binding

The catalog input consists of ordinary Issue #57 output files. Its validation
result must match the selected requirement IDs and source hashes. Actor, event,
phase, and case-record selections use folder-relative paths and domain YAML.
Every ordinary evidence file must match its adjacent documented SHA-256 before
assessment. Selection YAML cannot add roots, commands, capabilities, output
authority, or network authority.

## Atomic assessment model

One record represents one `requirement × actor × event or phase` unit. It
preserves stable identities, policy and event dates, applicability, violation,
evidence completeness, supporting and contrary source references, missing
predicates, conflicts, bounded explanation, review state, and input
fingerprints.

Applicability is `applies`, `not_applicable`, or `uncertain`. Violation is
`yes`, `likely`, `unlikely`, `no`, or `indeterminate`. Evidence is `complete`,
`incomplete`, `disputed`, or `unavailable`. `no` requires complete affirmative
support for nonviolation. `not_applicable` requires `indeterminate`, not a
nonviolation finding. Incomplete, disputed, unavailable, or silent records
cannot become `no`.

## Outputs and validation

The helper validates proposed in-memory records and returns deterministic
output-relative YAML, Markdown, and JSON bytes. It never opens an input or
output root. The trusted host publishes through the append-immutable writer and
records the terminal receipt. Inputs remain byte-identical.

## Failure model

Missing or stale catalog validation, changed source bytes, path escape,
unresolved IDs, invalid dates or states, duplicate assessment units, mixed
actors or phases, unsupported `no`, model-policy-as-department-policy treatment,
and liability language fail validation. Missing evidence, unavailable sources,
uncertain applicability, and conflicts remain explicit gaps or bounded
assessment states rather than invented facts.
