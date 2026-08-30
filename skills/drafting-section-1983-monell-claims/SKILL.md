---
name: drafting-section-1983-monell-claims
description: >-
  Use when drafting or revising approved municipal-liability paths for a Section
  1983 complaint after Monell planning.
---

# Drafting Section 1983 Monell Claims

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `planning-handoff` contains the litigation principal's recorded path decisions
  and the approved planning records.
- `record` contains the approved facts, chronology, exhibits, and claim map.
- `authorities` contains verified governing authority and audit material.
- `filing` contains any complaint being revised or audited.

Target is optional in `filing`; omit it only when producing deltas for a new
complaint. Internet is `disabled`. Return the approved-path complaint deltas and
structured findings; only the trusted host derives the canonical output-relative
path and publishes them in append-immutable mode beneath the declared output
folder. Report unavailable prerequisites as gaps without searching undeclared
paths.

## Scope and prerequisites

Draft only the Monell paths expressly approved by the litigation principal.
Never select, add, abandon, merge, or omit a claim merely because the planning
skill recommended it. Read both install-local references completely:

- [references/approved-planning-handoff.md](references/approved-planning-handoff.md)
- [references/monell-complaint-delta.md](references/monell-complaint-delta.md)

Also load `drafting-section-1983-complaints` and its canonical Markdown and JSON
contracts. That skill remains the whole-complaint owner. If the approved
planning handoff or any canonical contract is unavailable, stop and report the
missing prerequisite.

## Drafting unit

For each approved `path_id`, draft one delta with one `path_type`. Preserve the
planning record's source, inference, attribution, mechanism, injury, causation,
temporal, contrary-material, and information-and-belief boundaries. Do not turn
an internal recommendation, discovery lead, graph label, or unresolved
connection into a factual allegation.

Draft facts first, then the reasonable municipal inference, then the
path-specific application and moving-force result. Use the precise governing
standard and verified pinpoint authority. If authority came through CaseGraph,
preserve the verified artifact, hash, pinpoint, and exact-text resolution
receipt; a citation string alone is not verified support.

## Handoff

Return complaint deltas, not a competing full complaint. Identify the target
count and factual locations, inserted or revised paragraphs, each typed Monell
path object, remaining gaps, and source identities. Hand the deltas to
`drafting-section-1983-complaints` for integration.

After integration, rerun `scripts/validate_complaint_handoff.py` from the
canonical complaint package in drafting mode. Do not describe a structural pass
as legal sufficiency or filing readiness.
