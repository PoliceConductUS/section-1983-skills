# Issue #17 implementation plan

## Goal

Complete the first installed Filing CI reference-checker story by verifying the
existing ordinary-folder milestone and enforcing canonical domain-YAML dates.

## Steps

1. Correct the live issue, publish this design on a stacked branch, and open a
   draft PR based on Issue #94's branch.
2. Add a focused RED regression proving a compact parseable date currently
   bypasses canonical source-documentation validation.
3. Move the canonical date comparison into the date validator without changing
   roles, output behavior, check semantics, or result classes.
4. Run the installed-checker, folder-native host, folder-contract, output, and
   governance suites plus full repository validation.
5. Perform whole-story review, archive OpenSpec, verify exact remote checks, and
   mark the PR ready while leaving PR and Issue #17 open.
