# Proposal: bind implemented skills to folder-native execution

## Why

The shared folder protocol is not yet consumable as an exact installed-skill
contract. Generic prose does not identify required roles or runtime policy, and
legacy executable seams still write to version-local audit directories or
delegate to configured commands. The implemented skills need one auditable,
install-local contract without changing their approved legal behavior.

## What changes

- Add `references/folder-contract.json` to all 22 public skill packages.
- Define exact role sets, target policy, internet policy, and `append-immutable`
  output mode for each skill.
- Extend repository governance validation to require exact schema-valid
  contracts that match the public skill name and approved matrix.
- Replace project/version-local quality-control report placement with the one
  caller-declared output folder and shared run receipts.
- Package Filing CI's supported checker wrapper and complaint mechanical checks;
  return stable unavailable results when no packaged checker supports the
  operation.
- Convert standalone helpers into input-confined deterministic processors that
  emit bytes or results for host publication without importing root scripts.
- Route adversarial-review and judge-overlay artifacts through the trusted
  host's `OutputRun` while retaining their substantive schemas and failure
  classes.
- Add migration tests for isolated installation, input non-mutation, output
  confinement, undeclared paths, internet-disabled behavior, receipts, and
  obsolete current-contract terminology.

## Impact

Each implemented skill becomes independently installable with an exact
folder-native interface. Existing legal semantics and immutable provenance
remain unchanged. The trusted host remains the only component that validates
absolute roots, enforces filesystem/network isolation, and persists outputs.

## Dependencies

This change depends on the durable `folder-scoped-skill-execution`,
`explicit-skill-output-persistence`, and `case-workspace-start-guide`
specifications. It adds no external runtime dependency.
