## MODIFIED Requirements

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

## ADDED Requirements

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
