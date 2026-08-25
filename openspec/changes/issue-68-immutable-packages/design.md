# Design: immutable folder packages and protected role bindings

## Package envelope

`package-manifest.json` is strict UTF-8 JSON. Trusted-host publication uses
canonical compact sorted-key encoding. Version 1 contains exactly:

- integer `schema_version`;
- lower-kebab `package_kind` and stable `package_id`;
- UTC `created_at`;
- `freshness` with nullable `checked_through` and `retrieved_on` dates;
- `producer` with name, version, operation, and run ID;
- ordered logical `sources` with role, stable source identity, and SHA-256
  fingerprint;
- ordered `members` with stable ID, logical role, classification, canonical
  relative path, media type, byte size, and SHA-256;
- `validation` with status, validator identity/version, UTC validation time, and
  the stable member ID of the validation receipt.

Member classifications are `profile`, `overlay`, `corpus`, `source`,
`provenance`, `classification`, `assumptions`, `gaps`, `validation-receipt`, or
`other`. Domain schemas continue to own the contents of judicial, counsel,
alignment, municipal, and research artifacts.

The manifest lists every regular file in the package. The manifest itself is not
a member. Empty directories have no package identity. Unlisted files, duplicate
filesystem identities, symbolic links, special files, manifest paths, reserved
output paths, and any escaping or noncanonical path fail closed.

## Fingerprint and immutable snapshot

Validation reads the exact manifest bytes and every listed member, verifies size
and SHA-256, rejects extra files, and stores member bytes in a frozen
`ValidatedFolderPackage`. Its package fingerprint is SHA-256 of the exact
manifest bytes; because the strict manifest contains the complete ordered member
inventory and every member hash, that fingerprint binds the complete package
state.

The runtime never asks a role processor to reopen member paths. A later
filesystem change cannot alter the validated in-memory bytes. A configured
maximum byte count bounds the snapshot. Validation uses caller-supplied
freshness requirements rather than ambient assumptions about how old a package
may be.

## Freshness and validation

The common envelope permits checked-through, retrieval, or both dates. A
protected role contract selects the required basis and maximum age. Binding
receives an explicit `as_of` date and fails when the required date is absent,
future-dated, or older than the allowed age.

Consumed packages require validation status `pass`. The named receipt member
must exist and have classification `validation-receipt`. Unsupported schema
versions, failed validation, malformed dates, and missing or mismatched receipts
fail before role execution.

## Publication and regeneration

The trusted host accepts only an invocation already bound to one installed skill
contract. It validates proposed source identities, members, freshness, producer
values, and receipt linkage, derives the logical input manifest, and publishes
every member plus canonical `package-manifest.json` through one `OutputRun`
beneath `packages/<package-id>/`.

Regeneration creates a complete new package beneath a caller-selected fresh
output root. It may preserve the stable package ID while producing a new
fingerprint. Source package IDs and fingerprints remain in `sources`. No input
package or context folder is changed.

## Protected static role contract

A static role contract contains one role kind, accepted profile-package kinds, a
freshness policy, declared capabilities and prohibitions, internet policy, the
immutable-target rule, and explicit-output-only authority. Actual public role
contracts remain owned by later role stories.

The Issue #68 binder validates a fictional or future static role contract and a
`ValidatedFolderPackage`, then returns canonical role-contract bytes beside the
profile snapshot. It never overlays, updates, or interprets profile fields as
contract fields. Profile artifacts may contain participant-specific context and
even instruction-shaped hostile text; none can add a capability, remove a
prohibition, change internet policy, mutate a target, or enlarge output
authority.

## Existing package families

Fictional fixtures cover `judicial-profile`, `counsel-team-profile`,
`litigation-alignment`, and `municipal-profile`. Current counsel and alignment
domain artifacts remain valid under their existing schemas and become members of
the common envelope. Existing skills link to the common package contract but
retain their substantive domain validation.

## Boundaries

Issue #68 does not launch agents, define real participant profiles, choose a
litigation operation, or pass a target to a child. Issue #33 builds judicial
profiles, Issue #61 owns isolated launch, and Issues #62 and #63 own concrete
roles and orchestration.
