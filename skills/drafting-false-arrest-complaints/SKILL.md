---
name: drafting-false-arrest-complaints
description:
  Use when drafting, revising, or auditing a federal false-arrest complaint or
  amended complaint, especially when probable cause, alternative offenses,
  arrest timing, qualified immunity, incorporated video, or access to discovery
  is disputed.
---

# Drafting False-Arrest Complaints

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Core principle

Organize the pleading around the probable-cause decision: **who seized the
plaintiff, when, for which suspected offense, based on what contemporaneous
facts, and which required element those facts did not support.** Prefer decisive
factual precision over length.

## Required skill order

Load section-1983-drafting, then drafting-section-1983-complaints, and then this
skill. Before applying this skill, require drafting-section-1983-complaints to
read both canonical general references:

- `references/complaint-contract.md`
- `references/complaint-structure-contract.json`

Then read this skill's local
[false-arrest complaint delta](references/false-arrest-complaint-delta.md). Load
each skill once; do not recurse between them.

If drafting-section-1983-complaints or either canonical general reference is
unavailable, report **complaint contract unavailable** and do not draft, revise,
or audit the complaint. Do not invent or reconstruct the missing requirements,
and do not promote this local delta into a replacement general contract.

Before acting, read the current pleading, controlling motions and rulings, claim
matrix, chronology, gaps, and the canonical sources material to each
proposition. If the repository supplies `AGENTS.md`, a fact-lock protocol,
versioning rules, or source gates, follow them. For filing-near authority, run
`audit-authorities` and complete the identity, status, pre-event date,
later-history, pinpoint, and rule-of-orderliness checks.

**REQUIRED FINAL EDITING SUB-SKILL:** Run `horan-bad-words` after the complaint
is substantively complete and rerun it after any material authority-driven
revision. Remove unsupported emphasis, legalese, mind-reading, accusation, and
rhetoric without deleting controlling terms of art, accurately quoted language,
offense elements, or necessary clearly-established-law distinctions.

## Load the right references

- Read [references/corpus-findings.md](references/corpus-findings.md) when
  comparing a pleading with complaints that obtained or were permitted
  discovery, discussing what “worked,” or citing corpus frequencies and
  examples.
- Read the local false-arrest complaint delta named above when drafting,
  revising, outlining, or auditing a false-arrest complaint.

## Workflow

1. **Classify the comparator outcome.** At the claim–defendant level, match the
   complaint version to the ruling that evaluated it. Record every applicable
   procedural category rather than forcing one label. A denial counts as
   pleading survival only when it decided sufficiency on the allegations.
   Summary judgment alone does not prove discovery. Discovery does not prove
   pleading sufficiency.
2. **Fix the seizure boundary.** Identify the earliest supported seizure point
   by exact time or the narrowest supported interval. State the show of
   authority or physical restraint, submission, decisionmaker, and joining
   actors. Do not substitute later touching, handcuffing, resistance, force,
   reporting, custody, or prosecution for an earlier supported seizure.
3. **Build the arrest-time matrices.** For each defendant, map action,
   knowledge, timing, causal role, and injury. For each stated or charged
   offense, and each alternative offense actually raised by the defense, a
   ruling, or controlling law, map every element against facts known at the
   seizure moment. Do not inventory merely conceivable offenses.
4. **Apply the false-arrest delta.** Use the canonical general complaint
   contract for the document and count structure. Add the local delta's
   stage-by-stage chronology, seizure boundary, offense matrix, actor matrix,
   warrant, incorporated-material, and compression requirements without
   restating the general contract.
5. **Draft the false-arrest application.** For each applicable canonical count
   mapping, connect the suspected offense and disputed element to the facts
   known by that defendant at the seizure or other legally relevant time. Apply
   the delta's offense → element → decisive facts → contemporaneous knowledge →
   probable-cause sequence. Address alternative or arguable probable cause only
   when made material by the defense, a controlling ruling, or governing law.
6. **Prune and compress.** Preserve more decisive facts, not more narrative.
   Remove redundant law, evidentiary appendices, discovery wish lists,
   unsupported labels, immaterial background, omnibus allegations, and claims
   missing a required element or actor-specific causal chain. Move research
   methods, full authority comparisons, and source annotations to internal work
   product when filing rules do not require them.
7. **Audit the false-arrest delta against the defense's actual premises.**
   Answer probable cause and arguable probable cause, alternative offenses,
   timing, personal participation, video characterization, warrant or
   intermediary doctrines, and incorporated-material risk as applicable. Route
   general qualified-immunity and Monell requirements through the canonical
   general contract. Log unsupported propositions as GAPs.
8. **Edit without erasing required law.** Apply the shared writing system and
   `horan-bad-words`. Preserve controlling terms of art, offense elements, and
   materially necessary false-arrest distinctions when a mechanical linter flags
   their words.

## Required audit output

Produce these false-arrest-delta sections when auditing rather than drafting.
Use the canonical general package's audit for the general complaint contract; do
not restate it here.

If no external comparator is invoked, mark the corpus qualification ledger not
applicable and classify only the target pleading and controlling rulings. Do not
invent a comparison.

| Section                                | Required content                                                                                                                                                          |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contract route                         | Canonical general package and both references available; local delta loaded after them                                                                                    |
| Corpus qualification ledger            | Complaint version, ruling, claim, defendant, procedural category, affirmative discovery proof, permitted use, limitation                                                  |
| Arrest-decision matrix                 | Defendant, seizure point, offense, element, contemporaneous fact, negating fact, later-only fact, probable-cause or arguable-probable-cause issue, GAP                    |
| Event-stage contamination audit        | Later facts being used to explain or justify an earlier decision                                                                                                          |
| Participation and causation audit      | Who decided, communicated, joined, restrained, reported, approved, or arrived later                                                                                       |
| Warrant and challenged-account audit   | Contributor, transmission, statement or omission, correction, materiality, intermediary issue, and causal role                                                            |
| Incorporated-material risk audit       | What each video, report, affidavit, or attachment resolves, obscures, disputes, or risks                                                                                  |
| False-arrest application audit         | Suspected offense, disputed element, seizure boundary, defendant's arrest-time knowledge, personal act, probable-cause application, alternative-offense issue when raised |
| Corpus-alignment and compression audit | Decisive false-arrest facts missing; material to keep, move, combine, or omit                                                                                             |
| GAPs                                   | Missing false-arrest fact, source, authority, identity, time, duration, offense element, or causal link                                                                   |

## Completion rule

Do not conclude that the false-arrest delta is satisfied unless a judge can find
the seizure point, decisive arrest-time facts, each defendant's contemporaneous
knowledge and participation, the resulting offense-element application, the
basis for every non-obvious inference, and the incorporated-material risks
without reconstructing the theory from scattered allegations.

Fail the false-arrest audit if the complaint uses a later event to justify an
earlier decision, uses a collective actor label where roles differ, states an
unsupported motive or credibility label as fact, inventories an unraised
alternative offense, or incorporates material without auditing its complete
defense-favorable effect.

The canonical general package alone controls general complaint completion,
including its qualified-immunity and Monell requirements. If that package or
either canonical reference cannot be verified, report **complaint contract
unavailable** and do not complete the false-arrest audit from this delta.

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
