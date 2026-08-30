# Verification

Verified on 2026-08-25 after the direct FilingPacket output correction.

- `python3 -m unittest evaluations.tests.test_filing_packets`
  - 9 tests passed.
- `npm run validate`
  - formatting passed;
  - 27 drafting unit tests passed;
  - 508 evaluation tests passed;
  - 22 skills were discovered;
  - 25 OpenSpec items passed;
  - corpus evaluation completed; and
  - governance validation passed.

The publisher now writes documents and `filing-packet.json` directly beneath the
invocation output root. The loader excludes only `.skill-runs/` and `temp/`
control trees while rejecting every other unlisted file.
