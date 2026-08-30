# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_static_role_launcher evaluations.tests.test_adversarial_shared_role evaluations.tests.test_adversarial_review_launcher evaluations.tests.test_adversarial_review_runtime evaluations.tests.test_adversarial_review_structure
```

Result: 42 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 543 evaluation tests passed.
- 22 installable skills were discovered.
- 27 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- Role inputs are selected ordinary files from declared recursive read-only
  folders; there is no package, manifest, graph, CaseGraph, repository, or
  ambient-workspace input abstraction.
- The child request contains logical names, exact UTF-8 bytes, hashes, and sizes
  but no absolute input or output path.
- A role-owned validator runs before dispatch. The adversarial role validates
  strict source YAML, root-relative source paths, source and YAML hashes,
  checked-through dates, source identities, and exact selections.
- The fresh process working directory and `TMPDIR`, `TMP`, and `TEMP` are all
  beneath `<output-folder>/temp/<run-id>/`.
- The adversarial role preserves five categories, corrections,
  plaintiff-decision gates, read-only targets, and bounded failures.
