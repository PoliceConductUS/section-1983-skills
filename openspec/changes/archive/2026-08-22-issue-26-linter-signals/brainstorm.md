# Brainstorm: Draft-linter signals

## Classification

This is a bounded extension of the existing `draft_lint.py` public interface. It
changes one established linter and its owning skill guidance without adding a
new dependency, executable subsystem, or legal-sufficiency gate.

## Approved direction

Preserve aggregate scores for before-and-after feedback. Add location-bearing
finding records, but do not convert warnings into legal or filing judgments.
Expose the three legal phrases proven to misfire as controlling terms of art; do
not add suggested phrases that already score zero. Add paragraph-level long-
sentence and citation-density warnings with documented fixed thresholds. Require
the drafting workflow to reconcile every residual hit as an unexempted
violation, verified accurate quotation, or controlling term of art.

## Rejected alternatives

- Replacing aggregate scores would break the useful delta workflow.
- Exempting all suggested phrases would add inert policy that no current check
  exercises.
- Automatically calling quoted text accurate would make a source-verification
  conclusion the linter cannot support.
- Making density warnings hard gates would turn a review heuristic into a false
  filing-readiness decision.
