# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_analyzing_police_policy_sources evaluations.tests.test_skill_folder_contracts evaluations.tests.test_source_documented_folders evaluations.tests.test_repository_governance evaluations.tests.test_skill_folder_guidance
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
- 587 evaluation tests passed.
- 26 installable skills were discovered.
- 33 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- Inputs are exactly `department-identity`, `jurisdiction`, `policy-source`, and
  `analysis-scope`; target is none and internet is disabled.
- Source material is ordinary files plus adjacent strict domain YAML. Every
  selected file is bound to its documented relative path and SHA-256.
- Only adopted policy with documented adoption, a candidate source record, and
  separate analysis approval may generate a requirement.
- The helper accepts in-memory values and returns only deterministic
  output-relative bytes; it cannot open folders, publish files, or use the
  internet.
- The shared trusted-host writer preserves inputs, confines durable output to
  the explicit output folder, and binds cwd, `TMPDIR`, `TMP`, and `TEMP` to
  `<output-folder>/temp/`.
- Fictional fixtures cover all four requirement types, triggers, exceptions,
  cross-references, source changes, retroactive dates, malformed provenance,
  rejected source records, and explicit gaps.
- No case-data package, package loader, FilingPacket, graph, CaseGraph,
  repository, Git, datastore, or ambient workspace is required.
