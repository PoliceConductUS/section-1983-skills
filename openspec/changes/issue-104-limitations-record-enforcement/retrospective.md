# Retrospective

## What changed

Issue #104 replaced the ambiguous one-date limitations guidance with a
machine-readable, per-defendant record. The installed complaint checker and the
independently installed Filing CI checker now enforce the same schema boundary,
derive affected intended defendants, require one unique record per affected
individual, and keep missing or unresolved material filing-critical without
deciding legal sufficiency.

## What the TDD cycle exposed

- The Issue #102 guidance activated too narrowly: a role-only intended defendant
  before an expressed deadline warning did not trigger the gate.
- A single knowable-date field collapsed source availability, source possession,
  objective ascertainability, and actual identification.
- Guidance alone did not reliably separate the three diligence periods, notice,
  service, and Rule 4(m) relief.
- The first corrected implementation had two installed-seam drifts found during
  completion review: Filing CI did not require actual-identification source and
  method through its schema, and it did not reject duplicate intended-defendant
  or record IDs. Shared regression tests now protect both seams.

## Behavioral review

The user authorized exactly six isolated pressure agents. Three recorded the
Issue #102 baseline and three different agents ran the same prompts against the
corrected skill. Scores improved from 4/6, 3/5, and 5/7 to 6/6, 5/5, and 7/7.
The exact inputs and outputs are preserved in `verify.md`.

## Boundary retained

The schema and validators check only mechanical completeness. Fact truth,
authority fit, relation back, tolling, mistake, notice and service sufficiency,
strategy, requested relief, and filing readiness remain reserved for the agent,
independent audit, and user. No CaseGraph, repository, graph, package,
persistence, network, or ambient-filesystem dependency was introduced.
