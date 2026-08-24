# judge-overlay-authoring Specification

## Purpose

Define an evidence-bounded, anti-gaming judge overlay as a judicial reasoning
profile for the assigned judge. Its authoring and lifecycle method preserves
source strength, keeps official court requirements separate from reasoning
evidence, enforces neutral transfer limits, creates immutable versions, and
fails closed when support is insufficient.

## Requirements

### Requirement: Discoverable reusable method

The repository SHALL publish a concise judge-overlay authoring guide, route to
it from README with confined relative links, and link it to the general case-
overlay lifecycle. The guide MUST use the existing Scholer overlay only as a
structural example and MUST NOT generalize or copy its judge-specific
conclusions.

The judge guide MUST define when to create, reuse, refresh, rebuild, and
supersede a judge overlay. Assignment or reassignment, a changed official rule,
procedure, or standing order, a new validated corpus or transfer card, stale
source checks, a changed prohibited inference, or a validator failure MUST
invalidate reuse as applicable. Every new version MUST preserve the prior
version and its source identities.

#### Scenario: Maintainer starts a new overlay

- **WHEN** a maintainer follows the README route
- **THEN** the maintainer reaches the repository guide, general lifecycle, and
  existing local corpus, validator, transfer-card, and worked-example sources

#### Scenario: Assigned judge or official procedure changes

- **WHEN** assignment changes or an applicable official procedure source changes
  after the pinned checked date
- **THEN** the prior judge overlay remains immutable and no judge-specific
  drafting change occurs until a new version passes its required validation

### Requirement: Validated evidence-strength method

The guide MUST define the canonical corpus contract, source hierarchy, coding
stages, denominator and missingness limits, example/cluster/tendency strength,
neutral transfer boundary, and degradation clause. A published or transferred
corpus MUST pass the canonical validator. Unsupported strength MUST fail closed
without adding a judge-specific proposition.

#### Scenario: Corpus is thin or incomplete

- **WHEN** a corpus cannot support a claimed cluster or tendency
- **THEN** the overlay preserves any verified example at its actual strength and
  adds no stronger judge-specific proposition

### Requirement: Judicial reasoning profile scope

The guide SHALL define a judge overlay as a judicial reasoning profile for the
assigned judge. The profile SHALL distinguish substantive doctrine, procedural
doctrine, reasoning patterns, authority hierarchy, factual methodology, error
sensitivities, and analytical presentation patterns for each supported issue and
procedural posture. Verified public opinions and orders are primary reasoning
sources. Public judge-authored articles, speeches, and books MAY provide bounded
context but MUST NOT become governing authority. Standing orders and courtroom
procedures SHALL remain separate compliance inputs.

The profile MAY support a request to apply the judge's own verified reasoning
consistently. It MUST NOT infer psychology or preference, imitate the judge's
voice, or convert descriptive patterns into outcome predictions.

#### Scenario: Prior reasoning supplies a supported framework

- **WHEN** verified sources establish the judge's rule, analytical sequence, and
  limiting principle for the same issue and posture
- **THEN** the transfer may organize the supported facts and requested
  application within that demonstrated method without predicting the result

### Requirement: Anti-gaming boundary

The method MUST prohibit manipulating or predicting judicial assignment,
exploiting perceived personal preferences, tailoring facts or law to a supposed
desired outcome, concealing adverse authority, distorting the record,
personalizing attacks on the court, and renaming another judge's conclusions.

#### Scenario: Proposed overlay uses a supposed preference

- **WHEN** a proposed overlay turns a perceived preference or predicted outcome
  into a drafting instruction
- **THEN** the method rejects that instruction rather than transferring it

### Requirement: Officially sourced court-conduct checklist

The method MUST require a source-bounded checklist for applicable official
rules, individual procedures, standing orders, candor duties, civility
requirements, ex parte limits, filing limits, and other express prohibitions or
discouragement. Every court-specific warning MUST identify its official source
and checked date. An unverified or stale warning SHALL remain a gap and MUST NOT
be stated as a court requirement.

#### Scenario: Conduct warning lacks current official support

- **WHEN** a proposed court-conduct warning lacks an official source identity or
  checked date
- **THEN** the guide classifies it as an unresolved source gap and does not
  state it as a requirement

### Requirement: Neutral downstream consumption

A drafting skill SHALL invoke the assigned-judge overlay separately after the
governing document and claim skills, using only that overlay's declared input
roles and target. It SHALL consume only validated neutral transfer cards,
preserve their source identity, evidence strength, permitted use, prohibited
inference, denominator, and missingness, and keep governing law separate. The
transfer MUST NOT expose private strategy or select a litigation path.

Every composition run SHALL return one canonical output-relative receipt plan
for publication by the trusted host. A prohibited inference or no qualifying
support produces no judge-specific drafting change and records the bounded
reason. Missing, stale, invalid, or unavailable required inputs fail closed and
are not represented as passing. The absence of judge-specific prose does not
establish that the overlay ran.

#### Scenario: Transfer card supports no drafting change

- **WHEN** the card prohibits the proposed inference or reports no qualifying
  support
- **THEN** the drafting skill makes no judge-specific change, preserves the
  card's limitation, and returns a receipt stating
  `no judge-specific drafting change`

#### Scenario: Applicable overlay never runs

- **WHEN** composition produces no host-published execution receipt
- **THEN** review treats overlay execution as unproven rather than inferring a
  successful no-change result from the filing text

### Requirement: Generic paired examples

The guide SHALL include a generic synthetic valid overlay example and a generic
synthetic thin-corpus example that fails closed. The examples MUST NOT contain a
private path, private case fact, or real judge-specific conduct conclusion.

#### Scenario: Reader compares evidence outcomes

- **WHEN** the reader reviews the paired examples
- **THEN** one demonstrates a bounded validated transfer and the other
  demonstrates no unsupported judge-specific proposition
