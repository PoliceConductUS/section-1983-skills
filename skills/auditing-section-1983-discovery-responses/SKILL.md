---
name: auditing-section-1983-discovery-responses
description: >-
  Use when a Section 1983 plaintiff needs to audit discovery responses,
  objections, productions, withholding statements, or missing response content.
---

# Auditing Section 1983 Discovery Responses

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
