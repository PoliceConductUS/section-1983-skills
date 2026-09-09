# Retrospective

## What changed during implementation

The approved design correctly selected one semantic owner, but test-first
implementation and independent review exposed several integration details that
the initial proposal did not resolve:

- assertion records need a result list because substantive support and
  documentation status can coexist;
- Filing CI output needs an explicit receiving role;
- multi-document Rule 59(e) packets need one validation invocation per
  court-facing document before packet reconciliation;
- generated declarations need direct routing even when invoked outside the
  umbrella drafting skill;
- exact prior reports need issue-register continuity; and
- target-hash changes require complete inventory reconciliation but must not
  automatically stale unrelated finding-level reviews.

The user also added and approved the event-source rule during implementation:
party-drafted advocacy cannot independently prove an underlying event or quoted
words, while separately documented Plaintiff memory can support an attributed
memory claim.

## TDD and pressure-test result

The contract and behavioral tests failed before their corresponding skill
language and routing were added. The complete fixture now contains a real
target, current source hashes, five atomic assertion records, a carried-forward
issue register, all status counts, and the Plaintiff-memory positive path.
Canonical corpus expected findings use evaluator finding IDs instead of private
regex location labels.

The baseline fresh-context run caught obvious errors but invented its schema,
statuses, issue lifecycle, and stopping rules and missed the declared Plaintiff-
memory and party-filing sources. Guided review with the installed skill found
all eight behaviors and caused the freshness, specialist-unavailability, and
fixture-method corrections recorded in `pressure-tests.md`.

## Scope and boundaries

The shared skill remains read-only, folder-scoped, internet-disabled, and
independent of CaseGraph. It returns proposed report content and structured
findings; only the trusted host publishes an append-immutable receipt. Drafting,
authority audit, adversarial review, and deterministic checking retain separate
authority. No case repository, filing, litigation position, or CaseGraph state
was changed.

## Follow-up

No additional feature is required for Issue #114. Real case controllers may
choose their private stable report filename and issue-register presentation, but
those project-specific choices remain outside this public skill.
