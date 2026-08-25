# filing-packet-lifecycle Specification

## Purpose

TBD - created by archiving change issue-66-filing-packets. Update Purpose after
archive.

## Requirements

### Requirement: FilingPacket manifests define complete ordered packets

A FilingPacket manifest MUST define a nonempty deterministic document order,
stable unique document identities, independent document kinds and packet roles,
canonical relative member paths, exact byte sizes, and lowercase SHA-256 values.
It MUST contain exactly one main document and MUST resolve every listed member
inside the declared packet root with matching bytes. The manifest and members
MUST be regular files at their canonical logical paths, not symbolic-link or
other filesystem aliases. The published schema and runtime validator MUST accept
the same version and member-path language.

#### Scenario: An amended complaint changes packet role

- **WHEN** the same amended-complaint document kind is the main document in one
  packet and an exhibit in another
- **THEN** each manifest preserves its document kind while recording the packet-
  specific role and order

#### Scenario: A manifest or member is an alias

- **WHEN** `filing-packet.json` or a listed member is a symbolic link, even one
  whose target remains inside the packet root
- **THEN** packet validation fails closed rather than assigning packet identity
  to aliased bytes

#### Scenario: Schema and runtime validate the same manifest values

- **WHEN** a manifest uses a boolean schema version, the manifest filename, a
  reserved output namespace, a noncanonical path, or a NUL-containing path as a
  member path
- **THEN** both the public schema and runtime validator reject that value

### Requirement: Revisions publish to the explicit output folder

A generation or revision invocation MUST receive one caller-selected absolute
fresh output folder, or stop and ask for it before work. The trusted host MUST
publish every proposed document and `filing-packet.json` directly beneath that
exact folder through one complete output run. It MUST NOT create an intermediate
`filing-packets/<packet-id>/` namespace or mutate the source packet. A revision
MUST record the validated source packet fingerprint and every output MUST record
the logical input-manifest fingerprint. Publication MUST receive an invocation
already bound to one installed skill's exact folder contract; a generic
folder-valid invocation MUST fail closed before starting an output run.

Writer-owned `.skill-runs/` receipts and `temp/` transient files are not packet
members. Every other regular file beneath the output root MUST resolve from and
match `filing-packet.json`.

#### Scenario: A source packet is revised

- **WHEN** a drafting operation proposes changed and unchanged packet members
- **THEN** the host creates the new complete packet directly in the selected
  output folder and the source packet remains byte-for-byte unchanged

#### Scenario: A generic invocation requests publication

- **WHEN** the publisher receives an invocation that was not validated against
  the installed skill package
- **THEN** it publishes no packet and reports an unbound invocation

### Requirement: Review targets are packet-bound

A review, authority audit, Filing CI, or adversarial review MUST target either
the FilingPacket manifest as a whole or exactly one manifest-listed document. An
unlisted, missing, escaping, directory, size-mismatched, or hash-mismatched
target MUST fail closed.

#### Scenario: A caller targets an unlisted file

- **WHEN** a file exists under the packet root but is absent from the manifest
- **THEN** review does not treat it as a packet member and publishes no result

### Requirement: Filing readiness requires complete packet gate coverage

A filing-ready result MUST require every required packet member to validate and
every configured packet-level quality gate to pass while addressing the whole
packet or every member. The result MUST remain mechanical and MUST NOT decide
legal quality, strategy, or filing authorization.

#### Scenario: One exhibit is omitted from Filing CI coverage

- **WHEN** the packet validates but one configured quality gate omits a required
  exhibit
- **THEN** the packet is not filing-ready and the missing document identity is
  reported
