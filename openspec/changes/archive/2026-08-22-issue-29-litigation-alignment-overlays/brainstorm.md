# Brainstorm: Case overlay lifecycle and litigation alignment

## Problem

A broad clean-room attack is necessary before an adversary has appeared, but it
is wasteful and sometimes distorting after the docket identifies the attacks
actually made against particular defendants and claims. The repository has a
judge-overlay method and an independent adversarial reviewer, but no case-level
overlay inventory, no litigation-alignment grouping contract, and no safe way to
compose adversary positions, plaintiff responses, and judicial treatment.

## Approved direction

- Treat defendant groups as issue-scoped **litigation-alignment groups**, not as
  caption-wide labels.
- Preserve every individual defendant and split groups when capacity, challenged
  act, relevant-time knowledge, qualified-immunity position, requested relief,
  or another material defense differs.
- Keep canonical adversary, plaintiff-response, and judicial-treatment ledgers
  separate. A derived matrix may link them but never copy one actor's position
  into another actor's ledger.
- Attribute recommendations, adoptions, modifications, independent reasoning,
  and appellate dispositions to the actual judicial actor.
- Use one immutable, versioned docket snapshot as overlay input. Overlay
  generation does not browse or silently refresh it.
- Run blind common-attack and actual-adversary reviews per target artifact and
  group. When no actual attack exists, run two fresh broad common reviews and
  report the actual profile unavailable rather than inventing one.
- Publish a general lifecycle guide at the repository root. Keep judge-specific
  triggers in `JUDGE_OVERLAYS.md`; reserve counsel-specific research and
  attribution for Issue 30.

## Options rejected

### One combined case-position profile

Rejected because a status such as `plaintiff-answered` or
`magistrate-judge-recommended` can be mistaken for an adversary concession when
all roles share one record.

### One permanent group per law firm or filing

Rejected because alignment changes by claim, challenged act, capacity, defense,
and requested disposition. Joint representation is evidence of possible
alignment, not the grouping rule.

### Browse during every drafting run

Rejected because ad hoc retrieval produces irreproducible overlays and makes it
impossible to know which docket state a filing consumed. A separately authorized
preflight owns snapshot refresh.

### Replace the broad reviewer after a motion is filed

Rejected because an actual adversary can omit a common attack or preserve it for
later. The blind common reviewer remains independent from the actual-adversary
reviewer.

## Public surface

- New public skill: `building-litigation-alignment-overlays`.
- New root guide: `OVERLAYS.md`.
- Install-local schemas and validator for docket snapshots, overlay sets, and
  filing-version overlay manifests.
- Modified README and drafting router.
- Modified judge-overlay guide and durable judge-overlay Purpose.
- Generic synthetic lifecycle fixtures only.

## Boundaries

The skill does not research defense attorneys, predict outcomes, characterize
personalities, select litigation strategy, edit a filing, or treat silence as
agreement, withdrawal, rejection, or adoption. It reports gaps for missing
documents, uncertain grouping, uncertain authorship, and unresolved treatment.
