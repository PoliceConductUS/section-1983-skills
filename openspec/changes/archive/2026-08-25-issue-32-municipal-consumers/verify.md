# Verification

## Focused

The focused suite covered municipal-profile validation, optional folder-role
composition, folder-scoped execution, repository governance, install-local
guidance, adversarial-review runtime dispatch, and existing filing behavior.

Result: 98 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result at pushed commit `c237289`:

- Prettier check passed.
- 27 drafting tests passed.
- 617 evaluation tests passed.
- 29 installable skills were discovered.
- 37 OpenSpec items passed with the change active.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- The municipal profile is an optional declared recursive read-only input role;
  existing non-profile invocations remain valid.
- A task that requests municipal-profile use must supply the complete four-file
  profile folder and may not substitute an empty placeholder.
- The adversarial runtime validates exact profile files and source bytes before
  provider dispatch and keeps the validator inside the installed skill.
- Profile validation checks artifact hashes, source hashes, upstream hashes,
  identity, staleness, folder fingerprint, and exact record shapes.
- Outputs remain ordinary files in the caller's exact output folder and all
  temporary work remains under `<output-folder>/temp/`.
- No CaseGraph, graph, repository, or ambient-workspace dependency was added.
