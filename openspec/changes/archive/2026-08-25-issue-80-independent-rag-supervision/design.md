# Design: Independent stage and immutable-byte supervision

## Invocation boundary

The generation stage writes an ordinary filing or research file beneath its
caller-declared output folder and records its exact SHA-256. The audit is a new
`audit-authorities` invocation. Its caller declares the folder containing that
file as recursive read-only `filing-source`, declares exact recursive read-only
`verified-authority` folders, selects one target file, and supplies a different
exact full absolute output folder. All audit transients stay beneath the new
output folder's `temp/` directory.

No package, manifest loader, graph, repository, persistence manager, or ambient
workspace mediates either stage. A trusted host supplies fingerprints and stage
provenance to the skill. A pure deterministic helper checks relationships; it
does not open folders, hash files, write output, or make legal judgments.

## Supervision record

The YAML-compatible supervision record extends the proposition audit with:

- generation and audit stage IDs and invocation IDs;
- optional model or provider identifiers;
- exact role, relative path, SHA-256 input fingerprints;
- selected authority-source identities;
- UTC execution times;
- output-folder fingerprints that prove the audit used a different output folder
  without exposing an absolute local path;
- an audit execution state of `successful`, `unavailable`, or `malformed`;
- a review relationship of `independent-stage`, `generator-self-review`, or
  `missing`; and
- `human_approval: not-provided`, because this AI-produced record is never a
  human filing decision.

The deterministic classifier compares the generation output hash, audit input
fingerprints, and current trusted-host fingerprints. Changed or missing bytes,
self-review, a missing stage, unavailable execution, and malformed output all
fail closed. Successful independent execution remains distinct from the
substantive proposition outcomes `unresolved`, `incorrect`, `misgrounded`,
`ungrounded`, and `grounded`. Only a successful independent stage with every
material proposition grounded may receive the supervision result `passed`; that
result still is not filing approval.

Provider credentials, tokens, continuation state, conversation IDs, and session
IDs are prohibited from the record.

## Regression corpus

`evaluations/legal-rag-regression-corpus/v1/` contains one versioned YAML
manifest and one YAML fixture per required failure mode. Each fixture embeds
synthetic immutable source text and its SHA-256, challenged text, expected
proposition correctness and groundedness, expected source voice, and the exact
reason a pass is allowed or forbidden.

Tests validate the complete taxonomy, source hashes, strict fields, stable
ordering, expected status relationships, and network independence. Optional
live-provider benchmarks remain outside this acceptance corpus and require dated
product, query-distribution, sample-size, and limitation disclosures.

## Human boundary

AI may prepare research, provenance, and audit records. The user retains legal
strategy, concessions, remediation choices, and filing approval. A separate
human decision may refer to the audit record, but the audit record itself cannot
claim or encode human approval.
