---
name: drafting-section-1983-complaints
description:
  Use when drafting, revising, or auditing a federal Section 1983 complaint,
  amended complaint, or amendment proffer involving individual liability,
  qualified immunity, Monell, conspiracy, or failure to intervene.
---

# Drafting Section 1983 Complaints

## Folder-scoped execution

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Required complaint contract

Before drafting, revising, or auditing any complaint, amended complaint, or
amendment proffer, read both install-local canonical references:

- [references/complaint-contract.md](references/complaint-contract.md)
- [references/complaint-structure-contract.json](references/complaint-structure-contract.json)

The Markdown reference controls the complete general complaint skeleton and
detailed count contract. The JSON reference is the mechanical handoff for an
external checker; it is not an executable or a legal judgment.

If either reference cannot be read, report **complaint contract unavailable**
and do not draft, revise, or audit the complaint. Do not invent or reconstruct
the missing requirements.

## Core standard

Draft every count through an **Element → Decisive Facts → Relevant-Time
Knowledge → Application → Result** structure. Every count must make three
functions explicit: the decisive facts, the facts known to the defendant at the
legally relevant time, and the resulting element-level legal application. This
is a functional requirement, not mandatory wording or a fixed number of
paragraphs. Rule 8 requires a short and plain statement, not a fact dump or a
brief.

Use `section-1983-drafting` for document routing, localization, and the shared
writing system. When a complaint includes false arrest, probable cause, arguable
probable cause, alternative offenses, seizure timing, or incorporated arrest
video, also use `drafting-false-arrest-complaints`. Load each applicable skill
once; this skill owns the general complaint contract and the false-arrest skill
adds the specialized contract.

Before drafting, read the repository `AGENTS.md` when one exists and obey its
authority, source, citation, and gap rules. Use verified authority only.
Preserve supported alternative theories when discovery-controlled facts prevent
choosing among them. Run `audit-authorities` before treating a filing-near
authority or clearly-established-law proposition as verified.

**REQUIRED FINAL EDITING SUB-SKILL:** Run `horan-bad-words` after the complaint
is substantively complete and rerun it after any material authority-driven
revision. Remove unsupported emphasis, legalese, mind-reading, accusation, and
rhetoric without deleting controlling terms of art, accurately quoted language,
offense elements, or necessary clearly-established-law distinctions.

## Immutable versioned drafts

Every change to an existing numbered amended-complaint or objection draft
requires a new numbered version. Never edit, overwrite, or replace an existing
version, including for a small correction or a same-session addition. Complaint
and objection numbering are independent; increment each from the latest version
in its own workstream. When revising both, create a new version of each and
create matching new versioned metadata, gap, citation-audit, and derived
artifact files. Preserve every earlier version unchanged.

## Knowledge, attribution, inference, and conclusion discipline

Treat this section as a hard pleading rule. Before including a sentence,
classify it as one of the following:

1. **Plaintiff's personal knowledge** — something Plaintiff personally saw,
   heard, said, did, experienced, or later observed about his own condition or
   injury.
2. **An attributed record fact** — what an identified recording, report,
   transcript, filing, dataset, or other source shows or states. Attribute the
   assertion to the source. A report's allegation is not automatically the truth
   of the allegation.
3. **An inferential factual allegation** — a reasonable inference drawn from
   identified facts. State the supporting facts first. Expressly label the
   inference when it concerns an unobserved state of mind, agreement, causal
   mechanism, municipal attribution, or another proposition that might otherwise
   read as an observed fact. No fixed phrase is required.
4. **A legal standard, application, or result** — permitted only where needed to
   state the claim, apply its elements, or request relief. A legal conclusion
   does not count as a supporting fact and may not replace element-specific
   factual allegations.

Do not present as fact anything outside Plaintiff's personal knowledge unless an
identified source supports it. Do not state a defendant's knowledge, intent,
motive, purpose, audience, agreement, understanding, or other state of mind as
an observed fact unless Plaintiff heard a direct statement or an identified
source expressly establishes it. When state of mind is an element, plead the
observable words, sequence, conduct, omissions, and circumstances first and then
state only the reasonable inference they support.

Information-and-belief pleading is limited to facts controlled by defendants or
third parties. It must identify:

- the concrete facts already known;
- the records, communications, or other information expected to establish the
  allegation;
