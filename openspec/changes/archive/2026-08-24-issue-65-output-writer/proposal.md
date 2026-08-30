# Proposal: route skill outputs through the explicit output folder

## Why

The folder-scoped invocation contract identifies where writes may occur but does
not yet provide a safe publication primitive or reproducible run receipt. Direct
skill writes can expose partial files, overwrite prior outputs, or claim success
without durable bytes.

## What changes

- Add a standard-library output-run writer bound to Issue #64's validated
  invocation.
- Accept only canonical output-relative artifact paths and publish staged bytes
  atomically without replacement.
- Define append-immutable and expressly fresh-regenerable run modes.
- Persist visible incomplete state plus terminal success or bounded-failure
  receipts under a reserved per-run output namespace.
- Add a machine-readable manifest schema and a canonical public protocol.
- Add synthetic tests for confinement, collision, input preservation, stream
  failure, interruption, retry, receipts, and internet provenance.

## Impact

Artifact-producing skills gain one shared persistence boundary without CaseGraph
or another service. Existing public skill legal behavior does not change.

## Dependencies

This change depends on the durable `folder-scoped-skill-execution` contract from
Issue #64 and no external runtime.
