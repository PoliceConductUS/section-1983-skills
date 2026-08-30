# Proposal: Folder-Scoped Skill Execution

## Why

Public Section 1983 skills must operate independently of CaseGraph and any other
case repository. A shared folder-native boundary is required before later skills
can safely consume ordinary source packages and generate ordinary output
packages.

## What Changes

- Add a versioned folder-invocation schema and deterministic conformance
  validator for named inputs, one output, target selection, runtime limits,
  internet authority, path confinement, and logical input manifests.
- Add one canonical execution-boundary owner document.
- Require every independently installable skill to carry the compact boundary.
- Extend repository governance validation and contribution review to protect the
  folder boundary.

## Capabilities

### New Capabilities

- `folder-scoped-skill-execution`: define folder-native invocation, validation,
  manifest, and host-enforcement contracts.

### Modified Capabilities

- `repository-skill-governance`: protect and deterministically validate the
  compact folder boundary in every public skill.

## Impact

The change affects repository governance, all public skill instructions, a new
JSON schema and standard-library conformance validator, public evaluation tests,
and contribution review. It adds no external dependency and no CaseGraph, Git,
MCP, virtual-filesystem, output-writer, or persistence behavior.
