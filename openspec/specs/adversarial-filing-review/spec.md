# adversarial-filing-review Specification

## Purpose

Define a clean-room, read-only adversarial review for supported Section 1983
filings using an immutable bounded packet, document-specific attacks,
categorized findings, source-supported corrections, and plaintiff-reserved
strategy decisions.

## Requirements

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
capability set MUST exclude filesystem, repository, browser, tool, and
conversation access. The trusted runtime MUST establish those restrictions
through its executable request or process boundary; a caller assertion or
Boolean flag MUST NOT establish independence. It MUST exclude drafting history,
redlines, strategy or control conclusions, prior reviews, checker output, and
inherited conversation or provider session state.

#### Scenario: Fresh reviewer cannot be started

- **WHEN** the runtime cannot create a fresh reviewer context with the bounded
  packet and required empty reviewer capability set
- **THEN** it reports `independent review unavailable` and does not simulate an
  independent review in the drafting context

#### Scenario: Caller asserts an unproved boundary

- **WHEN** a custom command is accompanied only by a caller assertion that empty
  capabilities exist
- **THEN** the launcher reports `independent review unavailable` before
  executing the command

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

### Requirement: Stateless trusted provider runtime

The public launcher SHALL provide a trusted stateless OpenAI Responses runtime
that accepts an explicit model and validated packet. Its provider request MUST
contain no enabled tools, MUST select no tool, MUST disable response storage,
and MUST omit conversation and previous-response identifiers. It MUST NOT send a
case path, repository path, credential, environment value, drafting history,
prior review, or other content outside the validated packet and bounded public
review instructions.

#### Scenario: Trusted review is dispatched

- **WHEN** the packet, model, credentials, and output destination are valid
- **THEN** one stateless no-tools request containing only the approved review
  input is dispatched and its capability boundary is recorded

#### Scenario: Provider configuration is unavailable

- **WHEN** the explicit model or required provider credential is absent
- **THEN** the launcher writes no successful review and reports independent
  review unavailable without exposing a credential value

#### Scenario: Provider protocol fails

- **WHEN** the provider times out, returns a non-success status, invalid UTF-8
  or JSON, missing output, or a response outside the review schema
- **THEN** the launcher fails closed with a stable bounded failure result and
  does not label the judgment as a completed adversarial review

### Requirement: Validated review response

The trusted runtime MUST accept only a response containing the five canonical
report categories. Every finding MUST satisfy the categorized report,
source-reference, proposed-correction, and plaintiff-reserved-decision
requirements before the host renders a completed report. Empty categories MUST
remain present and render `None found`.

#### Scenario: Complete structured review is returned

- **WHEN** the provider returns a schema-valid review with supported source IDs
- **THEN** the host renders all five categories and preserves each complete
  finding, correction, and unselected plaintiff decision

#### Scenario: Review response is incomplete

- **WHEN** a category or required finding field is absent, a source identifier
  is unapproved, a correction is partial, or a plaintiff choice is selected
- **THEN** response validation fails before any completed report is written

### Requirement: Immutable execution report

The launcher SHALL resolve one existing version folder inside an explicit
project boundary and SHALL write only one new report under that version's
canonical `audits/` directory. It MUST verify that the audited artifact bytes
match the packet draft fingerprint before provider dispatch. The report MUST be
named `adversarial-filing-review-<UTC timestamp>-<run-id>.md` and MUST record
the runtime type, explicit model, local run identity, document family, packet
and artifact fingerprints, source identities, time, outcome, and stable failure
class when present. It MUST NOT record credentials or provider-session
continuation state. Existing reports and reviewed artifacts MUST remain
byte-for-byte unchanged.

#### Scenario: Completed review is recorded

- **WHEN** the trusted runtime returns a valid categorized review
- **THEN** the launcher exclusively creates one immutable report in the audited
  version's `audits/` directory and returns its path and completed outcome

#### Scenario: Review is unavailable

- **WHEN** the trusted runtime fails before completing a valid review
- **THEN** the launcher may exclusively create one honest unavailable report,
  returns a nonzero result, and does not synthesize findings or a passing label

#### Scenario: Report path collides or escapes

- **WHEN** the report already exists, the version is outside the project
  boundary, traversal is attempted, or the audits path resolves outside its
  canonical directory
- **THEN** the launcher fails closed, writes nowhere else, and preserves every
  existing byte
