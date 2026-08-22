# judge-overlay-authoring Specification

## Purpose

Define an evidence-bounded, anti-gaming judge overlay as a judicial reasoning
profile for the assigned judge. Its authoring and lifecycle method preserves
source strength, keeps official court requirements separate from reasoning
evidence, enforces neutral transfer limits, creates immutable versions, and
fails closed when support is insufficient.

## Requirements

### Requirement: Discoverable reusable method

The repository SHALL publish a concise judge-overlay authoring guide and route
to it from README with confined relative links. The guide MUST use the existing
Scholer overlay only as a structural example and MUST NOT generalize or copy its
judge-specific conclusions.

#### Scenario: Maintainer starts a new overlay

- **WHEN** a maintainer follows the README route
- **THEN** the maintainer reaches the repository guide and its existing local
  corpus, validator, transfer-card, and worked-example sources

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

The judge overlay SHALL be a judicial reasoning profile for the assigned judge.
For each supported issue and procedural posture, it SHALL distinguish
substantive doctrine, procedural doctrine, reasoning patterns, authority
hierarchy, factual methodology, error sensitivities, and analytical presentation
patterns. It SHALL use verified public opinions and orders as its primary
reasoning sources. Public judge-authored articles, speeches, and books MAY
provide bounded context but MUST NOT become governing authority. Standing orders
and courtroom procedures SHALL remain separate compliance inputs.

The profile MAY support a request to apply the judge's own verified reasoning
consistently. It MUST NOT infer psychology or personal preference, imitate the
judge's voice, or convert descriptive patterns into outcome predictions.

#### Scenario: Prior reasoning supports the current analytical sequence

- **WHEN** verified sources establish the judge's rule, reasoning sequence, and
  limiting principle for the same issue and posture
- **THEN** a neutral transfer may organize the supported facts and requested
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

A drafting skill SHALL consume only validated neutral transfer cards, preserve
their source identity, evidence strength, permitted use, prohibited inference,
denominator, and missingness, and keep governing law separate. The transfer MUST
NOT expose private strategy or select a litigation path.

#### Scenario: Transfer card supports no drafting change

- **WHEN** the card prohibits the proposed inference or reports no qualifying
  support
- **THEN** the drafting skill makes no judge-specific change and preserves the
  card's limitation

### Requirement: Generic paired examples

The guide SHALL include a generic synthetic valid overlay example and a generic
synthetic thin-corpus example that fails closed. The examples MUST NOT contain a
private path, private case fact, or real judge-specific conduct conclusion.

#### Scenario: Reader compares evidence outcomes

- **WHEN** the reader reviews the paired examples
- **THEN** one demonstrates a bounded validated transfer and the other
  demonstrates no unsupported judge-specific proposition
