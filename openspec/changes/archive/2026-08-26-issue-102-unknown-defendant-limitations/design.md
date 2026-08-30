# Design: Defendant-specific limitations completion gate

## Context

The canonical complaint skill owns the complete complaint contract and its
completion audit. Those references already treat limitations as a possible
dispositive premise, but they do not require a complete record when an amendment
adds, identifies, or substitutes an individual defendant.

## Goals

- Detect the approved limitations-risk conditions before treating an amendment
  as filing-ready.
- Require the ten approved categories for every affected individual.
- Preserve separate legal analyses where the governing rules differ.
- Fail closed internally when any required entry remains unresolved.

## Non-goals

- No universal numeric definition of "near limitations."
- No resolution of legal strategy or authorization to file.
- No adverse merits concession in filed text.
- No change to false-arrest seizure timing or general actor-causation rules.
- No new runtime tool, package, graph, repository, or persistence layer.

## Decisions

The complaint contract owns the trigger and defendant-specific record. The
completion audit owns the fail-closed filing-readiness check. The trigger is
satisfied when the calculated limitations deadline has passed or when the
supplied record, an opposing party, the court, or the caller raises a
limitations, relation-back, Rule 4(m) notice or service, diligence, concealment,
or tolling issue.

The record remains internal work product. It records the supported facts,
authority status, and unresolved issues; it does not force the complaint to
volunteer an adverse characterization. Focused regression scenarios exercise the
trigger, per-defendant cardinality, complete-record path, and unresolved
fail-closed path.

## Risks and trade-offs

- **A jurisdiction-specific deadline cannot be calculated** -> record the
  unresolved accrual, limitations rule, or deadline as filing-critical rather
  than inventing it.
- **Several defendants have different notice or diligence histories** -> use one
  record per affected defendant rather than a collective analysis.
- **The amendment is close to a deadline but no fixed threshold exists** ->
  trigger on identified record or caller risk, not a repository-wide day count.

## Migration plan

New complaint amendments and material revisions adopt the gate immediately.
Declared inputs remain read-only, and existing generated artifacts are not
edited in place.

## Open questions

None.
