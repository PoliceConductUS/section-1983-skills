# Immutable Folder Packages

An immutable folder package is the caller-selected output directory itself. It
contains `package-manifest.json` and the regular files listed by that manifest
directly beneath that root. This contract is independent of CaseGraph, Git, a
package registry, and any ambient workspace convention.

## Trusted-host boundary

The trusted host validates a package before a skill or role receives it. It
rejects malformed metadata, unsupported package kinds, stale packages, symlinks,
special files, path escapes, duplicate identities, missing files, unlisted
files, failed validation, invalid receipt linkage, byte-limit excess, and hash
or size mismatches. Every non-manifest regular file must appear exactly once in
the ordered `members` array.

Validation reads every member into a bounded immutable byte snapshot. The role
run uses only that snapshot; it never rereads the source folder. The package
fingerprint is the SHA-256 of the exact manifest bytes, whose complete member
inventory binds every member's SHA-256 and size.

Only the trusted host may publish a package. Publication requires an invocation
bound to an installed folder contract and writes every member plus
`package-manifest.json` directly beneath the caller's explicit fresh output
folder. It does not add a `packages/<package-id>/` namespace. Inputs remain
recursively read-only. Regeneration requires another fresh output folder,
creates a complete replacement package with a new fingerprint, and preserves
declared source package identities and fingerprints. `.skill-runs/` contains
trusted-host receipts, and `temp/` is the invocation's only transient workspace;
neither is a package member.

## Manifest fields

Version 1 records `package_kind`, stable `package_id`, UTC `created_at`,
explicit freshness dates, producer and operation identity, ordered logical
sources, ordered complete members, and a passed validation receipt. Member
classifications distinguish profiles, overlays, corpora, sources, provenance,
classification, assumptions, gaps, validation receipts, and other artifacts.

The public schema is
[`governance/immutable-folder-package.schema.json`](governance/immutable-folder-package.schema.json).
Judicial-profile, counsel-team-profile, litigation-alignment, and
municipal-profile packages share this envelope while retaining their existing
domain-artifact schemas and validators.

## Static roles remain protected

A profile package is data for an agent playing a role; it is not executable role
configuration. The protected static role contract exclusively determines
capabilities, prohibitions, internet policy, target-mutation policy, and output
authority. Binding checks package kind and freshness while keeping canonical
role-contract bytes separate from the immutable package snapshot. Instructions
or capability-shaped fields inside profile data cannot alter role behavior.

The public schema is
[`governance/static-role-contract.schema.json`](governance/static-role-contract.schema.json).
The launcher and actual role contracts are separate later stories.
