# Proposal: make the explicit output folder the produced folder

## Why

The first Issue #68 implementation writes a complete artifact folder at
`<output-folder>/packages/<package-id>/`. The user clarified that every
invocation is given, or must ask for, the full output-folder path. That selected
folder is the produced profile or artifact folder; no registry-like intermediate
namespace belongs between the invocation and its output.

## What changes

- Publish `package-manifest.json` and every declared member directly beneath the
  invocation's output root.
- Load the resulting output root while excluding only the trusted-host
  `.skill-runs/` receipt tree and `temp/` transient tree from artifact
  membership.
- Update public guidance and deterministic tests.

## Non-goals

- Removing manifests, hashes, validation receipts, provenance, or static-role
  separation.
- Adding CaseGraph, Git, a registry, or another persistence layer.
