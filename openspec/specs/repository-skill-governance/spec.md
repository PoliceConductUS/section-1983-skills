# repository-skill-governance Specification

## Purpose

TBD - created by archiving change issue-14-judgment-rules-governance. Update
Purpose after archive.

## Requirements

### Requirement: User-reserved litigation judgment

Public skills MUST reserve litigation strategy, positions, concessions,
requested relief, filing, and other material legal choices to the user. When a
skill can support multiple material paths, it SHALL state the supported choices
and consequences, select none, and identify the user decision required.

#### Scenario: Multiple supported litigation paths

- **WHEN** a skill encounters a material choice among supported litigation paths
- **THEN** it presents the supported choices and consequences, identifies the
  user decision required, and does not choose a path

#### Scenario: User has supplied a decision

- **WHEN** the user expressly selects a supported path
- **THEN** the skill may apply that decision without enlarging it or silently
  deciding a different material choice

### Requirement: Jurisdiction-specific proposition confinement

A current jurisdiction-specific legal proposition MUST appear only in a verified
reference that identifies its jurisdiction, authoritative source provenance, and
checked date. This includes a deadline, limit, local rule, standing-order
requirement, judge requirement, or judge-specific legal proposition. A public
SKILL file SHALL route to that reference and preserve source gates without
restating the proposition.

#### Scenario: Maintainer adds a local requirement

- **WHEN** a maintainer adds a current district or judge requirement
- **THEN** the proposition is placed in a jurisdiction reference with the
  jurisdiction, authoritative source, and checked date rather than in SKILL
  workflow prose

#### Scenario: Jurisdiction source is unavailable or stale

- **WHEN** the required jurisdiction reference is unavailable or its currency
  cannot be established
- **THEN** the skill reports the source gap and does not supply the proposition
  from memory or a generic substitute

### Requirement: Complete rules-freshness registry

The repository MUST maintain a public machine-readable registry containing
exactly one classification for every public skill. Each entry SHALL have a
nonempty rationale and ISO review date. A bundled-rules-dependent entry MUST
identify authoritative source records with HTTPS provenance URLs and concrete
checked dates. A runtime-sourced entry MUST define that the skill's returned
artifact exposes the actual approved source identity and checked date used.

#### Scenario: New public skill is unclassified

- **WHEN** a public `skills/*/SKILL.md` exists without a matching registry entry
- **THEN** repository validation fails before the change is accepted

#### Scenario: Rules-dependent entry lacks provenance

- **WHEN** a bundled-rules-dependent skill has no authoritative source ID, URL,
  or checked date
- **THEN** repository validation fails with the incomplete entry identified

#### Scenario: Runtime-sourced skill completes work

- **WHEN** a runtime-sourced skill applies an approved rule or order source
- **THEN** its returned artifact exposes the stable source identity and the date
  that source was checked

### Requirement: Protected legal-gate review

Contribution guidance MUST identify verification, factual and authority source,
permission, filing-readiness, judgment-routing, rules-provenance, and
tool-ownership gates as protected. A contribution that weakens or bypasses one
of those gates SHALL require explicit human review that names the affected gate
and rationale.

#### Scenario: Pull request changes a protected gate

- **WHEN** a contribution weakens, bypasses, removes, or changes a protected
  gate
- **THEN** the contribution identifies the affected gate and rationale and
  requests explicit review before acceptance

#### Scenario: Review prompt is removed

- **WHEN** repository contribution surfaces no longer require protected-gate
  review
- **THEN** repository validation fails

### Requirement: Thin skill-wrapper ownership boundary

The repository MUST retain only public skill instructions and
repository-specific validation or evaluation support. General-purpose executable
rule retrieval, citation verification, evidence processing, filing inspection,
or other reusable tooling SHALL belong in its owning repository, with only a
thin skill wrapper here when needed.

#### Scenario: Contribution proposes reusable executable tooling

- **WHEN** a contribution's executable behavior is general-purpose rather than
  specific to validating or evaluating this repository
- **THEN** maintainers route it to an owning repository and keep at most the
  public thin skill wrapper in this repository

### Requirement: Governance validation is repository-specific and fail-closed

Repository validation MUST deterministically compare public skill directories
with the rules registry and validate governance policy and contribution-review
surfaces. It SHALL use no network retrieval and MUST fail on malformed JSON,
duplicate or unknown skill entries, invalid modes or dates, unknown source IDs,
insecure or malformed provenance, or missing protected policy language.

#### Scenario: Valid governance state

- **WHEN** all public skills are classified and all required policy, provenance,
  and review data is valid
- **THEN** governance validation exits successfully without network access

#### Scenario: Invalid governance state

- **WHEN** any required governance invariant is absent or malformed
- **THEN** governance validation exits nonzero and identifies the violated
  invariant

### Requirement: Durable contributor workflow

The contribution guide MUST require one story per stacked branch, RED/GREEN TDD,
OpenSpec design/tasks/verification/retrospective artifacts, archive of the
completed change, refactoring only while tests remain green, and the complete
repository validation gate before release.

#### Scenario: Contributor begins a story

- **WHEN** a contributor starts one backlog story
- **THEN** the contributor uses one stacked branch, writes the failing test
  before implementation, completes the OpenSpec cycle, and runs the full gate

### Requirement: Human-controlled legal judgment

The contribution guide MUST preserve the existing protected-gates authority and
state that automation does not silently select plaintiff decisions, litigation
strategy, or legal conclusions.

#### Scenario: Automation encounters a protected choice

- **WHEN** a contribution could automate a material legal choice
- **THEN** it routes the choice through the existing governance authority and
  leaves the selection to the human

### Requirement: Measurement remains feedback

The contribution guide MUST state that measurement is feedback, never a verdict.
Score deltas and judgment-based evaluations SHALL reveal change or prompt review
and MUST NOT decide legal quality, filing readiness, or human judgment.

#### Scenario: Evaluation score changes

- **WHEN** a score or judgment-based evaluation changes
- **THEN** the contributor investigates the signal without treating it as a
  verdict

### Requirement: Self-documenting code and bounded comments

The contribution guide MUST require self-documenting code and refactoring before
adding a comment. A necessary comment SHALL be short and clear and SHOULD
reference an ADR or recorded decision when practical.

#### Scenario: Code appears to need an explanatory comment

- **WHEN** clearer names or structure can express the reason
- **THEN** the contributor refactors instead of adding the comment

### Requirement: Immutable release contribution

The contribution guide MUST link the existing release authority, state that a
push to `main` is not publication, and require immutable semantic-version tags
after complete validation.

#### Scenario: Contributor finishes a branch

- **WHEN** the contribution is complete and green
- **THEN** it remains unreleased until the existing tagged-release process
  validates and publishes the integrated commit

### Requirement: Confined owner links without policy duplication

The contribution guide MUST use confined relative links to the existing
governance and publishing owners. Both destinations SHALL resolve inside the
repository. The guide MUST NOT copy the protected-gates registry, release
workflow command, or owner section as a parallel policy.

#### Scenario: Contributor consults an owner policy

- **WHEN** the contribution guide routes a protected-gate or release question
- **THEN** its relative link resolves to the existing owner and the guide does
  not embed a parallel registry or release procedure

### Requirement: Deterministic contribution validation

Repository governance validation MUST fail when the contribution contract or its
owner links are missing or semantically inverted. The validator MUST check only
deterministic documentation and workflow boundaries and MUST NOT score
subjective prose, comment, test, or legal quality.

#### Scenario: Contribution contract omits a protected workflow rule

- **WHEN** a required deterministic rule is absent or inverted
- **THEN** repository governance validation fails with a stable contribution
  contract finding
