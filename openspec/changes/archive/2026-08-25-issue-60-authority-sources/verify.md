# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_collecting_legal_authority_sources evaluations.tests.test_skill_folder_contracts evaluations.tests.test_source_documented_folders evaluations.tests.test_repository_governance evaluations.tests.test_skill_folder_guidance
```

Result: 62 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 602 evaluation tests passed.
- 28 installable skills were discovered.
- 35 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- Inputs are exactly `legal-question`, `jurisdiction`, `court-hierarchy`,
  `relevant-date`, `seed-authority`, and `approved-source-system`; target is
  none and internet is authorized only for bounded collection.
- Retrieved material remains ordinary files beneath `sources/` with adjacent
  strict domain YAML and matching SHA-256.
- Source type, decision-date state, proposed or mistaken identity, review state,
  limitations, duplicates, exact queries, dates, result identities, and coverage
  gaps remain explicit.
- The helper accepts in-memory values and returns deterministic output-relative
  bytes; it cannot open folders, publish files, or use the internet.
- The shared writer preserves inputs, confines durable output to the explicit
  output folder, records artifact-level internet provenance, and binds cwd,
  `TMPDIR`, `TMP`, and `TEMP` to `<output-folder>/temp/`.
- Fictional fixtures cover unofficial mirrors, mistaken identities, duplicate
  relationships and result identities, changed bytes, instruction-shaped fields,
  incomplete and empty searches, and collector/auditor separation.
- No case-data package, package loader, FilingPacket, graph, CaseGraph,
  repository, Git, datastore, or ambient workspace is required.
