# filing-packet-lifecycle Specification Delta

## MODIFIED Requirements

### Requirement: Revisions publish to the explicit output folder

A generation or revision invocation MUST receive one caller-selected absolute
fresh output folder, or stop and ask for it before work. The trusted host MUST
publish every proposed document and `filing-packet.json` directly beneath that
exact folder through one complete output run. It MUST NOT create an intermediate
`filing-packets/<packet-id>/` namespace or mutate the source packet.

Writer-owned `.skill-runs/` receipts and `temp/` transient files are not packet
members. Every other regular file beneath the output root MUST resolve from and
match `filing-packet.json`.

#### Scenario: A drafting stage revises a packet

- **WHEN** a drafting stage receives a source packet and a distinct fresh
  absolute output folder
- **THEN** it writes the complete new packet directly into that output folder,
  preserves source fingerprint provenance, and leaves the source packet
  byte-for-byte unchanged
