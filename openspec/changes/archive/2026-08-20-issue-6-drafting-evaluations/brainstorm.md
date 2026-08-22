# Drafting-Skill Regression Evaluations

## Outcome

Add a repository-owned evaluation harness and synthetic corpus that can detect
whether public drafting-skill changes preserve or regress required behavior.

## Approved Seams

The repository owns fixture contracts, deterministic grading, fresh-process
orchestration, variance aggregation, baseline comparison, and pull-request
reporting. It does not own an LLM provider or embed credentials. Candidate and
judgment agents enter through configured commands that exchange JSON over
standard input and output.

## Options Considered

### Provider-specific evaluation SDK

This would simplify one model integration but add a runtime dependency,
credentials, network assumptions, and provider coupling. It does not fit a
public skills repository.

### Markdown-only example corpus

Examples would be easy to review but could not enforce stable grader findings,
fresh process isolation, repeated runs, variance, or machine-readable PR gates.

### Standard-library harness with configured agent commands

This keeps deterministic behavior reproducible, lets local and CI environments
select their own candidate and judge agents, and makes unavailable judgment runs
visible rather than silently substituting a heuristic. This is the selected
design.

## Fixture Shape

Each fixture is explicitly synthetic and contains:

- a stable fixture identifier and target skill;
- a prompt and bounded source set;
- deterministic requirements for contract fields, ordered headings, banned
  terms, and citation identifiers;
- a judgment rubric with stable criterion identifiers;
- a known passing candidate; and
- permanent regression examples with expected finding identifiers.

No fixture may contain private case material. Paths resolve inside the fixture
directory, and citation identifiers must resolve to its source manifest.

## Execution Model

Every candidate or judgment run starts a new process in a new empty temporary
working directory. The harness sends one complete request on standard input and
accepts one documented response on standard output. It never reuses a
conversation or provider session identifier.

Judgment evaluation requires at least three independent runs. Reports include
per-criterion pass rate, Bernoulli variance, and instability rather than hiding
disagreement behind a single majority result.

## Pull-Request Behavior

Pull requests always run fixture validation, deterministic graders, permanent
regression examples, and harness tests. The workflow writes the Markdown report
to the job summary and fails on a deterministic or baseline regression.

Configured live candidate and judgment commands may add repeated judgment
results. If they are unavailable, the report must say so and must not describe
judgment behavior as evaluated.

## Boundaries

- No private case data.
- No model credentials or provider SDK.
- No invented candidate or judge command.
- No `docs/` or `.superpowers/` directory.
- No silent baseline update.
