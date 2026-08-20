# Design: Section 1983 Declarations and Evidence

## Context

Issue #9 requires a declaration-and-evidence skill for Section 1983 plaintiffs
preparing summary-judgment materials. Rule 56(c)(4) requires a supporting or
opposing declaration to be made on personal knowledge, set out facts that would
be admissible in evidence, and show that the declarant is competent to testify
on the matters stated. Section 1746 permits a written, dated, subscribed
declaration under penalty of perjury and supplies different language depending
on whether execution occurs within or without the United States.

The repository already routes summary-judgment responses and audits completed
filings. It does not own statement-level declaration classification,
exhibit-foundation prompts, or human execution approval.

## Goals

- Add one independently installable public skill.
- Make the source and knowledge basis of every proposed proposition visible.
- Prevent record content, analysis, inference, legal conclusion, or discovery
  expectation from masquerading as firsthand testimony.
- Preserve the two statutory execution forms and human signature boundary.
- Prompt for missing exhibit foundation without inventing or certifying it.
- Make explicit human declarant approval of every retained statement observable.

## Non-goals

- A universal evidence, hearsay, best-evidence, or admissibility engine.
- An expert, custodian, business-record certification, affidavit, deposition, or
  Rule 56(d) drafting system.
- Signing, dating, executing, notarizing, filing, or certifying a declaration.
- Replacing local-rule, authority, filing-review, or Filing CI gates.

## Decisions

### One self-contained peer package

The public package contains only `SKILL.md` and `agents/openai.yaml`. Its
contract is short enough to remain standalone. Existing README and umbrella
routes compose it with summary-judgment work.

### Statement classification precedes drafting

Every proposition receives a stable statement ID and one classification:
firsthand fact, attributed record fact, derived analysis, inference, legal
conclusion, or discovery expectation. The classification ledger records exact
text, declarant knowledge and competency bases, approved source and exhibit IDs,
disposition, gap, and approval status.

Attributed record facts remain descriptions of what an identified record states
or shows. Reading a record does not convert its content into firsthand knowledge
of the event. Derived analysis, inference, legal conclusions, and discovery
expectations remain outside the factual declaration in this first contract.

### One material proposition per approval unit

Each numbered paragraph contains one material proposition. Every included
paragraph begins pending. The human declarant may approve, revise, or omit it.
Silence is not approval, and a revision resets the affected paragraph to
pending. Execution readiness remains blocked until the human declarant approves
every retained exact paragraph.

### Execution location selects the statutory form

The skill uses the supplied actual place of execution, not residence, venue, or
custody location. Domestic execution uses the statutory domestic phrase.
Execution without the United States adds
`under the laws of the United States of America`. Unknown location blocks form
selection. Date and signature remain blank for the human.

### Foundation is prompted, not certified

The exhibit map records the exhibit ID and description, statement links, how the
declarant recognizes it, the supplied creation, receipt, observation, or
maintenance relationship, applicable accuracy or completeness basis, and any
missing facts. The skill asks focused questions for missing foundation and never
declares an exhibit authentic or admissible.

## Risks and mitigations

- **Generic personal-knowledge recital hides unsupported paragraphs** → require
  a statement-specific perception and competency basis.
- **Record review launders another person's assertion into firsthand fact** →
  preserve attribution and the declarant's limited relationship.
- **Wrong § 1746 form is selected** → require actual execution location and fail
  closed when it is absent.
- **Minor edits bypass approval** → approval applies to exact retained text and
  changed text returns to pending.
- **Preparation is mistaken for an admissibility ruling** → prohibit claims of
  truth, authentication, admissibility, execution, filing, or filing readiness.

## Migration plan

Add the peer skill, public routes, structural tests, and synthetic fixtures. No
existing artifact or dependency migrates. Archive the change on the Issue #9
branch after fresh behavior and repository verification pass.

## Open questions

None. Expert, custodian, business-record, Rule 56(d), and general admissibility
work remain outside this issue unless separately approved.
