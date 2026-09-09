# Verification

## Scope

- Branch: `codex/monell-proposition-classes`
- Base: verified `origin/main` at `4ddaf5196cb9029223faa204368515b8fee07e5b`
- Worktree: `.worktrees/monell-proposition-classes`
- OpenSpec change archived on this owning branch before publication.
- No CaseGraph dependency or case-repository change was added.

## Contract result

- Planning owns a three-class proposition record for source-documented facts,
  supported inferences, and expected-discovery propositions.
- Source-documented facts and supported inferences require attribution and
  temporal limits. Supported inferences also identify their pleaded factual
  premises.
- Expected-discovery propositions remain in the discovery plan and cannot be
  treated as present facts or evidence.
- A supporting brief may explain an inference already grounded in pleaded facts
  but cannot supply a missing complaint-level factual premise.
- The approved planning handoff and typed complaint delta preserve proposition
  identity, classification, placement, and class-specific support.
- The install-local complaint-handoff validator rejects missing, duplicate,
  malformed, misclassified, misplaced, and unresolved proposition records.
- Planning requires a complete staged-development record for every supported but
  incomplete path, including request-specific relevance, restrictions, dates,
  diligence, deadline, evidence threshold, reassessment triggers, and
  limitations or relation-back risk.
- Discovery and amendment remain conditional. After the scheduling-order
  deadline, Rule 16 good cause precedes Rule 15; amendment requires developed
  support and litigation-principal approval.
- Drafting bars boilerplate, incident-only, and expected-discovery placeholders.
  Shared assertion validation checks that predictions have not become existing
  Monell facts or a substitute for complaint-level support.

## TDD and behavioral evidence

- The initial focused RED had two failures for the absent planning and drafting
  proposition contracts.
- Corrective RED tests exposed the missing structured proposition collection,
  class-specific bases and placement, unresolved inference premises, malformed
  scalar fields, invalid reference arrays, and the former uncaught `TypeError`.
- Five fresh baseline agents used the unchanged public skill. Two placed
  unavailable expected-discovery content in complaint text; three stayed within
  the intended boundary.
- Five fresh guided agents used the revised public skill. All five kept expected
  discovery in the discovery plan and refused to let a brief cure missing
  complaint facts.
- The permanent behavioral fixture has one passing candidate and seven isolated
  regressions. Each regression triggers only its intended deterministic rule,
  including paraphrased unsupported-policy and brief-cure variants.
- Five staged-development baseline runs reliably preserved incomplete paths but
  omitted one or more required discovery, diligence, deadline, threshold, risk,
  or amendment fields.
- Five successful guided runs supplied the complete staged record. One initial
  guided run improperly derived a date from an unsupported relative interval; a
  focused RED and fresh replacement run corrected that gap.
- The staged-development fixture uses a field-complete structured passing record
  and fourteen isolated regressions covering placeholder pleading, generic
  relevance, restrictions, the date triad, diligence, deadline resolution,
  evidence threshold, reassessment, limitations risk, Rule 16 sequencing,
  principal approval, and prediction-as-fact.
- Structured fixture rules require nonempty typed values, exact mandatory gate
  values, complete records for every keyed discovery request, and equality
  between each collection key and its stable request ID.

## Independent review

Review first found that proposition records were not structurally carried
through the path, handoff, and delta. It then found malformed-value crash paths
and under-discriminating behavioral regressions. Staged-strategy review found an
incomplete passing fixture, inadequate regression enforcement, and stale
OpenSpec lifecycle statements. Final re-review exposed incomplete multi-request
validation, invented fixture relevance, key-order and request-identity bypasses,
generic regression relevance, and permissive reassessment values. Each accepted
finding received a focused failing test or lifecycle correction. The final
independent review reported no remaining Critical or Important findings and
marked the change ready to merge.

## Commands

- `python3 -m unittest evaluations.tests.test_deterministic evaluations.tests.test_fixtures evaluations.tests.test_monell_contract_v2 evaluations.tests.test_monell_claim_skills evaluations.tests.test_post_draft_assertion_validation`
  — 74 passed after the strengthened structured fixture and final review
  corrections.
- `npm exec -- openspec validate 2026-09-09-monell-proposition-classification --strict`
  — passed.
- `npm run validate` — passed on the final reviewed bytes: formatting; 27
  drafting-script tests; 734 evaluation tests; 32 discovered skills; 42 OpenSpec
  items; corpus evaluation; governance validation.
- `git diff --check` — passed.

## Delivery state

The completed OpenSpec change is archived. After the user explicitly authorized
publication, implementation commit `b8ed434` was pushed to
`origin/codex/monell-proposition-classes`. Creating a GitHub issue or PR was not
requested.
