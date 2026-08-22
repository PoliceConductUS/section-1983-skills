---
name: studying-rule-59e-decisions
description:
  Use when researching patterns in Rule 59(e) rulings, postjudgment amendment
  decisions, judge-specific reconsideration practice, or comparisons between
  successful and unsuccessful Rule 59 motions.
---

# Studying Rule 59(e) Decisions

## Purpose

Build an evidence-coded corpus that separates governing law from local decision
examples. Search results are retrieval leads, not a sample. A ruling shows what
the court decided and said; it does not show which drafting choices mattered
unless the motion and relevant record are also reviewed.

Read [references/corpus-contract.md](references/corpus-contract.md) before
beginning a study or adding a corpus conclusion to another skill.

Use
[references/decision-corpus.schema.json](references/decision-corpus.schema.json)
for every published or transferred corpus and
[references/transfer-card.schema.json](references/transfer-card.schema.json) for
standalone downstream transfers. Before release, run
`python3 scripts/validate_corpus.py <corpus.json>` from the installed skill
directory. CSV, YAML, and databases remain valid working formats, but they must
export canonical JSON that passes the validator before publication or transfer.

## Required companion skill

Use `audit-authorities` for every legal proposition, quotation, pinpoint,
posture classification, and later-history conclusion used in a filing or
drafting rule.

## Define two universes

Keep these studies separate:

1. **Governing-law corpus:** the Federal Rules, applicable statutes, Supreme
   Court holdings, Fifth Circuit en banc and published panel holdings, and
   binding former Fifth Circuit holdings addressing Rule 59(e), postjudgment
   amendment, Rule 15(a), futility, preservation, supersession, and appellate
   review. Add controlling state substantive law when the federal issue depends
   on it.
2. **Decisionmaker corpus:** all reasonably retrievable Rule 59 dispositions for
   the identified judge or judge pair within a stated court, date range, motion
   type, and case category.

Expand to a broader district comparison only after reporting why the
judge-specific universe is too small or incomplete.

## Unit of analysis

Use one parent row per motion-disposition pair and one child record per asserted
ground. Link related records when a recommendation, adoption order, amended
ruling, appeal, or remand belongs to the same motion. This preserves motions
that were denied overall but produced a correction or prevailed on one ground.

Count the motion once in outcome totals. A recommendation, adoption order,
amended order, and appeal are linked stages, not additional Rule 59 motions.
Treat a full or partial grant of operative requested relief as a substantive
success. Report correction without relief, procedural disposition, and
administrative-only action separately rather than as grants.

Retrieve when available:

- judgment or order challenged;
- Rule 59 motion and supporting brief;
- response and reply;
- proposed amended pleading or other requested replacement document;
- recommendation;
- adopting, rejecting, or independently reasoned district order;
- amended judgment; and
- appellate disposition.

An order-only row may support the stated ground and result. It may not support a
conclusion about motion organization, omitted material, or persuasive drafting
choices that the order does not identify.

## Evidence hierarchy

1. Official opinions, rules, statutes, and docket documents.
2. PACER or RECAP docket artifacts with stable identity.
3. Reliable docket indexes used as retrieval leads.
4. Search snippets and secondary descriptions used only to locate primary
   material.

Preserve the source URL or canonical path, docket number, document number,
retrieval date, and artifact hash when the repository requires hashes.

## Coding rules

Code the fields and controlled values in the corpus contract and canonical
schema. At minimum record:

- assigned judge, reasoning author, recommendation author, and adopting judge;
- whether the ruling contains independent reasoning, adopts another judge's
  analysis, or states only an outcome;
- motion type and legal vehicle;
- case category and judgment posture;
- amendment timing, prior leave request, proposed pleading status, and claimed
  Rule 59 ground;
- disposition: grant, partial grant, correction without relief, denial,
  procedural disposition, administrative-only action, withdrawn, or unresolved;
