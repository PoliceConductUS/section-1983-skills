# Proposal: Defense-counsel overlays

## Why

Actual-adversary review is stronger when it can distinguish the current docket's
attacks from a source-backed history of how the responsible counsel team has
litigated comparable issues. The repository needs that professional behavior
layer without unsupported individual attribution, personal profiling,
denominator-free tendencies, or certainty about future conduct.

## What Changes

- Add one public defense-counsel overlay skill with install-local schemas, a
  standard-library validator, and generic fixtures.
- Define separate identity, team membership, historical argument, judicial
  treatment, current-attack link, and forecast records.
- Define attribution roles that prevent joint papers from becoming unsupported
  individual-attorney behavior.
- Define complete-corpus, denominator, missingness, comparison, confidence, and
  contrary-evidence requirements for patterns and forecasts.
- Define counsel-specific immutable lifecycle rules and public-source boundaries
  in `COUNSEL_OVERLAYS.md`.
- Extend filing manifests and actual-adversary review slices with validated
  counsel identity/team overlay pins while preserving blind-review isolation.
- Route the skill from README and the drafting umbrella and register its runtime
  source provenance.

## Capabilities

### New capabilities

- `building-defense-counsel-overlays`: creates, validates, versions, and
  consumes evidence-coded professional litigation profiles for individual
  defense attorneys and counsel teams.

### Modified capabilities

- `building-litigation-alignment-overlays`: composes counsel overlay pins and
  relevant counsel-team slices into filing manifests and actual-adversary review
  jobs without exposing them to blind review.

## Impact

Adds one public skill package, one root counsel guide, generic JSON fixtures, a
standard-library validator, and focused tests. Modifies README, the drafting
router, the general overlay guide, governance registry, filing-manifest schema,
and litigation-alignment validator. Adds no dependency, workflow, private or
case-specific data, paid retrieval, filing edit, PR, or issue closure.
