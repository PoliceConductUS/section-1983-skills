# Brainstorm: immutable folder packages

## Selected model

Every immutable profile, overlay, or research-corpus folder carries one strict
`package-manifest.json` sidecar. Domain JSON remains in independently validated
member artifacts; the common envelope owns membership, logical roles, freshness,
provenance, fingerprints, producer identity, and validation receipt identity.

The trusted host validates a package into an immutable in-memory byte snapshot.
A role binding keeps the protected static role contract and profile package in
separate namespaces and never merges package data into behavior. The shared
launcher in Issue #61 will later consume this validated binding.

## Alternatives rejected

### Add common fields to every domain schema

Rejected. Judicial, counsel-team, litigation-alignment, municipal, and research
schemas would duplicate filesystem validation, provenance, freshness, and
fingerprinting rules and drift independently.

### Infer packages from directory conventions

Rejected. Directory names cannot establish intentional membership, stable
identity, source roles, validation state, or one reproducible fingerprint.

### Put profile differences into generated skills

Rejected. Person-, team-, court-, posture-, and assumption-specific material is
data. Behavior remains in one protected static contract per role kind.
