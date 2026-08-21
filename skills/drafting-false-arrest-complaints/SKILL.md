---
name: drafting-false-arrest-complaints
description:
  Use when drafting, revising, or auditing a federal false-arrest complaint or
  amended complaint, especially when probable cause, alternative offenses,
  arrest timing, qualified immunity, incorporated video, or access to discovery
  is disputed.
---

# Drafting False-Arrest Complaints

## Core principle

Organize the pleading around the probable-cause decision: **who seized the
plaintiff, when, for which suspected offense, based on what contemporaneous
facts, and which required element those facts did not support.** Prefer decisive
factual precision over length.

**REQUIRED SKILL ORDER:** Load `section-1983-drafting`, then
`drafting-section-1983-complaints`, then this skill. This skill owns the
false-arrest specialization. The other skills own document routing, writing
rules, and the general complaint contract. Load each once; do not recurse
between them.

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
- Read [references/complaint-contract.md](references/complaint-contract.md) when
  drafting, revising, outlining, or auditing a complaint.

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
4. **Draft the common spine.** Use parties and capacities; jurisdiction and
   venue; the stage-by-stage facts contract in
   `references/complaint-contract.md`; separate defendant-specific counts;
   damages, relief, and jury demand. In each factual paragraph, keep one stage
   and one material event or closely connected set of circumstances; name the
   actor, what that actor knew then, and what that actor did.
5. **Draft each count through the required contract.** Use Element → Decisive
   Facts → Relevant-Time Knowledge → Application → Result. State the decisive
   facts, the facts known to each defendant at the seizure or other legally
   relevant time, and the resulting element-level legal application. Treat this
   as a functional requirement, not mandatory wording. Use an expressly labeled
   inference only when a non-obvious inferential bridge would otherwise be
   unclear. For every individual-capacity claim, establish the right at the
   required factual specificity and explain, **in the filed complaint text**,
   how verified, binding, pre-event authority gave that defendant fair warning.
   This concise fair-warning unit is non-waivable: no case-specific strategy,
   control, routing, or "clearly-established goes in the brief only" instruction
   removes it from the complaint (see `drafting-section-1983-complaints` →
   "Complaint-level clearly-established law is mandatory and non-waivable"). A
   brief may add authority discussion; it never substitutes for the complaint's
   unit. A count against a defendant who cannot assert qualified immunity (e.g.,
   a municipality on a Monell count) is exempt. Use only relevant incorporated
   paragraphs.
6. **Prune and compress.** Preserve more decisive facts, not more narrative.
   Remove redundant law, evidentiary appendices, discovery wish lists,
   unsupported labels, immaterial background, omnibus allegations, and claims
   missing a required element or actor-specific causal chain. Move research
   methods, full authority comparisons, and source annotations to internal work
   product when filing rules do not require them.
7. **Audit against the defense’s actual premises.** Answer probable cause and
   arguable probable cause, alternative offenses, timing, personal
   participation, video characterization, clearly established law, intermediary
   doctrines, and Monell attribution as applicable. Log unsupported propositions
   as GAPs.
8. **Edit without erasing required law.** Apply the shared writing system and
   `horan-bad-words`. Preserve controlling terms of art, offense elements,
   materially necessary distinctions, and the concise fair-warning analysis even
   when a mechanical linter flags their words.

## Required audit output

Produce these sections when auditing rather than drafting:

If no external comparator is invoked, mark the corpus qualification ledger not
applicable and classify only the target pleading and controlling rulings. Do not
invent a comparison.

| Section                                | Required content                                                                                                                                                           |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Corpus qualification ledger            | Complaint version, ruling, claim, defendant, procedural category, affirmative discovery proof, permitted use, limitation                                                   |
| Complaint spine                        | Missing, misplaced, or overgrown sections                                                                                                                                  |
| Arrest-decision matrix                 | Defendant, seizure point, offense, element, contemporaneous fact, negating fact, later-only fact, probable-cause and arguable-probable-cause issue, gap                    |
| Event-stage contamination audit        | Later facts being used to explain or justify an earlier decision                                                                                                           |
| Participation and causation audit      | Who decided, communicated, joined, restrained, reported, approved, or arrived later                                                                                        |
| Incorporated-material risk audit       | What each video, report, affidavit, or attachment resolves, obscures, disputes, or risks                                                                                   |
| Count audit                            | Element → decisive facts → relevant-time knowledge → application → result; non-obvious inference and qualified immunity where applicable                                   |
| Clearly-established-law matrix         | Claim, defendant, event date, precise right or rule, binding pre-event authority and status, materially similar facts, material differences, fair-warning explanation, gap |
| Corpus-alignment and compression audit | Decisive facts missing; material to keep, move, combine, or omit                                                                                                           |
| Gaps                                   | Missing fact, source, authority, identity, duration, or causal link                                                                                                        |

## Completion rule

Do not conclude that the complaint follows the corpus-derived pattern unless a
judge can find the seizure point, decisive facts, each defendant's arrest-time
knowledge, the resulting offense-element application, each defendant’s
participation, the factual basis for every non-obvious inference, and the
claim-by-claim fair-warning explanation without reconstructing the theory from
scattered allegations. Fail the audit if the complaint uses a later event to
justify an earlier decision, uses a collective actor label where roles differ,
states an unsupported motive or credibility label as fact, or incorporates
material without auditing its whole defense-favorable effect.

**Fail the audit** if any individual-capacity count against a
qualified-immunity-eligible defendant lacks its concise fair-warning unit in the
complaint text, or if that unit was omitted, thinned, or routed to a brief,
control memo, or internal matrix on the strength of a case-specific strategy or
routing instruction. The brief supplying the analysis for some counts does not
cure the complaint. Do not mark such a complaint filing-ready; identify the
defective counts and advise restoring the unit in a later authorized drafting
stage or log a filing-critical GAP for strategy decision.

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
