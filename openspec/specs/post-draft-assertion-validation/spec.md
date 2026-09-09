# post-draft-assertion-validation Specification

## Purpose

TBD - created by archiving change issue-114-post-draft-assertion-validation.
Update Purpose after archive.

## Requirements

### Requirement: Every generated court-facing document enters the validation loop

Every generated court-facing document MUST follow the sequence draft, identify
assertions, trace assertions to original sources, substantively validate,
produce a report, correct defects in a separately authorized editing stage,
revalidate affected assertions and dependencies, and perform final
whole-document and rendered-file review.

#### Scenario: Draft reaches post-draft review

- **WHEN** an authorized drafting stage produces a complete candidate
- **THEN** the workflow validates that candidate under the shared contract
  before describing it as validation-complete

### Requirement: Independent assertion validation is read only

The independent validation stage MUST preserve the reviewed target and all
declared inputs byte-for-byte and MUST return only report content and structured
findings for trusted-host publication. Correction MUST occur only in a separate
authorized drafting or revision stage.

#### Scenario: Review finds an incorrect assertion

- **WHEN** source review proves that a drafted assertion is incorrect
- **THEN** validation reports the defect without editing the target and routes
  correction to a separate editing stage

### Requirement: Report identity and methods are reproducible

The report MUST record the reviewed commit when applicable, exact target and
source hashes, applicable control identities and versions, review scope, and
only the methods actually used.

#### Scenario: Transcript was reviewed without native audio

- **WHEN** the reviewer inspected a transcript but did not listen to the native
  recording
- **THEN** the report records transcript review and does not claim native-audio
  verification

### Requirement: Every proposition has an atomic assertion record

The validator MUST split compound sentences into separately assessed
propositions, cover inherited and unchanged text, and record for each assertion
its stable ID, exact text and location, classification, optional supplied
documentation route, original supporting passage or recording observation,
pinpoint, contrary context, inference reasoning, result, and corrective action.

#### Scenario: One sentence makes two claims

- **WHEN** a sentence asserts both an officer's command and the subject's
  response
- **THEN** the report contains separately supported or failed assertion records
  for the command and the response

### Requirement: Substantive validation tests the asserted relationship

Each assertion review MUST evaluate actor, conduct, timing, duration,
attribution, knowledge, causation, quotation accuracy, and degree of certainty
as applicable. A related citation, documentation link, route, or matching hash
MUST NOT be treated as substantive validation by itself.

#### Scenario: Command is rewritten as submission

- **WHEN** an original recording shows an arrest command but the draft says the
  person submitted
- **THEN** the report identifies the unsupported change in conduct and degree of
  certainty rather than passing the assertion because the recording is cited

### Requirement: Party-drafted documents cannot bootstrap event or quotation support

A document drafted by either Plaintiff or the defense MUST NOT be treated as
evidence for an underlying event or quoted words. Such a document MAY establish
its own text, an attributed party position, or a procedural act. Plaintiff
memory MAY support an event or quotation only through a separate identified
source document recording the Plaintiff's memory claims, with that source voice
and degree of certainty preserved.

#### Scenario: Filing repeats an event and quotation

- **WHEN** a party-drafted filing is the only supplied document stating that an
  event occurred or that a person spoke quoted words
- **THEN** the event or quotation assertion has insufficient independent source
  support even though the filing may support an attributed description of the
  party's position

#### Scenario: Plaintiff memory is separately documented

- **WHEN** a separate declared source document records the Plaintiff's memory of
  an event or quotation
- **THEN** the report may treat that memory claim as an independent source while
  preserving its attribution and without treating it as adjudicated fact

### Requirement: Inferences remain distinct from personal knowledge

The report MUST distinguish source facts, supported inferences, and personal-
knowledge assertions and MUST state the premise facts and reasoning for every
supported inference.

#### Scenario: Inference is attributed as personal knowledge

- **WHEN** the sources support only an inference about what a person knew
- **THEN** the personal-knowledge assertion fails and the report records the
  supported premise and permissible inference separately

### Requirement: Authority propositions receive specialist validation

Every material authority proposition MUST be reviewed through the authority-
audit contract for actual holding, pinpoint, controlling status, posture,
relevant later treatment, factual fit, and application. The report MUST keep
pre-event clearly established law, defendant knowledge, municipal notice, and
Rule 15(c) notice of the lawsuit as distinct legal uses.

If the required authority audit or a current authority-specific finding is
unavailable, the validator MUST record the proposition as an unchecked assertion
and stop without substituting its own abbreviated authority review.

#### Scenario: Generally relevant case does not support the proposition

- **WHEN** a cited decision concerns the general subject but does not support
  the drafted proposition
- **THEN** the authority assertion fails notwithstanding the decision's general
  relevance

#### Scenario: Required authority finding is unavailable

- **WHEN** a material authority proposition lacks a current `audit-authorities`
  finding
