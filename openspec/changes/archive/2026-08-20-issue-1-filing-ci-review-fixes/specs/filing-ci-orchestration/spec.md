## MODIFIED Requirements

### Requirement: Read-only orchestration

The skill MUST treat checker execution and result reporting as read-only
orchestration. It MUST NOT silently edit the controlling filing, create project
paths, rewrite checker output, or represent a correction as user-approved.

A Filing CI response with findings MUST stop after reporting and returning those
findings. It MUST NOT edit the filing or perform a drafting handoff in that same
response. Any user-authorized correction MUST occur through the applicable
drafting workflow as a separate subsequent step. A general instruction to make a
document filing-ready MUST NOT be treated as approval of particular corrective
language.

The later drafting workflow MAY use exact replacement text actually supplied by
the checker or source-supported drafting. It MUST NOT infer corrective
sentences, placeholders, merits assertions, or legal conclusions from a
structural finding or attacked location. After any material correction, a
separate later Filing CI response MUST run the checker again against the current
draft.

#### Scenario: Checker identifies a correctable defect

- **WHEN** a checker finding could be corrected in the draft
- **THEN** the skill reports the attacked location and required correction to
  the drafting loop without modifying the controlling filing

#### Scenario: Filing CI response contains findings

- **WHEN** Filing CI reports any checker finding
- **THEN** that response stops after returning the finding and does not edit the
  filing or begin the drafting handoff

#### Scenario: User generally requests filing readiness

- **WHEN** a broader user request asks to make the document filing-ready but
  does not approve specific corrective language
- **THEN** Filing CI does not treat that request as authority to draft or apply
  a particular correction

#### Scenario: Finding supplies no exact replacement text

- **WHEN** a checker identifies a structural defect or location without
  supplying exact replacement text
- **THEN** the later drafting workflow does not infer sentences, placeholders,
  merits assertions, or legal conclusions from the finding

#### Scenario: Separate drafting workflow changes the filing

- **WHEN** a user-authorized later drafting workflow materially corrects the
  controlling filing
- **THEN** Filing CI runs again in a separate subsequent response before its
  gate can pass
