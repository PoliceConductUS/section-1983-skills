## Why

The repository's drafting skills require authority and writing audits before a
filing is described as ready, but they do not invoke the deterministic filing
checker that validates document integrity. A thin orchestration skill is needed
to run the configured checker at the required workflow stages and to keep the
filing gate open whenever execution or hard findings remain unresolved.

## What Changes

**Filing-integrity orchestration**

- From: Agents can complete prose audits without a standard route to a project's
  deterministic filing-integrity checker.
- To: A `filing-ci` skill resolves and runs the project-configured checker after
  material drafting changes and before filing readiness.
- Reason: Deterministic document-integrity failures must control the filing gate
  rather than depend on prose review.
- Impact: Non-breaking addition of a public skill; projects without checker
  configuration remain explicitly blocked rather than receiving a guessed
  invocation.

**Failure return to drafting**

- From: No shared contract classifies checker configuration, execution, input,
  and hard-finding failures for the drafting loop.
- To: The skill explains each failure class, preserves checker severities, and
  returns actionable findings without editing the filing.
- Reason: A failed check must lead to correction and rerun, not a silent bypass.
- Impact: Filing-readiness statements require a current successful checker run.

## Capabilities

### New Capabilities

- `filing-ci-orchestration`: Runs a configured filing-integrity checker, routes
  findings back to drafting, and controls the filing-readiness gate.

### Modified Capabilities

None.

## Impact

- Add `skills/filing-ci/SKILL.md`.
- Add `filing-ci` to the README skill inventory and composition sequence.
- Add no deterministic checker, authority store, formatter, or project-specific
  path to this repository.
- Validate through fresh-context skill pressure scenarios, package discovery,
  runtime skill validation, formatting, and OpenSpec validation.
