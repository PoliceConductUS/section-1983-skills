# collecting-legal-authority-sources Specification

## Purpose

Define a folder-native authorized collector that returns ordinary
legal-authority source files, adjacent domain YAML, candidates, and bounded gaps
for later independent authority audit.

## Requirements

### Requirement: Collection uses exact declared folders

The installed skill MUST accept exactly the recursive read-only
`legal-question`, `jurisdiction`, `court-hierarchy`, `relevant-date`,
`seed-authority`, and `approved-source-system` roles, no target, expressly
authorized internet, and one explicit output folder. Temporary work MUST remain
under `<output-folder>/temp/`.

#### Scenario: Bounded source collection is authorized

- **WHEN** the trusted host validates the exact roles, source limits, and
  enforceable isolation
- **THEN** collection uses only declared inputs and expressly authorized network
  access

### Requirement: Every retrieved file has exact provenance

Each retrieved ordinary file MUST have adjacent strict domain YAML binding its
relative path, SHA-256, source URL, query, filters, checked and retrieval dates,
result identity, classification, decision-date evidence or gap, proposed
citation identity, limitations, and duplicate relationships.

#### Scenario: Retrieved bytes changed

- **WHEN** ordinary source bytes no longer match their documented SHA-256
- **THEN** validation fails before publication

### Requirement: Source types remain distinct

The collector MUST distinguish official text, authenticated opinions, docket
copies, mirrors, citator records, secondary material, and unverified references.

#### Scenario: Opinion comes from an unofficial mirror

- **WHEN** the retrieved file is not official or authenticated
- **THEN** it remains `mirror` or `unverified_reference` rather than official
  text

### Requirement: Search gaps remain explicit

The collector MUST preserve empty, incomplete, inaccessible, paid, ambiguous,
and out-of-scope search results as bounded gaps and MUST NOT establish that no
authority exists from those results.

#### Scenario: Approved source returns no accessible result

- **WHEN** the bounded query cannot retrieve an authority source
- **THEN** the collector returns a coverage gap with the exact query, filters,
  date, source-system identity, and limit

### Requirement: Collection never substitutes for authority audit

The collector MUST leave candidate identity, publication, binding
classification, treatment, proposition fit, quotation, pinpoint, and
fair-warning value unverified until a separate `audit-authorities` invocation.

#### Scenario: Candidate source is collected

- **WHEN** collection validates and publishes the ordinary file and source YAML
- **THEN** the candidate may become a later audit input but not a verified
  authority

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
