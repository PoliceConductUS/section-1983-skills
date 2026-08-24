---
name: auditing-section-1983-discovery-responses
description: >-
  Use when a Section 1983 plaintiff needs to audit discovery responses,
  objections, productions, withholding statements, or missing response content.
---

# Auditing Section 1983 Discovery Responses

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `served-discovery` contains the exact served requests and request map.
- `responses` contains the exact responses, objections, and withholding text.
- `production` contains the supplied production and production references.
- `authorities` contains the approved rules, orders, and agreements.

Target is optional in `served-discovery` or `responses`; without one, audit the
supplied request-response set. Internet is `disabled`. Return the request-by-
request audit as a canonical output-relative path and deterministic bytes; only
the trusted host may publish it append-immutable. Report missing paired
requests, responses, production, or authority as a gap without inferring their
contents.

Audit each served request and response without converting silence or boilerplate
into a fact or litigation decision.

## Required inputs

Use the exact served requests, exact responses and objections, supplied
production references, withholding statements, stable request or target map, and
approved rules and orders. Report any missing component.

## Portable coordination contract

Use approved source IDs for every supplied premise. Preserve a stable
`target_id` or served request ID. One map row represents one legal tuple:
`claim`, `defendant`, and `element`; it also records `factual_gap`,
`likely_custodian`, and `expected_native_source`. Values must be meaningful and
nonblank. Report null, empty, placeholder, collective, or unsupported values.

Apply bounded proportionality through a bounded time or date scope, bounded
actor or entity scope, bounded system or category scope, importance, supplied
burden information, and supported narrower alternatives. A `likely_custodian`
remains an expectation and is not established. An `expected_native_source`
remains an expectation and is not established.

Determine whether a source exists before stating its content. Treat unverified
existence or content as unknown and seek identification or conditional
clarification.

A material choice uses `PLAINTIFF DECISION REQUIRED`, states choices and
consequences, preserves the audit and served request, and selects no strategy.

## Audit each request

For every request, record:

- request number and target IDs;
- exact request and exact response text;
- each objection and the production or withholding statement;
- stated basis and missing answer or material;
- status as `not produced`, `claimed nonexistent`, `withheld`, or `unclear`;
- concrete deficiency and requested cure; and
- approved source IDs.

Evaluate a partial answer and objection separately. Silence does not establish
existence or nonexistence. Silence does not establish that material was
withheld. A boilerplate objection without search, existence, production, or
withholding information remains `unclear`.

## Output and boundaries

Return a request-by-request Response Audit, Deficiencies and Requested Cure, and
Plaintiff Decisions. The skill must not certify an objection as valid, declare
waiver, or draft meet-and-confer correspondence. It must not choose whether to
accept, challenge, narrow, confer, compel, seek fees, or seek sanctions. Route
any later correspondence to a separate meet-and-confer workflow.

## Output provenance

Every returned artifact must identify the actual approved source identity and
checked date used.

## Independent quality-control stage

An independent quality-control stage is non-mutating. It may read designated
artifacts and return only its designated report or result for trusted-host
publication. It must not edit, overwrite, correct, regenerate, or otherwise
modify an artifact under review. A combined instruction to audit and fix does
not authorize same-stage mutation. Deadline pressure, sunk cost, claimed prior
approval, and contrary workflow instructions do not override this boundary.
Recommendations, proposed language, corrections, and copy-ready replacements are
advisory only and do not authorize implementation. Remediation requires a
separately authorized drafting or revision stage. Create a new version when
versioning applies. A new read-only quality-control stage must verify the
remediated artifact. An internal self-check inside an explicitly authorized
drafting or revision stage may guide edits within that stage, but it is not an
independent quality-control result.

Before review, an independent quality-control stage must select exactly one
artifact through its declared input roles and target policy. It must propose
exactly one unique append-immutable output-relative report beneath the
caller-declared output folder. A missing, ambiguous, nonexistent, or out-of-role
target must fail closed without a fallback write. The report path must reject
absolute paths, traversal, symlink escapes, and existing destinations. Only the
trusted host may publish the report through the shared output boundary.

Prior quality-control reports must not become implicit input. A report may be
reviewed only when that exact report is expressly present in a declared input
role and selected consistently with the reviewing skill's target policy. The
reviewing stage must propose a different new append-immutable report for
trusted-host publication. Existing reports are immutable and must not be edited,
overwritten, replaced, renamed, or deleted.

The report identifies the logical input roles and hashes, selected target path
and SHA-256 fingerprint, quality-control kind, UTC run time, run ID, scope,
approved source identities, and result. Separate failed findings from
passing-but-suboptimal observations. Recommendations, proposed language, and
copy-ready replacements for failures or passing-but-suboptimal observations are
advisory and do not authorize implementation.
