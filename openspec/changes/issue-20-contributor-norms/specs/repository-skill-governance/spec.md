# repository-skill-governance Specification

## ADDED Requirements

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
