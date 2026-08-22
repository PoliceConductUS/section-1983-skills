# Verification

## Branch and scope

- Branch: `codex/issue-28-adversarial-review-runtime`
- Parent: `codex/issue-25-complaint-candor-pruning`
- Pre-archive reviewed HEAD: `3c629df`
- Commits: design `129f306`, initial RED `376ddf3`, caller-trust RED `d54194d`,
  core GREEN `b2d6e94`, public route and credential correction `3e47761`, and
  whole-review corrections `3c629df`.
- No dependency, workflow, root `docs/`, or `.superpowers/` directory was added.

## Runtime result

- The public launcher has one built-in stateless OpenAI Responses mode with an
  explicit model, environment-only credential, no tools, no storage, and no
  conversation or prior-response continuation.
- A caller Boolean cannot establish arbitrary-command isolation. The legacy
  command seam fails before command execution.
- The host validates the exact embedded packet and every fingerprint before
  provider dispatch.
- A completed provider response must have status `completed` and satisfy the
  exact five-category finding, correction, source, and plaintiff-decision
  schema.
- The launcher verifies the canonical artifact, opens the `audits/` directory
  without following a final symlink, creates the report exclusively relative to
  that directory, and preserves existing bytes.
- The public CLI returns only outcome, report path, runtime, and empty
  capability set. It does not echo the draft, approved sources, provider
  request, or credential.

## TDD and review evidence

- Initial RED proved that no trusted stateless provider entry point existed and
  that the public command route trusted a caller-supplied isolation Boolean.
- Protocol and output RED covered provider failures, invalid bytes, strict
  categorized responses, exact artifact fingerprints, path confinement,
  collisions, immutable reports, and unavailable-result honesty.
- Public-route testing prevents the skill or README from restoring the
  caller-asserted command path.
- Live synthetic dogfood reached the OpenAI endpoint and returned HTTP 401
  because the environment credential is invalid. The first response exposed a
  masked credential fragment in the provider error body. A failing regression
  test drove removal of HTTP response bodies from retained diagnostics; a
  repeated live call returned only the stable 401 classification with empty
  retained streams.
- Whole-story review added three failing probes: an incomplete provider status
  was accepted, the successful CLI echoed the full packet, and an `audits/`
  symlink replacement between preflight and write escaped confinement. All three
  now fail closed, and the focused suite passes.

## Commands

- `python3 -m unittest evaluations.tests.test_adversarial_review_structure evaluations.tests.test_adversarial_review_launcher evaluations.tests.test_adversarial_review_runtime evaluations.tests.test_non_mutating_quality_control -v`
  — 32 tests passed before whole-story correction; the corrected cases also
  passed in the complete suite.
- `python3 -m py_compile skills/adversarial-filing-review/scripts/launch_review.py evaluations/tests/test_adversarial_review_runtime.py`
  — passed.
- `python3 /Users/dalelotts/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/adversarial-filing-review`
  — `Skill is valid!`.
- `npm run validate` — passed after review correction: formatting; 16 drafting
  tests; 285 evaluation tests; 20 discovered skills; 17 OpenSpec items; corpus
  evaluation; governance.
- `git diff --check` — passed.

## Remote state

Every implementation commit was pushed with `git town sync`. No PR was created
and Issue 28 remains open.

## Archive verification

The repository-local OpenSpec CLI archived the change as
`2026-08-22-issue-28-adversarial-review-runtime` and merged three added
requirements plus the modified packet requirement into the durable
`adversarial-filing-review` specification. The existing concrete Purpose was
preserved; no placeholder or TBD purpose was generated.

After archive, the focused launcher, runtime, structure, and non-mutating-QC
suites passed 32 tests. `npm run validate` passed formatting, 16 drafting tests,
285 evaluation tests, 20 discovered skills, 16 durable OpenSpec specifications,
corpus evaluation, and governance. Strict durable-spec validation, Python
compilation, forbidden-directory checks, code-comment checks, and
`git diff --check` also passed.
