# building-judicial-reasoning-profiles Specification

## Purpose

TBD - created by archiving change issue-33-judicial-profiles. Update Purpose
after archive.

## Requirements

### Requirement: One generic builder produces immutable judicial profiles

The repository MUST provide one install-local
`building-judicial-reasoning-profiles` skill and MUST NOT provide a real-judge,
judge-named, or generated profile skill. The builder MUST consume only declared
folder roles and return proposed package members for trusted-host publication
through the common immutable folder-package contract.

#### Scenario: A new assigned judge needs a profile

- **WHEN** approved public materials exist for the assigned judge
- **THEN** the same generic builder compiles those materials into a distinct
  `judicial-profile` package without creating or editing a skill

### Requirement: Acquisition and compilation are separate invocations

Acquisition MUST require expressly authorized internet access and MUST return
only provenance-bearing source-package output. Compilation MUST disable internet
access and MUST consume only previously approved read-only inputs. Newly
acquired bytes MUST NOT become compilation input until a later invocation
declares their validated package folder in `approved-sources`.

#### Scenario: Research discovers a new public order

- **WHEN** an acquisition invocation retrieves the order
- **THEN** the current output contains source bytes and provenance but no
  judicial profile, and compilation can use the order only in a later invocation

### Requirement: Source classes and attribution remain distinct

Every judicial-profile record MUST preserve its exact proposition, source
identity, source date, issue, posture, attribution status, and one source class:
`revealed_reasoning`, `stated_philosophy`, `self_presentation`, or
`court_compliance`. Adoption-only orders, recommendations, and outcome-only
records MUST NOT be represented as the assigned judge's independent reasoning.

#### Scenario: The assigned judge adopts a recommendation

- **WHEN** the order supplies no independent substantive reasoning
- **THEN** the record remains `adoption_only` and cannot support an independent
  revealed-reasoning transfer

### Requirement: Cross-class comparisons preserve bounded evidence

Each comparison MUST identify both records and preserve both exact propositions,
sources, dates, issue, posture, similarities, differences, and one state:
`aligned`, `tension`, `divergent`, or `indeterminate`. The builder MUST reject
source-class averaging, psychological characterization, hypocrisy claims,
preference claims, manipulation opportunities, and outcome prediction.

#### Scenario: A speech and opinion differ

- **WHEN** a comparison describes the record relationship
- **THEN** it retains both propositions and sources and reports only the bounded
  comparison state without inferring motive, personality, or result

### Requirement: Neutral transfer requires independently revealed reasoning

The builder MUST require independently revealed reasoning for every transfer.
Only validated `revealed_reasoning` records attributed as
`independent_reasoning` MAY support a neutral judge-specific drafting transfer.
Every supporting record MUST match the transfer's issue and posture. Missing or
ineligible support MUST produce no judge-specific drafting change and an
explicit gap.

#### Scenario: Only philosophy and outcome records address the issue

- **WHEN** compilation finds no independently reasoned revealed-reasoning record
- **THEN** the profile contains no neutral transfer for that issue and preserves
  the missing-support gap

### Requirement: Profile data cannot become role behavior

The domain schema MUST reject profile fields that attempt to define role
capabilities, prohibitions, internet policy, target mutation, output authority,
system prompts, or agent instructions. Static judicial-reviewer behavior MUST
remain separate and is consumed only through the downstream shared launcher.

#### Scenario: A profile member requests write authority

- **WHEN** profile data contains instruction-shaped role controls
- **THEN** domain validation fails and no role execution or package publication
  occurs
