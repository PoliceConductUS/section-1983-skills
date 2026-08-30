# Brainstorm

## Problem

The canonical complaint contract describes qualified-immunity and Monell work in
prose, but its machine handoff validates only generic count fields. A draft can
therefore pass structural review without defendant-specific individual-capacity
analysis or a path-specific Monell attribution and causation analysis. The
municipal-profile skill cannot close this gap because it is a neutral evidence
profile and expressly does not recommend liability paths or draft allegations.

## Approaches considered

### Extend only the general complaint skill

This would minimize new packages, but it would leave Monell planning implicit
and turn the canonical complaint owner into a large strategy, planning,
drafting, and validation package.

### Add one combined Monell skill

This would give Monell work a dedicated route, but it would conflate evaluating
and recommending possible paths with drafting only the paths the litigation
principal approves.

### Add separate planning and drafting skills with typed validation

This preserves one responsibility per skill. A planning skill compares and
recommends supported paths without silently making the litigation decision. A
drafting skill applies the approved paths. The canonical complaint owner retains
whole-document ownership and publishes a strict version-2 typed contract.

## Approved design

The user approved the third approach and a strict version-2 migration.

- Add `planning-section-1983-monell-claims`.
- Add `drafting-section-1983-monell-claims`.
- Keep `building-municipal-monell-profiles` neutral and optional.
- Keep `drafting-section-1983-complaints` as the canonical complaint owner.
- Add individual-capacity, qualified-immunity, and path-specific Monell records
  to the canonical machine handoff.
- Reject version-1 handoffs rather than preserving a weak compatibility path.
- Separate deterministic structural findings from reasoned legal assessments.
- When an on-disk CaseGraph is supplied, read and evaluate its files directly;
  do not invoke or require a CaseGraph CLI.
- Treat a missing, invalid, incompatible, stale, or incomplete graph as an
  explicit assessment state. Never silently convert it into a merits pass.
- Keep all graph access read-only.

## Monell paths

The planner and drafter treat the following as separate paths:

- express or formally adopted policy;
- persistent widespread custom or practice;
- decision by a final municipal policymaker;
- ratification;
- failure to train; and
- failure to supervise or discipline.

FTO transfer, complaint review, arrest review, jail intake, supervisory review,
and rubber-stamp review are possible implementation or transmission mechanisms.
They do not become freestanding Monell paths unless approved authority supplies
that doctrinal route.

## CaseGraph clarification

The CaseGraph codebase is incomplete and is not a runtime dependency. The
optional evaluator consumes the graph already stored on disk. A valid graph
slice has parseable recognized envelopes, unique and matching UIDs, resolvable
claim-relevant references, source and authority provenance, the required
procedural context, and a complaint fingerprint matching the evaluated draft.
Unrelated graph defects do not invalidate a claim slice, but they remain
reported. Missing relevant nodes produce an incomplete or indeterminate
assessment rather than invented connections.

## Open questions

None. The user approved the architecture, strict migration, and direct on-disk
graph evaluation.
