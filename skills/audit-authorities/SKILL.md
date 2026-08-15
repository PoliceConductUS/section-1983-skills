---
name: audit-authorities
description: "Use when auditing citations, authorities, quotations, pinpoints, procedural-posture fit, record support, distinguishing claims, or clearly-established-law analysis in a pleading, amendment proffer, motion, response, brief, RRD, or filing-ready legal document."
---

# SKILL: Audit Authorities, Citations, and Differentiators in a Legal Response

## Goal

Verify that every cited authority, factual assertion, and "differentiator" (distinguishing fact/holding) is:

1. **Real and correctly identified**
2. **Accurately described** (holding vs dicta, standard, posture)
3. **Pinpoint-supported** (the cited page/paragraph actually says what is claimed)
4. **On-point** (relevant jurisdiction, procedural posture, materially similar facts)
5. **Not undermined** (distinguished, limited, overruled, abrogated, or factually inapplicable)
6. **Used honestly** (no "laundering" of a proposition through a quote or parenthetical)

This skill applies to complaints, amendment proffers, RRDs, motions, responses, replies, briefs, declarations, and appendices.

## Project Integration

### Input files

Resolve the controlling draft, verified-authority root, source units, and audit-output location from the repository instructions. If no repository schema exists, ask for or identify explicit paths. A citation tracker is optional and never replaces the document body or authority source.

### Output file

Write the audit where the repository requires. If no location is defined, return the structured audit without inventing a source-tree path.

### Authority sourcing and verification

Before auditing, obtain the best available source copy for every cited authority:

1. Check the repository's verified authority unit and metadata.
2. If missing, check the source metadata for a retrieval URI.
3. If no URI, attempt to fetch from known free sources:
   - **SCOTUS**: Library of Congress (`tile.loc.gov/storage-services/service/ll/usrep/`)
   - **Fifth Circuit**: `ca5.uscourts.gov/opinions/`
   - **General**: CourtListener RECAP archive
4. Preserve the source and retrieval provenance where repository rules require.
5. Do not mark an authority verified merely because a PDF was downloaded. Verification requires identity, court, publication and binding status, proposition and pinpoint, holding classification, procedural posture, pre-event timing when material, later history, and any rule-of-orderliness check.
6. If a load-bearing or filing-near authority cannot be verified, mark a filing-critical GAP. Do not treat the document as filing-ready.

### Audit depth by citation role

- **Plaintiff's affirmative authorities**: Full 10-stage audit (all stages)
- **Defendants' authorities cited only to distinguish**: Stages 2 (identity), 5 (on-point / posture match), and 9 (differentiator validity) only - skip pinpoint/context/quote verification since we're not relying on them for propositions

### Direct quote verification (CRITICAL)

For every phrase in quotation marks attributed to an authority:

1. Locate the **exact text** in the authority PDF at the cited pinpoint
2. Compare **character-by-character** (watch for: missing qualifiers like "generally," "in this case," "under these facts"; changed verb tenses; omitted conditions)
3. If the quote does not appear verbatim in the authority: **FATAL**
4. If the quote appears but at a different pinpoint: **MODERATE** (fix the pinpoint)
5. If the quote is a paraphrase presented as a direct quote: **MAJOR**

This catches fabricated language attributed to real cases - a common AI-assisted drafting failure.

## Attorney expectation model (how it's _supposed_ to work)

In competent practice, citation auditing is not "spot checking." It's a **chain-of-support test**:

- **Every legal proposition** must be supported by authority that actually states it **in the context claimed**.
- **Every factual assertion** must be supported by record evidence (exhibits, declarations, transcripts).
- **Every key inference** must be tagged as inference and must be reasonable under the governing standard.
- **Every use of precedent** must respect:

  - jurisdiction (binding vs persuasive),
  - procedural posture (MTD vs SJ vs trial),
  - standard (plausibility vs summary judgment evidence),
  - and material similarity of facts.

Your audit should catch: wrong pinpoints, misleading parentheticals, overbroad "stands for" claims, and "case name drop" citations that don't actually support the sentence they're attached to.

## Definitions

- **Authority**: case, statute, rule, regulation, treatise, jury instruction, local rule, secondary source.
- **Proposition**: the legal claim _made in your text_ (the "why the court should rule for you" part).
- **Pinpoint**: the exact location the proposition appears (page/paragraph/Westlaw star page).
- **Differentiator**: a fact or legal feature that distinguishes your case from adverse authority (or aligns you with favorable authority).
- **Posture**: where you are procedurally (12(b)(6), 12(c), 56, preliminary injunction, etc.).
- **Holding vs dicta**:

  - **Holding** = necessary to the judgment.
  - **Dicta** = not necessary; may still be persuasive but should not be represented as binding.

