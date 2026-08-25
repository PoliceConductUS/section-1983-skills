# Verification

Verified on 2026-08-25 after restacking on the corrected direct-root
FilingPacket foundation.

- `python3 -m unittest evaluations.tests.test_immutable_folder_packages`
  - 14 tests passed.
- `npm run validate`
  - formatting passed;
  - 27 drafting unit tests passed;
  - 523 evaluation tests passed;
  - 22 skills were discovered;
  - 26 OpenSpec items passed;
  - corpus evaluation completed; and
  - governance validation passed.

The publisher now writes `package-manifest.json` and members directly beneath
the selected output root. The same root reloads successfully while
`.skill-runs/` and `temp/` remain trusted-host control namespaces rather than
package artifacts.
