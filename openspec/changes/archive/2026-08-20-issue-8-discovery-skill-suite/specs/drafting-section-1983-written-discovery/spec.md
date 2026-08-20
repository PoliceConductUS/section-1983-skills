## ADDED Requirements

### Requirement: Traceable Discovery Target Map

The written-discovery skill SHALL create a stable target map containing
meaningful nonblank `target_id`, `claim`, `defendant`, `element`, `factual_gap`,
`likely_custodian`, and `expected_native_source` values, supporting approved
source IDs, and bounded proportionality scope for every drafted request. Likely
custodians and expected native sources MUST remain labeled expectations rather
than established facts. Proportionality MUST NOT use a placeholder or facially
unbounded scope. One row MUST represent one claim-defendant-element tuple.

#### Scenario: Request serves more than one legal tuple

- **WHEN** one proposed request serves multiple claims, defendants, or elements
- **THEN** the map uses a separate target row for each tuple and links the
  request to every applicable stable target ID

#### Scenario: Mapping support is missing

- **WHEN** approved sources do not support a required mapping value
- **THEN** the skill reports the mapping gap and does not infer, leave blank, or
  invent the value

### Requirement: Distinct bounded request forms

The skill SHALL separately number requests for production, interrogatories, and
requests for admission and link each to target IDs. Requests for production MUST
identify bounded document or ESI categories and requested native form when
supported; interrogatories MUST seek bounded facts or identities; and each
request for admission MUST state one discrete proposition. The skill MUST
account for approved numerical limits and time, actor, entity, system, category,
importance, burden, and narrower-alternative information.

#### Scenario: Three request types are supported

- **WHEN** the approved packet supports an RFP, interrogatory, and RFA
- **THEN** the output keeps the forms separately numbered and applies the
  correct form-specific contract to each

### Requirement: Existence before unverified content

The skill MUST distinguish a source expected to exist from a verified source and
MUST NOT state expected content as established. When existence or content is
unverified, it SHALL draft an existence-identification request, a production
request conditioned on existence, or another bounded request that does not
assume the answer.

#### Scenario: Expected recording is unverified

- **WHEN** a target identifies a recording as expected but no approved source
  verifies its existence or content
- **THEN** the request asks whether it exists and seeks identification or
  production if it exists without asserting what it depicts

### Requirement: Written-discovery strategy remains reserved

The skill MUST NOT select service, sequencing, priority, request-cap allocation,
narrowing, stipulation, contention timing, or another material strategy. It
SHALL emit `PLAINTIFF DECISION REQUIRED`, state choices and consequences,
preserve the current draft, and select none.

#### Scenario: Numerical limit requires prioritization

- **WHEN** supported proposed requests exceed an approved numerical limit
- **THEN** the skill presents prioritization choices and consequences without
  deleting, combining, serving, or selecting requests
