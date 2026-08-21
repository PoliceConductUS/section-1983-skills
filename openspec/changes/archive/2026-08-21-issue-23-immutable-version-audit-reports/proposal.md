# Proposal: Immutable Version-Local Quality-Control Reports

## Why

Independent quality-control stages are now non-mutating, but the repository does
not define where their reports belong or whether a later run may replace an
earlier result. Reports written beside a version, outside the version tree, or
over an earlier report break provenance and make the audit history ambiguous.

## What changes

- Require one new report per quality-control run under the audited version's
  `audits/` directory.
- Make report paths unique and immutable.
- Exclude generated audit reports from the review scope unless one is expressly
  designated for a separate review.
- Require report metadata, findings, and advisory recommendations for both
  failures and passing-but-suboptimal observations.
- Fail closed when the version folder or safe report path cannot be resolved.

## Capabilities

### New capabilities

None.

### Modified capabilities

- `repository-skill-governance`: define and validate immutable version-local
  quality-control report behavior.

## Impact

The change updates repository governance, the existing quality-control-capable
public skill entrypoints, and deterministic governance tests. It adds no
dependency, filing mutation, general remediation engine, root `docs/`, or
`.superpowers/` directory.
