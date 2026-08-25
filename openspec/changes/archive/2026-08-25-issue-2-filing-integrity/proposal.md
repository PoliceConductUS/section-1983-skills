# Proposal: Deterministic folder-scoped filing-integrity checker

## Why

Filing CI currently routes to one install-local complaint checker but still
describes that boundary as a package and does not implement Issue #2's complete
folder-native integrity checks. The checker must operate only on declared
ordinary files and domain YAML, remain read-only, and publish through the
explicit output folder.

## What changes

- Replace package vocabulary and package-named checker metadata with an
  installed fixed checker registry owned by `filing-ci`.
- Expand the exact Filing CI folder contract to the six ordinary input roles
  required by the selected check set.
- Add strict domain-YAML validation for filing membership, source identity,
  hashes, dates, docket-to-appendix relationships, and verified authority
  references.
- Add deterministic initial checks for paragraph and section structure,
  exhibit/docket/appendix references, persistent citation IDs, and open filing
  gates.
- Publish human findings, JSON findings, and `run-receipt.yaml` through the
  existing explicit output writer with every transient byte beneath
  `<output-folder>/temp/`.
- Keep the checker read-only and preserve stable unavailable, open, and failed
  exit classes.

## Capabilities

### New capability

- `deterministic-filing-integrity`

### Modified capability

- `filing-ci-orchestration`

## Non-goals

- No package, package loader, graph, CaseGraph object, repository, Git,
  separately configured executable, substantive authority judgment, automatic
  correction, renumbering, or filing-readiness decision.
