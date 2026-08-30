# Proposal: Complete the installed filing reference checker

## Why

Issue #2 delivered the first installed filing-integrity checker ahead of Issue
#17, but Issue #17 still needs an exact ordinary-folder acceptance record and a
strict validation correction. The current date validator parses a date but does
not execute its canonical-spelling comparison.

## What changes

- Confirm the exact six recursive read-only roles, required filing target,
  disabled internet policy, explicit output folder, and output-local temporary
  boundary.
- Require selected domain YAML to use canonical ISO dates in addition to exact
  fields, roles, classifications, relative paths, and source hashes.
- Add a RED regression for noncanonical but parseable date spellings and fix the
  unreachable comparison.
- Re-verify the installed check set, deterministic outputs, stable result
  classes, isolated installation, and input preservation.

## Capability

- `deterministic-filing-integrity`

## Non-goals

- No substantive authority judgment, automatic correction, filing decision,
  external executable, persistence service, or filing-folder abstraction.
