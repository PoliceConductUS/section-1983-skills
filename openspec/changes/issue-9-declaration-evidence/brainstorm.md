# Brainstorm: Section 1983 Declarations and Evidence

## Scope

Add one public skill for a Section 1983 plaintiff preparing a factual human
declaration and exhibit-foundation materials for summary judgment. The skill
classifies every proposition before drafting, uses the applicable 28 U.S.C. §
1746 execution form, and requires explicit human declarant approval of every
retained statement before execution.

## Approaches considered

### One declaration-and-evidence skill

One self-contained peer owns statement classification, declaration drafting,
execution language, exhibit-foundation prompts, and the approval gate.

**Selected.** These responsibilities operate on the same proposed statements and
exhibits. One public contract keeps their handoffs observable without a
coordinator or machine protocol.

### Separate declaration and exhibit skills

This would test drafting and foundation independently, but it would duplicate
the statement-to-exhibit map and create a new handoff for one compact outcome.

**Rejected.** The issue asks for one declaration-and-evidence contract, and no
separate lifecycle justifies another public package.

### A general summary-judgment evidence system

This could cover all admissibility objections, experts, custodians, Rule 56(d),
and local appendix practice.

**Rejected.** It exceeds the issue and risks certifying admissibility without a
fact-specific authority and foundation record.

## Agreed public contract

Create `drafting-section-1983-declarations-and-evidence` with only `SKILL.md`
and `agents/openai.yaml`. Route it from README, `section-1983-drafting`, and the
existing summary-judgment response reference.

Every proposed proposition receives a stable statement ID and exactly one
classification: firsthand fact, attributed record fact, derived analysis,
inference, legal conclusion, or discovery expectation. The last four do not
become firsthand testimony. Attributed record content stays attributed and
requires an actual declarant relationship or remains a gap.

Use one material proposition per numbered declaration paragraph. For each
retained paragraph, record the exact text, personal-knowledge basis, competency
basis, approved source IDs, exhibit IDs, and human declarant approval status. A
generic opening recital does not cure a missing statement-specific basis.

The domestic and foreign § 1746 forms remain distinct. Select one only from the
actual supplied execution location. If location is missing, keep execution
blocked. Leave the date and signature to the human declarant.

For every proposed exhibit, record how the declarant recognizes it and any
supplied creation, receipt, observation, maintenance, accuracy, or completeness
basis. Missing foundation produces a focused prompt, never an invented fact or
authentication conclusion.

Each retained statement begins pending. Silence is not approval. The skill may
prepare an unsigned draft but cannot call it ready for execution until the human
declarant expressly approves the exact text of every retained statement. A
changed statement requires new approval. The skill never signs, dates, executes,
files, or certifies truth, authentication, admissibility, or filing readiness.

## Boundaries

- Rule 56(d) discovery-showing declarations remain with the existing summary-
  judgment workflow. Expected discovery is reported as a gap and never laundered
  into personal knowledge.
- Derived analysis remains separately labeled and outside factual declaration
  paragraphs in this first contract.
- Expert, custodian, business-record certification, and universal evidence-
  objection work are not added.
- `audit-authorities` retains authority verification;
  `adversarial-filing-review` retains independent completed-filing review; and
  `filing-ci` does not certify knowledge, truth, execution, authentication, or
  admissibility.

## Test seams

- Structural tests cover the public package, metadata, routes, statutory forms,
  statement classification, knowledge and competency, exhibit prompts, and the
  human declarant approval gate.
- Five synthetic fixtures isolate discovery expectation as knowledge, derived
  analysis retained in a declaration, attributed-record content as firsthand
  knowledge, unsupported exhibit foundation, and execution before approval. The
  execution fixture also rejects location inference and post-approval edits that
  bypass renewed approval.
- Fixture tests require the exact intended finding and prove an unrelated rule
  cannot satisfy the permanent regression.
- Fresh bounded scenarios cover both execution locations, mixed proposition
  classes, a missing foundation, and one unresolved approval.
