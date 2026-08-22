## MODIFIED Requirements

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
