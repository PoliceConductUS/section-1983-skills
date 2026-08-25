# Design: Bounded legal-authority source collection

## Invocation boundary

The installed contract accepts exactly six recursive read-only roles:
`legal-question`, `jurisdiction`, `court-hierarchy`, `relevant-date`,
`seed-authority`, and `approved-source-system`. Target is none. Internet is
authorized only for bounded collection. The caller supplies one full absolute
output folder, and the trusted host confines cwd, downloads, extraction, cache,
staging, and temporary environment variables to `<output-folder>/temp/`.

## Collection plan

The legal-question, jurisdiction, hierarchy, date, seed, and source-system files
bound exact queries, filters, courts, date intervals, access methods, and cost
limits. Input YAML cannot add roots, commands, capabilities, output authority,
or broader internet authority.

Every retrieved ordinary file is proposed beneath `sources/` with an adjacent
`<source-name>.SOURCE.yaml`. The strict record binds exact bytes to source URL,
query, filters, checked and retrieval dates, result identity, source type,
decision-date evidence or gap, proposed citation identity, review state,
limitations, and duplicate relationships.

## Source classifications and handoff

Source type is exactly `official_text`, `authenticated_opinion`, `docket_copy`,
`mirror`, `citator_record`, `secondary_material`, or `unverified_reference`.
Collection may propose a citation identity but never verifies publication,
binding force, treatment, proposition fit, quotation, pinpoint, or fair-warning
value. Those decisions belong to `audit-authorities` in a later invocation.

## Outputs and validation

The helper validates proposed in-memory records and returns deterministic
output-relative ordinary bytes and YAML. It never opens an input or output root
or performs network access. The trusted host performs authorized retrieval and
publishes through the append-immutable writer, including artifact-level internet
provenance and the terminal receipt.

## Failure model

Malformed or escaping paths, invalid URLs or timestamps, future checked dates,
unknown classifications, missing decision-date evidence/gaps, self or unknown
duplicates, duplicate result identities, and plan collisions fail before
publication. Empty, incomplete, inaccessible, paid, ambiguous, or out-of-scope
searches remain explicit gaps and never become a no-authority conclusion.
