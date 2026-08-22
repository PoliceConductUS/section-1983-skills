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
