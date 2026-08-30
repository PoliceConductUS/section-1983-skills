# Retrospective

## Outcome

Issue 31 now provides an offline municipal-profile skill over caller-declared
folders and source-documented ordinary files. It keeps institutional evidence,
counterevidence, questions, and gaps separate across five domains without
deciding Monell liability or selecting a theory.

## What RED established

The profile needed exact source bytes and adjacent YAML hashes, passing upstream
results, complete folder fingerprints, stable IDs, and cross-record validation.
It also needed explicit rejection of unresolved references, unassigned domain
records, conclusion fields, and affirmative liability language.

## What worked

- A pure in-memory helper kept filesystem and network authority in the trusted
  host.
- Exact record fields made unsupported conclusions and accidental schema drift
  observable.
- Deterministic sorting made repeated profile plans byte-identical.
- The five-domain mapping preserved contrary material and gaps rather than
  collapsing them into a single favorable result.

## Review correction

The initial schema rejected conclusion fields but still allowed a proposition to
state an affirmative liability conclusion. A focused failing test drove a narrow
language gate before output serialization.

## Reusable lesson

Folder isolation and source hashes define where evidence came from; they do not
by themselves preserve the legal boundary. Output schemas and deterministic
tests must separately prevent an evidence-organizing skill from becoming a
liability decision-maker.
