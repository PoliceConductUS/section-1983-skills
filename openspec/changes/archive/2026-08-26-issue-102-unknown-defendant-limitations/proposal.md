# Proposal: Add an unknown and new-defendant limitations gate

## Why

A complaint amendment that adds, identifies, or substitutes an individual near
or after limitations can fail even when its underlying claim is otherwise
adequately pleaded. The canonical complaint contract currently inventories
limitations as a defense premise but does not require the defendant-specific
relation-back, notice, diligence, concealment, tolling, and fallback analysis
needed to decide whether such an amendment is ready for filing.

## What changes

- Trigger a limitations gate from a calculated passed deadline or an identified
  limitations-related risk, without inventing a universal "near limitations" day
  count.
- Require one complete limitations record for each affected individual.
- Treat every missing or unresolved required entry as an internal
  filing-critical GAP that blocks filing-ready status.
- Add deterministic regression coverage while leaving the existing false-arrest
  and actor-causation contracts unchanged.

## Capabilities

- Modified capability: `drafting-section-1983-complaints`

## Impact

The change affects the canonical complaint contract, its completion audit, the
durable complaint specification, and focused evaluation fixtures. It adds no
runtime dependency, persistence abstraction, or change to specialized
false-arrest or general actor-causation guidance.
