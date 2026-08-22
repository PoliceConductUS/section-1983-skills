## ADDED Requirements

### Requirement: Classify every proposed declaration statement

The skill SHALL assign every proposed proposition a stable statement ID and
classify it as firsthand fact, attributed record fact, derived analysis,
inference, legal conclusion, or discovery expectation before drafting. The
classification record MUST preserve the exact proposed text, declarant knowledge
basis, competency basis, approved source IDs, exhibit IDs, disposition, gap, and
human declarant approval status.

#### Scenario: Mixed propositions are supplied

- **WHEN** supplied material contains an observed event, record content,
  calculated comparison, inference, legal conclusion, and expected discovery
- **THEN** the skill separates all six propositions and does not silently
  rewrite any of them as firsthand fact

### Requirement: Gate factual paragraphs on personal knowledge and competency

Each included declaration paragraph MUST contain one material proposition and
MUST have a supplied statement-specific basis showing how the declarant
perceived it and is competent to testify to it. A generic opening recital MUST
NOT substitute for a missing basis. Attributed record content MUST stay
attributed and MUST NOT become personal knowledge of the underlying event merely
because the declarant read the record.

#### Scenario: Statement has no perception basis

- **WHEN** a proposed factual paragraph lacks a supplied basis showing how the
  declarant saw, heard, did, received, created, or maintained the matter
- **THEN** the skill reports a gap and does not place the proposition in the
  declaration as personal knowledge

#### Scenario: Declarant read an attributed record

- **WHEN** the declarant personally reviewed a record but did not perceive the
  event the record describes
- **THEN** the skill preserves what the identified record states or shows as an
  attributed record fact and does not recast the event as firsthand testimony

### Requirement: Refuse knowledge laundering

Derived analysis, inference, legal conclusions, and discovery expectations MUST
remain separately labeled in `Excluded or Separate Material` and MUST NOT appear
as retained declaration paragraphs. Expected, requested, missing, or unproduced
discovery MUST be reported as a gap and MUST NOT be stated as what a recording,
witness, record, or other source will show, prove, or confirm.

#### Scenario: Expected recording is unproduced

- **WHEN** the supplied materials say a recording is expected but its existence
  or content is unverified
- **THEN** the skill reports the discovery gap and does not state the expected
  recording content in declaration voice

#### Scenario: Comparison was derived from records

- **WHEN** a proposed proposition is a calculation, aggregation, coding result,
  or cross-record comparison rather than a perceived event
- **THEN** the skill labels it derived analysis, places it in
  `Excluded or Separate Material`, and does not retain it in any declaration
  paragraph

### Requirement: Use the applicable Section 1746 execution form

The skill SHALL select the execution language from the supplied actual place of
execution. For execution within the United States, its territories, possessions,
or commonwealths, the unsigned block MUST state
`I declare under penalty of perjury that the foregoing is true and correct. Executed on (date).`
For execution without the United States, the unsigned block MUST state
`I declare under penalty of perjury under the laws of the United States of America that the foregoing is true and correct. Executed on (date).`
The skill MUST leave the date and signature to the human declarant. It MUST NOT
infer the execution place from residence, venue, or incarceration.

#### Scenario: Execution is within the United States

- **WHEN** the human declarant supplies a domestic execution location
- **THEN** the draft uses the domestic statutory form and leaves date and
  signature blank

#### Scenario: Execution is without the United States

- **WHEN** the human declarant supplies an execution location outside the United
  States
- **THEN** the draft uses the form containing
  `under the laws of the United States of America` and leaves date and signature
  blank

#### Scenario: Execution location is missing

- **WHEN** no actual execution location is supplied
- **THEN** the skill reports the missing input, does not select or combine the
  statutory forms, and keeps execution blocked

### Requirement: Keep exhibit foundation source bounded

For every proposed exhibit, the skill SHALL record its ID and description,
linked statement IDs, how the declarant recognizes it, any supplied creation,
receipt, observation, custody, or maintenance basis, applicable accuracy or
completeness basis, and missing foundation facts. Missing foundation MUST
produce focused prompts rather than an invented custodian, relationship,
creation method, chain, accuracy statement, or authentication conclusion. The
skill MUST NOT declare an exhibit authenticated or admissible.

#### Scenario: Exhibit relationship is missing

- **WHEN** an exhibit is supplied without facts showing how the declarant
  recognizes it or is related to it
- **THEN** the skill reports the missing foundation and asks focused questions
  without calling the exhibit authentic or a true and correct copy

### Requirement: Require human declarant approval before execution

Every retained statement MUST begin pending and MUST be presented as exact text
for the human declarant to approve, revise, or omit. Silence MUST NOT count as
approval. Any changed statement MUST return to pending. The skill MUST refuse to
call the declaration ready for execution while any retained statement lacks the
human declarant's explicit approval. It MUST NOT sign, date, execute, file, or
claim execution for the declarant.

#### Scenario: One retained statement remains pending

- **WHEN** the human declarant approved every other paragraph but has not
  approved one retained exact statement
- **THEN** the skill preserves the unsigned draft, marks execution blocked, and
  does not represent the declaration as approved or executed

#### Scenario: Approved statement changes

- **WHEN** the text of an approved paragraph changes
- **THEN** that paragraph returns to pending and execution remains blocked until
  the human declarant explicitly approves the revised exact text

### Requirement: Return bounded preparation outputs

The skill SHALL return a statement classification ledger, unsigned draft
declaration, exhibit foundation map, excluded or separate material, and human
approval and execution status. It MUST NOT certify the truth, authentication,
admissibility, execution, filing, or filing readiness of any statement,
declaration, or exhibit.

#### Scenario: Draft and exhibit map are complete

- **WHEN** all available inputs have been classified and the unsigned draft is
  prepared
- **THEN** the output keeps the ledger, draft, foundation map, excluded
  material, and human declarant approval status distinct without making a
  certification
