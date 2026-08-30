# Proposal: generate and review folder-backed FilingPackets

## Why

Current folder contracts can select individual filing files but do not define a
complete multi-document filing unit. Complaint packages, leave-to-amend motions,
responses, proposed orders, and exhibit sets need stable membership, order,
roles, hashes, revision provenance, and packet-level review coverage without an
external persistence product.

## What changes

- Add a strict version-1 FilingPacket manifest schema and standard-library
  validator.
- Require stable document IDs, deterministic array order, independent document
  kinds and packet roles, canonical confined paths, byte sizes, and SHA-256.
- Require exactly one `main` member and explicit authorization for every other
  role used by an operation.
- Add a trusted-host packet planner/publisher that writes one complete proposed
  packet beneath the invocation output and never mutates source/context inputs.
- Record source packet and logical input-manifest fingerprints for revisions.
- Resolve review targets as either the packet manifest or one listed member and
  require packet-level gates to address all required members before a
  filing-ready result.
- Add four synthetic packet fixtures and deterministic tests.
- Update relevant public skill guidance and durable contracts.

## Non-goals

- Electronic filing or court-specific role catalogs.
- Mutation of an input packet.
- CaseGraph, graph resources, repository history, or a universal runner.
