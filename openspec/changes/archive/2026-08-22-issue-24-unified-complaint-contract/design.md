# Design

## Context

Agents compose independently installable skills. Today the umbrella's
`references/documents/complaint.md` contains the whole skeleton, the general
complaint `SKILL.md` contains the detailed count contract, and the false-arrest
package's `references/complaint-contract.md` repeats a differently ordered
skeleton and a second detailed count contract. No single package owns the full
general contract.

## Goals and non-goals

### Goals

- One canonical install-local owner for the complete general complaint contract.
- Explicit fail-closed composition for umbrella and specialization packages.
- One machine-readable description of the deterministic mechanical subset.
- Tests that fail for omissions, duplicate ownership, escaping links, and
  behavior that invents or silently reconciles requirements.

### Non-goals

- Implementing a complaint checker in this repository.
- Deciding fact truth, legal sufficiency, authority fit, material analogy,
  strategy, or filing readiness.
- Rewriting claim-specific legal doctrine unrelated to contract ownership.
- Changing Filing CI failure classes or checker execution semantics.

## Decisions

### Canonical ownership

`drafting-section-1983-complaints` owns:

- `references/complaint-contract.md`, the human/agent contract containing the
  document skeleton and detailed count contract; and
- `references/complaint-structure-contract.json`, the stable mechanical handoff
  for external checkers.

Its `SKILL.md` retains a compact core standard and must require both references
before complaint drafting, revision, or audit. Detailed requirements do not
remain duplicated in the umbrella or false-arrest package.

### Canonical document and count shapes

The document order preserves the existing umbrella contract: caption, optional
introduction, jurisdiction and venue, parties, chronological statement of facts,
counts, prayer for relief, jury demand, and signature block.

Every count has one mapping per claim-defendant-capacity tuple. The mechanical
record identifies the count, constitutional source, defendant, capacity,
challenged act, event stage, governing standard and pinpoint, decisive-fact and
incorporated paragraph references, relevant-time knowledge, application,
qualified-immunity fields when applicable, injury, relief, and result.

### Routing packages

The umbrella retains a complaint document entry only to route the task. It must
require the canonical general complaint skill and its two references, and it
must report the contract unavailable rather than draft or audit from a local
fallback.

The false-arrest package retains a renamed
`references/false-arrest-complaint-delta.md`. That reference may define seizure,
offense, actor, chronology, incorporated-material, and false-arrest compression
rules. It must not restate the generic whole-document skeleton or count field
list. The package fails closed when the canonical general complaint contract is
unavailable.

### External checker handoff

The JSON contract identifies its owner and version, ordered sections, count
cardinality, required count fields, conditional qualified-immunity fields,
mechanical checks, excluded judgments, and stable finding shape. It is an input
contract, not an executable or a claim that checks ran.

`filing-ci` continues to run only a complete project-configured invocation. The
CaseGraph implementation is tracked separately and may consume this handoff
while following CaseGraph's own sidecar and provenance ADRs.

### Verification

Deterministic tests parse the JSON, enumerate packages, resolve live local
links, and exercise isolated package compositions. Fresh agents receive the same
synthetic deadline/authority/sunk-cost scenarios against current and revised
packages. GREEN requires one traceable complete contract or an explicit
fail-closed result; it does not accept invented requirements or silent conflict
resolution.

## Risks and trade-offs

- A summary in `SKILL.md` could become a second contract. Keep it compact and
  route every detailed decision to the canonical reference.
- A machine-readable contract could be mistaken for a legal validator. State
  exclusions in both JSON and Markdown and leave execution to CaseGraph.
- Cross-package Markdown links break independent installation. Use skill names
  for dependencies and only install-local file links.
- Removing duplicated false-arrest material could drop a true specialization.
  Preserve arrest-specific chronology, matrices, warrants, video, and
  compression rules in the delta.

## Migration plan

Create the canonical references first in GREEN, update the three skill routes,
rename/narrow the false-arrest reference, update README, and rerun isolated
composition tests. No consumer file is rewritten automatically. Existing users
must install the general complaint package when using the umbrella or
false-arrest package for complaint work.

## Open questions

None.
