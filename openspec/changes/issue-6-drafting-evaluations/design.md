# Design: Drafting-Skill Regression Evaluations

## Components

### Corpus loader

The loader discovers fixture directories, validates manifest fields, confines
referenced files to the fixture directory, requires `synthetic: true`, resolves
every citation identifier against `sources.json`, and rejects duplicate fixture,
source, finding, or rubric identifiers.

### Deterministic grader

The grader accepts Markdown or JSON candidate output. It emits stable findings
for:

- missing dot-addressed JSON contract fields;
- missing or out-of-order Markdown headings;
- configured banned terms or regular expressions;
- missing required citation identifiers; and
- unknown citation identifiers not present in the fixture source set.

The result includes fixture id, pass state, findings, and counts. Grading never
edits candidate output.

### Fresh-process runner

Candidate and judge commands are argument arrays supplied through CLI
configuration. The harness invokes commands without a shell. Each invocation has
a new empty temporary working directory and receives a complete JSON request on
standard input. Standard output must satisfy the documented response contract.

Candidate responses contain `output`. Judgment responses contain the fixture id,
run id, and one decision per rubric criterion. Missing, duplicate, or unknown
criteria fail that run.

### Judgment aggregation

At least three runs are required. For each criterion the report records passes,
run count, pass rate, Bernoulli variance `p * (1 - p)`, and whether outcomes are
unstable. The aggregate retains each raw reason for review.

### Regression comparison

The committed baseline records minimum deterministic pass counts and optional
minimum judgment pass rates. The comparator emits stable regression findings; it
never updates the baseline. Permanent regression examples must fail for their
declared finding identifiers, proving the corpus still detects the original
failure.

### Reporting

One command writes the same result as JSON and Markdown. The Markdown form shows
fixture status, deterministic findings, judgment availability, pass-rate
variance, and baseline regressions. Exit status is nonzero for invalid fixtures,
unexpected permanent-example results, deterministic candidate failures, or
baseline regressions.

## Initial Corpus

The first fixtures encode synthetic versions of demonstrated or recurring
failure classes:

1. Filing CI unavailable configuration must fail closed without an invented
   command.
2. A hard filing finding must not trigger a same-response draft edit or inferred
   replacement text.
3. A stale Filing CI result must not support filing readiness after a material
   draft change.

Each fixture includes a source manifest, a passing output, at least one
regression output, deterministic rules, and judgment criteria.

## CI

The existing validation workflow runs unit tests and the corpus gate. A focused
pull-request workflow writes the evaluation Markdown to `GITHUB_STEP_SUMMARY`.
Configured live commands can be supplied by the execution environment; their
absence is explicit in the report and cannot be confused with a judgment pass.

## Comment Policy

Implementation names and types carry the contract. Code comments are avoided;
any non-obvious durable decision belongs in this design or a later ADR.
