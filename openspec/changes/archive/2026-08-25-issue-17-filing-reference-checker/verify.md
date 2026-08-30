# Verification

## RED and focused GREEN

The new regression supplied `checked_through: 20260825`. Python parsed that
value, and the pre-fix host incorrectly continued through checker execution and
output publication instead of raising an invalid source-documentation result.

After moving the canonical comparison into `_date`, the focused suite covered
the folder-native Filing CI host, isolated installed checkers, exact folder
contracts, folder-scoped execution, and repository governance.

Result: 84 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result at pushed commit `4749e73`:

- Prettier check passed.
- 27 drafting tests passed.
- 615 evaluation tests passed.
- 29 installable skills were discovered.
- 38 OpenSpec items passed with the change active.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- The existing six required recursive read-only folder roles remain unchanged.
- Target remains required in `filing-source`; internet remains disabled.
- Domain YAML binds exact ordinary source bytes by role, classification, path,
  SHA-256, checked-through date, and exact fields before checker execution.
- Noncanonical date input is `invalid`, invokes no checker, and publishes no
  output.
- The installed checker remains deterministic and usable from an isolated skill
  copy without a repository path, external executable, persistence service, or
  network access.
- JSON, Markdown, receipt, and terminal output remain beneath the exact output
  folder; temporary work remains beneath `<output-folder>/temp/`.
- No filing-folder object, folder-wide membership file, graph, CaseGraph
  dependency, datastore, or ambient workspace was added.
