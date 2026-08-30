# building-judicial-reasoning-profiles Specification

## Purpose

TBD - created by archiving change issue-33-judicial-profiles. Update Purpose
after archive.

## Requirements

### Requirement: One generic builder produces immutable judicial profiles

The repository MUST provide one install-local
`building-judicial-reasoning-profiles` skill and MUST NOT provide a real-judge,
judge-named, or generated profile skill. The builder MUST consume only declared
folder roles and return ordinary proposed files for trusted-host publication
through the explicit output-folder contract.

#### Scenario: A new assigned judge needs a profile

- **WHEN** approved public materials exist for the assigned judge
- **THEN** the same generic builder compiles those materials into distinct
  profile files with domain YAML source documentation without creating or
  editing a skill

### Requirement: Acquisition and compilation are separate invocations

The builder MUST expose separate acquisition and compilation operations.
Acquisition MUST require expressly authorized internet and MUST write ordinary
source bytes plus domain `SOURCE.yaml` provenance directly beneath the explicit
output folder. Compilation MUST disable internet, MUST use only files from its
declared read-only inputs, and MUST write `judicial-profile.json`,
`judicial-profile-sources.yaml`, and `validation-receipt.json` directly beneath
a different explicit output folder. Every temporary file MUST remain beneath
`<output-folder>/temp/`. Neither operation may create or consume a package
manifest, package identity, package loader, graph, or CaseGraph object.

#### Scenario: Newly acquired source becomes eligible for compilation

- **WHEN** acquisition writes public-source bytes and matching `SOURCE.yaml`
  provenance into its explicit output folder
- **THEN** compilation may use those bytes only in a later invocation that
  declares the acquisition folder as recursive read-only `approved-sources`

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
- **THEN** domain validation fails and no role execution or profile publication
  occurs

### Requirement: Profile source references preserve folder provenance

The compiled profile MUST retain each source ID and MUST emit a domain YAML
source index mapping that ID to the declared input role, folder-relative
`SOURCE.yaml`, referenced artifact path, SHA-256, applicable dates,
classification, validation state, limitations, and gaps. Missing, malformed,
escaping, mismatched, or stale required source records MUST stop compilation
before semantic work.

#### Scenario: Profile source hash does not match

- **WHEN** a source index entry's SHA-256 does not match the referenced bytes in
  its declared read-only input folder
- **THEN** compilation fails and emits no profile

### Requirement: CourtListener discovery preserves judge identity and candidate disposition

The acquisition operation MUST document a CourtListener REST API discovery path
that resolves the judge before searching cases, prefers a stable judge
identifier, and permits a documented name-query fallback. It MUST distinguish
opinion authorship from docket assignment and referral, and MUST narrow
candidates by applicable court, judicial tenure or date range, case category,
procedural posture, and the profile's research question. Nature-of-suit,
cause-of-action, Section 1983, and police or law-enforcement search terms MUST
remain discovery leads rather than proof that a candidate belongs in the profile
corpus.

Before inclusion, the acquisition operation MUST require primary docket material
to verify the judge relationship, Section 1983 basis, police or law- enforcement
involvement, and relevant posture. It MUST preserve sanitized query provenance,
stable result identity, pagination or cursor identity, selection or exclusion
status, and an inspectable reason for every reviewed candidate. It MUST NOT
persist API tokens, credentials, cookies, authorization headers, or other
secrets.

#### Scenario: Judge-name search returns mixed civil-rights cases

- **WHEN** CourtListener returns candidates that include non-police cases,
  agency-only matters, unresolved judge relationships, or non-Section 1983
  claims
- **THEN** acquisition retains each reviewed candidate's stable identity and
  exclusion reason and admits only candidates independently verified from
  primary docket material

### Requirement: PACER fallback requires separate access and fee authority

The acquisition operation MUST treat PACER or court-specific CM/ECF as an
optional official fallback for docket identity, assignment, status, and
completeness. It MUST require explicit authorization to use the access method
and separate approval before incurring any fee. Credentials MUST remain in the
authorized runtime and MUST NOT be written to the acquisition output, source
provenance, profile, receipt, or temporary files.

#### Scenario: CourtListener coverage is incomplete

- **WHEN** a candidate cannot be verified completely from public CourtListener
  and court materials
- **THEN** acquisition records the coverage gap and uses PACER or CM/ECF only
  after both access authorization and any required fee approval are present
