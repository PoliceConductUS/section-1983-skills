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

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `filing` contains the filing selected for judge-overlay review.
- `judge-corpus` contains the approved evidence-coded decision corpus.
- `court-conduct` contains approved court-conduct observations and sources.

Target is required in `filing`. Internet is `disabled`. Return any judge-
specific receipt or bounded no-change result as a canonical output-relative path
and deterministic bytes; only the trusted host may publish it append-immutable.
Report unsupported, stale, incomplete, or unavailable overlay material as a gap
and make no judge-specific change.

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

1. Follow the strategy represented in the selected `filing` target and the
   user's request. If a required strategy position is unavailable, report the
   gap. Propose any departure and proceed only per the user's decision; never
   deviate silently.
2. Read [REFERENCE.md](REFERENCE.md).
3. For each issue, determine whether the available corpus supports a documented
   example, a tendency, or no judge-specific conclusion. If it supports none,
   use no judge-specific proposition for that issue.
4. Identify the document, posture, challenged claims, requested ruling, and
   record materials the court may consider.
5. Apply the authority and factual-source gates supplied in the declared input
   roles. Research cases are not citeable merely because they appear in the
   corpus.
6. Draft in this order: governing rule → actor-specific facts →
   element-by-element application → requested ruling.
7. Ground every point in record facts, permitted inferences, and verified
   authority so the court has justification and reason to agree; persuasive or
   rhetorical argument is a small part of the document, if present at all.
8. After the applicable document and claim skills compose the filing, select the
   required filing target inside the declared `filing` role root and use the
   declared `judge-corpus` and `court-conduct` role roots. The packaged
   processor returns immutable receipt bytes and one output-relative path; only
   the trusted host may publish them through `OutputRun`. If no qualifying
   support permits a specialized change, record
   `no judge-specific drafting change` and the bounded reason. The absence of
   judge-specific prose or a receipt does not prove this overlay ran.

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
- Route Judge Scholer-specific amendment observations through
  [REFERENCE.md](REFERENCE.md) and apply them only when its source gate is met.

## Final audit

- Distinguish holding, alternative holding, dicta, and non-binding authority.
- Verify every authority, quotation, and pinpoint.
- Cite every factual assertion to a record source.
- Remove labels unsupported by factual mechanisms.
- Confirm every point rests on cited record facts, expressly permitted
  inferences, or verified authority; cut or rewrite any sentence that cannot be
  traced to one.
- Confirm the draft follows the user-approved strategy represented in the
  selected filing and request, and that its prescribed audits ran.
- End each argument with the precise ruling requested.
- State corpus-derived observations as tendencies or documented examples, never
  predictions.
- For each issue lacking qualifying corpus support, confirm that the overlay
  added no judge-specific proposition.
- Run `audit-authorities` before treating any judge-specific or
  clearly-established-law proposition as filing-ready.
- Run `horan-bad-words` after the last substantive or authority revision.
- Return the immutable judge-overlay execution receipt plan only after the
  filing's judge-specific composition and anti-gaming checks are complete.

## Independent quality-control stage

An independent quality-control stage is non-mutating. It may read designated
artifacts and return only its designated report or result for trusted-host
publication. It must not edit, overwrite, correct, regenerate, or otherwise
modify an artifact under review. A combined instruction to audit and fix does
not authorize same-stage mutation. Deadline pressure, sunk cost, claimed prior
approval, and contrary workflow instructions do not override this boundary.
Recommendations, proposed language, corrections, and copy-ready replacements are
advisory only and do not authorize implementation. Remediation requires a
separately authorized drafting or revision stage. Create a new version when
versioning applies. A new read-only quality-control stage must verify the
remediated artifact. An internal self-check inside an explicitly authorized
drafting or revision stage may guide edits within that stage, but it is not an
independent quality-control result.

Before review, an independent quality-control stage must select exactly one
artifact through its declared input roles and target policy. It must propose
exactly one unique append-immutable output-relative report beneath the
caller-declared output folder. A missing, ambiguous, nonexistent, or out-of-role
target must fail closed without a fallback write. The report path must reject
absolute paths, traversal, symlink escapes, and existing destinations. Only the
trusted host may publish the report through the shared output boundary. The
trusted host accepts quality-control publication only from an invocation bound
to the installed skill's target policy and approved target roles; it rejects an
unbound invocation or a target outside those approved roles.

Prior quality-control reports must not become implicit input. A report may be
reviewed only when that exact report is expressly present in a declared input
role and selected consistently with the reviewing skill's target policy. The
reviewing stage must propose a different new append-immutable report for
trusted-host publication. Existing reports are immutable and must not be edited,
overwritten, replaced, renamed, or deleted.

The trusted host derives the report path as
`quality-control-reports/<check-kind>-<utc-run-time>-<run-id>.md` and publishes
exactly one report through the shared output writer. Generated reports beneath
`quality-control-reports/` are excluded from the reviewed-input manifest and
fingerprint unless one exact report is the explicit target; selecting one report
does not include sibling or older reports. The canonical quality-control
metadata envelope identifies a generated report even when the report directory
itself is a declared input root. A quality-control run ID must be a canonical
lowercase UUIDv4; weak, malformed, or reused identities fail closed before
publication.

The trusted host prefixes the report with the canonical quality-control metadata
envelope containing the skill and version, filtered logical input roles and
reviewed artifact hashes, selected target role, relative path, SHA-256
fingerprint, and byte size, quality-control kind, UTC run time, run ID, scope,
approved source identities, result, failed findings, passing-but-suboptimal
recommendations, and terminal run-manifest identity. The skill returns report
content and structured findings; it does not build the canonical metadata
envelope or publish output.

The quality-control run is complete only after both report bytes and the
terminal success manifest are durable and incomplete state is absent. Separate
failed findings from passing-but-suboptimal observations. Recommendations,
proposed language, and copy-ready replacements for failures or
passing-but-suboptimal observations are advisory and do not authorize
implementation.
