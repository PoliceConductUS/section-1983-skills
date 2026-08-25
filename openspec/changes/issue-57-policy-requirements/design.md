# Design: Source-bounded policy requirement catalogs

## Invocation boundary

The installed contract accepts exactly four recursive read-only roles:
`department-identity`, `jurisdiction`, `policy-source`, and `analysis-scope`.
Target is none and internet is disabled. The caller supplies one full absolute
output folder. The trusted host confines cwd, extraction scratch files, staging,
and temporary environment variables to `<output-folder>/temp/`.

## Selected source binding

The analysis scope selects ordered folder-relative `SOURCE.yaml` paths from
`policy-source`. Each strict record binds one adjacent ordinary file, SHA-256,
source URL, classification, proposed adoption relationship, review state,
effective-date evidence or gap, and limitations. Selected input must be reviewed
and approved for analysis. Missing, malformed, escaping, stale, or
hash-mismatched material fails before semantic work.

Only `adopted_policy` with a documented adoption relationship may be represented
as department policy. Other classifications may supply bounded context or
comparison but cannot generate department-policy requirements.

## Atomic requirement model

One record represents one independently testable operative unit. It preserves
stable ID, policy/source identity, quotation, pinpoint, source path/hash,
effective interval or date gap, actor, triggers, requirement type, action,
exceptions, definitions, dependencies, cross-references, documentation/review
duties, and unresolved gaps.

Requirement type is exactly `mandatory`, `prohibited`, `permitted`, or
`discretionary`. Conditions do not become unconditional duties. Permissions do
not become duties. Discretion does not become a prohibition or mandate. Every
exception and dependency stays attached to the same record or produces a hard
gap.

## Outputs and validation

The helper validates proposed in-memory records and returns deterministic
output-relative YAML and Markdown bytes. It never opens input or output roots.
The trusted host publishes through the existing append-immutable writer and
records the terminal receipt. Input fingerprints and source hashes remain in the
domain validation result.

## Failure model

Invalid dates, unsupported types, duplicate IDs, missing quotations or
pinpoints, unresolved source IDs, lost exception/cross-reference markers,
retroactive scope, and adopted-policy claims from another classification are
invalid. Missing pages, illegible text, uncertain adoption or dates, incomplete
history, and ambiguous cross-references remain explicit gaps; they never become
invented requirements.
