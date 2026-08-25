# Design: Deterministic filing integrity over ordinary folders

## Installed behavior and declared inputs

The `filing-ci` skill owns a fixed registry of checker IDs and install-local
checker code. Case data cannot add a checker, command, executable, flag,
permission, path resolver, or output rule.

One validated invocation declares the recursive read-only roles `filing-source`,
`filing-index`, `record-reference`, `exhibit`, `docket-to-appendix`, and
`verified-authority`, plus one full absolute output folder. A required target
selects one ordinary filing source. The checker reads only caller-selected
relative files through the validated invocation.

## Domain YAML

The checker accepts strict version-1 domain YAML records with duplicate-key
rejection, bounded UTF-8 bytes, canonical relative paths, SHA-256 values, ISO
dates, stable IDs, and exact fields for their record kind. These records
document sources and relationships but cannot grant folder membership.

The initial records are:

- a filing index that identifies the filing, selected target path and hash,
  declared section ownership, and any open filing-gate IDs;
- `SOURCE.yaml` records for record, exhibit, and verified-authority bytes; and
- a docket-to-appendix index that maps a docket entry and page to one declared
  appendix page range and source ID.

Every referenced ordinary file must resolve inside its named declared folder and
match the documented hash. Missing, stale, mismatched, escaping, duplicate, or
ambiguous records fail before semantic checks.

## Initial deterministic checks

The first installed check set consumes the existing structured filing JSON used
by the complaint checker and adds only mechanical validation:

- required section ownership and order;
- continuous unique paragraph numbers and in-bounds paragraph references;
- exhibit paragraph ranges and supported internal short forms;
- docket-page to appendix-page consistency;
- unique stable persistent citation IDs with explicit unresolved state; and
- open filing-gate markers.

Persistent citation markup is identity and routing data only. It does not prove
the cited proposition, quotation, pinpoint, precedential status, or good law.

## Output and failure model

The checker produces one canonical JSON report and one Markdown rendering with
stable finding IDs, severity, location, message, and optional documented cure.
The trusted host publishes those files and `run-receipt.yaml` through the
existing output writer. Process working directory, staging, and temporary
environment variables remain under `<output-folder>/temp/`.

Exit classes are stable: `passed`, `findings`, `unavailable`, and `invalid`.
Missing required folders or domain YAML is unavailable, malformed or mismatched
selected input is invalid, and any hard finding keeps the gate open. The checker
never edits or renumbers the filing.
