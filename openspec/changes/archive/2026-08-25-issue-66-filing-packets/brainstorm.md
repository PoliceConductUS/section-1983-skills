# Brainstorm: folder-backed FilingPackets

## Selected model

A FilingPacket is an ordinary declared input folder containing
`filing-packet.json` and its member files. The manifest is the sole packet
membership and order authority. Each member has a stable document ID, document
kind, packet role, canonical relative path, byte size, and SHA-256.

The trusted host validates packet bytes within the already validated folder
invocation. Drafting processors return proposed member bytes. The host builds a
complete output packet, records the source packet fingerprint when revising, and
publishes every member plus the manifest through one `OutputRun` beneath the
explicit output folder.

## Alternatives rejected

### Infer packets from directory trees

Rejected. Directory enumeration cannot distinguish document kind from packet
role, does not supply stable identities, and cannot prove intentional order.

### Put packet membership in skill prose

Rejected. Review and filing-readiness checks need a machine-readable, hashed
contract shared across independently installed skills.

### Mutate a source packet in place

Rejected. Folder inputs remain recursively read-only. Revision creates a new
packet with provenance to the input packet fingerprint.

### Use CaseGraph resources

Rejected. Issue #66 is folder-native and has no CaseGraph dependency.

## Target semantics

The packet manifest is the whole-packet target. Any other valid target must be
the exact canonical path of one manifest-listed document. A directory, unlisted
file, missing member, or hash mismatch fails closed.
