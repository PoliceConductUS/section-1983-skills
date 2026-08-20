# filing-ci-orchestration Specification

## Purpose

Define thin, project-configured Filing CI orchestration that runs deterministic
filing-integrity checks at the required workflow stages, preserves checker
findings, and fails closed without taking ownership of checker logic or
drafting.

## Requirements

### Requirement: Configured checker resolution

The `filing-ci` skill SHALL resolve the checker invocation and controlling draft
from repository instructions, project configuration, or explicit user input. It
MUST run the configured invocation rather than describe or reproduce the
deterministic checks in prose. It MUST NOT invent executable paths, flags,
source paths, or output locations.

#### Scenario: Project supplies a complete checker invocation

- **WHEN** a project identifies the controlling draft and a complete
  filing-integrity checker invocation
- **THEN** the skill runs that invocation against the identified draft without
  substituting an inferred command

#### Scenario: Checker invocation is not configured

- **WHEN** no repository instruction, project configuration, or explicit user
  input supplies a complete checker invocation
- **THEN** the skill reports unavailable checker configuration and leaves the
  filing gate open without inventing a command

### Requirement: Workflow-stage execution

The skill MUST run Filing CI after every material drafting change and again
immediately before describing the document as filing-ready. A material change
MUST invalidate an earlier successful result.

#### Scenario: Draft changes after a successful run

- **WHEN** the controlling draft changes materially after Filing CI succeeds
- **THEN** the skill treats the prior result as stale and requires a new run
  before filing readiness

#### Scenario: Filing-readiness review begins

- **WHEN** the workflow reaches a filing-readiness decision
- **THEN** the skill requires a current successful Filing CI result for the
  controlling draft

### Requirement: Verified-authority root integration

The skill MUST use the project's configured verified-authority root when one is
present and the checker requires authority verification. It MUST NOT hardcode a
machine-specific root or silently substitute another authority directory.

#### Scenario: Project configures a verified-authority root

- **WHEN** project instructions or configuration identify a verified-authority
  root and the checker invocation accepts that input
- **THEN** the skill runs the checker with that configured root

#### Scenario: Required root cannot be supplied

- **WHEN** authority verification is required but the configured invocation
  cannot resolve or accept the project's verified-authority root
- **THEN** the skill reports the unresolved input and leaves the filing gate
  open

### Requirement: Failure classification and drafting-loop return

The skill SHALL distinguish unavailable configuration, unavailable execution,
unreadable or unresolved required inputs, malformed promised output, and
checker-reported findings. It MUST explain the blocking class, preserve the
checker's documented severity, and return actionable findings to the drafting
loop for correction and rerun.

#### Scenario: Executable is unavailable

- **WHEN** the configured checker cannot be executed
- **THEN** the skill reports an unavailable-execution failure and does not claim
  that any deterministic check ran

#### Scenario: Checker reports hard findings

- **WHEN** the checker exits with or reports unresolved hard findings
- **THEN** the skill identifies those findings as an open filing gate and sends
  them back to the drafting loop

#### Scenario: Checker reports non-hard findings

- **WHEN** the checker reports warnings or another documented non-hard class
- **THEN** the skill preserves that class and presents the findings without
  silently downgrading, dismissing, or correcting them

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

### Requirement: Fail-closed filing gate

The skill MUST keep the filing gate open when the checker is unavailable, a
required input is unresolved, output cannot be reliably interpreted, a material
change has made the result stale, or a hard finding remains unresolved. It SHALL
describe a filing as passing Filing CI only after a current successful run for
the controlling draft.

#### Scenario: Hard failure remains unresolved

- **WHEN** any hard checker failure remains open
- **THEN** the skill refuses to describe the document as filing-ready

#### Scenario: Current run succeeds

- **WHEN** the configured checker completes successfully for the current draft
  with no unresolved hard findings
- **THEN** the skill may report that Filing CI passed while preserving any
  documented warnings and other independent filing gates
