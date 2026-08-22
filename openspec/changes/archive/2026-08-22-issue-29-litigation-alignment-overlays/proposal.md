# Proposal: Litigation-alignment overlays

## Why

Drafting and adversarial review need reproducible case-specific context after a
docket reveals which defendants align, what attacks they actually make, how the
plaintiff responds, and what each judicial actor does. The current repository
has no immutable overlay lifecycle or role-separated machine contract.

## What Changes

- Add one public litigation-alignment overlay skill with install-local schemas,
  a validator, and synthetic fixtures.
- Add a general case-overlay lifecycle guide and route it from README and the
  drafting umbrella.
- Define issue-scoped groups that preserve individual defendants and material
  differences.
- Define separate adversary-attack, plaintiff-response, and judicial-treatment
  ledgers plus a source-preserving derived matrix.
- Define per-target/group blind and actual-adversary review plans, including the
  no-responsive-filing degradation route.
- Define filing-version manifest pins and event-driven immutable lifecycle
  rules.
- Link the judge-overlay guide to the general lifecycle and add judge-specific
  refresh/rebuild triggers without weakening anti-gaming or corpus validation.
- Replace the generated placeholder Purpose in the durable judge-overlay spec.

## Capabilities

### New capabilities

- `building-litigation-alignment-overlays`: creates, validates, versions, and
  consumes docket-derived litigation-alignment overlays.

### Modified capabilities

- `judge-overlay-authoring`: participates in the shared lifecycle and defines
  judge-specific invalidation triggers.

## Impact

Adds one public skill package, root documentation, generic JSON fixtures, a
standard-library validator, and focused tests. Modifies README, the drafting
router, and the existing judge-overlay guide/spec. Adds no dependency, workflow,
case-specific data, attorney research, filing edits, PR, or issue closure.
