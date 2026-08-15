---
name: drafting-false-arrest-complaints
description: Use when drafting, revising, or auditing a federal false-arrest complaint or amended complaint, especially when probable cause, alternative offenses, arrest timing, qualified immunity, incorporated video, or access to discovery is disputed.
---

# Drafting False-Arrest Complaints

## Core principle

Organize the pleading around the probable-cause decision: **who seized the plaintiff, when, for which suspected offense, based on what contemporaneous facts, and which required element those facts did not support.** Prefer decisive factual precision over length.

**REQUIRED SKILL ORDER:** Load `section-1983-drafting`, then `drafting-section-1983-complaints`, then this skill. This skill owns the false-arrest specialization. The other skills own document routing, writing rules, and the general complaint contract. Load each once; do not recurse between them.

Before acting, read the current pleading, controlling motions and rulings, claim matrix, chronology, gaps, and the canonical sources material to each proposition. If the repository supplies `AGENTS.md`, a fact-lock protocol, versioning rules, or source gates, follow them. For filing-near authority, run `audit-authorities` and complete the identity, status, pre-event date, later-history, pinpoint, and rule-of-orderliness checks.

**REQUIRED FINAL EDITING SUB-SKILL:** Run `horan-bad-words` after the complaint is substantively complete and rerun it after any material authority-driven revision. Remove unsupported emphasis, legalese, mind-reading, accusation, and rhetoric without deleting controlling terms of art, accurately quoted language, offense elements, or necessary clearly-established-law distinctions.

## Load the right references

- Read [references/corpus-findings.md](references/corpus-findings.md) when comparing a pleading with complaints that obtained or were permitted discovery, discussing what “worked,” or citing corpus frequencies and examples.
- Read [references/complaint-contract.md](references/complaint-contract.md) when drafting, revising, outlining, or auditing a complaint.

## Workflow

1. **Classify the comparator outcome.** At the claim–defendant level, match the complaint version to the ruling that evaluated it. Record every applicable procedural category rather than forcing one label. A denial counts as pleading survival only when it decided sufficiency on the allegations. Summary judgment alone does not prove discovery. Discovery does not prove pleading sufficiency.
2. **Fix the seizure boundary.** Identify the earliest supported seizure point by exact time or the narrowest supported interval. State the show of authority or physical restraint, submission, decisionmaker, and joining actors. Do not substitute later touching, handcuffing, resistance, force, reporting, custody, or prosecution for an earlier supported seizure.
3. **Build the arrest-time matrices.** For each defendant, map action, knowledge, timing, causal role, and injury. For each stated or charged offense, and each alternative offense actually raised by the defense, a ruling, or controlling law, map every element against facts known at the seizure moment. Do not inventory merely conceivable offenses.
4. **Draft the common spine.** Use parties and capacities; jurisdiction and venue; the stage-by-stage facts contract in `references/complaint-contract.md`; separate defendant-specific counts; damages, relief, and jury demand. In each factual paragraph, keep one stage and one material event or closely connected set of circumstances; name the actor, what that actor knew then, and what that actor did.
5. **Draft each count through the required contract.** Use Element → Facts → Inference → Result. For every individual-capacity claim, establish the right at the required factual specificity and explain, **in the filed complaint text**, how verified, binding, pre-event authority gave that defendant fair warning. This concise fair-warning unit is non-waivable: no case-specific strategy, control, routing, or "clearly-established goes in the brief only" instruction removes it from the complaint (see `drafting-section-1983-complaints` → "Complaint-level clearly-established law is mandatory and non-waivable"). A brief may add authority discussion; it never substitutes for the complaint's unit. A count against a defendant who cannot assert qualified immunity (e.g., a municipality on a Monell count) is exempt. Use only relevant incorporated paragraphs.
6. **Prune and compress.** Preserve more decisive facts, not more narrative. Remove redundant law, evidentiary appendices, discovery wish lists, unsupported labels, immaterial background, omnibus allegations, and claims missing a required element or actor-specific causal chain. Move research methods, full authority comparisons, and source annotations to internal work product when filing rules do not require them.
7. **Audit against the defense’s actual premises.** Answer probable cause and arguable probable cause, alternative offenses, timing, personal participation, video characterization, clearly established law, intermediary doctrines, and Monell attribution as applicable. Log unsupported propositions as GAPs.
8. **Edit without erasing required law.** Apply the shared writing system and `horan-bad-words`. Preserve controlling terms of art, offense elements, materially necessary distinctions, and the concise fair-warning analysis even when a mechanical linter flags their words.

## Required audit output

Produce these sections when auditing rather than drafting:

If no external comparator is invoked, mark the corpus qualification ledger not applicable and classify only the target pleading and controlling rulings. Do not invent a comparison.

| Section                                | Required content                                                                                                                                                           |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Corpus qualification ledger            | Complaint version, ruling, claim, defendant, procedural category, affirmative discovery proof, permitted use, limitation                                                   |
| Complaint spine                        | Missing, misplaced, or overgrown sections                                                                                                                                  |
| Arrest-decision matrix                 | Defendant, seizure point, offense, element, contemporaneous fact, negating fact, later-only fact, probable-cause and arguable-probable-cause issue, gap                    |
| Event-stage contamination audit        | Later facts being used to explain or justify an earlier decision                                                                                                           |
| Participation and causation audit      | Who decided, communicated, joined, restrained, reported, approved, or arrived later                                                                                        |
| Incorporated-material risk audit       | What each video, report, affidavit, or attachment resolves, obscures, disputes, or risks                                                                                   |
| Count audit                            | Element → Facts → Inference → Result; qualified immunity where applicable                                                                                                  |
| Clearly-established-law matrix         | Claim, defendant, event date, precise right or rule, binding pre-event authority and status, materially similar facts, material differences, fair-warning explanation, gap |
| Corpus-alignment and compression audit | Decisive facts missing; material to keep, move, combine, or omit                                                                                                           |
| Gaps                                   | Missing fact, source, authority, identity, duration, or causal link                                                                                                        |

## Completion rule

Do not conclude that the complaint follows the corpus-derived pattern unless a judge can find the seizure point, arrest-time knowledge, offense-element gap, each defendant’s participation, the factual basis for every requested inference, and the claim-by-claim fair-warning explanation without reconstructing the theory from scattered allegations. Fail the audit if the complaint uses a later event to justify an earlier decision, uses a collective actor label where roles differ, states an unsupported motive or credibility label as fact, or incorporates material without auditing its whole defense-favorable effect.

**Fail the audit** if any individual-capacity count against a qualified-immunity-eligible defendant lacks its concise fair-warning unit in the complaint text, or if that unit was omitted, thinned, or routed to a brief, control memo, or internal matrix on the strength of a case-specific strategy or routing instruction. The brief supplying the analysis for some counts does not cure the complaint. Do not mark such a complaint filing-ready; identify the defective counts and either restore the unit or log a filing-critical GAP for strategy decision.
