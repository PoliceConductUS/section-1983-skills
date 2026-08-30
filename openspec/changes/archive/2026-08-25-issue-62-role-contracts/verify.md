# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_profile_conditioned_roles evaluations.tests.test_skill_folder_contracts
```

Result: 15 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 548 evaluation tests passed.
- 24 installable skills were discovered.
- 28 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- Each role receives selected exact bytes only from declared recursive read-only
  `profile`, `filing`, and `approved-sources` folders.
- The role-owned validators accept the existing defense-counsel and judicial
  profile schemas and require validated source-documentation YAML plus its
  hash-matched ordinary source file.
- The child receives no local input or output paths. Its fresh working directory
  and `TMPDIR`, `TMP`, and `TEMP` are beneath `<output-folder>/temp/<run-id>/`.
- Output validation is findings-only, source-allowlisted, and fail-closed.
  Checked-in fixtures prove disposition fields and profile attempts to add
  capabilities are rejected for both roles.
- The selected filing and every other selected input remain unchanged; the child
  has no durable-write authority.
- No package, manifest, graph, CaseGraph, repository, or ambient-workspace
  abstraction appears in the runtime implementation.
