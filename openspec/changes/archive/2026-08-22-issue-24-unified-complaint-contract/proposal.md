# Proposal: Unified Section 1983 Complaint Contract

## Why

The whole-complaint skeleton and detailed count contract currently have
different owners, while the false-arrest specialization repeats both. Partial
installations omit requirements and complete compositions expose competing
general contracts. One canonical install-local owner is required so every
complaint workflow receives the same structure and count rules.

## What changes

- Make `drafting-section-1983-complaints` the canonical owner of the complete
  general complaint contract.
- Publish its deterministic subset as an install-local machine-readable contract
  for an external checker.
- Convert the umbrella complaint document to routing and fail-closed behavior.
- Reduce the false-arrest complaint reference to specialization-only deltas.
- Document the composition and external CaseGraph checker boundary.
- Add deterministic package-contract tests and fresh-context behavior pressure
  tests.

## Capabilities

### New capabilities

- `drafting-section-1983-complaints`: define canonical complaint ownership,
  composition, the complete general skeleton/count contract, and its
  deterministic checker handoff.

### Modified capabilities

None. Existing Filing CI orchestration already resolves only a
project-configured external checker and fails closed when it is unavailable.

## Impact

The change updates the umbrella, general complaint, and false-arrest skill
packages, README composition guidance, and evaluation tests. It adds one
Markdown reference and one JSON contract under the canonical owner, renames and
narrows the false-arrest reference, and adds no executable filing checker,
dependency, workflow, root `docs/`, or `.superpowers/` directory.
