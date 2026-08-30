# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_assessing_police_policy_compliance evaluations.tests.test_skill_folder_contracts evaluations.tests.test_source_documented_folders evaluations.tests.test_repository_governance evaluations.tests.test_skill_folder_guidance
```

Result: 63 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 595 evaluation tests passed.
- 27 installable skills were discovered.
- 34 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- Inputs are exactly `policy-catalog`, `actor`, `event`, `phase`, `case-record`,
  and `assessment-scope`; target is none and internet is disabled.
- The catalog is ordinary Issue #57 output. Selected case sources are ordinary
  files with adjacent domain YAML, folder-relative paths, and matching SHA-256.
- Assessment-scope YAML must authorize the exact selected source-documentation
  paths and cannot add roots or capabilities.
- The helper accepts in-memory values and returns deterministic output-relative
  bytes; it cannot open folders, publish files, or use the internet.
- The shared writer preserves inputs, confines durable output to the explicit
  output folder, and binds cwd, `TMPDIR`, `TMP`, and `TEMP` to
  `<output-folder>/temp/`.
- Fictional fixtures cover every applicability, violation, and evidence state;
  separate actors and phases; policy dates; changed evidence; stale catalog
  validation; missing and conflicting evidence; undeclared source paths; and
  exact input fingerprints.
- No case-data package, package loader, FilingPacket, graph, CaseGraph,
  repository, Git, datastore, or ambient workspace is required.
