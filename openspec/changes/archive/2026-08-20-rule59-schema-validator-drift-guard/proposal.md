## Why

The Rule 59 corpus schema and standard-library validator deliberately implement
the same public contract in parallel. Behavioral fixtures prove important
outcomes, but a newly required field or controlled value can otherwise be added
to only one artifact without an immediate, focused failure.

## What Changes

- Add an automatic test that compares every mapped schema `required` set with
  the corresponding validator required-field constant.
- Add an automatic test that compares every mapped schema enum with the
  corresponding validator controlled-value constant.
- Extract currently inline validator enum sets into named constants without
  changing accepted values or validator behavior.
- Keep the existing real-CLI fixture suite as the semantic contract.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `studying-rule-59e-decisions`: Make schema-validator structural drift fail the
  repository test suite.

## Impact

The change adds one evaluation test module and refactors controlled-value
literals in the existing validator into named constants. It changes no public
schema, accepted corpus, output, dependency, skill instruction, or CI command.
