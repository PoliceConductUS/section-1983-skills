# Design: Drafting-Skill Regression Evaluations

## Components

### Corpus loader

The loader discovers fixture directories, validates manifest fields, confines
referenced files to the fixture directory, requires `synthetic: true`, resolves
every citation identifier against `sources.json`, and rejects duplicate fixture,
source, finding, or rubric identifiers.

The canonical corpus root also confines each immediate fixture directory. A
fixture-directory symlink that resolves outside that root is invalid even when
its contents would otherwise satisfy the fixture contract.

### Deterministic grader

The grader accepts Markdown or JSON candidate output. It emits stable findings
for:

- missing dot-addressed JSON contract fields;
- missing or out-of-order Markdown headings;
- configured banned terms or regular expressions;
- missing required citation identifiers; and
- unknown citation identifiers not present in the fixture source set.

Candidate text identifies a bounded source only with the explicit token
`[cite:<source-id>]`. Ordinary Markdown links, checkboxes, footnotes, and image
alt text are not citation tokens.

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

Commands have a finite, non-boolean positive timeout that defaults to 60
seconds. Operators may set a different valid timeout. The runner does not
inherit environment variables whose normalized names contain `conversation`,
`session`, or `thread`, and it does not inherit `PWD` or `OLDPWD`.

Command failures use stable classes for unavailable execution, timeout, nonzero
exit, malformed JSON, and incomplete protocol output. Captured standard output
and error included in a report are truncated to 8,192 characters per stream with
the stable marker `[truncated]`.

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

Before any agent runs, baseline validation requires an object keyed by known
fixture identifiers. Deterministic minimums are nonnegative integers, judgment
maps reference known rubric identifiers, and judgment rates are finite numbers
from zero through one. Booleans are not numeric minimums.

### Reporting

One command writes the same result as JSON and Markdown. The Markdown form shows
fixture status, deterministic findings, judgment availability, pass-rate
variance, and baseline regressions. Exit status is nonzero for invalid fixtures,
unexpected permanent-example results, deterministic candidate failures, or
baseline regressions.

Before candidate or judgment execution, the CLI resolves and validates the
corpus, baseline, and both output destinations. Output paths must be distinct,
must not alias the baseline, and must not resolve inside the corpus. Both parent
directories must be valid output destinations before either report is replaced.
Each report is written to a temporary sibling and atomically replaces its own
destination. The command does not claim cross-filesystem atomicity across both
report files.

An unavailable configured candidate command fails with a stable report and skips
judgment. An unavailable judgment command remains explicitly unavailable; if a
reviewed judgment minimum exists, comparison emits
`baseline-judgment-unavailable` without inventing a current rate and fails
closed.

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
