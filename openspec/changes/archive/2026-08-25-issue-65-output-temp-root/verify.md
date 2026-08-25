# Verification

Verified on 2026-08-25 at branch head after the exclusive invocation-temp
implementation.

## Focused verification

- `python3 -m unittest evaluations.tests.test_skill_output_writer`
  - 62 tests passed.
- `npm run openspec:validate`
  - 23 OpenSpec items passed.

## Full verification

- `npm run validate`
  - formatting passed;
  - 26 drafting unit tests passed;
  - 438 evaluation tests passed;
  - 22 skills were discovered;
  - 23 OpenSpec items passed;
  - corpus evaluation completed; and
  - governance validation passed.

## Boundary evidence

- Writer staging is created only beneath `temp/<run-id>/` relative to the
  retained output-root directory descriptor.
- Public artifact paths beginning with `temp/` or `.skill-runs/` fail before an
  artifact attempt.
- The trusted-host process configuration selects canonical
  `<output-folder>/temp/` for `cwd`, `TMPDIR`, `TMP`, and `TEMP`.
- Synthetic alias tests prove `temp` namespace and run-ID symlinks do not write
  through to outside directories.
- Existing atomic publication, failure injection, collision, receipt, retry, and
  input-preservation tests remain green after moving staging.
