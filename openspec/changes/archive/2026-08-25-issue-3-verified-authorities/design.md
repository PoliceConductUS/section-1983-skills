# Design: Verified authority audits over folders and YAML

## Invocation boundary

The installed `audit-authorities` contract has exactly two recursive read-only
input roles: `filing-source` and `verified-authority`. A required target selects
one ordinary filing file. One caller-supplied full absolute output folder is the
only writable root. Ordinary `audit` runs disable internet. A distinct
`freshness-research` operation may authorize internet but cannot certify an
authority or change input files.

## Authority documentation

One caller-selected corpus YAML contains an ordered list of relative authority
YAML paths. Each strict authority YAML identifies one logical authority, one
relative opinion path, one relative `SOURCE.yaml` path, hashes, dates, court and
status fields, proposition, quotation, pinpoint, later-history state,
rule-of-orderliness state, and text-layer status. The source YAML independently
documents the same ordinary opinion bytes and provenance.

All paths resolve inside `verified-authority`. YAML is untrusted data: it cannot
add a root, command, executable, output path, capability, or network permission.
Duplicate IDs, paths, or fields and mismatched hashes fail before citation
analysis.

## Citation and quotation checks

The trusted host invokes installed eyecite APIs over the selected filing text to
extract citations and resolve short-form antecedents. Eyecite output identifies
candidates only. Persistent citation markup, when present, supplies stable
identity and an authority ID but does not bypass any authority gate.

An authority is verified only when selected YAML and exact bytes establish its
identity and required states. Direct quotations must occur verbatim in an
authority document whose text layer is marked usable; otherwise the result is a
hard finding or pending visual review. Missing cited authorities fail closed.

## Output and failure model

The host publishes canonical JSON findings, deterministic Markdown, and
`run-receipt.yaml` through the shared explicit output writer. All staging,
extraction scratch data, process working directories, and temporary environment
variables remain under `<output-folder>/temp/`. Inputs remain byte-identical.

Stable result classes are `passed`, `findings`, `unavailable`, and `invalid`.
Missing required selected YAML or source bytes is unavailable; malformed,
escaping, duplicate, or hash-mismatched documentation is invalid; unresolved
hard findings keep the audit gate open.
