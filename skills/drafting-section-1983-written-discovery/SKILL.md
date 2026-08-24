---
name: drafting-section-1983-written-discovery
description: >-
  Use when a Section 1983 plaintiff needs to draft or revise requests for
  production, interrogatories, or requests for admission.
---

# Drafting Section 1983 Written Discovery

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

Draft traceable, bounded written discovery without turning an expected source or
answer into a factual premise.

## Required inputs

Use the supported claim and defendant map, element definitions, known facts,
open factual gaps, approved source content, localized rules and orders, and any
supplied numerical limits. Report a missing input instead of supplying it.

## Portable coordination contract

Use approved source IDs for every supplied premise. Each request links to a
stable `target_id`. One map row represents one legal tuple: `claim`,
`defendant`, and `element`. The row also records `factual_gap`,
`likely_custodian`, and `expected_native_source`. All values must be meaningful
and nonblank; report a null, empty, placeholder, collective, or unsupported
value as a gap.

Use bounded proportionality: a bounded time or date scope, bounded actor or
entity scope, bounded system or category scope, importance, supplied burden
information, and supported narrower alternatives. A `likely_custodian` remains
an expectation and is not established. An `expected_native_source` remains an
expectation and is not established.

Determine whether a source exists before stating its content. If existence or
content is unverified, ask about existence and identification, request
production if it exists, or use a conditional premise.

A material choice uses `PLAINTIFF DECISION REQUIRED`, states choices and
consequences, preserves the current draft, and selects no strategy.

## Draft the requests

1. Build the target map. Use multiple rows when one request serves more than one
   claim-defendant-element tuple.
2. Apply every approved numerical limit before drafting. If supported targets
   exceed a limit, preserve them and route prioritization to the plaintiff.
3. Separately number requests for production, interrogatories, and requests for
   admission. Link every request to each applicable target ID.
4. Requests for production identify bounded document or ESI categories and
   requested native form when supported.
5. Interrogatories seek bounded facts or identities.
6. Each request for admission states one discrete fact or proposition.
7. Audit every request for importance, supplied burden, and a supported narrower
   alternative.

## Output

Return the Discovery Target Map, separately numbered Requests for Production,
Interrogatories, Requests for Admission, reported gaps, and Plaintiff Decisions.

Do not serve discovery or select service, sequencing, priority, request-cap
allocation, narrowing, stipulation, or contention timing. Do not invent a rule,
fact, custodian, source, record, or expected content.

## Output provenance

Every returned artifact must identify the actual approved source identity and
checked date used.
