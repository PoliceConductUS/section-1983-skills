# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_source_documented_folders evaluations.tests.test_repository_governance evaluations.tests.test_folder_operations_guide evaluations.tests.test_defense_counsel_overlay_structure evaluations.tests.test_litigation_alignment_overlay_structure
```

Result: 88 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 513 evaluation tests passed.
- 22 installable skills were discovered.
- 25 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- The generic package schema, loader, publisher, fixtures, binder, guide, and
  durable package specification are absent.
- Public profile/overlay guidance uses declared recursive read-only folders,
  direct output, `<output-folder>/temp/`, and domain-owned YAML source records.
- No CaseGraph, graph, package registry, or root package envelope is required.