## Output contract (what you produce)

For each citation (and each differentiator that matters), produce one structured audit record with:

- what the brief claims,
- what the authority actually says,
- whether it supports the claim,
- and what to fix.

### Severity levels

- **FATAL**: authority does not exist, wrong case, wrong statute, or proposition not present; or citation contradicts statement.
- **MAJOR**: authority exists but posture/standard/facts mismatch makes it misleading as used.
- **MODERATE**: partially supported; needs narrowing, better phrasing, or better cite.
- **MINOR**: formatting/pinpoint/parenthetical cleanup; still basically correct.

## Workflow (repeatable, attorney-style)

### Stage 0 - Build the audit inventory

1. Parse the draft response.
2. Extract:

   - every **citation** (case, rule, statute),
   - every **record cite** (exhibit, declaration, transcript),
   - every **legal standard sentence** (often most error-prone),
   - every **differentiator claim** ("Unlike X, here Y…").

Deliverable: an ordered list of audit items in the same order as the brief.

### Stage 1 - Extract the _actual proposition_ being asserted (not the label)

For each sentence/paragraph with citations:

1. Write the proposition in plain English, scoped narrowly:

   - Bad: "Qualified immunity doesn't apply."
   - Good: "At the 12(b)(6) stage, the court must accept pleaded facts as true and may deny qualified immunity when the complaint plausibly alleges violation of clearly established law."

2. Identify whether the proposition is:

   - legal rule/standard,
   - application of rule to facts,
   - factual claim,
   - inference,
   - or procedural claim.

Deliverable: proposition statement + type.

### Stage 2 - Validate authority identity (existence + metadata)

For each cited authority:

1. Confirm it exists (correct caption, reporter, court, year).
2. Confirm you're using the correct version/source (official reporter vs slip opinion vs Westlaw/Lexis).
3. Record metadata:

   - court,
   - jurisdiction,
   - date,
   - whether binding in your court,
   - posture of the cited decision.

Fail conditions:

- wrong case,
- wrong year,
- wrong court,
- or a similarly named case substituted accidentally.

Deliverable: "Identity check: PASS/FAIL" with corrected cite if needed.

### Stage 3 - Pinpoint verification (the "does it say that _there_?" test)

1. Go to the cited pinpoint.
2. Extract the smallest slice that contains the supposed rule (quote/paraphrase).
3. Confirm:

   - the text exists at that pinpoint,
   - the pinpoint isn't off by 1-5 pages due to PDF vs reporter pagination,
   - the quote isn't missing qualifiers ("generally," "in this case," "under these facts").

Deliverable: pinpoint snippet summary + "Pinpoint supports: YES/NO/PARTIAL".

### Stage 4 - Context verification (the "are you laundering dicta?" test)

Even if the text exists, read enough context to classify it:

1. Is it **holding** or **dicta**?
2. Is it **majority**, **concurrence**, or **dissent**?
3. Is the statement conditional or fact-bound?
4. Is the authority addressing the same legal question or a different one?

Fail conditions:

- citing dicta as binding,
- citing a dissent like it's law,
- quoting a standard that was later rejected in the same opinion.

Deliverable: holding/dicta classification + notes.

### Stage 5 - On-point analysis (posture/standard/facts match)

This is where most "technically true but misleading" citations get caught.

Checklist:

1. **Procedural posture match**:

   - MTD rule cited from a summary judgment case?
   - Qualified immunity standard cited from trial evidence posture?

2. **Legal standard match**:

   - "probable cause" vs "arguable probable cause"
   - "reasonable suspicion" vs "probable cause"
   - "clearly established" framing correct for your circuit?

3. **Fact similarity** (material facts only):

   - what facts did that court treat as decisive?
   - do you have those facts, or the opposite?

Deliverable: "On-point rating":

- ON-POINT (strong),
- ON-POINT (limited),
- PERSUASIVE ONLY,
- DISTINGUISHABLE,
- INAPPLICABLE.

### Clearly established law audit — required for individual-capacity claims

For every claim, defendant, and challenged act, verify a separate fair-warning record:

| Field              | Required content                                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Event              | Event date, stage, and challenged conduct                                                                                       |
| Rule               | The constitutional right or rule at the conduct-specific level                                                                  |
| Authority          | Case, court, publication and binding status, decision date, and pinpoint                                                        |
| Precedential force | Holding, alternative holding, implicit holding, dicta, silence or non-holding, appellate fact statement, or persuasive-only use |
| Comparison         | Material factual similarities and material differences                                                                          |
| Fair warning       | Why the authority made the alleged unlawfulness apparent on the event date                                                      |
| Status             | Verified, needs narrowing, or filing-critical GAP                                                                               |

