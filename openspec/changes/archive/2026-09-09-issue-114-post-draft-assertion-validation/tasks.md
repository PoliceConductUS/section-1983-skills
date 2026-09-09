## 1. Baseline and red tests

- [x] 1.1 Record the approved design, current skill ownership, and baseline
      validation evidence.
- [x] 1.2 Add failing contract tests for the shared skill, consumer routing,
      report fields, status separation, freshness, omission coverage, and
      deterministic-claim limits.
- [x] 1.3 Add failing behavioral fixtures for all eight Issue #114 acceptance
      scenarios, including the party-document source-independence rule.
- [x] 1.4 Run fresh-context baseline pressure checks and preserve the observed
      failures.

## 2. Shared validation owner

- [x] 2.1 Add the independently installable `validating-court-facing-assertions`
      package and folder contract.
- [x] 2.2 Define the read-only stage sequence, atomic assertion model,
      original-source checks, omission mapping, and specialist handoffs.
- [x] 2.3 Define report metadata, statuses, Mermaid summary, freshness and
      dependency invalidation, private-report boundary, and stopping criteria.
- [x] 2.4 Register and document the new public skill.

## 3. Existing-skill integration

- [x] 3.1 Update `section-1983-drafting` to orchestrate validation, separate
      correction, targeted revalidation, and final whole-document/render review.
- [x] 3.2 Route complaint and Rule 59(e) final candidates through the shared
      contract.
- [x] 3.3 Route integrated Monell text through the canonical complaint owner and
      shared contract.
- [x] 3.4 Make authority audit, adversarial review, and Filing CI contribute
      only their bounded responsibilities.
- [x] 3.5 Update repository governance to enforce one semantic owner without
      removing required install-local QC safeguards.
- [x] 3.6 Route declaration and multi-document Rule 59(e) outputs through one
      validation invocation per court-facing target, and preserve prior issue-
      register continuity.

## 4. Green verification and delivery

- [x] 4.1 Run focused contract and behavioral evaluations until all Issue #114
      scenarios pass.
- [x] 4.2 Run fresh-context post-change pressure checks and preserve results.
- [x] 4.3 Run formatting, complete repository validation, and an independent
      code review; correct any defects and rerun affected checks.
- [x] 4.4 Complete verification and retrospective artifacts, archive the
      OpenSpec change, push every commit, and mark the draft PR ready while
      leaving PR and issue open.
