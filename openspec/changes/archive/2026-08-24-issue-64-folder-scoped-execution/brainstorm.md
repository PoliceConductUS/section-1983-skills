# Brainstorm

## Problem

The pending skills stack was designed around CaseGraph resources, commits, and
traversal. That makes otherwise reusable legal workflows depend on a specific
case repository. The approved replacement is folder-native: each invocation
receives a fixed set of ordinary input folders, one ordinary output folder, and
only the internet authority declared by the invoked skill.

The contract must be meaningful when one skill is installed by itself. It must
also remain honest about enforcement: skill prose can declare and preserve a
boundary, but only a trusted host can enforce filesystem mounts, process
capabilities, and network access.

## Approved approach

- Define one versioned JSON invocation envelope with named absolute input
  folders, exactly one absolute output folder, optional target selection,
  runtime limits, internet policy, and an explicit host-isolation declaration.
- Resolve canonical paths before semantic work. Reject missing or non-directory
  roots, duplicate roles, input/output containment, traversal, absolute child
  paths, and symlink escapes.
- Produce a deterministic logical input manifest containing role names, relative
  file paths, byte sizes, and SHA-256 hashes. Persist no machine- specific
  absolute path in that manifest.
- Provide a standard-library repository conformance validator and path resolver.
  It is test and host integration support, not a runtime dependency of a skill.
- Publish the complete contract once in repository documentation. Embed only a
  compact four-sentence boundary in each independently installable `SKILL.md`.
- Extend deterministic governance validation so a new or edited skill cannot
  omit or invert the compact boundary.

## Rejected alternatives

### Keep the CaseGraph contract as an optional backend

Supporting both graph and folder contracts would retain two execution models,
two test matrices, and hidden graph assumptions. CaseGraph may adapt its own
data externally, but no adapter belongs in this repository.

### Add a custom resource URI or virtual filesystem

A URI tool would become another mandatory dependency and would not make shell
paths or ordinary file-consuming tools work. The approved contract uses real
folders.

### Claim that `SKILL.md` instructions enforce isolation

Prompt instructions communicate allowed behavior but do not restrict the host
process. The invocation must fail before reading case material when the host
cannot establish the declared filesystem and network capability boundary.

## Boundaries

- No CaseGraph, Git, MCP, virtual filesystem, bridge, or repository adapter.
- No output writer, atomic persistence lifecycle, or run receipt; #65 owns those
  behaviors.
- No per-skill input-role migration; #71 assigns concrete roles and internet
  policies to already implemented skills.
- No new external dependency.

## Open questions

None. Input/output role design and the enforcement boundary were approved in the
architecture discussion and recorded in Issue #64.
