# Proposal: publish FilingPackets at the explicit output root

## Why

The original publisher writes to `<output-folder>/filing-packets/<packet-id>/`.
The clarified invocation contract supplies the full output-folder path for the
generated packet, making that intermediate namespace incorrect.

## What changes

- Write `filing-packet.json` and all documents directly beneath the invocation's
  fresh output root.
- Treat `.skill-runs/` and `temp/` as trusted-host control namespaces, not
  packet members.
- Update the schema, loader, guidance, and deterministic tests.

## Non-goals

- Removing packet identity, revision provenance, hashes, or document roles.
- Adding a registry, CaseGraph path, Git operation, or electronic filing.
