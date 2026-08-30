## Why

The municipal-profile skill correctly fails closed when its validated policy
catalog or compliance assessment is absent, but a public user receives no
deterministic route for producing those prerequisites through the already
installed policy skills. Adding staged prerequisite resolution makes the entry
skill usable while preserving independent review, least-privilege folders,
offline semantic stages, and explicit output ownership.

## What Changes

**Municipal-profile entry workflow**

- From: Missing catalog or assessment input stops profile output with a bounded
  failure.
- To: A prerequisite-resolution operation returns a deterministic state and the
  next eligible installed collection, analysis, assessment, or profile stage.
- Reason: Public agents need an actionable, testable recovery path.
- Impact: Additive; existing profile compilation inputs and outputs remain
  unchanged.

**Stage transitions**

- From: Users manually infer when an upstream output can become a later input.
- To: The skill requires explicit output folders, trusted-host publication,
  terminal receipts, passing validation, matching fingerprints, new read-only
  declarations, and independent source review where required.
- Reason: Automatic continuation must not weaken semantic or filesystem gates.
- Impact: Additive public workflow guidance and deterministic planning output.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `building-municipal-monell-profiles`: Add deterministic prerequisite
  resolution and staged routing through existing police-policy skills without
  changing the compilation contract.

## Impact

- Update `skills/building-municipal-monell-profiles/SKILL.md` and its
  references.
- Extend its deterministic helper with prerequisite-plan output.
- Add public-seam evaluation coverage and update README routing.
- Add one durable requirement to the existing municipal-profile specification.
- Add no dependency, network client, credential store, graph, repository layer,
  or general workflow engine.
