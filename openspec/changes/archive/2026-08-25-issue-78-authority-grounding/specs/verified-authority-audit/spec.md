# verified-authority-audit Specification

## ADDED Requirements

### Requirement: Material statements are audited as atomic propositions

The audit MUST decompose every material generated or filing-near statement into
atomic propositions before authority approval. Every proposition MUST have a
stable identifier, filing location, exact text, and legal, factual, procedural,
application, or inference type. One citation attached to several propositions
MUST pass only when its exact source supports every material proposition in the
context asserted.

#### Scenario: One source supports only half of a compound statement

- **WHEN** a filing sentence asserts two material propositions and its cited
  source supports only one
- **THEN** the audit creates two proposition records and does not pass the
  unsupported proposition

### Requirement: Correctness and groundedness remain separate

Each proposition MUST record correctness as `verified`, `incorrect`, or
`unresolved`. A verified proposition MUST separately record groundedness as
`grounded`, `misgrounded`, or `ungrounded`. An incorrect or unresolved
proposition MUST record groundedness as `not-applicable`. No citation-level or
document-level aggregate result may conceal a failed or unresolved proposition.

#### Scenario: Correct rule cites an irrelevant case

- **WHEN** a proposition is legally correct but the cited authority does not
  support it in the asserted context
- **THEN** correctness may be `verified` while groundedness is `misgrounded` or
  `ungrounded`
- **AND** the audit cannot report an unqualified pass

### Requirement: Exact source support and voice are recorded

Every proposition MUST map each relied-on citation to its exact selected
authority artifact, artifact hash, domain-YAML paths, pinpoint, source text,
scope and qualifiers, jurisdiction, decision date, posture, precedential force,
support status, and source voice. Source voice MUST distinguish majority
holding, court dicta, party argument, lower-court ruling under review, factual
or procedural background, concurrence, dissent, and quoted secondary authority.
Ambiguous or incorrect attribution MUST fail closed.

#### Scenario: Party argument is described as a holding

- **WHEN** the cited words appear only in a party's argument summarized by the
  court
- **THEN** the source voice is `party-argument`
- **AND** an audit calling it a majority holding fails

### Requirement: Proposition audits preserve verification provenance

The machine-readable record and human-readable report MUST expose stable
proposition IDs, correctness, groundedness, source support, source voice, and
verification provenance. Provenance MUST identify the audit stage, exact input
fingerprints, selected source identities, auditor model or provider when
available, and checked time. A working link, real citation, source list, or
positive treatment symbol MUST NOT substitute for exact proposition support.

#### Scenario: Citation exists but is irrelevant

- **WHEN** the cited authority is authentic but addresses another legal issue
- **THEN** the record preserves the real source and classifies its support as
  irrelevant
- **AND** the proposition does not pass as grounded

### Requirement: Audit scope is necessary and bounded

Research and audit output MUST remain limited to propositions necessary to
answer the question or support the filing. Every additional material proposition
MUST receive the same atomic decomposition, correctness, groundedness, source
support, source voice, and provenance treatment.

#### Scenario: Auditor adds a material proposition

- **WHEN** an audit report introduces a new material legal proposition
- **THEN** that proposition receives its own complete audit record before it may
  be treated as verified

### Requirement: Legal judgments remain human or agent audit work

The audit MUST reserve legal correctness, groundedness, source voice, authority
applicability, litigation strategy, and filing readiness for substantive audit
work and human litigation judgment. Deterministic software MAY validate record
shape, status vocabulary, hashes, and source-document integrity but MUST NOT
decide legal correctness, groundedness, source voice, authority applicability,
litigation strategy, or filing readiness. Existing non-mutation,
declared-folder, authority-identity, quotation, pinpoint, binding-status,
posture, factual-fit, later-history, rule-of-orderliness, fair-warning, and
human-decision gates MUST remain in force.

#### Scenario: Record conforms to the JSON schema

- **WHEN** a proposition audit is structurally valid
- **THEN** schema conformance alone does not make any legal conclusion verified
  or filing-ready
