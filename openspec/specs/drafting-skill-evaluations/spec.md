# drafting-skill-evaluations Specification

## Purpose

Define a synthetic, deterministic, and reviewable evaluation system for legal-
drafting skills, including isolated optional judgment runs, permanent regression
fixtures, reviewed baselines, safe reports, and pull-request enforcement.

## Requirements

### Requirement: Synthetic fixture corpus

The evaluation system SHALL load only fixtures explicitly marked synthetic and
SHALL confine every prompt, source, candidate, and regression-example path to
its fixture directory. Each fixture MUST have a stable identifier, target skill,
bounded source manifest, deterministic contract, judgment rubric, passing
candidate, and at least one permanent regression example.

The canonical corpus root MUST also contain the resolved directory of every
immediate fixture child; a symlinked fixture directory that resolves outside the
corpus is invalid.

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
output. Candidate text SHALL encode source identifiers only as
`[cite:<source-id>]`; ordinary Markdown bracket syntax MUST NOT be treated as a
citation.

#### Scenario: Candidate violates multiple deterministic gates

- **WHEN** a candidate omits a required field, uses a banned term, or cites an
  identifier absent from the bounded source manifest
- **THEN** the result reports every applicable stable finding and fails the
  deterministic gate

#### Scenario: Permanent regression example is evaluated

- **WHEN** the corpus gate grades a checked-in regression example
- **THEN** the observed finding identifiers must equal or include its declared
  expected findings or the corpus gate fails

#### Scenario: Candidate contains ordinary Markdown brackets

- **WHEN** candidate text contains a link label, checkbox, footnote, or image
  alt text without the explicit citation-token prefix
- **THEN** the grader does not report that bracketed text as an unknown citation

### Requirement: Independent judgment runs

The system SHALL invoke a configured judgment command in a new process and new
empty working directory for every run. It MUST NOT reuse conversation or
provider session identifiers. Judgment output MUST address every stable rubric
criterion and MUST retain each run's reason. Each candidate or judgment command
MUST have a finite, non-boolean positive timeout, defaulting to 60 seconds, and
inherited environment variables MUST exclude conversation, session, thread, and
stale working-directory state.

#### Scenario: Judgment evaluation is configured

- **WHEN** an operator requests judgment evaluation with a configured command
- **THEN** every fixture and repetition starts an independent process with only
  that run's complete request

#### Scenario: Judgment command is unavailable

- **WHEN** no judgment command is configured or it cannot execute
- **THEN** the report marks judgment evaluation unavailable and does not
  substitute deterministic grading or describe judgment behavior as passing

#### Scenario: Configured command fails or times out

- **WHEN** a candidate or judgment command is unavailable, times out, exits
  nonzero, or violates its response protocol
- **THEN** the system emits a stable failure class in bounded JSON and Markdown
  reports, exits nonzero when required, and does not expose more than 8,192
  captured characters per output stream without the stable marker `[truncated]`

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
Before any candidate or judgment command executes, the system MUST reject a
baseline whose root, fixture map, or fixture minimum is not an object; whose
deterministic minimum is not a nonnegative integer; whose judgment minimum is
not a finite number from zero through one; or whose fixture or rubric identifier
does not exist in the validated corpus. Booleans MUST NOT satisfy numeric
minimums.

#### Scenario: Current result falls below baseline

- **WHEN** a fixture's current pass count or criterion pass rate is below its
  reviewed minimum
- **THEN** the report identifies the fixture, metric, expected minimum, and
  current value and the regression command fails

#### Scenario: Required judgment baseline cannot be measured

- **WHEN** judgment execution is unavailable and a reviewed minimum judgment
  rate exists
- **THEN** the report emits `baseline-judgment-unavailable`, does not fabricate
  a current rate, and fails closed

### Requirement: Safe report destinations

Before any candidate or judgment command executes, the system MUST validate that
JSON and Markdown report paths are distinct, do not alias the baseline, do not
resolve inside the fixture corpus, and have valid parent destinations. A
rejected configuration MUST NOT change or add a corpus, baseline, or report
file. Each accepted report MUST be written through a temporary sibling and
atomically replace its own destination.

#### Scenario: Report path aliases protected input

- **WHEN** a report destination equals or resolves through a symlink to the
  baseline, corpus, or other report destination
- **THEN** configuration fails before any candidate or judgment process runs and
  every protected input remains byte-for-byte unchanged

#### Scenario: One report destination is predictably invalid

- **WHEN** either report destination cannot pass preflight validation
- **THEN** neither existing report is replaced

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

### Requirement: Actor-unit regression remains semantically reviewable

The synthetic corpus SHALL preserve a paired multi-officer complaint fixture.
The failing candidate MUST contain actor headings, omnibus incorporation or
paragraph ranges, and element and qualified-immunity conclusions without a
direct actor-specific factual bridge. The passing candidate MUST identify each
actor's own incorporated paragraphs and directly apply that actor's
contemporaneous facts to the disputed element, causal role, injury, and both QI
prongs while excluding later-only facts from the earlier knowledge set.

The fixture's independent rubric MUST separately evaluate actor-specific
incorporation, relevant-time fact-to-element application, later-fact limits,
causation and injury, and both QI prongs. Deterministic grading MAY preserve an
explicit demonstrated shortcut but MUST NOT claim to establish semantic closure,
legal sufficiency, or filing readiness.

#### Scenario: Regression uses headings and conclusions without a bridge

- **WHEN** the permanent regression candidate names each officer but directs the
  reader to a broad paragraph range before stating conclusions
- **THEN** the deterministic gate preserves its declared narrow shortcut finding
  and the independent rubric supplies the semantic criteria

#### Scenario: Passing candidate closes each officer unit

- **WHEN** every officer's unit supplies its own incorporated paragraphs,
  relevant-time facts, element application, causal role, injury, later-fact
  boundary, and both QI-prong applications
- **THEN** the candidate passes the deterministic fixture contract and is
  available for independent judgment without a claim of automatic legal
  sufficiency
