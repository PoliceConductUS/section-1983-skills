# Design: Evidence-coded municipal profiles

## Invocation boundary

The installed contract accepts exactly seven recursive read-only roles:
`municipality`, `department`, `source`, `policy-catalog`, `policy-assessment`,
`case-record`, and `verified-authority`. Target is none and internet is
disabled. The caller supplies one full absolute output folder. The trusted host
confines cwd, extraction, cache, staging, and temporary environment variables to
`<output-folder>/temp/`.

## Input binding

Municipality and department files establish approved identity only. Source and
case-record folders provide selected ordinary institutional records with
adjacent domain YAML. Policy-catalog and policy-assessment folders contain the
ordinary validated outputs of Issues #57 and #58. Verified-authority contains
separately audited authority files. Every selected path, hash, validation
result, input fingerprint, and cross-record identity must match before profile
work.

## Evidence model

Each evidence use preserves stable identity, one analysis domain, one category,
source role/path/hash/location, date, bounded proposition, support direction,
limitations, and review state. Support direction is `favorable`, `unfavorable`,
`disconfirming`, or `neutral`. Categories distinguish formal policy, custom,
training, supervision, FTO transmission, complaints/internal affairs,
ratification candidates, litigation positions, institutional feedback, and
institutional learning.

Entities, institutional events, notice/corrective chains, comparisons,
contradictions, and similarity features reference evidence IDs rather than
restate unsupported facts. Every comparison remains a question. Settlement,
complaint, accusation, silence, non-discipline, outlier, contradiction, and
similarity lead remain limited evidence types rather than proof.

## Five-domain profile

`Practice`, `Knowledge`, `Authority`, `Causation`, and `Recurrence` each
preserve supporting evidence IDs, counterevidence IDs, gap IDs, and bounded
questions. No field represents an element as satisfied, proved, established, or
legally sufficient.

## Outputs and failure model

The helper validates proposed in-memory records and returns deterministic
output-relative YAML, Markdown, and JSON bytes. It never opens folders or uses
the network. Missing or failing upstream validation, changed bytes, stale
fingerprints, unresolved IDs, mixed domains, unsupported proof language, or
invalid paths fail before profile output. Missing material remains an explicit
gap.