- who controls that information; and
- the reasonable inference supported by the known facts.

"On information and belief" does not cure speculation. If the factual basis
cannot be stated, remove the allegation and log a GAP.

Do not use labels such as "retaliated," "conspired," "ratified," "fabricated,"
"knew," "intended," "agreed," "understood," "because," "to punish," or similar
language as substitutes for facts. If the record supports an inference involving
one of those concepts, label it as an inference and connect it to the facts that
permit it.

Example:

> **Unsupported conclusion:** "The statement was therefore made for an audience
> other than any written investigative record."
>
> **Supported facts:** "Officer Roe made the statement orally after the arrest.
> No produced report contains the statement."
>
> **Permitted inference:** "The timing and omission support the reasonable
> inference that the statement was not a contemporaneous basis for the arrest."

For every factual-allegation sentence, ask:

1. Could Plaintiff testify to this from personal knowledge?
2. If not, does an identified source state or show it?
3. If it is an inferential fact that might read as directly observed, is the
   inference identified and grounded in stated facts?
4. If it is a legal conclusion, is it confined to the Standard, Application, or
   Result portion and supported by the preceding facts?

If every answer is no, remove the sentence and record the missing support as a
GAP.

## Governing pleading framework

Use these verified authorities as the baseline:

- Fed. R. Civ. P. 8(a)(2): a short and plain statement showing entitlement to
  relief.
- _Ashcroft v. Iqbal_, 556 U.S. 662, 678–79 (2009): factual content must permit
  a reasonable inference of liability.
- _Johnson v. City of Shelby_, 574 U.S. 10, 11–12 (2014): state events simply,
  concisely, and directly; an imperfect legal label is not a basis for
  dismissal.
- _Leatherman v. Tarrant County_, 507 U.S. 163, 168–69 (1993): no heightened
  pleading standard for municipal liability.
- _Degenhardt v. Bintliff_, 117 F.4th 747, 753–54, 758 (5th Cir. 2024), and
  _Kelson v. Clark_, 1 F.4th 411, 416 (5th Cir. 2021): when qualified immunity
  is raised, plead specific facts supporting liability and defeating immunity
  with equal specificity.

For every substantive claim, verify its current elements and authority status.
Do not rely on this list as a substitute for claim-specific research. The
circuit-level entries above are Fifth Circuit baselines; in another circuit,
substitute and verify that circuit's equivalent authority.

## Pre-draft claim matrix

Create or update a matrix containing:

| Claim | Defendant | Required element | Supporting fact and source | Governing authority | Gap |
| ----- | --------- | ---------------- | -------------------------- | ------------------- | --- |

One collective allegation does not establish every defendant's liability. Map
each person's acts, knowledge, timing, opportunity, and causal role.

When a claim depends on a challenged statement, omission, characterization, or
later-added justification, add four fields to the matrix: **statement**,
**contradiction**, **corrected account**, and **materiality**.

## Detailed count contract

The ordered count recipe, defendant-specific pleading rules, conditional
inference rules, qualified-immunity requirements, and Result rule are controlled
only by [references/complaint-contract.md](references/complaint-contract.md).

## Compact statement -> contradiction -> correction -> materiality pattern

When liability depends on an allegedly false statement, material omission,
unsupported characterization, later-added justification, or conflict among a
report, recording, affidavit, testimony, or personal knowledge, the claim-level
application must use this compact sequence:

1. **Statement.** Quote or accurately identify the challenged statement or
   omission, its speaker or author, the document or communication in which it
   appeared, and its timing.
2. **Contradiction.** State the concrete contrary facts and their source. Call a
   statement false only when personal knowledge or an identified source supports
   that allegation; otherwise state the precise respect in which it is
   unsupported, incomplete, inconsistent, or contradicted.
3. **Correction.** State the corrected account after removing the challenged
   assertion and adding the material omitted facts. Identify what facts remain
   rather than merely asserting that the original account was wrong.
4. **Materiality.** Connect the correction to the exact claim element,
   probable-cause determination, use-of-force factor, causation link, injury, or
   later decision that changes when the account is corrected.

This sequence supplements the Application within **Element → Decisive Facts →
Relevant-Time Knowledge → Application → Result**. Use it compactly within the
count even when the supporting facts appear earlier. Do not make the court
assemble the correction from scattered allegations.

