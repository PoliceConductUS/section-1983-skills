## ADDED Requirements

### Requirement: Independent review packet

The adversarial review orchestrator SHALL start a fresh reviewer process or
context with only the immutable canonical draft content, its version and
fingerprint, one supported document family, the public review skill and
checklist, and explicit user- or repository-approved sources. Every source MUST
contain a stable identifier, role, immutable content, and content fingerprint.
Paths and URLs MUST NOT appear in the packet. The orchestrator MUST resolve and
verify every fingerprint before dispatch. Each draft and source fingerprint MUST
use a `sha256` field containing the lowercase hexadecimal SHA-256 digest of the
exact UTF-8 bytes of its `content` field.

The launcher MUST reject extra packet fields and MUST expose the complete
dispatched payload and enabled capability set for verification. The reviewer
capability set MUST exclude filesystem, repository, browser, and conversation
access. The orchestrator MUST verify the configured runtime can enforce those
restrictions before dispatch. It MUST exclude drafting history, redlines,
strategy or control conclusions, prior reviews, checker output, and inherited
conversation or provider session state.

#### Scenario: Fresh reviewer cannot be started

- **WHEN** the runtime cannot create a fresh reviewer context with the bounded
  packet and required empty reviewer capability set
- **THEN** it reports `independent review unavailable` and does not simulate an
  independent review in the drafting context

#### Scenario: Approved source is missing

- **WHEN** an approved source entry lacks immutable content or its content does
  not match its fingerprint
- **THEN** validation reports a scoped source gap before dispatch and does not
  browse for, invent, or silently approve a substitute source

### Requirement: Document-specific adversarial passes

The skill SHALL apply one universal attack pass and exactly one checklist for
complaint or amended complaint, motion-to-dismiss response, summary-judgment
response, leave to amend, extension motion, R&R objection, or R&R response. It
MUST report an unsupported document family rather than substitute the nearest
checklist. Those seven human-readable names SHALL be the canonical
`document_family` values.

#### Scenario: Supported filing is reviewed

- **WHEN** a bounded packet identifies one supported document family
- **THEN** the reviewer applies the universal attacks and every attack in that
  family's checklist

#### Scenario: Filing family is unsupported

- **WHEN** the packet cannot be classified as one supported document family
- **THEN** the reviewer reports the unsupported family and does not claim that a
  document-specific review occurred

### Requirement: Categorized read-only report

The report MUST keep `Fatal Defects`, `Credible Opposition Arguments`,
`Factual Disputes`, `Discovery Issues`, and `Style Complaints` as distinct
headings and MUST state `None found` when a category is empty. Every finding
MUST include a stable identifier, exact attacked quote, paragraph, page, or
heading location, approved source identifiers, concrete attack, consequence, and
status. A fatal defect means filing-critical under the supplied posture and
approved rules; it MUST NOT be presented as an outcome prediction.

#### Scenario: Review finds different kinds of defects

- **WHEN** the same draft contains a procedural omission, a plausible nonfatal
  defense attack, a source conflict, opponent-controlled support, and rhetoric
- **THEN** the report places them exclusively in Fatal Defects, Credible
  Opposition Arguments, Factual Disputes, Discovery Issues, and Style Complaints
  respectively without collapsing or inflating the categories

#### Scenario: Category has no finding

- **WHEN** a completed attack pass finds no item in one required category
- **THEN** that category remains visible and states `None found`

### Requirement: Auditable proposed corrections

A proposed correction SHALL be offered only when complete language is supported
by the approved sources and does not decide plaintiff strategy. It MUST identify
the exact attacked text as `Replace:` and provide complete copy-ready prose as
`With:`. It MUST NOT contain a placeholder, invented fact, invented citation, or
silent edit to the canonical filing.

#### Scenario: Supported correction is available

- **WHEN** approved sources support a complete non-strategic correction
- **THEN** the report supplies the exact attacked text and complete replacement
  while the canonical draft remains byte-for-byte unchanged

#### Scenario: Correction cannot be fully supported

- **WHEN** a finding lacks approved support for complete replacement prose
- **THEN** the reviewer reports the gap without presenting a partial or
  placeholder correction

### Requirement: Plaintiff-reserved decisions

The reviewer MUST NOT decide whether to retain, narrow, or omit a claim, theory,
fact, defense response, or requested relief. It SHALL preserve the canonical
text and emit `PLAINTIFF DECISION REQUIRED` with the precise choice and
consequences. It MUST NOT label a selected option or replacement as a proposed
correction until the plaintiff decides in a separate workflow.

#### Scenario: Narrowing could answer an attack

- **WHEN** narrowing or omitting a claim, theory, fact, response, or requested
  relief could answer a finding
- **THEN** the reviewer states the available choices and consequences without
  selecting an option or changing the canonical filing

### Requirement: Workflow boundaries

The skill MUST NOT certify authority identity, binding status, quotation
accuracy, filing readiness, or outcome. It MUST NOT create an RRD, run Filing
CI, or edit the filing. A user-approved revision SHALL occur through a separate
drafting workflow, after which authority, adversarial-review, and Filing CI
gates must rerun as applicable.

#### Scenario: User requests review and automatic correction

- **WHEN** a request asks the adversarial reviewer to review and revise the
  filing in one workflow
- **THEN** the reviewer returns the read-only report and routes any later
  approved correction to a separate drafting workflow
