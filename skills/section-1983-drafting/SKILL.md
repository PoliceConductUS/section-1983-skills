---
name: section-1983-drafting
description:
  Draft, revise, or edit litigation documents in civil rights cases under 42
  U.S.C. § 1983 in plain, forceful, slop-free prose. Use this skill whenever the
  user asks to write or edit any filing in a Section 1983 or federal civil
  rights case — a complaint or amended complaint, a response to a motion to
  dismiss or for summary judgment, a motion for extension of time or for leave
  to amend, objections to a magistrate judge's report and recommendation (R&R)
  or a response supporting one, a Monell claim, or any excessive force, false
  arrest, deliberate indifference, or First Amendment retaliation filing against
  police, jails, schools, or other state actors — even if they do not say "1983"
  and even for a single count, section, or paragraph. Also use it when the user
  asks what to file in response to a docket event or deadline, or asks to remove
  banned words, intensifiers, legalese, or "AI slop" from an existing filing.
  Also use it to route discovery requests, audits, conferences, privilege logs,
  or depositions.
---

# section-1983-drafting

## Folder-scoped execution

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

Draft litigation documents in Section 1983 cases that read like a dispassionate
factual record, not like advocacy theater and not like AI slop. The theory of
this skill: adjectives and adverbs tell; facts show. A judge reading "Officer
Doe struck the handcuffed plaintiff four times with a closed fist" needs no help
from "brutally." Understatement backed by specific facts is the most persuasive
register available, and it also satisfies Iqbal/Twombly, which discounts
conclusions and credits facts.

The skill is layered the way the law varies: an invariant writing system, a
uniform federal baseline per document type, and a protocol for the
district-by-district layer that cannot be authored in advance.

## Skill routing and precedence

Load each applicable skill once, in this order:

1. Use this skill for routing, deadlines, localization, authority sourcing, and
   writing rules.
2. Add `drafting-section-1983-declarations-and-evidence` for a factual human
   declaration or exhibit-foundation preparation supporting summary judgment.
3. Add `drafting-section-1983-complaints` for a complaint, amended complaint, or
   amendment proffer.
4. Add `drafting-false-arrest-complaints` when false arrest, probable cause,
   arguable probable cause, alternative offenses, seizure timing, or
   incorporated arrest video is material.
5. Add an assigned-judge overlay, such as `drafting-for-judge-scholer`, after
   the applicable document and claim skills.
6. Add `building-litigation-alignment-overlays` before drafting an amended
   complaint, leave-to-amend package, or other filing that should consume actual
   adversary attacks or judicial treatment from the current approved docket
   snapshot. A stale or failing overlay produces no specialized drafting change.
7. Add `building-defense-counsel-overlays` when an actual-adversary review
   should consume validated professional litigation history for the effective
   counsel team. Keep every counsel overlay out of the blind common-attack
   review.
8. Add `drafting-section-1983-written-discovery` for requests for production,
   interrogatories, or requests for admission.
9. Add `auditing-section-1983-discovery-responses` for a request-by-request
   response, objection, production, and withholding audit.
10. Add `drafting-section-1983-meet-and-confer` for correspondence based on a
    completed discovery-response audit.
11. Add `auditing-section-1983-privilege-logs` to determine approved log
    requirements or audit a supplied privilege log.
12. Add `drafting-section-1983-deposition-outlines` for chronology- and element-
    gap-driven deposition questions.
13. Run `audit-authorities` before treating a filing or clearly-established-law
    proposition as verified.
14. Run `horan-bad-words` on the substantively complete draft and rerun it after
    any material authority-driven revision.

The more specific skill adds requirements. It does not relax this skill,
governing court rules, repository instructions, source gates, or authority
gates.

**REQUIRED FINAL EDITING SUB-SKILL:** Every drafting task must use
`horan-bad-words`. Apply it after the facts, claims, requested relief, and
authorities are complete. It may remove unsupported emphasis, legalese,
mind-reading, accusation, and rhetoric. It may not delete or paraphrase
controlling terms of art, accurately quoted language, offense elements, or
necessary clearly-established-law distinctions.

## No-concession default

No concession by default. Do not accept, adopt, or restate an adverse
characterization as fact without express user approval of that exact
proposition. This rule applies to characterizations by an opposing party, the
court, a witness, or any other source. Attribution is not agreement. State an
adverse position as that source's position. Then state the user's position and
the supported facts.

Do not volunteer caveats or speculate against the user's position. If accurate
drafting may require an adverse admission, stop and ask the user before
including it.

## Grounding over persuasion

Point every argument at facts in the record, reasonable inferences the court is
entitled to draw, statutes, rules, and controlling or persuasive precedent —
give the court justification and reason to agree. The document's job is to hand
the court a ruling it can write, not to talk the court into one. Persuasive or
rhetorical argument is a small part of any document, if present at all.

- Every sentence traces to a record citation, a pleaded fact, an inference the
  procedural posture permits, or an authority. Cut or rewrite any sentence that
  cannot be traced.
- Replace a characterization with the cited fact that would earn it.
- When asking the court to draw an inference, state the premise facts and the
  rule that permits the inference; do not ask the court to feel its way there.
- Rhetoric, when used at all, is confined to at most a sentence or two of
  framing and is never load-bearing.

## Workflow

1. Strategy. Locate the case strategy file: `strategy.md`, or the
   highest-numbered `strategy-v*.md` if versions exist, in the case or
   workstream folder. If none is found, ask the user for it (or for permission
   to proceed without one) before drafting. Follow its objective and relief
   hierarchy, argument-structure directives (which theory leads, which
   corroborates, claim-lane rules), filing-packet requirements, and prescribed
   audits. If the work surfaces a reason to depart — a new fact, a better
   authority, a structural problem — do not deviate silently: propose the change
   as the next strategy version and proceed only per the user's decision. Never
   edit a strategy version in place.
