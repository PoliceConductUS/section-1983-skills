# Drafting-Skill Evaluation Implementation Plan

**Goal:** Add deterministic and repeated fresh-context regression evaluations
for the public drafting skills.

**Architecture:** A standard-library Python package loads checked-in synthetic
fixtures, grades stable deterministic contracts, invokes externally configured
candidate and judge commands in isolated processes, aggregates variance, and
compares reviewed baselines. GitHub Actions publishes the same Markdown report
used locally.

## Task 1: Establish RED Loader and Grader Tests

Create `evaluations/tests/test_fixtures.py` and
`evaluations/tests/test_deterministic.py`. Test path escape, missing synthetic
flag, duplicate identifiers, missing JSON fields, ordered headings, banned
patterns, missing citations, unknown citations, multi-finding output, and
read-only candidate handling. Run the tests and record the expected import or
assertion failures before implementation.

## Task 2: Establish RED Runner and Reporting Tests

Create `evaluations/tests/test_judgment.py` and
`evaluations/tests/test_reporting.py`. Use temporary fake commands to prove each
run has a distinct working directory and process, strict rubric coverage,
minimum repetitions, pass rates, Bernoulli variance, baseline regression
findings, JSON and Markdown parity, and nonzero regression exit status. Run the
tests RED before implementation.

## Task 3: Implement the Minimal Package

Create focused modules under `evaluations/` for models and fixture loading,
deterministic grading, configured process execution, aggregation, comparison,
reporting, and the CLI. Use descriptive names and no code comments. Run the
focused tests after each minimal behavior group reaches GREEN.

## Task 4: Add Permanent Synthetic Fixtures

Add three fixture directories for unavailable checker configuration, hard-
finding edit-loop behavior, and stale results. Each contains a prompt, bounded
sources, passing candidate, regression candidate, manifest, and judgment rubric.
Run the corpus command and prove each known regression produces its declared
stable finding identifiers.

## Task 5: Add Repository and PR Gates

Extend `npm run test:unit` with evaluation tests and add an evaluation corpus
script used by `npm run validate`. Add a pull-request workflow that writes
Markdown to `GITHUB_STEP_SUMMARY`, retains JSON in the workspace, and fails when
the corpus or reviewed baseline regresses. Do not add a provider SDK or secrets.

## Task 6: Verify, Review, and Archive

Run the complete repository suite, each runtime skill validator, OpenSpec
validation, `git diff --check` from the Issue #1 parent head, and
forbidden-folder checks. Obtain a task review and a fresh full-diff review.
Produce verification and retrospective artifacts, archive on the Issue #6
branch, and run `git town sync` after every commit.
