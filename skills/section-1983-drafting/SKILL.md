---
name: section-1983-drafting
description: Draft, revise, or edit litigation documents in civil rights cases under 42 U.S.C. § 1983 in plain, forceful, slop-free prose. Use this skill whenever the user asks to write or edit any filing in a Section 1983 or federal civil rights case — a complaint or amended complaint, a response to a motion to dismiss or for summary judgment, a motion for extension of time or for leave to amend, objections to a magistrate judge's report and recommendation (R&R) or a response supporting one, a Monell claim, or any excessive force, false arrest, deliberate indifference, or First Amendment retaliation filing against police, jails, schools, or other state actors — even if they do not say "1983" and even for a single count, section, or paragraph. Also use it when the user asks what to file in response to a docket event or deadline, or asks to remove banned words, intensifiers, legalese, or "AI slop" from an existing filing.
---

# section-1983-drafting

Draft litigation documents in Section 1983 cases that read like a
dispassionate factual record, not like advocacy theater and not like AI
slop. The theory of this skill: adjectives and adverbs tell; facts show. A
judge reading "Officer Doe struck the handcuffed plaintiff four times with
a closed fist" needs no help from "brutally." Understatement backed by
specific facts is the most persuasive register available, and it also
satisfies Iqbal/Twombly, which discounts conclusions and credits facts.

The skill is layered the way the law varies: an invariant writing system,
a uniform federal baseline per document type, and a protocol for the
district-by-district layer that cannot be authored in advance.

## Skill routing and precedence

Load each applicable skill once, in this order:

1. Use this skill for routing, deadlines, localization, authority sourcing, and writing rules.
2. Add `drafting-section-1983-complaints` for a complaint, amended complaint, or amendment proffer.
3. Add `drafting-false-arrest-complaints` when false arrest, probable cause, arguable probable cause, alternative offenses, seizure timing, or incorporated arrest video is material.
4. Add an assigned-judge skill, such as `drafting-for-judge-scholer`, as a court-specific overlay.
5. Run `audit-authorities` before treating a filing or clearly-established-law proposition as verified.
6. Run `horan-bad-words` on the substantively complete draft and rerun it after any material authority-driven revision.

The more specific skill adds requirements. It does not relax this skill, governing court rules, repository instructions, source gates, or authority gates.

**REQUIRED FINAL EDITING SUB-SKILL:** Every drafting task must use `horan-bad-words`. Apply it after the facts, claims, requested relief, and authorities are complete. It may remove unsupported emphasis, legalese, mind-reading, accusation, and rhetoric. It may not delete or paraphrase controlling terms of art, accurately quoted language, offense elements, or necessary clearly-established-law distinctions.

## No-concession default

No concession by default. Do not accept, adopt, or restate an adverse
characterization as fact without express user approval of that exact
proposition. This rule applies to characterizations by an opposing party,
the court, a witness, or any other source. Attribution is not agreement.
State an adverse position as that source's position. Then state the user's
position and the supported facts.

Do not volunteer caveats or speculate against the user's position. If
accurate drafting may require an adverse admission, stop and ask the user
before including it.

## Grounding over persuasion

Point every argument at facts in the record, reasonable inferences the
court is entitled to draw, statutes, rules, and controlling or persuasive
precedent — give the court justification and reason to agree. The
document's job is to hand the court a ruling it can write, not to talk
the court into one. Persuasive or rhetorical argument is a small part of
any document, if present at all.

- Every sentence traces to a record citation, a pleaded fact, an
  inference the procedural posture permits, or an authority. Cut or
  rewrite any sentence that cannot be traced.
- Replace a characterization with the cited fact that would earn it.
- When asking the court to draw an inference, state the premise facts and
  the rule that permits the inference; do not ask the court to feel its
  way there.
- Rhetoric, when used at all, is confined to at most a sentence or two of
  framing and is never load-bearing.

## Workflow

