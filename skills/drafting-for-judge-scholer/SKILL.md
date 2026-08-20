---
name: drafting-for-judge-scholer
description:
  Drafts and audits federal civil-rights pleadings and briefs for matters
  assigned to Judge Karen Gren Scholer using an evidence-coded Section 1983
  decision corpus. Use when preparing a complaint, Rule 12 response,
  qualified-immunity argument, Monell theory, objection, summary-judgment paper,
  or judge-specific strategy for Judge Scholer.
---

# Drafting for Judge Scholer

## Role in the skill stack

Use this skill as a judge-specific overlay after the applicable document and
claim skills. For a false-arrest complaint, load `section-1983-drafting`,
`drafting-section-1983-complaints`, `drafting-false-arrest-complaints`, and then
this skill. This skill adds only issue-specific Judge Scholer observations that
the available reviewed corpus supports. It does not replace governing authority,
the complaint contract, or the authority-verification gate.

When the coded corpus contains no independently reasoned Judge Scholer decision
on the issue, say that the corpus adds no judge-specific information for that
issue. Apply only this skill's generic drafting discipline. Do not convert an
adoption order, outcome-only entry, incomplete retrieval set, or decision by
another judicial officer into a Scholer tendency.

**REQUIRED FINAL EDITING SUB-SKILL:** Run `horan-bad-words` after the
judge-specific and authority audits and rerun it after any material revision.
Remove unsupported emphasis, legalese, mind-reading, accusation, and rhetoric
without deleting controlling terms of art, accurately quoted language, or
necessary clearly-established-law distinctions.

## Quick start

1. Locate and follow the case strategy file: `strategy.md`, or the
   highest-numbered `strategy-v*.md`, in the case or workstream folder; ask the
   user for it if missing. Propose any needed departure as a new strategy
   version and proceed only per the user's decision — never deviate silently,
   and never edit a strategy version in place.
2. Read [REFERENCE.md](REFERENCE.md).
3. For each issue, determine whether the available corpus supports a documented
   example, a tendency, or no judge-specific conclusion. If it supports none,
   use no judge-specific proposition for that issue.
4. Identify the document, posture, challenged claims, requested ruling, and
   record materials the court may consider.
5. Apply the repository authority and factual-source gates. Research cases are
   not citeable merely because they appear in the corpus.
6. Draft in this order: governing rule → actor-specific facts →
   element-by-element application → requested ruling.
7. Ground every point in record facts, permitted inferences, and verified
   authority so the court has justification and reason to agree; persuasive or
   rhetorical argument is a small part of the document, if present at all.

## Evidence hierarchy

Use corpus signals in this order:

1. Scholer's independently reasoned memorandum opinions.
2. Scholer's independent orders with substantive reasoning.
3. Scholer orders adopting a magistrate recommendation, clearly labeled as
   adoption evidence.
4. Judgments and docket-only entries for outcomes, never for unobserved
   reasoning.

Never attribute a magistrate judge's wording to Scholer merely because she
adopted the recommendation.

## Required drafting workflow

### Rule 12

- Tie each element to concrete pleaded facts: actor, act or omission, time,
  knowledge, injury, and causal link.
- Separate facts in the complaint from facts asserted only in briefing.
- Address incorporated documents, video, and judicially noticeable records
  accurately.
- Answer every dispositive argument with authority; flag an unanswered premise
  before drafting around it.

### Qualified immunity

- State both prongs.
- Describe the challenged conduct at the correct level of specificity.
- Build a fact-to-fact comparison to binding clearly-established-law cases.
- Use unpublished decisions only for their proper non-binding or illustrative
  role.
- For force, divide the encounter into phases and state when threat, flight, or
  resistance changed.

### Monell

For each separate theory, state:

1. the identified policy/custom/final-decision/training/ratification path;
2. concrete supporting facts;
3. the precise municipal inference;
4. final-policymaker attribution and notice/deliberate indifference;
5. the particular constitutional injury; and
6. the direct moving-force mechanism.

Do not combine alternative theories into an omnibus Monell paragraph. Do not
treat violated regulations as a municipal policy that caused injury unless the
alleged causal policy is independently identified.

### Amendment

- If dismissal is possible, request leave expressly.
- Identify the curable defect and the facts that can cure it.
- Explain why amendment is not futile.
- Warn when an earlier Scholer ruling already identified the same defect;
  repeated conclusory repleading increases prejudice risk.

## Final audit

- Distinguish holding, alternative holding, dicta, and non-binding authority.
- Verify every authority, quotation, and pinpoint.
- Cite every factual assertion to a record source.
- Remove labels unsupported by factual mechanisms.
- Confirm every point rests on cited record facts, expressly permitted
  inferences, or verified authority; cut or rewrite any sentence that cannot be
  traced to one.
- Confirm the draft follows the case strategy file and its prescribed audits
  ran.
- End each argument with the precise ruling requested.
- State corpus-derived observations as tendencies or documented examples, never
  predictions.
- For each issue lacking qualifying corpus support, confirm that the overlay
  added no judge-specific proposition.
- Run `audit-authorities` before treating any judge-specific or
  clearly-established-law proposition as filing-ready.
- Run `horan-bad-words` after the last substantive or authority revision.
