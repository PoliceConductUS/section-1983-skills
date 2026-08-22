# Verification

## Branch and scope

- Branch: `codex/issue-30-defense-counsel-overlays`
- Parent: `codex/issue-29-litigation-alignment-overlays`
- Pre-archive reviewed HEAD: `a7d43b0`
- Commits: design `2749a59`, RED `e998d6f`, GREEN `95c45ff`, and integrity
  review correction `a7d43b0`.
- No dependency, workflow, root `docs/`, `.superpowers/`, private case data,
  paid retrieval, filing edit, PR, or issue closure was added.

## Public result

- `building-defense-counsel-overlays` consumes one immutable approved public-
  source snapshot and publishes two install-local Draft 2020-12 schemas, one
  standard-library validator, and four generic synthetic fixtures.
- Identity, time-bounded counsel teams, historical arguments, judicial
  treatments, current attack links, patterns, forecasts, overrides, gaps, and
  review slices remain separately keyed and fingerprinted.
- Joint filings default to counsel-team behavior. Signer, named-author, oral-
  advocate, appearance-counsel, and listed-counsel roles remain distinct, and an
  appearance or listing cannot establish individual authorship.
- Patterns and forecasts require a reconciled complete denominator, missingness,
  posture, support, contrary evidence, confidence, sources, and checked-through
  date. Incomplete public coverage degrades to bounded examples and gaps.
- Blind review receives no counsel material. Actual-adversary review receives
  only the effective team's relevant slice, and a forecast cannot suppress a
  common attack.
- `COUNSEL_OVERLAYS.md` owns counsel-specific sources, attribution, calibration,
  substitution, realignment, and lifecycle triggers. `OVERLAYS.md` retains the
  shared inventory, precedence, manifest, immutable-version, and supersession
  rules.

## TDD and review evidence

- Initial RED ran 22 methods with 23 expected failures for the absent skill,
  schemas, validator, fixtures, guide, routes, governance registration, and
  filing-manifest kinds.
- Focused GREEN reached 23 methods after malformed nested IDs, common-attack
  classification, and formatted-prose normalization were corrected.
- A schema drift guard made all ten overlay record shapes concrete and now
  compares every published required-field set with the validator constants.
- Whole-story pressure added test-backed source-union checks for identity, team,
  patterns, forecasts, and current attacks; team effective dates; invalid source
  snapshot gating; full filing-manifest pin validation; and cross-record
  attribution.
- Exhaustive mutation of every fixture leaf to a list and object produced zero
  validator exceptions after correction.

## Commands

- `python3 -m unittest evaluations.tests.test_defense_counsel_overlay_structure evaluations.tests.test_defense_counsel_overlay_validator -q`
  — 28 focused tests passed.
- `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/building-defense-counsel-overlays`
  — `Skill is valid!`.
- `npm run validate` — passed after review correction: formatting; 16 drafting
  tests; 341 evaluation tests; 22 discovered skills; 18 OpenSpec items; corpus
  evaluation; governance.
- `git diff --check` — passed.

## Remote state

Every implementation commit was pushed with `git town sync`. No PR was created
and Issue 30 remains open.

## Archive verification

- The archive created the durable `building-defense-counsel-overlays`
  specification and updated the durable `building-litigation-alignment-overlays`
  specification.
- Both durable specifications passed strict OpenSpec validation.
- The focused suite, standalone skill validator, full repository validation,
  Python compilation, forbidden-directory and private-marker checks,
  code-comment checks, and diff checks passed before the archive commit was
  synced.