Check actual probable cause separately from arguable probable cause. Do not use a district-court decision, nonprecedential decision, or later-decided case as the source of clearly established law. When several cases allegedly combine to supply fair warning, verify the contribution and status of each case and explain the combined rule. Apply the rule of orderliness and later-history checks before approving the proposition.

### Stage 6 - Negative authority / undermining checks

For each key authority you rely on (and each adverse case you cite):

1. Does the decision contain limiting language that narrows the rule?
2. Is it criticized, limited, overruled, or abrogated?
3. Are there later cases in your court that changed the test?
4. If your opponent cites the same case differently, who is right?

Deliverable: "Undermining risk: LOW/MED/HIGH" + recommended swap/additional cite.

_(If you have access to Shepard's/KeyCite, use it; if not, do a reasonable web check for "overruled", "abrogated by", "limited by" and later circuit authority.)_

### Stage 7 — Quote and parenthetical integrity

Quotes and parentheticals are common failure points — and parentheticals are the #1 vector for AI hallucination. A fabricated parenthetical on a real case with a correct citation is nearly undetectable without reading the source.

**Mandatory method**: For every parenthetical, you MUST:

1. Open the authority PDF (not your training data, not your memory of the case)
2. Read the actual holding and the text at the cited pinpoint
3. Verify that the parenthetical accurately describes what the court held or said
4. If the parenthetical describes a proposition that does not appear anywhere in the opinion: **MAJOR** (fabricated parenthetical)
5. If the parenthetical overstates, inverts, or materially mischaracterizes the holding: **MAJOR**

Additional rules for quoted text:

1. Quotes must preserve meaning; ellipses can't change substance.
2. If you paraphrase, you still must be faithful to qualifiers.

**Do not trust your own knowledge of what a case holds.** The entire point of this stage is to catch propositions that sound right but aren't in the source. Read the PDF.

Deliverable: "Quote integrity: PASS/FAIL" + corrected parenthetical + page in PDF where verified (or "NOT FOUND IN SOURCE").

### Stage 8 - Record cite and inference audit (facts vs evidence)

For each factual claim, first classify it as a source observation, pleaded allegation, party or court characterization, permitted inference, or GAP. Then:

1. Identify whether it is:

   - directly supported by evidence,
   - supported by testimony,
   - or an inference.

2. Ensure the record cite actually supports it at that location.
3. For inferences:

   - state as inference ("a reasonable inference is…"),
   - ensure it's permitted under the procedural posture (MTD vs SJ).

Deliverable: record support status + suggested reword if needed.

### Stage 9 - Differentiator audit (your "unlike X, here Y" claims)

For each differentiator:

1. Identify the adverse authority's decisive fact(s) or rule condition(s).
2. Verify those are actually decisive in the authority.
3. Verify your claimed difference is real and material.
4. Confirm you're not creating a strawman version of the adverse case.

Deliverable: "Differentiator validity: VALID/WEAK/INVALID" + tighter framing.

### Stage 10 - Remediation plan (make it court-safe)

For every issue found, supply a fix that fits one of these patterns:

- **Narrow the proposition** to what the authority truly supports.
- **Replace the authority** with one that actually supports it.
- **Add a second authority** (belt-and-suspenders).
- **Rewrite as inference** rather than asserted fact.
- **Move statement** to background / persuasive section if not binding.

Deliverable: one-line edit + replacement citation recommendation.

## Quality bar: "Would I sign this?"

Before finalizing:

- Every paragraph with a legal conclusion has at least one authority that **directly supports** it.
- Every key authority is not only correct, but **not misleading** in posture and scope.
- Every adverse case is either:

  - fairly summarized and distinguished, or
  - acknowledged with limiting language (if it hurts you).

- Every record cite is accurate.

## Suggested YAML schema (drop-in for audit results)

```yaml
audit_item:
  id: "cite-0001"
  brief_location:
    document: "response-to-mtd.md"
    section: "II.B"
    paragraph_index: 3
    sentence_index: 2
  proposition:
    text: "At the Rule 12(b)(6) stage, the court must accept pleaded facts as true and may deny qualified immunity when the complaint plausibly alleges violation of clearly established law."
    type: "legal_standard" # legal_standard | application | factual_claim | inference | procedural_claim
  citations:
    - raw_citation: "Case Name, 123 F.3d 456, 460 (5th Cir. 2019)."
      authority_type: "case" # case | statute | rule | regulation | secondary
      binding_level: "binding" # binding | persuasive | nonbinding
      posture_in_authority: "appeal-from-12b6"
      pinpoint_claimed: "p. 460"
  verification:
    identity_check: "pass" # pass | fail
    pinpoint_check: "partial" # pass | fail | partial
    context_check:
      holding_or_dicta: "dicta"
      notes: "Statement appears in background discussion, not necessary to judgment."
    on_point_rating: "on-point-limited" # on-point-strong | on-point-limited | persuasive-only | distinguishable | inapplicable
    undermining_risk: "medium" # low | medium | high
  findings:
    - severity: "MAJOR" # FATAL | MAJOR | MODERATE | MINOR
      issue: "Quoted language exists but is dicta; posture differs."
      impact: "Overstates binding force; opponent can attack as misleading."
      fix:
        recommended_edit: "Rephrase as persuasive guidance and add a binding 12(b)(6) QI standard case."
        replacement_citations:
          - "Add binding circuit precedent directly addressing QI at 12(b)(6)."
  status: "needs-revision" # ok | needs-revision
```

## Opinion (what matters most, practically)

If you do only three things, do these:

1. **Posture match** (MTD vs SJ) - this is the #1 way briefs accidentally become misleading.
2. **Holding vs dicta** - courts hate "case says X" when it's dicta.
3. **Material facts** - the "on-point" question is usually won or lost on 1-2 decisive facts.

## Stage 11 — Regenerate Table of Authorities and Statutes/Rules

After completing the audit and any remediation, regenerate the TOA and Statutes/Rules tables in the response document to reflect exactly what is cited in the body.

### Process

1. **Extract all case citations from the body** (everything after the TOA, starting from INTRODUCTION or ARGUMENT). Parse each unique case with its full citation format (name, reporter, year).

2. **Extract all statute/rule citations from the body.** Include federal statutes (42 U.S.C. §), Federal Rules (Fed. R. Civ. P., Fed. R. Evid.), state statutes (Tex. Penal Code, Tex. Code Crim. Proc.), and local rules.

3. **Preserve existing page numbers.** If the document already has a TOA with page numbers filled in, carry those forward for any case that remains cited. New citations get empty page number fields. Removed citations are dropped.

4. **Sort cases alphabetically** by case name (ignore "In re", "Estate of", etc. for sort — sort on the substantive first word).

5. **Sort statutes/rules** by: federal statutes first (by title number), then Federal Rules (Civ. P., then Evid.), then state statutes (alphabetical by code name), then local rules.

6. **Replace the existing TOA and Statutes/Rules tables** in the document. Find the `### Cases` and `### Statutes and Rules` sections within the `## TABLE OF AUTHORITIES` block and replace their table contents entirely.

7. **Verify no orphans**: every case in the new TOA must appear in the body; every case in the body must appear in the TOA. Report any mismatches.

### Table format

Use the same markdown table format as the existing document:

```markdown
### Cases

| Case                         | Page(s) |
| ---------------------------- | ------- |
| _Case Name_, Reporter (Year) |         |
```

```markdown
### Statutes and Rules

| Authority        | Page(s) |
| ---------------- | ------- |
| 42 U.S.C. § 1983 |         |
```

This stage ensures the TOA is always in sync with the body after edits, additions, or removals during the audit.

### Recommended: Citation markup for reliable extraction

Regex-based citation extraction is inherently fragile due to format variations (short-forms like `_Iqbal_`, signal words like `_See_`, split citations across lines). For reliable automated TOA generation, consider wrapping citations in semantic markup during drafting:

```markdown
<cite case="ashcroft-v-iqbal" reporter="556 U.S. 662" year="2009">_Ashcroft v. Iqbal_, 556 U.S. 662, 678 (2009)</cite>
```

Or for statutes:

```markdown
<cite statute="42-usc-1983">42 U.S.C. § 1983</cite>
```

Benefits:

- TOA extraction becomes a simple DOM query, not a regex battle
- Short-form references (`_Iqbal_`) can use the same tag with a `short="true"` attribute
- Page numbers can be auto-populated from the rendered PDF
- Audit can verify every `<cite>` tag matches an authority on disk

This is a future enhancement — the manual/regex approach works for now but does not scale.

## Optional upgrades

- Add a "**Key propositions list**" at the top (10-20 propositions that are load-bearing) and audit those first.
- Maintain a "**Known-good authority library**" for recurring standards (Rule 12, QI, probable cause, etc.) so you're not re-auditing basics each time.
- Add a "**court-facing candor check**": if a case is adverse but central, acknowledge it and distinguish it cleanly.

If you want, paste one paragraph from your response (with its citations) and I'll show what a **completed audit_item** looks like end-to-end, including a court-safe rewrite.
