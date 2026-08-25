# Proposal: Use validated municipal profile folders in workflows

## Why

Issue #31 produces source-documented municipal profile files, but downstream
skills need a shared fail-closed rule for using those files without treating the
profile as proof, law, or a completed Monell element.

## What changes

- Add one exact recursive read-only `municipal-profile` input role to complaint,
  city Rule 12, written-discovery, deposition-outline, and adversarial-review
  consumers.
- Require the four ordinary Issue #31 output files and validate their versions,
  identities, hashes, record IDs, checked-through date, and passing result
  before specialized work.
- Define consumer-specific uses for theory mapping, motion-response planning,
  gap-directed discovery, gap-directed examination, and independent attack.
- Preserve each consumer's existing target, internet, output, and temporary-file
  policy.

## Capability

- `municipal-profile-consumption`

## Non-goals

- No liability decision, automatic element completion, authority verification,
  source collection, input mutation, or litigation-strategy selection.
