## ADDED Requirements

### Requirement: Canonical published corpus schema

A published or transferred Rule 59 decision corpus MUST use a versioned
canonical JSON object containing a study manifest, denominator, decision
records, retrieval-gap log, and neutral transfer cards. The public schema SHALL
encode court, judge, authorship, posture, grounds, requested relief, proposed
material, reasoning independence, disposition, source provenance, missing
documents, and appellate history.

#### Scenario: Complete canonical export

- **WHEN** a researcher publishes or transfers a Rule 59 decision corpus
- **THEN** the export contains every canonical top-level component and every
  decision record supplies the fields required by the public schema

#### Scenario: Researcher uses another working format

- **WHEN** a study is maintained in CSV, YAML, or a database
- **THEN** the study exports an equivalent canonical JSON artifact and validates
  that artifact before publication or downstream transfer

### Requirement: Distinct decision stages and authorship

Each decision record MUST distinguish a recommendation, adoption-only order,
independently reasoned final decision, consent final decision, and outcome-only
order. The record SHALL separately identify the assigned judge, reasoning
author, recommendation author, and adopting judge as applicable and MUST use a
reasoning- independence value consistent with the decision type.

#### Scenario: Recommendation record

- **WHEN** a record represents a magistrate judge recommendation
- **THEN** it is coded as `recommendation`, uses `recommendation-only`,
  identifies the recommendation author, and is not counted as a final district
  decision

#### Scenario: Adoption-only order

- **WHEN** a district judge adopts a recommendation without additional reasoning
- **THEN** the order is coded as `adoption-only-order`, uses
  `adopts-without-additional-reasoning`, identifies the adopting judge, and does
  not attribute the recommendation's reasoning to that judge

#### Scenario: Independently reasoned final decision

- **WHEN** a final decision contains its own substantive reasoning
- **THEN** it is coded as `independently-reasoned-final-decision`, uses
  `independent`, and identifies the reasoning author

### Requirement: Motion, grounds, relief, material, disposition, and appeal coding

Each parent record MUST represent one motion-disposition pair and SHALL encode
the challenged disposition and judgment posture, every asserted ground in stable
child records, the exact categories of requested relief, proposed material
status, disposition code and stated reasons, and appellate history checked
through a concrete date.

#### Scenario: One motion has multiple grounds

- **WHEN** one Rule 59 motion asserts multiple grounds and receives one
  disposition
- **THEN** the corpus contains one parent motion-disposition record with one
  stable child record per ground rather than counting multiple motions

#### Scenario: Related recommendation, adoption, and appeal exist

- **WHEN** a recommendation, adopting order, amended judgment, or appeal relates
  to the same motion
- **THEN** those artifacts are linked stages and appellate history within the
  same motion-disposition unit rather than extra Rule 59 motions

### Requirement: Missing-document and denominator disclosure

The corpus MUST record every known missing document and denominator limit. Each
missing document SHALL appear in the affected decision record and in a stable
retrieval-gap entry. The denominator SHALL state its defined universe, located
candidate count, coded pair count, research-question-complete count,
completeness status, and explicit limits.

#### Scenario: Motion-side material is unavailable

- **WHEN** a ruling is reviewed but the motion or proposed material is
  unavailable
- **THEN** the record and retrieval-gap log identify the missing artifact and
  the corpus does not treat the pair as complete for motion-design analysis

#### Scenario: Candidate universe remains unresolved

- **WHEN** a capped search, inaccessible docket, or unresolved candidate remains
- **THEN** the denominator status is incomplete and the unresolved limit is
  stated

### Requirement: Incomplete-sample claim prohibition

An incomplete or convenience corpus MUST NOT produce a tendency or success-rate
transfer card. A tendency or success-rate card SHALL validate only when the
declared universe is complete and relevant unresolved missingness is zero.
Incomplete corpora may support only bounded examples or documented-cluster
transfers with explicit limits.

#### Scenario: Incomplete corpus attempts tendency

- **WHEN** a transfer card claims `tendency` while the denominator is incomplete
  or relevant missingness remains unresolved
- **THEN** validation fails without publishing the tendency

#### Scenario: Convenience sample attempts success rate

- **WHEN** a transfer card presents a success-rate metric from a convenience
  sample
- **THEN** validation fails even if the numerator and denominator are
  numerically valid

#### Scenario: Incomplete corpus transfers an example

- **WHEN** a verified record from an incomplete corpus is transferred only as an
  `example` with its limits and prohibited inference stated
- **THEN** the card may validate without implying frequency or predictive value

### Requirement: Neutral transfer-card format

Every downstream transfer MUST use the public neutral transfer-card schema. A
card SHALL identify its stable ID, proposition, defined universe, numerator,
denominator, date range, supporting row IDs, evidence level, missingness,
disconfirming row IDs, permitted use, prohibited inference, checked-through
date, actual source identity, and source checked date. It MUST NOT select
litigation strategy or describe a correlation as causal or predictive.

#### Scenario: Supported bounded transfer

- **WHEN** a corpus finding is supplied to another skill
- **THEN** the transfer card exposes its source rows, evidence strength,
  denominator, missingness, permitted use, and prohibited inference without
  selecting a legal path

### Requirement: Install-local deterministic validation

The public skill MUST include a standard-library validator that accepts one
canonical corpus JSON path, performs shape, controlled-value, unique-ID,
reference, authorship, gap, denominator, and transfer-strength checks without
network access, and exits nonzero with stable line-oriented findings on invalid
input. The validator SHALL fail cleanly on malformed JSON or malformed field
types without a traceback.

#### Scenario: Valid canonical corpus

- **WHEN** a complete canonical corpus satisfies all shape and semantic
  invariants
- **THEN** the validator exits zero and reports validation success

#### Scenario: Invalid authorship combination

- **WHEN** an adoption-only order claims independent reasoning or attributes the
  recommendation's reasoning to the adopting judge
- **THEN** the validator exits nonzero with a stable authorship-stage finding

#### Scenario: Malformed corpus input

- **WHEN** the input is invalid JSON or a required object has the wrong type
- **THEN** the validator exits nonzero with a stable malformed-input finding and
  no traceback

### Requirement: Synthetic validation fixtures

The repository MUST include generic synthetic fixtures that exercise a valid
complete corpus, a valid incomplete example or documented cluster, an invalid
incomplete tendency or success-rate claim, and an invalid authorship-stage
combination. Fixtures SHALL contain no private case materials, machine-specific
paths, or real unpublished research artifacts.

#### Scenario: Fixture validation suite runs

- **WHEN** repository tests execute the validator against all checked-in corpus
  fixtures
- **THEN** each valid fixture passes, each invalid fixture fails for its
  declared stable finding, and no fixture discloses private case content