1. Strategy. Locate the case strategy file: `strategy.md`, or the
   highest-numbered `strategy-v*.md` if versions exist, in the case or
   workstream folder. If none is found, ask the user for it (or for
   permission to proceed without one) before drafting. Follow its
   objective and relief hierarchy, argument-structure directives (which
   theory leads, which corroborates, claim-lane rules), filing-packet
   requirements, and prescribed audits. If the work surfaces a reason to
   depart — a new fact, a better authority, a structural problem — do not
   deviate silently: propose the change as the next strategy version and
   proceed only per the user's decision. Never edit a strategy version in
   place.
2. Route. Identify the document from the user's request or the docket
   event using `references/case-map.md`, which maps events to responsive
   documents and their federal deadline baselines. When the user asks
   "what do I file," the case map is the answer.
3. Calendar. Establish the deadline before drafting. A perfect late
   filing loses. Local rules control most response deadlines.
4. Localize. Run `references/localization.md`: use the cached
   `references/jurisdictions/<district>.md` if one exists, otherwise
   fetch the district's local rules and the assigned judges' standing
   orders, answer the checklist, and write the cache file.
5. Source authorities. Follow `references/authorities.md` for every
   citation: a verified-authorities tool or repository when available,
   binding before persuasive, and a `[VERIFY]` marker on anything cited
   without a verified source. Never invent a citation.
6. Gather the facts: who did what to whom, when, where, under what
   authority. Ask for what is missing before drafting.
7. Draft from the skeleton in `references/documents/<type>.md`. For a
   document type with no skeleton yet, follow the localization answers
   and the court's conventions, and apply the writing system in full.
8. Audit every party position under the no-concession default. Remove
   each unapproved concession. Attribute each adverse characterization
   and do not repeat it in the drafter's own voice. Audit grounding:
   confirm every point rests on cited facts, permitted inferences, or
   authority, and run any audits the strategy file prescribes.
9. Self-edit against `references/banned-words.md`, then run the linter
   and repair every violation:

   ```bash
   python3 scripts/draft_lint.py draft.md
   ```

   Score is violations per 100 words. Lint, revise, lint again; target
   zero banned words.

## The writing system

One unified system, merged from ASD-STE100 Simplified Technical English and
the legal editing guides (Horan, _Bad Words_; McAlpin, _Beyond the First
Draft_). Read `references/writing-system.md` before drafting a single
sentence — it is the controlling style authority for everything this skill
produces.

The precedence rule: bans stack (any source's ban is a ban), but where the
sources' advice conflicts, ASD-STE100 controls. STE governs the writer's
own voice, which covers the factual narrative: plain, dry, active, and
repetitive by design, with "show" not "demonstrate," "Officer Doe" by the
same name in every paragraph, no elegant variation, no voice. The law's
voice is different: legal standards and element recitations track the
controlling authority's wording with a citation, and quoted matter is
exempt. Terms of art ("clearly established," "deliberate indifference,"
"under color of state law") are STE technical names and keep their
required wording.

## Reference files

- `references/writing-system.md` — the full merged writing system with the
  precedence rule and the ordered self-edit pass. Controlling.
- `references/banned-words.md` — the consolidated banned list from all
  sources, with source tags. Read it before the self-edit pass.
- `references/case-map.md` — docket event to responsive document, with
  federal deadline baselines.
- `references/localization.md` — the protocol for district and judge
  variation, cached per forum under `references/jurisdictions/`.
- `references/authorities.md` — citation sourcing rules and the interface
  this skill expects from a verified-authorities tool or repository.
- `references/documents/` — one federal-baseline skeleton per document
  type: complaint.md, mtd-response.md, leave-to-amend.md,
  extension-motion.md, rr-objection.md, rr-response.md, msj-response.md.
- `scripts/draft_lint.py` — deterministic linter for the mechanical subset
  of the writing rules. It cannot judge whether a fact is well pleaded; it
  can only catch the form of slop.

## What this skill is not for

State-court petitions, criminal filings, prisoner-specific practice (PLRA
exhaustion, screening, in-forma-pauperis mechanics), or appellate briefs —
the writing rules transfer but the structure references do not. It also
does not give legal advice about whether a claim is viable; it structures
and edits the document the user has decided to file.
