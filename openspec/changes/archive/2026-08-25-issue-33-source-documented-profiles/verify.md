# Verification

## Focused

Commands covered the Judicial Reasoning Profile tests, repository governance,
folder contracts, skill-folder guidance, judge-overlay guidance, folder
operations, and source-documented folders.

Result: 110 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 529 evaluation tests passed.
- 22 installable skills were discovered.
- 27 OpenSpec items passed with the correction active.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- The generic builder and real-judge-skill removal remain intact.
- Acquisition publishes ordinary source bytes and `SOURCE.yaml` provenance.
- Compilation publishes `judicial-profile.json`,
  `judicial-profile-sources.yaml`, and `validation-receipt.json`.
- No package helper, folder envelope, package manifest, graph, or CaseGraph
  dependency is present.
- All invocation temporary work remains under `<output-folder>/temp/`.
