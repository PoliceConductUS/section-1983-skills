# verified-authority-audit Specification

## Purpose

Define folder-scoped authority-source integrity, proposition-level correctness
and groundedness review, exact source-voice and support records, deterministic
mechanical gates, and human-reserved legal-judgment boundaries.

## Requirements

### Requirement: Authority audit is folder scoped

The skill MUST read only one required target inside `filing-source` and selected
ordinary files inside `verified-authority`. It MUST publish only beneath one
explicit output folder and MUST use its `temp/` directory for all transient
work. It MUST NOT require a case-data package, manifest-based input format,
graph, CaseGraph, repository, Git, global datastore, or ambient workspace.

#### Scenario: Authority YAML names another root

- **WHEN** selected YAML attempts to add or escape to another folder
- **THEN** validation rejects it before citation analysis

### Requirement: Authority YAML binds exact ordinary bytes

Selected corpus, authority, and source YAML MUST use strict bounded schemas,
canonical relative paths, stable IDs, hashes, ISO dates, exact fields, and
deterministic ordering. Authority and source YAML MUST independently agree on
the selected ordinary opinion bytes.

#### Scenario: Opinion hash differs

- **WHEN** selected YAML does not match the authority document bytes
- **THEN** the audit returns invalid and performs no citation verification

### Requirement: Eyecite is extraction only

The audit MUST use eyecite for candidate extraction and antecedent resolution
without treating its output as proof of identity, binding status, proposition,
pinpoint, quotation, later history, or good law.

#### Scenario: Eyecite extracts an absent case

- **WHEN** an extracted citation has no selected verified-authority record
- **THEN** the audit returns a missing-authority hard finding

### Requirement: Quotation and authority gates fail closed

The audit MUST verify required authority identity and status fields and MUST
require each asserted direct quotation to occur verbatim in the exact selected
document. An unusable text layer MUST remain pending visual review rather than
pass.

#### Scenario: Quotation is absent

- **WHEN** an asserted quotation does not occur verbatim in the selected
  authority document
- **THEN** the audit returns a stable hard quotation finding

### Requirement: Ordinary audit is deterministic and offline

The `audit` operation MUST disable internet and produce deterministic findings
for identical logical input bytes. A separately authorized `freshness-research`
operation MAY retrieve candidate material but MUST NOT certify good law or
mutate inputs.

#### Scenario: Ordinary audit lacks internet

- **WHEN** an ordinary authority audit runs with all selected files present
- **THEN** it completes without network access

### Requirement: Results are explicit and read only

The host MUST publish deterministic JSON and Markdown findings plus
`run-receipt.yaml` beneath the explicit output folder. Exit classes MUST be
`passed`, `findings`, `unavailable`, or `invalid`, and all selected inputs MUST
remain byte-identical.

#### Scenario: Required authority YAML is absent

- **WHEN** selected authority documentation is missing
- **THEN** the result is unavailable and never verified

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
