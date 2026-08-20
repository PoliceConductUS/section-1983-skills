# Brainstorm: Section 1983 Discovery Skill Suite

## Design summary

Decompose Issue #8 into exactly the five requested peer public skills: written
discovery, response and objection audit, meet-and-confer drafting, privilege-log
requirements and audit, and deposition outlines. The existing
`section-1983-drafting` skill remains the entrypoint and hosts one shared
discovery-coordination reference. Each peer skill repeats the compact operative
contract so it remains safe and usable when installed independently.

## Alternatives considered

### One monolithic discovery skill

One file would avoid repeated language but would blur drafting, audit,
correspondence, privilege, and deposition responsibilities. One test surface
would not satisfy the issue's separately tested decomposition.

### Five peer skills plus the existing drafting entrypoint

This tracks all five proposed subskills literally. The existing entrypoint
routes and hosts a consolidated explanation; the five public skills own and
repeat the operative contract. This is the selected approach.

### Five peer skills plus a new discovery router

A dedicated router would make coordination explicit but would add an unrequested
sixth public skill and overlap the existing drafting entrypoint.

## Agreed approach

Add these five public skills and same-named durable capabilities:

1. `drafting-section-1983-written-discovery`
2. `auditing-section-1983-discovery-responses`
3. `drafting-section-1983-meet-and-confer`
4. `auditing-section-1983-privilege-logs`
5. `drafting-section-1983-deposition-outlines`

Add `references/discovery-coordination-contract.md` under the existing drafting
entrypoint, then route the peer skills from that entrypoint and README. Peer
skills do not link to that sibling package; each contains its minimum operative
contract and keeps every relative link install-local.

## Key decisions

- A Discovery Target Map uses meaningful nonblank `target_id`, `claim`,
  `defendant`, `element`, `factual_gap`, `likely_custodian`, and
  `expected_native_source` values, supporting approved source IDs, and bounded
  proportionality scope.
- Likely custodians and expected native sources remain labeled expectations, not
  established facts. Unverified content produces an existence, identification,
  or conditional request.
- Downstream skills preserve stable target and served-request IDs instead of
  silently remapping the request.
- Proportionality covers supplied time, actors or entities, systems or
  categories, importance, burden, and narrower alternatives.
- A material choice uses `PLAINTIFF DECISION REQUIRED`, states choices and
  consequences, preserves the current artifact, and selects none.
- Five generic synthetic fixtures provide one discriminating permanent
  regression per public skill. Structural tests and fresh behavior checks prove
  the complete map without imposing an unrequested JSON output schema.

## Open questions

None. The user approved the design and test-seam workflow and requested
unattended execution.
