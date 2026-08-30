# Design: Folder-scoped role orchestration

## Trusted-host inputs

The helper receives a nonempty tuple of variant IDs and `BoundRoleLaunch` values
created through the shared launcher. A variant is data, not behavior. It cannot
supply an adapter, role, operation, permission, output validator, path resolver,
or publication policy.

All variants in one sweep must bind the same fixed role ID, operation, target
logical name, target bytes, and target hash. Their selected profile files and
source-documentation YAML may differ. Each bound invocation names a distinct
full absolute output folder that is a direct child of the sweep's declared
`runs/` output directory.

## Fresh runs and publication

The helper assigns a fresh UUID to each child dispatch and calls the shared
launcher once per variant. The launcher owns exact-byte snapshots, domain input
validation, process isolation, input preservation, output validation, and the
`<run-output-folder>/temp/` boundary.

After the child returns, the trusted host uses the existing output writer bound
to that variant's invocation. A successful run publishes the proposed findings
artifact plus `run-receipt.yaml`; a failed run publishes a bounded failure
receipt and no findings artifact. The receipt records only logical relative
paths, hashes, versions, role and operation identity, variant ID, terminal
status, and output hashes. It never records absolute paths or case excerpts.

The sweep coordinator uses `<sweep-output-folder>/temp/` for its own transient
work. It publishes the comparison beneath a separate explicit `comparison/`
output folder through the same output writer.

## Deterministic comparison

A finding key is its category, attacked quote, and logical location. Its value
is its sorted source IDs, analysis, and limitation. When every selected run
succeeds, the comparison reports:

- stable findings whose key and value appear in every variant;
- subset findings whose exact key and value appear in some but not all variants;
  and
- flipped findings whose key appears with more than one value, with the
  supporting variant IDs for each value.

Variant IDs, finding keys, source IDs, and comparison entries are sorted before
serialization. Input order therefore cannot change the comparison bytes.

If any selected run is failed or unavailable, the comparison status is
`incomplete`; it lists successful and failed variants but emits no stable,
subset, or flipped conclusion. A failure is never a negative observation.

## Artifact-only sequences

A sequence is a bounded ordered tuple of independently bound role launches.
After one hop publishes, a later hop may proceed only when one of its selected
input snapshots equals the prior hop's selected persisted artifact path and hash
and that artifact's output folder is declared as the later invocation's
read-only input root. The later hop receives a fresh process and its own full
absolute output folder. No hidden child state, conversation, or in-memory
finding object crosses the boundary.
