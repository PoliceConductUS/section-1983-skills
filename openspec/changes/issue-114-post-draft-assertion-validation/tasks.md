## 1. Baseline and red tests

- [ ] 1.1 Record the approved design, current skill ownership, and baseline
      validation evidence.
- [ ] 1.2 Add failing contract tests for the shared skill, consumer routing,
      report fields, status separation, freshness, omission coverage, and
      deterministic-claim limits.
- [ ] 1.3 Add failing behavioral fixtures for all seven Issue #114 acceptance
      scenarios.
- [ ] 1.4 Run fresh-context baseline pressure checks and preserve the observed
      failures.

## 2. Shared validation owner

- [ ] 2.1 Add the independently installable `validating-court-facing-assertions`
      package and folder contract.
- [ ] 2.2 Define the read-only stage sequence, atomic assertion model,
      original-source checks, omission mapping, and specialist handoffs.
- [ ] 2.3 Define report metadata, statuses, Mermaid summary, freshness and
      dependency invalidation, private-report boundary, and stopping criteria.
- [ ] 2.4 Register and document the new public skill.

## 3. Existing-skill integration

- [ ] 3.1 Update `section-1983-drafting` to orchestrate validation, separate
      correction, targeted revalidation, and final whole-document/render review.
- [ ] 3.2 Route complaint and Rule 59(e) final candidates through the shared
      contract.
- [ ] 3.3 Route integrated Monell text through the canonical complaint owner and
      shared contract.
- [ ] 3.4 Make authority audit, adversarial review, and Filing CI contribute
      only their bounded responsibilities.
- [ ] 3.5 Update repository governance to enforce one semantic owner without
      removing required install-local QC safeguards.

## 4. Green verification and delivery

- [ ] 4.1 Run focused contract and behavioral evaluations until all Issue #114
      scenarios pass.
- [ ] 4.2 Run fresh-context post-change pressure checks and preserve results.
- [ ] 4.3 Run formatting, complete repository validation, and an independent
      code review; correct any defects and rerun affected checks.
- [ ] 4.4 Complete verification and retrospective artifacts, archive the
      OpenSpec change, push every commit, and mark the draft PR ready while
      leaving PR and issue open.