- **THEN** the validator records an unchecked assertion and cannot complete
  validation

### Requirement: Omission coverage maps approved requirements to the draft

The validator MUST map every approved claim, material source fact, principal
correction, and applicable document requirement supplied in declared inputs to
an exact draft location or record an omission. It MUST preserve an authorized
unknown and its authorized treatment without treating unknown status alone as a
drafting defect.

#### Scenario: Approved claim is absent

- **WHEN** a declared current control approves a claim but the draft contains no
  authorized disposition or corresponding claim
- **THEN** the report records an unauthorized omission

#### Scenario: Identity remains unknown by authorization

- **WHEN** a declared current control authorizes an identity to remain unknown
  and the draft uses the approved treatment
- **THEN** the report records the factual unknown without classifying it as a
  drafting defect

### Requirement: Findings use separate status classes

The report MUST separately present supported assertions, supported inferences,
contradictions, overstatements, insufficient sources, missing documentation
links, unchecked assertions, omissions, and unresolved factual questions.
Missing documentation and missing substantive support MUST remain distinct. An
assertion or coverage record MUST accept one or more independently applicable
results so that substantive support and documentation status can be reported
together without collapsing either condition.

#### Scenario: Source supports an assertion but its optional route is absent

- **WHEN** an original source substantively supports the assertion but a
  supplied documentation system lacks the expected route
- **THEN** the report records support and a missing documentation link as
  separate statuses

### Requirement: Mermaid summary reflects report records

The report MUST include a Mermaid summary generated from the report's actual
status classes and counts. The diagram MUST NOT replace assertion-level records
or contain invented counts.

#### Scenario: Report contains three unresolved omissions

- **WHEN** the assertion and coverage records classify three items as omissions
- **THEN** the Mermaid summary displays an omission count of three derived from
  those records

### Requirement: Freshness follows assertions and dependencies

Changed assertion text or dependencies MUST invalidate affected reviews across
documents. Dependencies include sources, controlling decisions, applicable
controls, and reasoning premises. The report MUST identify the exact reviewed
target hash, but a target-hash change alone MUST NOT invalidate a finding whose
assertion text and dependencies remain unchanged. An unaffected finding MAY be
reused only after its bindings and continued applicability are verified. The
final candidate MUST receive complete coverage reconciliation.

#### Scenario: Previously passing wording changes

- **WHEN** reviewed wording changes while its old assertion record remains
- **THEN** the old pass is stale for the changed assertion and every dependent
  conclusion until revalidation

### Requirement: Stopping criteria preserve litigation decisions and unknowns

Validation MUST NOT complete with unchecked assertions, unresolved drafting
defects, or unauthorized omissions. It MUST account for remaining factual
unknowns and their authorized treatment and MUST NOT equate pleading support
with trial proof. A finding MUST NOT be closed by silently dropping a claim,
weakening an approved theory, inventing a fact, or relabeling a failed check.

#### Scenario: Evidence or a principal decision is unavailable

- **WHEN** unavailable evidence or a reserved litigation decision prevents
  resolution
- **THEN** the workflow records the precise issue and tradeoffs and stops rather
  than repeatedly regenerating drafts or changing strategy

### Requirement: Independent receipts and private current reports have separate owners

Every independent validation run MUST preserve its append-immutable receipt.
When a case project requires one stable private current report with Git history,
the public skill MUST treat its maintenance as a trusted case-controller action,
MUST NOT overwrite a declared input, and MUST preserve independently authored
receipts.

#### Scenario: Prior report is supplied for iteration

- **WHEN** a declared prior report is used to prepare the next current-report
  contents
- **THEN** the skill returns proposed new bytes while leaving the prior report
  and every independent receipt unchanged

### Requirement: Existing issue registers retain continuity

When an exact prior report is supplied, the proposed successor report MUST reuse
its existing issue register and stable issue identities. It MUST preserve
unresolved entries, explicitly dispose of corrected or otherwise resolved
entries, and add new entries without replacing the register with a parallel
history.

#### Scenario: Prior report contains an unresolved finding

- **WHEN** a declared prior report contains an unresolved issue-register entry
- **THEN** the successor proposal retains that issue ID and records its current
  disposition rather than silently omitting it or assigning a new ID

### Requirement: Specialist outputs cross declared role boundaries

Applicable Filing CI reports and freshness signals MUST enter assertion
validation only through the optional declared `deterministic-results` input
role. Each Rule 59(e) court-facing document and each generated declaration MUST
receive its own one-target validation invocation and receipt. Packet-level
reconciliation MUST NOT combine several filing targets into one invocation.

#### Scenario: Rule 59(e) packet has three court-facing documents

- **WHEN** a Rule 59(e) workflow generates a motion, proposed amended complaint,
  and proposed order
- **THEN** it performs three one-target validation invocations and then
  reconciles cross-document consistency at the packet level
