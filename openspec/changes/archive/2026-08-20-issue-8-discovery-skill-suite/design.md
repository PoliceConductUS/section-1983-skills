# Design: Section 1983 Discovery Skill Suite

## Context

The repository has drafting, response-planning, authority-audit, adversarial-
review, and filing-integrity skills but no discovery drafting or response
workflow. Issue #8 requires a coordinated suite and requires decomposition into
separately tested skills before implementation.

## Goals

- Publish the five discovery skills described by Issue #8.
- Make discovery targets traceable to a claim, defendant, element, factual gap,
  likely custodian, and expected native source.
- Preserve proportionality and distinguish expected from established evidence.
- Keep material litigation decisions with the plaintiff.
- Make each peer skill independently discoverable, installable, and testable.

## Non-goals

- Supplying court-specific discovery law without approved localized sources.
- Serving discovery, sending correspondence, noticing a deposition, filing a
  motion, asserting waiver, seeking sanctions, or selecting strategy.
- Certifying authority, privilege, authenticity, truth, or completeness.
- Adding a sixth public coordinator, executable tool, provider SDK, or private
  case material.

## Decisions

### Five peer capabilities and the existing router

The five public skills and same-named durable capabilities jointly own the
operative coordination contract. The existing `section-1983-drafting` skill
routes them and hosts `references/discovery-coordination-contract.md` as a
non-public consolidated explanation. Each peer repeats the compact required
fields and boundaries. Every relative peer link resolves inside that peer's
directory; no peer depends on a sibling skill for safe operation.

### Discovery Target Map

The map uses a stable nonblank `target_id` and meaningful nonblank `claim`,
`defendant`, `element`, `factual_gap`, `likely_custodian`, and
`expected_native_source` values. The factual gap separates what approved sources
presently support from what remains missing. Likely custodians and expected
native sources remain labeled expectations. Supporting approved source IDs and
bounded time, actor or entity, system or category scope make the map auditable
and support proportionality analysis. Null, blank, placeholder, or facially
unbounded values do not satisfy the map.

One row represents one claim-defendant-element tuple. A request serving more
than one tuple uses multiple rows rather than a collective label. Missing
mapping is a reported gap, not something the skill invents. If existence or
content is unverified, the request asks whether a source exists, seeks its
identification or production if it exists, or uses a conditional premise.

### Written-discovery ownership

`drafting-section-1983-written-discovery` creates separately numbered requests
for production, interrogatories, and requests for admission. It maps each
request to target IDs, applies request-type rules, numerical limits, native-form
needs, and bounded scope, and never states expected records or content as
established.

### Response-audit ownership

`auditing-section-1983-discovery-responses` evaluates every exact served
request, response, objection, production, and withholding state. It
distinguishes not produced, claimed nonexistent, withheld, and unclear; supplies
a concrete deficiency and cure; and does not equate silence with nonexistence or
declare waiver.

### Meet-and-confer ownership

`drafting-section-1983-meet-and-confer` consumes a completed audit rather than
redoing it. It organizes neutral correspondence by request number, target ID,
exact deficiency, approved rule or order source, cure, reservation, and a
user-supplied or approved proposed date. An unapproved date remains a plaintiff
decision. The skill returns a separate factual conference record without
claiming consent.

### Privilege-log ownership

`auditing-section-1983-privilege-logs` determines a scoped requirements
checklist from supplied approved sources whether or not a log has arrived. When
a log exists, it audits each supplied entry and request relationship, identifies
missing metadata, and does not invent facts, reveal privileged substance,
adjudicate a claim, or declare waiver.

### Deposition-outline ownership

`drafting-section-1983-deposition-outlines` organizes witness role and
chronology before element gaps. Each topic or question cluster links to target
and approved source IDs. It distinguishes a question from expected testimony and
includes only applicable foundation, authentication, preservation,
contradiction, and closing-gap modules.

### Plaintiff-reserved choices

Routine source-supported wording can proceed. Service, sequencing, priority, cap
allocation, narrowing, stipulation, acceptance or challenge of an objection,
conferral, date selection, waiver theory, fees, sanctions, motion practice,
deposition selection or order, 30(b)(6) scope, impeachment timing, and any
theory-changing choice are not selected. The skill emits
`PLAINTIFF DECISION REQUIRED`, states choices and consequences, preserves the
current artifact, and selects none.

### Composition boundaries

The umbrella skill routes, localizes, and supplies writing rules; it does not do
the peer's work. `audit-authorities` verifies rules, orders, and privilege
propositions. Complaint and RRD skills may identify gaps, but discovery cannot
create a missing plausible allegation. Adversarial filing review may classify a
gap as a Discovery Issue but does not design discovery. Filing CI does not
certify discovery strategy or completeness.

## Risks and trade-offs

- Repeating compact fields across five skills creates some duplication but
  preserves safe independent installation.
- A likely custodian or expected source can be wrong. Explicit labels and
  existence-first drafting prevent expectation from becoming a factual claim.
- General public skills cannot encode every court's numerical limits, timing,
  log rules, or conference requirements. Approved localized sources remain
  required inputs, and missing law remains a gap.
- Five fixtures add corpus runtime, but deterministic evaluation remains bounded
  and standard-library-only.

## Migration plan

This is additive. Add RED structural and corpus tests first, implement the five
skills and shared route, run fresh bounded behavioral scenarios, verify the
complete repository, then archive on the Issue #8 branch.

## Open questions

None.
