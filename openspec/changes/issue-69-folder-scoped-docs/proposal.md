# Proposal: document folder-scoped skill operations

## Why

Issues #64 and #65 provide shared folder-native execution and output contracts,
but current onboarding still starts from an example case-workspace layout and
names a product-specific checker. Users need one product-independent guide that
shows how to select existing folders, validate an invocation, exercise a
determinate input-read-only host-conformance operation, and verify its exact
output and receipt without claiming that an installed public skill is migrated.

## What changes

- Replace the case-workspace start guide with one folder-scoped operations guide
  linked from README.
- Document stable logical input roles, configurable caller folder names and
  locations, one output folder, target selection, internet policy, and enforced
  isolation.
- Add an ordered synthetic first-hour flow through invocation validation, host
  conformance, and exact output/manifest verification.
- Document folder-backed filing packets, immutable QC reports, profile packages,
  research corpora, and isolated role runs.
- Link documented operations to their owning public skill contracts.
- Remove current public product-specific graph/checker language without
  rewriting historical archives or implementing an adapter.
- Add deterministic documentation tests for links, terminology, synthetic
  examples, invocation consistency, and the complete flow.

## Impact

Public onboarding matches the folder-native boundary while approved legal
behavior and skill-specific execution remain unchanged.

## Dependencies

This change depends on the durable `folder-scoped-skill-execution` and
`explicit-skill-output-persistence` specifications. It has no external runtime
dependency.
