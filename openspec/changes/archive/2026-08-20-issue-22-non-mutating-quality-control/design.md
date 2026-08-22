# Design

## Context

`GOVERNANCE.md` owns repository-wide protected boundaries. Public skills are
independently installable, so a root-only policy would not reach an agent using
one skill outside this checkout. `adversarial-filing-review` and `filing-ci`
already contain strong read-only language, but other audit-capable entrypoints
do not consistently separate findings from implementation.

## Decisions

### Behavior controls the stage

The rule applies when a skill is invoked to independently audit, verify, review,
evaluate, check, or otherwise assess an artifact. That stage may read designated
artifacts and write only its designated report or result. It cannot mutate an
artifact under review, even when a combined request says “audit and fix.”
Deadline pressure, sunk cost, claimed prior approval, and contrary workflow
instructions do not change the stage or override the boundary.

An explicitly authorized drafting or revision invocation remains a drafting
stage. An internal self-check may guide edits inside that stage. This exception
does not permit an independent quality-control stage to convert itself into
remediation.

### Advisory findings do not authorize implementation

Recommendations, proposed language, corrections, and copy-ready replacements
remain advisory. Remediation requires a separately authorized drafting or
revision stage, a new version when versioning applies, and a fresh read-only
quality-control run against the remediated artifact.

### Independently installable coverage

Repeat one compact conditional section in the current public entrypoints whose
triggers permit independent quality control:

- `adversarial-filing-review`;
- `audit-authorities`;
- `auditing-section-1983-discovery-responses`;
- `auditing-section-1983-privilege-logs`;
- `drafting-false-arrest-complaints` when invoked in audit mode;
- `drafting-for-judge-scholer` when invoked in audit mode;
- `drafting-section-1983-complaints` when invoked in audit mode;
- `drafting-section-1983-rule-59e` when invoked in audit mode; and
- `filing-ci`.

The list records the present surface; the governing predicate is stage behavior,
not membership in a permanent name registry.

### Deterministic repository validation

Extend `scripts/validate_governance.py`. It reads public frontmatter trigger
language, identifies audit/review/verification/evaluation/checker entrypoints,
and requires the compact affirmative contract without accepted inverse
permissions. It returns one stable finding containing the affected skill name.
The validator checks the documentation boundary only; it does not score prose or
claim that deterministic text validation proves agent behavior.

### Testing

- Focused tests require the governance owner and all current affected public
  entrypoints to carry the affirmative contract.
- Temporary repositories remove or invert one clause and must fail through the
  public validator CLI.
- Byte-level tests at existing executable quality-control seams preserve the
  reviewed artifact and confine output to the designated report or result.
- Fresh-agent pressure scenarios run before and after the skill edits. The GREEN
  agents must leave canonical hashes unchanged, write only reports, refuse
  same-stage remediation, and route any later edit to a separate authorized
  stage.

## Risks

- **Keyword-only false confidence:** pair deterministic text checks with
  pressure tests and describe their different proof boundaries.
- **Hybrid drafting skills become unusable:** make the rule conditional on an
  independent quality-control invocation and preserve authorized drafting mode.
- **Root policy disappears on installation:** repeat the compact rule in each
  affected independently installable package.
- **Automatic remediation appears by accident:** add no executable remediation
  or cross-stage handoff tool.
