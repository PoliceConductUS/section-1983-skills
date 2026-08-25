# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_collecting_police_policy_sources evaluations.tests.test_skill_folder_contracts evaluations.tests.test_source_documented_folders evaluations.tests.test_repository_governance evaluations.tests.test_skill_folder_guidance
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
- 580 evaluation tests passed.
- 25 installable skills were discovered.
- 32 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- Runtime inputs are exactly `department-identity`, `jurisdiction`,
  `approved-source-system`, and `research-scope`; target is none and internet is
  authorized only for bounded collection.
- The helper returns only deterministic output-relative artifact plans and has
  no filesystem, output-root, temporary-directory, process, or network API.
- Every retrieved ordinary file has adjacent domain YAML with matching SHA-256,
  URL, retrieval time, classification, proposed adoption relationship,
  effective-date evidence or gap, limitations, and duplicate relationships.
- The shared writer publishes artifacts only beneath the explicit output folder,
  records internet provenance, and binds cwd, `TMPDIR`, `TMP`, and `TEMP` to
  `<output-folder>/temp/`.
- Fixtures are fictional and cover model-policy separation, uncertain adoption,
  missing versions, incomplete coverage, changed bytes, detached documentation,
  unknown duplicate references, and collector/analyzer separation.
- Inputs remain byte-identical. No case-data package, package loader,
  FilingPacket, graph, CaseGraph, repository, Git, datastore, or ambient
  workspace is required.
