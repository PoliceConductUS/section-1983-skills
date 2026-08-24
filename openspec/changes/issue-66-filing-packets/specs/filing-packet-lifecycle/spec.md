# filing-packet-lifecycle Delta

## ADDED Requirements

### Requirement: FilingPacket manifests define complete ordered packets

A FilingPacket manifest MUST define a nonempty deterministic document order,
stable unique document identities, independent document kinds and packet roles,
canonical relative member paths, exact byte sizes, and lowercase SHA-256 values.
It MUST contain exactly one main document and MUST resolve every listed member
inside the declared packet root with matching bytes.

#### Scenario: An amended complaint changes packet role

- **WHEN** the same amended-complaint document kind is the main document in one
  packet and an exhibit in another
- **THEN** each manifest preserves its document kind while recording the packet-
  specific role and order

### Requirement: Packet generation and revision preserve source inputs

The trusted host MUST publish a complete proposed FilingPacket beneath the
explicit output folder without mutating a source packet or context input. A
revision MUST record the validated source packet fingerprint and every output
MUST record the logical input-manifest fingerprint.

#### Scenario: A source packet is revised

- **WHEN** a drafting operation proposes changed and unchanged packet members
- **THEN** the host creates a new complete packet and the source packet remains
  byte-for-byte unchanged

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
