---
name: drafting-section-1983-meet-and-confer
description: >-
  Use when a Section 1983 plaintiff needs to draft meet-and-confer
  correspondence based on a completed discovery-response audit.
---

# Drafting Section 1983 Meet-and-Confer Correspondence

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

Turn a completed request-by-request audit into neutral correspondence without
redoing the audit, changing a served request, or selecting escalation.

## Required inputs

Use the completed audit, exact served request and response text, approved rule
or order sources, supplied conference facts, and a user-supplied or approved
proposed response date. If the audit is incomplete, report that prerequisite gap
instead of adding a deficiency.

## Portable coordination contract

Use approved source IDs for every supplied premise. Preserve each stable
`target_id` and served request ID. One map row represents one legal tuple:
`claim`, `defendant`, and `element`; it also records `factual_gap`,
`likely_custodian`, and `expected_native_source`. Values must be meaningful and
nonblank. Report null, empty, placeholder, collective, or unsupported values.

Apply bounded proportionality through a bounded time or date scope, bounded
actor or entity scope, bounded system or category scope, importance, supplied
burden information, and supported narrower alternatives. A `likely_custodian`
remains an expectation and is not established. An `expected_native_source`
remains an expectation and is not established.

Determine whether a source exists before stating its content. Unverified
existence or content stays unknown and receives an existence, identification, or
conditional request.

A material choice uses `PLAINTIFF DECISION REQUIRED`, states choices and
consequences, preserves the served request and draft, and selects no strategy.

## Draft from the completed audit

For each request-specific deficiency, state the request number, target ID, exact
response or objection, concrete deficiency, requested cure supported by an
approved rule, order, or source, reservation, and proposed response date. Use an
actual date only when the user supplied or approved it. Otherwise put date
options under `PLAINTIFF DECISION REQUIRED`.

Return a separate factual conference or certification record containing only
supplied dates, participants, methods, positions, agreements, and unresolved
issues. Silence does not establish consent or agreement.

## Output and boundaries

Return Draft Correspondence, a separate Conference Record, and Plaintiff
Decisions. The skill must not silently narrow a request or alter the completed
audit. It must not decide whether or when to send, compromise, move to compel,
assert waiver, seek fees, seek sanctions, or threaten automatic relief.

## Output provenance

Every returned artifact must identify the actual approved source identity and
checked date used.
