# Proposal: Preserve contributor norms

## Why

The repository has durable release and legal-gate policies, but its contribution
guide does not yet preserve the stacked-story, TDD, OpenSpec, measurement, and
comment disciplines that produced them.

## What Changes

- Add the missing engineering and epistemic contract to `CONTRIBUTING.md`.
- Link the existing governance and publishing owners without duplicating them.
- Extend the repository governance validator and tests for deterministic
  documentation boundaries.

## Capabilities

### New capabilities

None.

### Modified capabilities

- `repository-skill-governance`: add the contributor contract and deterministic
  validation requirement.

## Impact

Documentation, repository-specific standard-library validation, tests, and
OpenSpec only. No CLA, governance body, dependency, public skill, or workflow
change.
