# Verification

## Branch and scope

- Branch: `codex/issue-29-litigation-alignment-overlays`
- Parent: `codex/issue-28-adversarial-review-runtime`
- Pre-archive reviewed HEAD: `e41426d`
- Commits: design `21e3bd4`, RED `df59ce7`, GREEN `a78e47b`, and
  provenance-integrity review correction `e41426d`.
- No dependency, workflow, root `docs/`, `.superpowers/`, attorney-research, or
  filing-edit capability was added.

## Public result

- `building-litigation-alignment-overlays` consumes one immutable approved
  docket snapshot and publishes three install-local Draft 2020-12 schemas, one
  standard-library validator, and five generic synthetic fixtures.
- Every individual defendant remains explicit. Generated and effective groups
  are issue-scoped and split on capacity, challenged act, relevant-time
  knowledge, qualified immunity, requested relief, or another material defense.
- Adversary attacks, plaintiff responses, and judicial treatments remain
  separate fingerprinted ledgers. Magistrate, district, and appellate stages
  preserve actual authorship.
- Review plans create fresh blind and actual-adversary jobs per target and
  group. Blind jobs contain no overlay material; actual jobs contain only the
  validated group slice. No responsive filing yields two blind jobs and an
  explicit unavailable actual profile.
- Filing manifests pin overlay and snapshot identity, version, SHA-256,
  checked-through date, and validator result.
- `OVERLAYS.md` owns the shared lifecycle. `JUDGE_OVERLAYS.md` now explicitly
  defines a judge overlay as an evidence-bounded Judicial Reasoning Profile and
  keeps court procedures as separate compliance inputs.

## TDD and review evidence

- Initial RED had 24 methods with 26 expected failures for absent skill,
  schemas, validator, fixtures, routes, lifecycle documentation, and durable
  Purpose.
- Focused GREEN covered complete and no-responsive lifecycles, grouping,
  overrides, role separation, judicial attribution, source unions, review
  isolation, four-job leave packages, and stale manifest rejection.
- The judicial-reasoning clarification was RED before the guide and durable
  specification named the profile, its seven dimensions, public source types,
  separate compliance component, and anti-prediction boundary.
- Whole-story review produced failing mutations for split provenance, source
  date drift, attack-dimension drift, judicial-source misattribution, unknown
  matrix sources, cross-attack links, target-family mismatch, future-dated
  snapshot sources, and malformed nested JSON types. Each now fails closed with
  a stable finding.

## Commands

- `python3 -m unittest evaluations.tests.test_litigation_alignment_overlay_validator -v`
  — 19 tests passed after review correction.
- `python3 -m unittest evaluations.tests.test_litigation_alignment_overlay_structure evaluations.tests.test_litigation_alignment_overlay_validator evaluations.tests.test_judge_overlay_guide -v`
  — focused structure, validator, and judge-guide integration passed.
- `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/building-litigation-alignment-overlays`
  — `Skill is valid!`.
- `npm run validate` — passed after review correction: formatting; 16 drafting
  tests; 313 evaluation tests; 21 discovered skills; 17 OpenSpec items; corpus
  evaluation; governance.
- `git diff --check` — passed.

## Remote state

Every implementation commit was pushed with `git town sync`. No PR was created
and Issue 29 remains open.

## Archive verification

The repository-local OpenSpec CLI archived the change as
`2026-08-22-issue-29-litigation-alignment-overlays`, created the durable
`building-litigation-alignment-overlays` specification, and updated the durable
`judge-overlay-authoring` specification. The generated placeholder Purpose was
replaced with a concrete capability statement.

After archive, the 39 focused structure, validator, and judge-guide tests
passed. `npm run validate` passed formatting, 16 drafting tests, 313 evaluation
tests, 21 discovered skills, 17 durable OpenSpec specifications, corpus
evaluation, and governance. Strict durable-spec validation, Python compilation,
forbidden-directory checks, code-comment checks, and `git diff --check` also
passed.
