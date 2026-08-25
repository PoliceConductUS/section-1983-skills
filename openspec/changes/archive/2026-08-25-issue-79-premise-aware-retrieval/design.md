# Design: Bounded retrieval frames and premise records

## Separation from authority audit

Collection produces a candidate-source handoff. It never certifies that a source
is binding, on point, current, accurately characterized, or sufficient for
filing. Issue #78's proposition audit remains a later independent stage.

## Retrieval frame

Each legal question has one strict frame containing a stable ID, exact legal
question, governing jurisdiction, court hierarchy, operative date, procedural
posture, statute or rule version, material factual trigger, source universe,
access and cost limits, and checked-through date. A new research thread requires
a new frame.

## Premises

Material premises receive stable IDs, a premise type, exact statement, and one
status: `verified`, `false`, or `unresolved`. A false premise requires evidence
and a correction. An unresolved premise requires a gap. Neither status is
silently treated as true.

The installed deterministic helper validates record shape and status
relationships. It does not decide whether evidence proves a premise.

## Source and rejection provenance

Every acquired source records the frame ID, source-system ID, provider or
product ID when available, exact query, ordered filters, execution date,
retrieval time, result identity, retrieval order, canonical URL, ordinary-file
path, hash, decision-date evidence, proposed legal role, source type,
limitations, and review state.

Rejected candidates remain in the source records and candidate index with one
stable reason: wrong issue, jurisdiction, court, date, statute, rule version,
posture, authority level, treatment, or factual trigger. Candidate sources have
no rejection reason.

## Gaps

Empty, incomplete, inaccessible, paid, ambiguous, and out-of-scope searches
record the frame, source system, exact query and filters, checked date, known
missingness, and coverage limit. They never prove that no authority exists.

## Outputs and confinement

The artifact plan adds strict `authority-retrieval-frame.yaml` and
`authority-retrieval-premises.yaml` records alongside the ordinary source files,
adjacent source YAML, candidates, and gaps. The helper remains pure: no
filesystem, network, output, process, or persistence authority. The trusted host
alone publishes append-immutable artifacts beneath the explicit output folder
and uses only `<output-folder>/temp/` for transient work.
