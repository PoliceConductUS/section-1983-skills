# Design: folder-backed FilingPackets

## Manifest

`filing-packet.json` is canonical compact UTF-8 JSON with sorted object keys. A
version-1 manifest contains `schema_version`, `packet_id`, `documents`, and
`provenance`. `documents` is an ordered nonempty array. Every document contains:

- unique lower-kebab `id`;
- lower-kebab `kind`, independent from its role;
- one role from `main`, `appendix`, `exhibit`, `proposed-order`, or `other`;
- a canonical relative `path` that is not the manifest or a reserved run path;
- lowercase SHA-256 and exact byte `size`.

Exactly one document has role `main`. Paths and IDs are unique. Array position
is the deterministic packet order. Validation resolves every member beneath the
packet root without following an escape, rejects directories and aliases, reads
the bytes, and verifies size and hash.

## Role authorization

The schema describes possible roles; an operation supplies the expressly
authorized role set. `main` is always required and authorized. A packet using an
appendix, exhibit, proposed-order, or other role fails unless that role is in
the operation's authorized set. The host does not infer authorization from
directory contents.

## Provenance

`provenance` contains the canonical logical input-manifest SHA-256 and either a
null `source_packet_sha256` for new generation or the canonical source manifest
SHA-256 for revision. The source fingerprint covers the exact validated source
manifest bytes. Relocation does not change either fingerprint.

## Publication

The processor proposes deterministic member IDs, kinds, roles, relative paths,
and bytes. The trusted host validates the installed invocation, derives the
logical input manifest, validates any source packet, builds the canonical output
manifest, and publishes all members plus `filing-packet.json` in one
append-immutable `OutputRun` under `filing-packets/<packet-id>/`.

Publication failure never reports completion. Inputs remain byte-for-byte
unchanged. A revision never reuses an existing destination and points back to
the validated source packet fingerprint.

## Review targets and gates

Selecting `filing-packet.json` targets the whole packet. Selecting another path
targets exactly one manifest-listed member. Packet validation occurs before any
quality gate. An unlisted, missing, directory, escaping, size-mismatched, or
hash-mismatched target fails closed.

A configured packet-level quality gate records either whole-packet coverage or
the exact set of document IDs it addressed. Filing readiness requires every
configured gate to pass and to address every required packet member. This is a
mechanical completeness result, not legal judgment or filing authorization.

## Skill boundary

Public drafting and review skills consume declared folders and return content,
findings, or proposed packet members. They do not open ambient paths, mutate a
source packet, publish output directly, or depend on CaseGraph.
