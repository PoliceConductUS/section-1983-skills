# Design: Ordinary filing folders

## Invocation surface

A filing-related invocation receives only its installed skill instructions,
assigned task, caller-declared recursive read-only input folders, expressly
authorized internet results, and exactly one full absolute output folder when
the operation writes durable output. A task identifies one filing target by its
input role and folder-relative path. A whole-folder task explicitly describes
the ordinary files in scope; no root manifest supplies membership.

Missing target or output-folder information is a caller-input failure. The skill
asks for the missing value and stops before substantive or filesystem work.
Inputs remain byte-for-byte unchanged. A revision receives the prior output
folder as a new declared read-only input and writes into a different fresh
output folder.

## Persistence deletion

The migration deletes `scripts/filing_packet.py`, the FilingPacket schema,
fixtures, specialized tests, public guide, and install-local contract copies.
Current skill instructions and specifications lose the FilingPacket boundary.
The active FilingPacket lifecycle specification is deleted and replaced by the
ordinary-folder capability in this change.

No manifest, package, loader, publisher, index, registry, graph, repository,
datastore, workspace convention, or renamed folder object replaces it. Domain
skills may continue to require their own YAML source records for particular
files. Those records do not enumerate a generic filing folder or define a shared
persistence layer.

## Output and temporary boundary

Durable generated files are written directly beneath the exact caller-selected
output folder. Cache, downloads, extraction, staging, process working directory,
`TMPDIR`, `TMP`, `TEMP`, and every other temporary byte are confined to
`<output-folder>/temp/`. Nothing in the migration creates an implicit output
path or relocates caller files.

## Regression boundary

Repository governance inventories current, non-archived documentation, code,
specifications, fixtures, and tests for obsolete FilingPacket artifacts. It also
rejects replacement generic persistence language while allowing negative
statements that explain the prohibited boundary. Archived OpenSpec changes
remain immutable historical records.
