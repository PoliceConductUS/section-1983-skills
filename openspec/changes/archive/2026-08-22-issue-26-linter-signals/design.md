# Design

## Context

`draft_lint.py` counts thirteen mechanical prose signals and reports violations
per one hundred words. Its score delta is useful feedback, but a count does not
tell an editor where to look. The phrase remover also exempts controlling terms
without reporting that classification, and the drafting instructions state a
zero-banned-word target without requiring an exhaustive reconciliation.

## Goals / Non-Goals

**Goals:**

- Preserve the current aggregate output keys and score calculations.
- Give every emitted violation an artifact, paragraph number, and line range.
- Record detected controlling-term exemptions separately from violations.
- Surface bounded paragraph heuristics for dense long sentences and case
  citations.
- Make the human final reconciliation exhaustive and fail closed on unverified
  quotations.

**Non-Goals:**

- Legal sufficiency, merits, authority verification, or filing readiness.
- A generic citation parser or new dependency.
- Automatic proof that quoted text is accurate.
- Inert exemptions for phrases that do not trigger a current check.

## Decisions

### Preserve aggregates and add records

`lint(text, artifact="<memory>")` retains `words`, `violations`, `total`, and
`total_per_hundred_words`. It adds `findings`, `exemptions`, and `warnings`.
`lint_paths` passes each supplied path as the artifact; standard input uses
`<stdin>`.

A finding groups one check within one paragraph and records a stable finding ID,
check ID, artifact, one-based paragraph, one-based start and end lines, count,
excerpt, and `unexempted_violation` classification. Grouping by paragraph keeps
the report bounded while locating every counted hit. The sum of finding counts
for each check must equal the existing aggregate count.

An exemption record uses the same location fields, the exact matched phrase, and
`controlling_term_of_art`. Exemptions do not increase aggregate violations. The
linter does not classify a quotation as accurate. A residual finding inside
quoted material remains a violation until the drafting stage verifies the quote
against an approved source and records that disposition.

### Exact proven exemptions

Baseline probes show these phrases currently produce `more_word` hits:

- `active resistance`;
- `materially similar`; and
- `reasonably trustworthy`.

The suggested phrases `arguable probable cause`, `particularized right`,
`moving force`, and `probable cause` already produce no hit. They are not added
to the exemption inventory.

### Paragraph and location model

A paragraph is one or more consecutive nonblank lines. Blank lines separate
paragraphs. The parser retains one-based source line numbers. An all-blank
artifact has no paragraphs or findings. Findings from separate paths retain the
exact supplied path string so multi-file reports cannot lose artifact identity.

### Review-only density warnings

Two fixed synthetic-calibrated thresholds apply per paragraph:

- `long_sentence_density`: warn when at least two sentences exceed twenty-five
  words; and
- `case_citation_density`: warn when at least four reporter-form case citations
  appear.

Warnings record the artifact, paragraph and line range, observed count,
threshold, and `review_heuristic` classification. They are not included in
`violations`, `total`, or `total_per_hundred_words`, never change exit status,
and cannot establish legal insufficiency or filing unreadiness. Individual long
sentences remain part of the existing mechanical aggregate.

### Final reconciliation

The owning skill and writing system set the target as zero unexempted
violations, not zero raw matches. After editing, the drafter lists every
remaining location-bearing ID exactly once as:

1. `unexempted_violation`, which must be repaired before completion;
2. `accurate_quotation`, verified against its approved source; or
3. `controlling_term_of_art`, supported by the linter exemption record.

Warnings are listed separately as reviewed heuristics. Score deltas remain
feedback only and never become a merits verdict.

## Testing

- Focused unit tests prove the three current false positives RED before adding
  exemptions and prove the four inert suggestions remain absent.
- Location tests use multi-paragraph and multi-path artifacts and reconcile
  finding counts with aggregate counts.
- Calibration tests use `unbearably` and `almost immediately`, a compliant
  legal-analysis paragraph, two long sentences, and four reporter citations.
- Mutation tests reject off-by-one locations, warnings counted as violations,
  automatic accurate-quotation classification, missing residual classes, and
  score-delta language converted into a verdict.
- Full repository validation remains the final gate.

## Risks / Trade-offs

Paragraph-level grouping is less granular than character offsets but is stable
under ordinary editing and matches the requested review unit. The citation
signal deliberately recognizes only a bounded reporter form; it is a heuristic,
not a complete citation inventory. The quotation boundary remains human because
accuracy requires source comparison.
