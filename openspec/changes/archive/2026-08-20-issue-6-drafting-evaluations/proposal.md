# Proposal: Drafting-Skill Regression Evaluations

## Why

The repository can validate skill structure and deterministic scripts, but it
cannot currently prove whether a skill edit preserves required drafting behavior
or reintroduces a previously observed failure. Single informal agent runs also
hide variance.

## What Changes

- Add a pure-Python evaluation harness for fixture validation, deterministic
  grading, configured fresh-process candidate and judgment runs, variance, and
  baseline comparison.
- Add synthetic fixtures with bounded source sets, passing candidates, and
  permanent regression examples.
- Add unit and command-level tests that start RED before implementation.
- Add pull-request evaluation reporting with a machine-readable result and
  Markdown job summary.
- Extend repository validation to run the evaluation tests and corpus gate.

## Boundaries

- The harness does not call a provider directly or store credentials.
- Checked-in fixtures contain no private case material.
- Judgment unavailability is reported, not replaced by deterministic prose.
- Baselines change only through reviewed file changes.

## Impact

New code and fixtures live under `evaluations/`. Pull requests gain a focused
evaluation workflow, and `npm run validate` gains deterministic evaluation
coverage.
