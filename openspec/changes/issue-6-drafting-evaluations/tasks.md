## 1. RED Evaluation Contracts

- [x] 1.1 Add failing tests for fixture confinement, synthetic-only data,
      required contract fields, headings, banned patterns, and citation gates.
- [x] 1.2 Add failing tests for fresh-process judgment runs, strict rubric
      output, three-run minimums, and variance.
- [x] 1.3 Add failing command tests for permanent regression examples, baseline
      regressions, JSON output, Markdown output, and exit status.

## 2. Minimal Harness

- [x] 2.1 Implement the fixture loader and deterministic grader with no external
      Python dependency.
- [x] 2.2 Implement configured candidate and judge process execution with one
      empty temporary directory per run.
- [x] 2.3 Implement variance aggregation, baseline comparison, and stable
      reports.

## 3. Synthetic Corpus

- [x] 3.1 Add synthetic unavailable-checker, hard-finding edit-loop, and stale-
      result fixtures with bounded source sets.
- [x] 3.2 Add one passing candidate and at least one permanent regression
      example per fixture.
- [x] 3.3 Confirm no fixture contains private case data or a machine-specific
      repository path.

## 4. Pull-Request Gate

- [x] 4.1 Extend repository unit validation with the evaluation tests and corpus
      regression command.
- [x] 4.2 Add a pull-request evaluation workflow that writes the Markdown report
      to the job summary and preserves machine-readable output.
- [x] 4.3 Prove deterministic or baseline regressions return nonzero and visible
      judgment unavailability does not masquerade as a pass.

## 5. Verification

- [x] 5.1 Run the complete repository suite, all runtime skill validators,
      OpenSpec validation, full-range whitespace checks, and forbidden-folder
      checks.
- [ ] 5.2 Obtain fresh task and final reviews, resolve findings, and archive
      this change on the Issue #6 branch.
