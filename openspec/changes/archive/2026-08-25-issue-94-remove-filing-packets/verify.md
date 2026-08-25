# Verification

## RED and focused GREEN

The new migration suite initially failed on 23 obsolete surfaces: the runtime
module, schema, fixtures, specialized tests, public guide, active lifecycle
specification, five install-local contracts, five skill sections, and current
public guidance.

After deletion and ordinary-folder updates, the focused suite covered the
migration regression contract, folder-operation guidance, and the existing
complaint fail-closed composition guard.

Result: 35 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result at pushed commit `8882b90`:

- Prettier check passed.
- 27 drafting tests passed.
- 614 evaluation tests passed.
- 29 installable skills were discovered.
- 37 OpenSpec items passed with the change active.
- evaluation corpus generation passed.
- governance validation passed.

## Deletion and boundary audit

- The implementation deletes 1,126 lines and adds 130 lines of replacement tests
  and ordinary-folder guidance.
- `FILING_PACKETS.md`, `scripts/filing_packet.py`, the schema, fixtures,
  specialized tests, active lifecycle spec, and five install-local references
  are absent.
- Current non-historical code, skill instructions, public guidance, and active
  specifications contain no FilingPacket contract or required filing manifest.
- The five affected skills identify ordinary files by declared input role and
  folder-relative path and do not infer folder membership.
- Durable writes remain beneath the exact output folder, and cache, extraction,
  staging, working-directory, and temporary bytes remain beneath
  `<output-folder>/temp/`.
- No replacement manifest, loader, publisher, index, registry, graph,
  repository, datastore, ambient workspace, or folder object was added.
