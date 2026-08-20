## ADDED Requirements

### Requirement: Synthetic fixture corpus

The evaluation system SHALL load only fixtures explicitly marked synthetic and
SHALL confine every prompt, source, candidate, and regression-example path to
its fixture directory. Each fixture MUST have a stable identifier, target skill,
bounded source manifest, deterministic contract, judgment rubric, passing
candidate, and at least one permanent regression example.

#### Scenario: Fixture contains private or unbounded input

- **WHEN** a fixture is not marked synthetic or references a path outside its
  directory
- **THEN** corpus validation fails before any candidate or judge command runs

#### Scenario: Demonstrated failure is added to the corpus

- **WHEN** an observed drafting or auditing failure is converted into a fixture
- **THEN** the fixture records a synthetic reproduction and the stable findings
  that its permanent regression example must trigger

### Requirement: Deterministic grading

The system SHALL grade required contract fields, ordered output headings, banned
terms or patterns, required citation identifiers, and unknown citation
identifiers. Findings MUST have stable identifiers, MUST identify the applicable
fixture and location or field when available, and MUST NOT modify candidate
output.

#### Scenario: Candidate violates multiple deterministic gates

- **WHEN** a candidate omits a required field, uses a banned term, or cites an
  identifier absent from the bounded source manifest
- **THEN** the result reports every applicable stable finding and fails the
  deterministic gate

#### Scenario: Permanent regression example is evaluated

- **WHEN** the corpus gate grades a checked-in regression example
- **THEN** the observed finding identifiers must equal or include its declared
  expected findings or the corpus gate fails

### Requirement: Independent judgment runs

The system SHALL invoke a configured judgment command in a new process and new
empty working directory for every run. It MUST NOT reuse conversation or
provider session identifiers. Judgment output MUST address every stable rubric
criterion and MUST retain each run's reason.

#### Scenario: Judgment evaluation is configured

- **WHEN** an operator requests judgment evaluation with a configured command
- **THEN** every fixture and repetition starts an independent process with only
  that run's complete request

#### Scenario: Judgment command is unavailable

- **WHEN** no judgment command is configured or it cannot execute
- **THEN** the report marks judgment evaluation unavailable and does not
  substitute deterministic grading or describe judgment behavior as passing

### Requirement: Repeated-run variance

Judgment evaluation MUST require at least three runs and SHALL report per-
criterion pass count, pass rate, Bernoulli variance, and instability together
with the raw run decisions.

#### Scenario: Judgment decisions disagree

- **WHEN** a criterion passes in some runs and fails in others
- **THEN** the report marks that criterion unstable and exposes its nonzero
  variance rather than reporting only a majority result

### Requirement: Baseline regression gate

The system SHALL compare current deterministic and configured judgment results
with a reviewed baseline without modifying that baseline. It MUST emit stable
regression findings and a nonzero exit status when a declared minimum regresses.

#### Scenario: Current result falls below baseline

- **WHEN** a fixture's current pass count or criterion pass rate is below its
  reviewed minimum
- **THEN** the report identifies the fixture, metric, expected minimum, and
  current value and the regression command fails

### Requirement: Pull-request reporting

Pull requests SHALL run unit tests, fixture validation, deterministic grading,
permanent regression examples, and baseline comparison. The workflow MUST write
a human-readable report to the pull-request job summary and MUST fail on a
deterministic or baseline regression.

#### Scenario: Pull request has no configured live judgment command

- **WHEN** the pull-request environment cannot supply candidate or judgment
  commands
- **THEN** the report still covers deterministic corpus regressions and clearly
  identifies live judgment evaluation as unavailable

#### Scenario: Pull request introduces a regression

- **WHEN** any required deterministic gate, permanent regression expectation, or
  reviewed baseline minimum fails
- **THEN** the workflow reports the regression before release and exits nonzero
