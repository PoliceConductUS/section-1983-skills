# Proposal: standardize immutable folder packages

## Why

Existing judicial, litigation-alignment, and defense-counsel workflows use
domain-specific manifests and fingerprints but lack one folder-level contract
that later role launchers can validate uniformly. Pending profile and role
stories need complete immutable membership, stable package identity, freshness,
source-role provenance, and protected behavior/data separation without Git,
CaseGraph, or version-numbered directories.

## What changes

- Publish strict schemas for `package-manifest.json` and protected static role
  contracts.
- Add a standard-library loader that rejects malformed, unsupported, stale,
  failed, incomplete, aliased, escaping, unlisted, or hash-mismatched packages
  and returns immutable member bytes plus a package fingerprint.
- Add a trusted-host publisher that writes one complete new package through the
  existing output writer without mutating inputs.
- Add a pure role/profile binding check that validates package-kind and
  freshness compatibility while preserving the static role contract unchanged.
- Add fictional judicial, counsel-team, litigation-alignment, and municipal
  fixtures and migration guidance for current overlay skills.
- Add governance, documentation, deterministic tests, verification, and
  retrospective evidence.

## Non-goals

- Launching a child agent, defining actual opposing-counsel or judicial-reviewer
  roles, or enumerating every future operation.
- Generating person-specific skills or treating profile data as instructions.
- Git, CaseGraph, a package registry, mutable package access, or electronic
  filing.
