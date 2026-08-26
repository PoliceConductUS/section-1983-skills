# Design: Arrest-driven defendant presentation order

## Context

The drafting stack already routes all Section 1983 filings through the umbrella
skill and routes complaints through one canonical complaint contract. The
false-arrest specialization already builds arrest-time actor matrices. No
current contract determines defendant presentation order from the arrest.

## Goals

- Audit whether an arrest occurred before drafting or materially revising a
  filing that names defendants.
- Put the designated primary arresting officer first in every ordered defendant
  presentation.
- Stop for caller clarification when several arresting officers exist without a
  declared primary.
- Preserve caller order when no arrest occurred.

## Non-goals

- No case-specific officer name in a public skill.
- No inference among several arresting officers.
- No reordering of chronology or substantive claim analysis.
- No package, graph, CaseGraph, repository abstraction, or new runtime tool.

## Decisions

The umbrella drafting workflow owns the cross-document trigger. The canonical
complaint contract owns complaint-specific presentation and its completion
audit. The false-arrest actor matrix identifies the arresting officer candidates
and whether the caller has designated one as primary.

Evaluation fixtures use synthetic names and structured expectations. One fixture
may use Markham as a synthetic caller-designated example, but no skill
instruction treats that name as a default.

## Risks and trade-offs

- **Conflicting source descriptions** -> report the identity gap and ask; do not
  infer a primary.
- **Legacy filing order appears intentional** -> the current invocation's
  approved rule controls every new or materially revised output.
- **Presentation order leaks into chronology** -> confine the rule to ordered
  defendant presentations and test that boundary explicitly.

## Migration plan

New and materially revised outputs adopt the rule immediately. Existing input
files remain read-only and unchanged.

## Open questions

None.
