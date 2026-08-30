# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_folder_native_filing_integrity evaluations.tests.test_filing_packets evaluations.tests.test_installed_filing_checks evaluations.tests.test_skill_folder_contracts evaluations.tests.test_repository_governance
```

Result: 75 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 563 evaluation tests passed.
- 24 installable skills were discovered.
- 30 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- Runtime inputs are only the six declared recursive read-only folders and
  strict selected source-documentation YAML records.
- YAML binds relative ordinary file paths, hashes, checked-through dates,
  classifications, and source identities; it cannot add behavior or redefine a
  selected folder role.
- The checker uses no case-data package, package loader, graph, CaseGraph,
  repository, Git, ambient folder discovery, or internet access.
- Durable JSON, Markdown, and YAML output is published only beneath the explicit
  output folder. Staging and transient files remain beneath its `temp/`
  directory.
- Repeated runs over identical inputs produce identical report and receipt
  bytes, while every selected input remains byte-identical.
- The checker reports only mechanical findings and does not decide fact truth,
  legal sufficiency, authority quality, strategy, or filing readiness.
