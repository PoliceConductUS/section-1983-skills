# Read-only on-disk CaseGraph assessment contract

## Access boundary

Use only an explicit graph-directory path. Read `config.yaml` and relevant
`<uid>/root.yaml` files directly and read-only. Do not search the filesystem,
write to the graph, or invoke a CaseGraph CLI. Support only declared on-disk API
versions; never assume public implementation `main` defines the stored format.

Before relying on a slice, verify parseable recognized envelopes, matching
directory and metadata UIDs, unique relevant UIDs, resolved traversed
references, source paths and hashes, governing jurisdiction, relevant date,
procedural lens, and the evaluated document fingerprint. Report unrelated
defects without invalidating an independent slice.

## Status

Return exactly one status:

- `completed`
- `partial`
- `not_run_missing`
- `not_run_invalid`
- `not_run_incompatible`
- `not_run_stale`

Missing substantive links produce `partial` and indeterminate components, not
invented edges. A missing path produces `not_run_missing`; parse or relevant
reference failure produces `not_run_invalid`; unsupported API version produces
`not_run_incompatible`; fingerprint mismatch produces `not_run_stale`.

## Verified authority resolution

Every used authority proposition must resolve:

`AuthorityProposition → authorityRef → Authority → verified authority unit → SOURCE.yaml → canonical opinion artifact + matching SHA-256 → provenance-linked text representation → cited pinpoint → exact matching passage`.

Record proposition and authority UIDs, verified-unit and `SOURCE.yaml` paths,
canonical opinion and text-representation paths and SHA-256 values, pinpoint,
exact matched text, stable locator, and normalization. Allowed deterministic
normalization is limited to recorded whitespace, Unicode punctuation, or PDF
line-break handling. A fuzzy or semantic near-match does not count and is
insufficient.

Use one resolution status: `resolved`, `missing`, `hash_mismatch`,
`pinpoint_unresolved`, `text_mismatch`, or `ambiguous_match`. Any status other
than `resolved` keeps the dependent component incomplete or indeterminate. A
derived text artifact is usable only when verified provenance links it to the
hashed canonical opinion.

## Reasoned component result

For each element or path component record coverage, connection quality, source
quality, procedural usability, confidence, opinion, explanation, supporting
path, contrary path, missing connection, and every authority resolution used. Do
not reduce those records to an opaque composite score or describe them as a
court adjudication.

Use only these values:

- `element_coverage`: `satisfied`, `partial`, `missing`, or `not_applicable`;
- `connection_quality`: `direct`, `strong_supported_inference`,
  `plausible_inference`, `weak_inference`, `unsupported`, or `contradicted`;
- `procedural_usability`: state the explicit Rule 12 or other governing record
  treatment rather than a composite score;
- `confidence`: `high`, `medium`, or `low`; and
- `opinion`: `likely_sufficient`, `plausibly_sufficient_but_vulnerable`,
  `likely_insufficient`, or `indeterminate`.