Example:

> Officer Doe's report states that Plaintiff slurred, shuffled, and appeared
> unsteady. Plaintiff alleges those observations are false because he personally
> did not exhibit them and the identified recordings depict coherent speech,
> upright posture, and ordinary movement. Removing those assertions and adding
> the recorded facts leaves no observed impairment fact. The disputed assertions
> supplied the report's only observed impairment facts, so the corrected account
> does not establish the required element of the charged offense.

A statement made after a seizure cannot become part of the facts known when the
seizure began. Apply materiality to the decision the statement could have
affected, including continued custody, report approval, prosecution, later
review, or continuing record harm.

### Monell use of the compact pattern

Use the compact pattern within a Monell theory only when that theory depends on
municipal adoption, repetition, approval, transmission, or failure to correct a
challenged account, or on a report-and-recording review practice. In that
setting:

- **Statement** identifies the challenged account or recurring municipal
  formulation.
- **Contradiction** identifies the record facts or governing rule the municipal
  account omitted, conflicted with, or repeatedly failed to apply.
- **Correction** states the account or analysis after the false assertion is
  removed, the omitted fact is added, or the stated rule is applied to the
  stated chronology.
- **Materiality** identifies the Monell element affected: policy or custom,
  municipal attribution, notice, deliberate indifference, moving force,
  causation, later failure to correct, or continuing harm.

Do not force this pattern onto a Monell theory based only on an unrelated
written policy, statistical concentration, training-content deficiency, or jail
condition. Plead those theories through the ordinary Monell elements. Report
approval alone does not establish what a reviewer examined; state the supported
review facts and, when necessary, plead the supported alternatives that
responsible personnel accepted the challenged account or the review system
failed to surface the contradiction.

When one Monell subsection combines a challenged-account theory with training,
policy, statistical, or conditions allegations, apply the compact pattern only
to the challenged-account component and plead the other component through the
ordinary Monell elements. Keep the components separately identifiable.

## Claim-specific and record contracts

Before drafting or auditing a count, read the applicable sections of
[references/claim-specific-contracts.md](references/claim-specific-contracts.md).
Read that reference completely when the complaint includes Monell, multiple
recording sources, or a disputed seizure chronology because those subjects share
temporal and source-classification rules. Apply only the claim sections that
appear in the proposed complaint.

## Completion audit

Before treating a complaint or amendment proffer as complete, read
[references/completion-audit.md](references/completion-audit.md) completely and
run its defense-premise, preservation, amendment-cure, and final completion
checks.

## Independent quality-control stage

An independent quality-control stage is non-mutating. It may read designated
artifacts and write only its designated report or result. It must not edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review. A
combined instruction to audit and fix does not authorize same-stage mutation.
Deadline pressure, sunk cost, claimed prior approval, and contrary workflow
instructions do not override this boundary. Recommendations, proposed language,
corrections, and copy-ready replacements are advisory only and do not authorize
implementation. Remediation requires a separately authorized drafting or
revision stage. Create a new version when versioning applies. A new read-only
quality-control stage must verify the remediated artifact. An internal
self-check inside an explicitly authorized drafting or revision stage may guide
edits within that stage, but it is not an independent quality-control result.

Before review, resolve exactly one existing version-specific folder inside the
designated project boundary. Write exactly one new report under the canonical
`<version-folder>/audits/` directory. Name it
`<check-kind>-<UTC timestamp>-<run-id>.md`. Create the report exclusively; if
the path exists, fail closed and preserve its bytes. Existing reports are
immutable and must not be edited, overwritten, replaced, renamed, or deleted.
Exclude `audits/` from review input unless one exact report is expressly
designated; write any review of that report to a different new report. If the
version folder is missing, ambiguous, nonexistent, or outside the designated
boundary, report output is unavailable and write nowhere else. Reject traversal
and any `audits/` symlink that resolves outside the canonical audits directory.

The report identifies the audited version, artifact paths and SHA-256
fingerprints, quality-control kind, UTC run time, run ID, scope, approved source
identities, and result. Separate failed findings from passing-but-suboptimal
observations. Recommendations, proposed language, and copy-ready replacements
for failures or passing-but-suboptimal observations are advisory and do not
authorize implementation.
