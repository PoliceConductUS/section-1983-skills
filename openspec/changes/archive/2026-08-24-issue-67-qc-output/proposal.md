# Proposal: publish quality-control reports as invocation-owned artifacts

## Why

The folder migration made quality-control stages read-only and moved their
reports beneath explicit output roots, but it does not yet provide one
executable report contract. Some quality-control skill contracts still permit an
invocation without a primary target, report metadata is prose-only, and the
generic logical input manifest does not distinguish prior generated reports from
reviewed artifacts.

## What changes

- Require one declared primary target whenever an entrypoint runs an independent
  quality-control stage; retain optional targets for non-QC drafting behavior.
- Add a trusted-host quality-control report publisher on top of the existing
  folder invocation validator and `OutputRun`.
- Give every report one canonical collision-resistant path containing its check
  kind, UTC run time, and run ID.
- Prefix report bytes with a canonical machine-readable metadata envelope that
  identifies the skill/version, filtered logical input roles and hashes, primary
  target, scope, result, findings, recommendations, and terminal run-manifest
  identity.
- Exclude generated quality-control reports from the reviewed-input manifest by
  default; include exactly one only when it is the invocation's explicit primary
  target.
- Update governance and all detected quality-control skills to name the same
  report contract and retain advisory-only remediation.
- Add filesystem and failure-path tests proving confinement, immutability,
  uniqueness, and honest terminal state.

## Impact

Quality-control processors still return content and never receive the output
root. The trusted host alone validates the invocation, constructs the report,
and publishes it through the existing output writer. No Git, CaseGraph, graph,
or external persistence dependency is introduced.

## Dependencies

This change depends on the durable `folder-scoped-skill-execution`,
`explicit-skill-output-persistence`, and `repository-skill-governance`
specifications implemented by Issues #64, #65, and #71.
