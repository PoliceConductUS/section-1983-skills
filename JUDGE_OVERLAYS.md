# Judicial Reasoning Profile

A judge overlay is an evidence-bounded judicial reasoning profile for the
assigned judge. It stratifies verified decisions by issue, procedural posture,
governing standard, reasoning authorship, and evidence strength. It is not a
prediction, personality profile, strategy file, or renamed copy of another
judge's conclusions. It supplements governing law and the applicable document
skill only when the reviewed corpus supports a neutral transfer.

Court-specific filing rules, procedures, standing orders, and documented conduct
requirements are a separate compliance component. They accompany the judicial
reasoning profile but do not become evidence about how the judge reasons or is
likely to rule.

[Manage case overlays](OVERLAYS.md) owns the shared immutable lifecycle,
inventory, precedence, manifest, and reuse rules. This guide adds the judge-
specific research and invalidation rules.

## Judge-overlay lifecycle

Create the first judge overlay after assignment is verified and before a filing
first seeks a judge-specific drafting input. Reuse it only while the assignment,
validated corpus, neutral transfer cards, official procedure and standing order
sources, prohibited inferences, checked date, and validator result remain
current.

Create a new immutable version after assignment or reassignment, a changed
official procedure or standing order, a new or corrected validated corpus or
transfer card, a stale checked date, a changed prohibited inference, or a failed
validator result. Preserve and supersede the prior version. Until the new
version validates, make no judge-specific drafting change.

## Judicial reasoning dimensions

Build the profile issue by issue and procedural posture by procedural posture.
Code only source-supported observations about:

- **substantive doctrine** and the legal rules the judge applies;
- **procedural doctrine** and distinctions among pleading, summary judgment,
  trial, postjudgment, and appellate stages;
- **reasoning patterns**, including demonstrated analogies, distinctions, and
  limiting principles;
- **authority hierarchy** and the authorities used for the relevant proposition;
- **factual methodology**, including chronology, quotations, record treatment,
  and relevant-time knowledge;
- **error sensitivities**, including identified standard, inference,
  preservation, authority, or internal-consistency defects; and
- **analytical presentation patterns**, without imitating or mimicking the
  judge's voice or personality.

Research published opinions and prior orders first. Authenticated public
articles, speeches, and books authored by the judge may supply bounded context,
but do not become governing authority. Standing orders and courtroom procedures
are separate compliance inputs, not proof of a reasoning pattern.

A validated transfer may organize an argument as the judge's established rule,
the supported facts, and the requested application. It may ask the judge to
apply the judge's own verified reasoning consistently. It must not state that a
result is likely, attribute a preference or psychology, or turn a descriptive
pattern into a prediction.

## 1. Define the research scope

Define the court, judicial role, date range, case category, motion type,
procedural posture, research question, planned sources, searches, exclusions,
and update date before retrieval. Keep the governing-law universe separate from
the decisionmaker universe.

Use this source hierarchy:

1. official primary materials, including opinions, rules, orders, and statutes;
2. authenticated docket documents with stable identity;
3. reliable docket indexes as retrieval leads; and
4. search snippets and secondary descriptions only as retrieval leads to primary
   material.

Never treat search visibility as the denominator. Seek favorable, unfavorable,
and adverse and disconfirming evidence under the same declared method.

## 2. Build and validate the corpus

Code one motion-disposition pair as the unit of analysis and link each related
recommendation, adoption, amendment, appeal, or remand stage. Record the
assigned judge, reasoning author, recommendation author, and adopting judge
separately. Record retrieval status, missing documents, exclusions, checked
dates, and later history rather than filling gaps from inference.

Use the canonical
[decision-corpus schema](skills/studying-rule-59e-decisions/references/decision-corpus.schema.json)
and its denominator, missingness, source, authorship, and retrieval-gap fields.
The canonical corpus must pass
[validate_corpus.py](skills/studying-rule-59e-decisions/scripts/validate_corpus.py)
before publication or transfer:

```bash
python3 skills/studying-rule-59e-decisions/scripts/validate_corpus.py --decisions-root "$PWD/skills/studying-rule-59e-decisions/references/fixtures" --corpus-target valid-complete.json
```

Validation proves the declared structural and semantic contract. It does not
turn a source into governing authority or cure an incomplete research universe.

## 3. Classify conclusion strength

- One verified disposition is an example.
- An incomplete or non-systematic group is a documented cluster.
- A tendency requires a disclosed complete denominator, complete-pair retrieval
  for every coded record, consistent coding, and an express missingness limit.

State the numerator, denominator, date range, case mix, missingness, confidence,
supporting rows, and disconfirming rows with every cluster or tendency. A result
at one strength never silently becomes a stronger result.

## 4. Build the court-conduct checklist

Review applicable official rules, individual procedures, standing orders, candor
duties, civility requirements, ex parte limits, filing limits, and other conduct
the court expressly prohibits or discourages. Treat these as compliance inputs,
not optimization targets.

