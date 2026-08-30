# collecting-legal-authority-sources Specification

## ADDED Requirements

### Requirement: Every legal question has one bounded retrieval frame

Collection MUST define one strict retrieval frame for each legal question. The
frame MUST record a stable ID, exact issue, governing jurisdiction and court
hierarchy, operative date, procedural posture, statute or rule version, material
factual trigger, source universe, access and cost limits, and checked-through
date. Additional research threads MUST use another explicit frame.

#### Scenario: Query omits the operative rule version

- **WHEN** a proposed retrieval frame lacks the applicable statute or rule
  version
- **THEN** validation rejects the frame before source publication

### Requirement: Material query premises are explicit

Collection MUST record each material query premise with a stable ID, type, exact
statement, and status of `verified`, `false`, or `unresolved`. A false premise
MUST include evidence and a correction. An unresolved premise MUST include a
gap. Collection MUST NOT answer as though a false or unresolved premise were
true.

#### Scenario: Asserted holding is false

- **WHEN** premise review finds that a cited case did not make the asserted
  holding
- **THEN** the premise is `false`, the record preserves the evidence and
  correction, and retrieval uses the corrected frame

### Requirement: Retrieval provenance and order are preserved

Every acquired source MUST record the frame, source system, provider or product
identity when available, exact query, ordered filters, execution date, retrieval
time, result identity, retrieval order, canonical URL, relative ordinary-file
path, byte hash, decision-date evidence, proposed legal role, and source
classification.

#### Scenario: Results are returned in ranked order

- **WHEN** a source system returns several candidate sources
- **THEN** each record preserves its original retrieval order independent of
  output filename ordering

### Requirement: Rejected candidates remain auditable

Collection MUST preserve candidate sources considered and material sources
rejected. Each rejected source MUST record one reason: wrong issue,
jurisdiction, court, date, statute, rule version, posture, authority level,
treatment, or factual trigger.

#### Scenario: Semantic match concerns another statute

- **WHEN** a real source is materially rejected because it interprets a
  different statute
- **THEN** the source remains in the collection as rejected with reason
  `wrong-statute`

### Requirement: Empty and incomplete results preserve coverage limits

Empty or incomplete retrieval MUST record the frame, searched source system,
exact query and filters, checked-through date, known missingness, and coverage
limits. It MUST NOT establish that no authority exists.

#### Scenario: Search index returns no result

- **WHEN** an authorized bounded search returns no candidate
- **THEN** the gap states the searched scope and known missingness and does not
  claim that no authority exists

### Requirement: Retrieval output remains a candidate handoff

Legal-AI, RAG, semantic-search, citator, and generated research output MUST
remain a retrieval lead. A real citation, working link, source list, snippet, or
positive treatment symbol MUST NOT establish proposition support or current
applicability. The underlying artifact MUST be acquired before later audit, and
Issue #78's independent proposition verification remains separate.

#### Scenario: Provider returns a positive treatment symbol

- **WHEN** a result includes a real citation and positive treatment indicator
- **THEN** collection may preserve it as a candidate but cannot certify the
  source as good law, on point, or filing-ready
