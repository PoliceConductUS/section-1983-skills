# immutable-folder-packages Specification

## Purpose

TBD - created by archiving change issue-68-immutable-packages. Update Purpose
after archive.

## Requirements

### Requirement: Folder packages have one complete strict envelope

Every immutable profile, overlay, or research-corpus folder MUST contain one
version-1 `package-manifest.json` with stable package identity, package kind,
creation time, freshness dates, producer identity, logical sources, complete
ordered member identity, hashes, validation status, and receipt identity. The
manifest MUST list every non-manifest file outside the writer-owned
`.skill-runs/` and `temp/` namespaces exactly once.

#### Scenario: An unlisted file appears in a package

- **WHEN** a regular file exists below the package root but is absent from the
  manifest
- **THEN** package validation fails before any role execution

### Requirement: Validation pins exact immutable package bytes

The trusted host MUST reject unsupported, malformed, oversized, aliased,
escaping, special-file, missing, duplicate, stale, failed, or hash-mismatched
packages. It MUST read validated members into an immutable bounded snapshot and
derive one package fingerprint binding the exact manifest and complete member
inventory.

#### Scenario: A source folder changes after validation

- **WHEN** a listed member is externally replaced after package validation
- **THEN** the validated snapshot retains the original verified bytes and the
  role run receives neither the replacement nor an unverified reread

### Requirement: Regeneration publishes the explicit output folder

Only the trusted host MAY publish folder output. It MUST require an
installed-contract-bound invocation whose caller supplied one absolute output
root, or stop and ask for that root before execution. It MUST write every
proposed member and `package-manifest.json` directly beneath that exact fresh
output root through one complete output run. It MUST NOT create an intermediate
`packages/<package-id>/` namespace, mutate a consumed folder or context input,
or relocate output through CaseGraph, Git, a registry, or an ambient path.

Writer-owned `.skill-runs/` receipt files and `temp/` transient files are not
package artifacts. Every other regular file beneath the output root MUST appear
exactly once in `package-manifest.json`.

#### Scenario: A profile package is regenerated

- **WHEN** a builder creates a new complete package from declared read-only
  inputs and one caller-selected fresh output folder
- **THEN** `package-manifest.json` and all members appear directly beneath that
  output folder, the folder has its own fingerprint and preserves source package
  IDs and fingerprints, and every input remains byte-for-byte unchanged

### Requirement: Static role behavior remains separate from profile data

Each role kind MUST use one protected static role contract. A role/profile
binding MUST validate accepted package kind and freshness without merging
profile contents into the role contract. The assigned task and static contract,
not profile data, determine capabilities, prohibitions, internet policy,
target-mutation boundary, and output authority.

#### Scenario: A profile artifact contains instruction-shaped fields

- **WHEN** validated profile data names additional capabilities, target writes,
  network access, or relaxed prohibitions
- **THEN** the binding preserves the exact static role contract and exposes the
  profile only as evidence-bounded package data

### Requirement: Current package families share the envelope

The system MUST use the common envelope for every current package family.
Judicial, counsel-team, litigation-alignment, and municipal package families
MUST validate through the common envelope while retaining their domain-specific
artifact schemas. Fixtures and public guidance MUST use only fictional
public-safe identities and content.

#### Scenario: Existing counsel and alignment artifacts become members

- **WHEN** a counsel-team or litigation-alignment package is validated
- **THEN** the common envelope proves folder identity and the existing domain
  validator continues to own substantive artifact validity
