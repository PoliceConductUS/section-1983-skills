# Verification

## Branch and scope

- Branch: `codex/issue-25-complaint-candor-pruning`
- Parent: `codex/issue-24-unified-complaint-contract`
- Pre-archive reviewed HEAD: `964b1ad517d9aadfe25e7c191568771a4b9bbff3`
- Origin parity before archive: local and origin both at
  `964b1ad517d9aadfe25e7c191568771a4b9bbff3`
- Commits: design `7a4e791`, RED `15eadf3`, GREEN `1c99f6e`, review and
  canonical-interface correction `964b1ad`
- No executable checker, dependency, workflow, root `docs/`, or `.superpowers/`
  directory was added.

## Contract result

- Filed complaint text distinguishes factual candor from an adverse assessment
  of its own legal merits.
- Each distinct complaint-level fair-warning proposition ordinarily uses one
  verified lead authority; every additional complaint-level authority must have
  a separately identified job.
- The completion audit removes or internalizes uncertain factual paragraphs that
  perform no element, actual-defense, material-chronology, or
  candor/preservation function.
- The false-arrest specialization completes an actually raised alternative-
  offense analysis without treating an unresolved fact as admitted.
- One canonical claim–defendant–challenged-act checklist owns the universal and
  conditional qualified-immunity field names.
- Missing universal fields make the mapping incomplete. Missing or unverified
  conditional qualified-immunity fields create an internal filing-critical GAP,
  block filing-ready status, and route a reserved strategy decision without
  placing an adverse merits assessment in filed text.
- The JSON mechanical handoff matches the human tuple cardinality and field
  identifiers. Capacity remains a required field. Detailed authority
  verification remains owned by `audit-authorities`.

## TDD and mutation evidence

- Initial focused RED: 10 tests, four intended failures for the four missing
  behavioral contracts.
- Corrective RED: 23 tests with five intended failures for the missing canonical
  checklist, authority-owner boundary, two inline `unless` loopholes, and a
  valid causal-first alternative-offense false positive.
- Interface RED: 36 tests with one intended failure for the stale JSON tuple
  cardinality; a separate mutation rejected collapse of universal and
  qualified-immunity failure classes.
- Final mutation review rejects inline strategy exceptions to universal
  incompleteness, qualified-immunity GAP creation, and the no-adverse-filed-
  assessment rule, plus a second qualified-immunity completion checklist.
- Final focused result: 40 tests passed.

## Independent review

The whole-story review exposed and drove corrections for fixture false greens,
inline `unless` exceptions, a valid Z2-first causal formulation, human/JSON
interface drift, collapsed failure classes, and duplicate checklist ownership.
The final review reported zero Critical and zero Important findings and
confirmed that all exact probes are rejected without duplicating the
authority-audit procedure.

## Commands

- `python3 -m unittest evaluations.tests.test_complaint_contract_composition evaluations.tests.test_complaint_candor_contract -q`
  — 40 passed.
- `python3 -m py_compile evaluations/tests/test_complaint_candor_contract.py` —
  passed.
- `npm run validate` — passed before archive: formatting; 16 drafting tests; 275
  evaluation tests; 20 discovered skills; 17 OpenSpec items; corpus evaluation;
  governance.
- `openspec validate issue-25-complaint-candor-pruning --strict` — passed.
- `git diff --check` — passed.

## Remote state

Commit `964b1ad` was pushed with `git town sync`. No PR was created and Issue 25
was not closed.

## Archive verification

OpenSpec archived the change as `2026-08-22-issue-25-complaint-candor-pruning`.
The existing durable capability purpose was preserved; this archive generated no
TBD purpose. The preexisting count-cardinality requirement was reconciled with
the canonical claim–defendant–challenged-act interface, while capacity remains a
required field.

After archive, the focused composition and candor suites passed 40 tests and
`npm run validate` passed formatting, 16 drafting tests, 275 evaluation tests,
20 discovered skills, 16 durable OpenSpec specifications, corpus evaluation, and
governance. `git diff --check` also passed.