Every court-specific warning must identify a stable source ID, the official
source, issuing body, jurisdiction or judge, checked date, bounded warning, and
verification status. An unverified or stale warning remains a gap and is not a
court requirement. Do not restate it from memory or a secondary description.

## 5. Export neutral transfer cards

Export each downstream proposition through the canonical
[transfer-card schema](skills/studying-rule-59e-decisions/references/transfer-card.schema.json).
Each card carries its proposition, universe, source rows, source identity and
checked date, evidence level, denominator and missingness, disconfirming rows,
permitted use, prohibited inference, and metric type. A card transfers bounded
evidence; it does not certify an authority, expose private strategy, or select a
litigation path.

## 6. Consume the overlay in drafting

Consume only neutral transfer cards that passed the canonical corpus validator.
Preserve each card's source identity and checked date, evidence level,
denominator and missingness, permitted use, and prohibited inference. Governing
law remains separate, and every legal proposition still passes the authority
gate.

A prohibited inference or no qualifying support produces no judge-specific
drafting change. The drafting skill does not expose private strategy and does
not select a litigation path.

## 7. Record execution

After the applicable document and claim skills compose the filing, validate one
execution packet against
`skills/section-1983-drafting/references/judge-overlay-execution.schema.json`
and produce its receipt with
`skills/section-1983-drafting/scripts/judge_overlay_receipt.py`.

The processor receives the declared `filing`, `judge-corpus`, and
`court-conduct` role roots. A required filing target selects one canonical
relative file inside `filing`. The processor verifies the frozen filing artifact
fingerprints and returns deterministic receipt bytes plus one output-relative
path. It must not edit or modify the filing or any artifact under review. Only
the trusted host may publish the receipt through `OutputRun`. Missing, stale,
invalid or failed, and unavailable required inputs fail closed with no drafting
change. A completed degradation records `no judge-specific drafting change` and
its bounded reason. The absence of judge-specific prose or an execution receipt
does not prove the overlay ran.

## 8. Apply the degradation clause

A thin or incomplete corpus adds no judge-specific proposition. Preserve a
verified example only at example strength. Report the missing source, incomplete
pair, unresolved candidate, stale check, or unsupported conclusion as a gap.
Rerun the corpus validator and downstream drafting audits after a material
corpus, source, or draft change.

## Anti-gaming boundary

The overlay never predicts an outcome or judicial behavior. It does not infer
judge psychology, does not publish unsupported tendencies, and does not use
unverified citations.

- Do not manipulate or predict judicial assignment.
- Do not exploit perceived personal preferences.
- Do not tailor facts or law to a supposed desired outcome.
- Do not conceal adverse authority.
- Do not distort the record.
- Do not personalize attacks on the court.
- Do not copy or rename another judge's conclusions.

Court procedures and conduct rules are compliance constraints. They are not
signals for assignment selection, personal appeals, record manipulation, or
outcome optimization.

## Generic synthetic conduct record

This fictional record demonstrates the required fields without stating a real
court requirement.

```yaml
source_id: COURT-SRC-001
official_source: https://court.example.invalid/rules
issuing_body: Example District Court
jurisdiction_or_judge: Example District
checked_on: 2026-08-20
warning: Use the fictional filing limit stated in the verified source.
status: verified
```

## Generic synthetic valid overlay

This example is expressly fictional and demonstrates one schema-valid bounded
card.

```yaml
fictional: true
court_id: Example District
judge_id: Judge Example
artifact: validated neutral transfer card
```

```json
{
  "card_id": "EXAMPLE-CARD-001",
  "proposition": "One fictional order stated the coded procedural ground.",
  "universe": "One verified fictional order in an incomplete Example District search",
  "numerator": 1,
  "denominator": 1,
  "date_range": "2026-01-01 through 2026-01-31",
  "source_row_ids": ["EXAMPLE-REC-001"],
  "evidence_level": "example",
  "missingness": "The broader fictional candidate universe remains incomplete",
  "disconfirming_row_ids": [],
  "permitted_use": "Use only as a bounded fictional example of the stated disposition",
  "prohibited_inference": "Do not infer frequency, prediction, causation, or strategy",
  "checked_through": "2026-08-20",
  "actual_source_identity": "Example District synthetic docket document 10",
  "source_checked_date": "2026-08-20",
  "metric_type": "descriptive"
}
```

## Generic synthetic thin-corpus result

This example is also fictional. It demonstrates the required fail-closed result
when the candidate universe is incomplete.

```yaml
fictional: true
court_id: Example District
judge_id: Judge Example
corpus_status: incomplete
overlay_result: no judge-specific proposition
gap: One fictional candidate lacks a complete motion-disposition pair.
```

## Structural example only

The existing [Scholer overlay](skills/drafting-for-judge-scholer/SKILL.md) is a
structural example only. It separates judicial authorship stages, preserves
evidence strength, and adds no judge-specific proposition when qualifying
support is absent. Do not copy its substantive conclusions.
