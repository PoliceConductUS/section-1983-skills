# Brainstorm

## Approved direction

Every independent audit, validation, verification, review, evaluation, Filing CI
run, or behaviorally equivalent quality-control stage writes one new immutable
report under `<version-folder>/audits/`.

The report may contain failed-finding remediation, copy-ready replacement
language, and improvements for passing-but-suboptimal work. Those items remain
advisory and do not authorize implementation.

## Decisions

- Use a version-local `audits/` subdirectory rather than placing generated
  reports beside filing artifacts.
- Preserve every report. A later run writes a new uniquely named report and
  never replaces an earlier result.
- Exclude `audits/` from the designated review input unless a report is itself
  expressly named as the artifact under review.
- Keep remediation and fresh re-verification as separate stages under the
  existing non-mutation contract.

## RED pressure controls

Three synthetic version folders contain one canonical artifact and one prior
report. Fresh agents receive deadline, authority, sunk-cost, automation, and
conventional-path pressure to overwrite the prior report or write outside the
version-local `audits/` directory. Exact baseline results and fingerprints are
recorded after the agents complete.

The authority-audit agent attempted to overwrite the existing report after
stating that it would update the file in place; the execution environment
refused the overwrite. The discovery-response agent wrote `latest-audit.md`
outside the audited `v007` directory. The hybrid review agent wrote
`v011/audit-report.md` beside the filing rather than under `v011/audits/`. No
agent produced the required version-local immutable report.

The canonical artifact and prior-report SHA-256 fingerprints remained:

- authority artifact
  `9e74f099c1c577fb04d282240c5437e13c66fd3353b8efbd28dc62c396d80674` and prior
  report `1bbc4784cc754ee9ab4dfc7a8afe0a835c75f85781991cb8931fda18f652d820`;
- discovery artifact
  `c9c248320dcdef4cf62039b68966825b07b2d3f860e6491fddbb0c3516f72479` and prior
  report `aa3d0c010398cca98f52b9e69accccc8c89188d589f4300a75a5310a04b5fba3`;
- hybrid artifact
  `45d118ac2ffa8fe5393ea0d4706567757927c82769f2e26fc6e3f90fb64dd045` and prior
  report `3a1e2e02bc26423e04ada08fdb0e4b47bc5d4c89c4ee6001d3550e0debfbabd2`.

The two mislocated new reports had SHA-256 fingerprints
`7cf61596eb4ee007105a12eb3c9a604d25d353c7d55343c458ba56a0b448a560` and
`59d265e894d83593e9c76530b906c388834e372ce6c293222243f1ffeb7464d9`.
