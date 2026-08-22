## ADDED Requirements

### Requirement: Request-by-request response audit

The response-audit skill SHALL consume the stable target or served-request map
and audit each exact request, response, objection, production reference, and
withholding statement separately. Each row MUST include request number, target
IDs, response and objection text, production or withholding status, stated
basis, missing answer or material, concrete deficiency, requested cure, and
approved source IDs.

#### Scenario: Response contains text and an objection

- **WHEN** a response supplies a partial answer and an objection to the same
  request
- **THEN** the audit preserves both exact components and separately evaluates
  the answer, objection, production status, deficiency, and cure

### Requirement: Production states remain distinct

The skill MUST distinguish `not produced`, `claimed nonexistent`, `withheld`,
and `unclear`. It MUST NOT convert silence, a boilerplate objection, or absent
production into a claim that responsive material does not exist or is withheld.

#### Scenario: Objection has no production statement

- **WHEN** a generic objection does not say whether a search occurred, material
  exists, material was produced, or material was withheld
- **THEN** the audit marks production and withholding status unclear and asks
  for concrete clarification supported by approved requirements

### Requirement: Audit conclusions and strategy are bounded

The skill MUST NOT certify an objection as valid, declare waiver, draft meet-
and-confer correspondence, or select whether to accept, challenge, narrow,
confer, compel, seek fees, or seek sanctions. A material choice SHALL use
`PLAINTIFF DECISION REQUIRED`, state choices and consequences, and select none.

#### Scenario: Full challenge and narrower cure remain supported

- **WHEN** both approaches remain supported
- **THEN** the audit describes both paths and consequences without choosing or
  drafting correspondence