- stated reasons and outcome-changing reason;
- standard of review and appellate result; and
- controlled retrieval status, coding confidence, and open gaps.

Do not attribute a magistrate judge's reasoning to the district judge merely
because the district judge adopted it. A consent-case final order by a
magistrate judge is different from a recommendation.

Use the same `motion_id` for every linked recommendation, adoption, or other
stage. Every retrieval gap identifies its stable candidate. A missing-document
gap also identifies its decision record and exact document type. An unresolved
candidate uses `unresolved-candidate` with a null `record_id`; do not fabricate
a decision record for it. `candidate_count` equals coded motion-disposition
pairs plus distinct unresolved-candidate IDs; record-linked document gaps do not
add candidates.

## Analysis gates

### Selection-bias gate

Include unfavorable and favorable results. Define the denominator before
describing a rate or pattern. Log the searches and missing documents.
Search-visible cases are not the denominator.

The attempted census closes only after the manifest's planned databases,
queries, variants, judge roles, and date range have been searched and every
located candidate is coded, excluded with a reason, or placed in the gap log. A
capped result set, inaccessible docket, or unresolved candidate makes the census
incomplete.

### Comparability gate

Stratify at least by:

- Rule 59(e) alter-or-amend versus Rule 59(a) new trial;
- postjudgment amendment versus evidence, damages, fee, habeas, or other
  reconsideration;
- civil-rights versus other case categories;
- represented versus pro se when known;
- recommendation, adoption, independent district ruling, and consent ruling; and
- complete proposed pleading, cure explanation only, and neither.

Do not combine materially different strata into a success rate.

### Conclusion-strength gate

- One verified disposition is an **example**.
- A non-systematic or incomplete group is a **documented cluster**.
- A **tendency** requires a disclosed denominator, `complete-pair` retrieval for
  every coded record, consistent coding, and an express missingness limit.
- A **drafting rule** requires controlling authority, an express court
  requirement, or repeated comparable decisions supported by reviewed
  motion-disposition pairs.

State numerator, denominator, date range, case mix, missingness, and confidence
with every pattern statement. Use tendencies as judge-specific overlays, never
as predictions or substitutes for governing law.

## Required outputs

Produce:

1. a methods memo defining scope, searches, exclusions, and completeness;
2. an evidence ledger using the corpus contract;
3. a retrieval-gap log;
4. governing-law findings separated from decisionmaker findings;
5. a motion-design comparison limited to complete motion-disposition pairs;
6. an adverse or disconfirming-evidence section; and
7. transfer cards stating exactly what, if anything, another drafting skill may
   use.

Each neutral transfer card must identify its source rows, evidence level,
denominator, missingness, permitted use, prohibited inference, actual source
identity, and checked dates. It transfers bounded evidence without selecting a
legal path or litigation strategy. If the evidence does not support a drafting
change, say so.

A card may cite `complete-pair` or `ruling-complete` source rows. `index-only`
and `lead-only` rows are retrieval leads, not verified card support. Every
`tendency` or `success-rate` corpus requires `complete-pair` status for all
coded records.

## Update rule

Before relying on an older corpus for a current filing, audit post-study
decisions and later history through the new research date. Preserve the earlier
corpus version and write a new versioned ledger and findings memo.

If the filing deadline prevents a complete study, issue a preliminary report
limited to verified binding rules and documented examples. Do not state a grant
rate, tendency, or motion-design pattern from the preliminary set. Record what
remains for the later complete study.

## Acceptance checks

Before release, confirm:

- grants and denials were both sought;
- authorship and adoption were coded separately;
- every pattern has a denominator and missingness statement;
- order-only rows did not produce motion-design rules;
- governing law and judge examples remain separate;
- later history and current rules were checked;
- quotations and pinpoints were verified from primary artifacts; and
- every downstream drafting instruction has a neutral transfer card; and
- the canonical JSON export passes `scripts/validate_corpus.py`.

## Output provenance

Every returned artifact must identify the actual approved source identity and
checked date used.