2. Route. For a complaint, amended complaint, or amendment proffer, before any
   drafting use the [complaint route](references/documents/complaint.md), load
   drafting-section-1983-complaints, and require that skill to read both of its
   canonical references. If the canonical package or either reference cannot be
   read, report **complaint contract unavailable** and do not draft, revise, or
   audit the complaint. Do not invent or reconstruct the missing requirements.
   For discovery, select the applicable peer skill above and apply
   `references/discovery-coordination-contract.md`. For another filing, identify
   the document from the user's request or docket event using
   `references/case-map.md`, which maps events to responsive documents and
   federal deadline baselines. When the user asks "what do I file," the case map
   is the answer.
3. Calendar. Establish the deadline before drafting. A perfect late filing
   loses. Local rules control most response deadlines.
4. Localize. Run `references/localization.md`: use the cached project
   localization record if one exists. Otherwise fetch the district's local rules
   and the assigned judges' standing orders and answer the checklist. Preserve
   it where the project requires; never write into an installed skill package or
   invent a repository path.
5. Source authorities. Follow `references/authorities.md` for every citation: a
   verified-authorities tool or repository when available, binding before
   persuasive, and a `[VERIFY]` marker on anything cited without a verified
   source. Never invent a citation.
6. Gather the facts: who did what to whom, when, where, under what authority.
   Ask for what is missing before drafting.
7. Draft from the selected document skeleton. For a complaint, draft from the
   canonical references loaded in step 2; the umbrella complaint entry is a
   route and supplies no fallback skeleton or count contract. For another
   document type with no skeleton yet, follow the localization answers and the
   court's conventions, and apply the writing system in full.
8. Audit every party position under the no-concession default. Remove each
   unapproved concession. Attribute each adverse characterization and do not
   repeat it in the drafter's own voice. Audit grounding: confirm every point
   rests on cited facts, permitted inferences, or authority, and run any audits
   the strategy file prescribes.
9. If an assigned-judge overlay was used, after composition write one immutable
   judge-overlay execution receipt under the version's canonical `audits/`
   directory. Use `references/judge-overlay-execution.schema.json` and
   `scripts/judge_overlay_receipt.py`. A completed degradation records exactly
   `no judge-specific drafting change` and a bounded reason. The absence of
   judge-specific prose or a receipt does not prove the overlay ran.
10. Self-edit against `references/banned-words.md`, then run the linter:

```bash
python3 scripts/draft_lint.py draft.md
```

Score is violations per 100 words. Lint, revise, and lint again. A score delta
is editing feedback only, never a merits verdict, legal-sufficiency decision, or
filing-readiness decision. Target zero unexempted violations. Reconcile every
residual finding exactly once as an unexempted violation, an accurate quotation
verified against its approved source, or a controlling term of art supported by
the linter exemption record. Repair every unexempted violation. Review paragraph
warnings as review heuristics; they do not change the score or establish filing
readiness.

## The writing system

One unified system, merged from ASD-STE100 Simplified Technical English and the
legal editing guides (Horan, _Bad Words_; McAlpin, _Beyond the First Draft_).
Read `references/writing-system.md` before drafting a single sentence — it is
the controlling style authority for everything this skill produces.

The precedence rule: bans stack (any source's ban is a ban), but where the
sources' advice conflicts, ASD-STE100 controls. STE governs the writer's own
voice, which covers the factual narrative: plain, dry, active, and repetitive by
design, with "show" not "demonstrate," "Officer Doe" by the same name in every
paragraph, no elegant variation, no voice. The law's voice is different: legal
standards and element recitations track the controlling authority's wording with
a citation, and quoted matter is exempt. Terms of art ("clearly established,"
"deliberate indifference," "under color of state law") are STE technical names
and keep their required wording.

## Reference files

- `references/writing-system.md` — the full merged writing system with the
  precedence rule and the ordered self-edit pass. Controlling.
- `references/banned-words.md` — the consolidated banned list from all sources,
  with source tags. Read it before the self-edit pass.
- `references/case-map.md` — docket event to responsive document, with federal
  deadline baselines.
- `references/localization.md` — the protocol for district and judge variation,
  using a project-defined cache when one exists and a returned internal audit
  otherwise.
- `references/authorities.md` — citation sourcing rules and the interface this
  skill expects from a verified-authorities tool or repository.
- `references/discovery-coordination-contract.md` — shared discovery target,
  proportionality, source, existence, and plaintiff-decision boundaries. Each
  public discovery peer repeats its operative minimum for standalone use.
- `references/judge-overlay-execution.schema.json` — exact packet contract for
  one assigned-judge overlay execution against one immutable filing version.
- `references/documents/` — the complaint route plus federal-baseline skeletons
  for mtd-response.md, leave-to-amend.md, extension-motion.md, rr-objection.md,
  rr-response.md, and msj-response.md.
- `scripts/draft_lint.py` — deterministic linter for the mechanical subset of
  the writing rules. It cannot judge whether a fact is well pleaded; it can only
  catch the form of slop.
- `scripts/judge_overlay_receipt.py` — validates one judge-overlay execution
  packet and writes one exclusive immutable receipt under the audited version's
  `audits/` directory.

## What this skill is not for

State-court petitions, criminal filings, prisoner-specific practice (PLRA
exhaustion, screening, in-forma-pauperis mechanics), or appellate briefs — the
writing rules transfer but the structure references do not. It also does not
give legal advice about whether a claim is viable; it structures and edits the
document the user has decided to file.
