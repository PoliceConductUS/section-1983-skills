---
name: drafting-section-1983-deposition-outlines
description: >-
  Use when a Section 1983 plaintiff needs a deposition outline anchored to a
  chronology, claim elements, factual gaps, and approved sources.
---

# Drafting Section 1983 Deposition Outlines

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `record` contains the approved chronology, claim gaps, exhibits, and sources.
- `authorities` contains approved deposition rules, orders, and limits.
- `discovery` contains produced material and outstanding-document information.
- `municipal-profile` contains the four validated ordinary Issue #31 output
  files when municipal examination topics are within scope.

For municipal examination topics, read
[municipal profile consumption](references/municipal-profile-consumption.md)
before building the outline.

Target is optional in `record`; without one, use the supplied witness and gap
scope. Internet is `disabled`. Return the deposition outline as a canonical
output-relative path and deterministic bytes; only the trusted host may publish
it append-immutable. Report missing witness, chronology, source, discovery, or
authority material as a gap without predicting testimony.

Build questions that test open element gaps without predicting testimony or
choosing deposition strategy.

## Required inputs

Use the locked chronology, claim-element gap register, witness role, produced
record, approved exhibits and source content, and outstanding-document list.
Report a missing input instead of treating a topic as grounded.

## Portable coordination contract

Use approved source IDs for every supplied premise. Preserve each stable
`target_id`. One map row represents one legal tuple: `claim`, `defendant`, and
`element`; it also records `factual_gap`, `likely_custodian`, and
`expected_native_source`. Values must be meaningful and nonblank. Report null,
empty, placeholder, collective, or unsupported values.

Apply bounded proportionality through a bounded time or date scope, bounded
actor or entity scope, bounded system or category scope, importance, supplied
burden information, and supported narrower alternatives. A `likely_custodian`
remains an expectation and is not established. An `expected_native_source`
remains an expectation and is not established.

Determine whether a source exists before stating its content. Unverified
existence or content stays unknown and receives conditional identification,
foundation, preservation, or content questions.

A material choice uses `PLAINTIFF DECISION REQUIRED`, states choices and
consequences, preserves the current outline, and selects no strategy.

## Build the outline

Organize the outline by open element gaps and anchor each gap to the chronology
and produced record. Each topic identifies the element it tests, approved source
or exhibit IDs, and the gap it aims to close. A question is not testimony or an
expected answer.

The outline MUST mark foundation needs and authentication needs. Flag every
dependency on an outstanding or not-produced document and identify the
foundation the topic will need. Include role, communication, policy,
preservation, contradiction, and closing-gap modules only when supported and
applicable.

Report a topic when it has no source, exhibit, record, element, or gap; do not
draft it as grounded. The skill must not script or invent an answer or
testimony, or state what a witness will admit, concede, say, or testify.

## Output and boundaries

Return the Target Map, Source and Exhibit Map, Deposition Outline, reported
dependencies or gaps, and Plaintiff Decisions. The skill must not choose or
select a deponent or witness, decide deposition order or which witness goes
first, or decide whether to take a deposition. It also must not select duration,
30(b)(6) scope, document sequencing, impeachment timing, or a theory-changing
follow-up.

## Output provenance

Every returned artifact must identify the actual approved source identity and
checked date used.
