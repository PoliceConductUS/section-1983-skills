# Proposal: Remove the FilingPacket persistence abstraction

## Why

The current repository still treats a filing folder as a `FilingPacket` defined
by `filing-packet.json`, a schema, a loader, a publisher, and packet membership
rules. That contradicts the corrected folder boundary: skills receive only
declared input folders and ordinary files and write to one explicit output
folder.

## What changes

- Delete the FilingPacket implementation, schema, fixtures, tests,
  documentation, install-local references, and active lifecycle specification.
- Remove FilingPacket sections from current skill instructions and current
  governance requirements.
- Define ordinary filing-folder behavior using declared recursive read-only
  roles and explicit role-relative target paths.
- Preserve direct writes to the exact output folder and exclusive temporary use
  of `<output-folder>/temp/`.
- Add regression governance proving no replacement persistence abstraction is
  introduced.

## Capability

- `ordinary-filing-folders`

## Non-goals

- No legal-workflow redesign, universal source YAML schema, electronic filing,
  rewrite of archived OpenSpec history, or replacement folder object model.
