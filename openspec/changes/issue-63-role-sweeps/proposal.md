# Proposal: Folder-scoped role sweeps and artifact-only sequences

## Why

Issue #63 needs deterministic orchestration above the fixed role launcher. The
orchestrator must repeat a protected role across explicitly selected profile
files and connect later roles through ordinary persisted files without creating
a package, graph, shared conversation, or mutable workspace.

## What changes

- Add a trusted-host sweep helper that accepts already validated and bound role
  launches over declared recursive read-only folders.
- Launch every selected profile in a fresh isolated process against the same
  exact target bytes and hash.
- Publish each run's proposed findings and an ordinary `run-receipt.yaml`
  beneath its own explicit output subfolder through the existing output writer.
- Publish one order-independent comparison beneath a separate comparison output
  subfolder.
- Permit a later hop to consume a selected persisted ordinary file only through
  a new declared read-only input folder and fresh role binding.
- Preserve unavailable and failed runs without treating them as agreement,
  absence, or success.

## Capability

### New capability

- `folder-scoped-role-orchestration`

## Non-goals

- No package, manifest-based input format, package loader, graph, CaseGraph,
  repository, ambient workspace, direct role conversation, recursive debate,
  strategy selection, disposition, concession, target edit, or remediation.
