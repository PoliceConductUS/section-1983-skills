# Design

## Context

`studying-rule-59e-decisions` already owns the canonical corpus, denominator,
retrieval-gap, authorship, transfer-card, and validation contracts.
`drafting-for-judge-scholer` already demonstrates degradation when qualifying
corpus support is absent. Issue 19 connects those existing seams without
creating another format or judge-specific product.

## Decisions

### Root guide and local routes

Add `JUDGE_OVERLAYS.md` at repository root and one README route. All repository
links in the guide are relative, resolve within the checkout, and point to
existing files. Fenced examples cannot satisfy link discovery.

### Reuse the canonical corpus contract

The guide requires the published corpus to use the existing decision-corpus and
transfer-card schemas and pass `validate_corpus.py`. It explains the source
hierarchy, research and coding stages, denominator/missingness limits, and the
strength ladder: example, documented cluster, tendency. No parallel schema or
validator is introduced.

### Separate research, transfer, and drafting

The research stage exports neutral transfer cards with source identity, checked
dates, evidence level, denominator, missingness, permitted use, and prohibited
inference. The drafting skill consumes only those cards and retains their
limits. The overlay cannot add a conclusion that is absent from the card, select
strategy, or replace governing authority.

### Fail closed and prevent gaming

The guide prohibits manipulating or predicting judicial assignment, exploiting
supposed preferences, tailoring facts or law toward a predicted result,
concealing adverse authority, distorting the record, personalizing attacks, and
renaming another judge's conclusions. A thin or incomplete corpus contributes no
judge-specific proposition beyond verified examples at their actual strength.

### Source court conduct independently

The conduct checklist covers official rules, individual procedures, standing
orders, candor, civility, ex parte limits, filing limits, and other express
court restrictions. Each court-specific warning identifies a stable source ID,
official provenance, issuing body, jurisdiction or judge, checked date, and
bounded warning. Missing or stale support remains a gap. Conduct constraints are
compliance inputs, never personality signals or optimization targets.

### Worked examples

Use a fictional court and judge for one valid overlay and one thin-corpus
degradation result. Discuss the Scholer overlay only as an existing structural
example: it distinguishes authorship, preserves the evidence ladder, and adds
nothing when qualifying support is absent. Do not repeat or generalize its
substantive conclusions.

## Risks

- **Keyword-only tests can accept inverted rules.** Add bounded affirmative
  patterns and direct semantic mutations for the protected boundaries.
- **A Markdown decoy can hide an external or traversal route.** Parse operative
  links outside fenced examples and resolve every repository target.
- **Method prose can become live court research.** Use only fictional conduct
  records and state the required official-source procedure.
