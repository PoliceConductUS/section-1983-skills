## Why

The complaint completion audit already requires fail-closed treatment of facts
and statements during recorded intervals. Intended matching prose was edited in
the wrong checkout and therefore has no test-backed stacked owner. The complaint
claim contract and Rule 59(e) packet gate should express the same boundary.

## What Changes

- Add a focused test requiring all three public contracts to preserve the same
  recorded-event, transcript, attribution, recollection, unresolved-recording,
  correction, and gap routes.
- Add a focused test requiring continuous numbering in the Rule 59(e) final
  review list.
- Transfer the exact intended complaint and Rule 59(e) prose from the `main`
  checkout onto this dedicated branch.

## Capabilities

### New Capabilities

- `recorded-evidence-drafting-contract`: Define the shared fail-closed boundary
  for recorded events and statements in complaint and Rule 59(e) drafting.

### Modified Capabilities

None.

## Impact

The change modifies two public skill documents and adds one evaluation test. It
changes no executable drafting script, dependency, workflow, or repository
layout.
