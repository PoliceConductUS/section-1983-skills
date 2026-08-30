# Retrospective

## Outcome

Issue #67 gives every independent quality-control stage one invocation-owned,
append-immutable report under the caller's explicit output folder. The trusted
host owns target authorization, report identity, canonical metadata, output
publication, and terminal receipts; public skill processors remain confined to
their declared inputs and return only content or findings.

## What worked

- Building on the existing installed-contract validator and `OutputRun` kept the
  change small and preserved one authority boundary for inputs and outputs.
- Canonical report metadata made the reviewed target, filtered inputs, sources,
  findings, recommendations, and terminal receipt mechanically inspectable.
- Explicit prior-report filtering prevented a later review from silently
  incorporating its own history while still permitting one report to be the
  selected target.
- Integration tests proved packaged processors can return deterministic bytes
  without receiving the output root or choosing an output path.
- Exact-SHA independent review found behavioral contradictions that prose-only
  governance checks had missed.

## Misses and corrections

- The first publisher accepted a generically validated invocation, so the target
  role was not demonstrably copied from the installed skill contract. The final
  publisher requires installed-contract target policy and roles.
- The first run-ID grammar accepted weak lower-kebab values. Quality-control
  publication now requires a canonical lowercase UUIDv4 before run-state
  mutation.
- Prefix-only report exclusion failed when `quality-control-reports/` itself was
  the declared role root. The first correction used a fence marker, but review
  correctly showed that malformed ordinary files could then disappear from the
  fingerprint. The final classifier requires the exact schema, canonical compact
  JSON, UUID/run-manifest binding, and closing fence.
- Several packaged helpers and one judge-overlay processor still returned paths
  selected inside the processor. Their tests now publish processor bytes through
  the trusted-host quality-control API and assert that no output path is
  returned.
- Mixed drafting/auditing skill guidance needed to distinguish a proposed
  drafting-artifact path from pathless independent quality-control content.
- Intermediate stacked commits intentionally made draft-PR CI red while tests
  referenced not-yet-added modules. Later commits added the tracked modules, and
  the final exact SHA passed GitHub Actions.

## Reusable lessons

- A package contract must be carried into the validated invocation used at the
  publication boundary; a nearby JSON file is not runtime authorization.
- Reserved path prefixes and content identity solve different cases. When a
  logical root erases the reserved prefix, content classification must validate
  the whole canonical envelope rather than trust a magic first line.
- Host-only publication requires executable searches and integration tests for
  processor-selected paths, not just shared prose in each public skill.
- Draft PRs can safely expose TDD RED commits, but final readiness must rely on
  the exact final SHA and fresh aggregate verification.

## Boundaries retained

This change does not add a trusted-host sandbox, universal runner, CaseGraph
adapter, graph model, electronic filing, or new legal judgment. It does not
authorize same-stage remediation or mutation of a reviewed artifact.
