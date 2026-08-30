# Full Authority-Audit Workflow

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

For each material generated or filing-near statement:

1. Split it into atomic propositions. A conjunction, embedded condition,
   exception, or second legal consequence ordinarily creates another audit unit.
   Preserve the exact filing location and exact text for each unit.
2. Write each proposition in plain English, scoped narrowly:
   - Bad: "Qualified immunity doesn't apply."
   - Good: "At the 12(b)(6) stage, the court must accept pleaded facts as true
     and may deny qualified immunity when the complaint plausibly alleges
     violation of clearly established law."

3. Give each proposition a stable ID and identify whether it is:
   - legal rule/standard,
   - application of rule to facts,
   - factual claim,
   - inference,
   - or procedural claim.

4. Mark whether each proposition is material to the answer or filing. Audit
   every material proposition under every remaining stage. New material
   propositions introduced by the audit receive the same treatment.

Deliverable: stable ID + filing location + exact atomic proposition + type +
materiality. No aggregate pass may hide a proposition that fails or remains
unresolved.

### Stage 2 - Validate authority identity (existence + metadata)

For each cited authority:

1. Record and verify the selected authority YAML, `SOURCE.yaml`, and exact
   relative document path inside `verified-authority`.
2. Record the explicit binding status and confirm it is legally correct for the
   governing court.
3. Confirm the case exists (correct caption, reporter, court, year).
4. Confirm you're using the correct version/source (official reporter vs slip
   opinion vs Westlaw/Lexis).
5. Record metadata:
   - court,
   - jurisdiction,
   - date,
   - whether binding in your court,
   - posture of the cited decision.

Fail conditions:

- case not found in the selected corpus YAML,
- missing or ambiguous authority status,
- wrong case,
- wrong year,
- wrong court,
- or a similarly named case substituted accidentally.

Deliverable: verified-unit path, cited-document path, recorded binding value,
"Library check: PASS/FAIL," and "Identity check: PASS/FAIL," with corrected cite
if needed.

### Stage 3 - Pinpoint verification (the "does it say that _there_?" test)

1. Go to the cited pinpoint.
2. Extract the smallest slice that contains the supposed rule
   (quote/paraphrase).
3. Confirm:
   - the text exists at that pinpoint,
   - every direct quote exists verbatim in the exact cited document,
   - the pinpoint isn't off by 1-5 pages due to PDF vs reporter pagination,
   - the quote isn't missing qualifiers ("generally," "in this case," "under
     these facts").

Deliverable: pinpoint snippet summary + "Pinpoint supports: YES/NO/PARTIAL". For
quoted text, also report `Exact quotation: PASS/FATAL` and the canonical
document path where it was checked.

### Stage 4 - Context verification (the "are you laundering dicta?" test)

Even if the text exists, read enough context to classify its source voice:

1. Is it a majority holding, court dicta, party argument, lower-court ruling
   under review, factual or procedural background, concurrence, dissent, or
   quoted secondary authority?
2. If it is court language, is it necessary to the judgment or dicta?
3. Is the statement conditional or fact-bound?
4. Is the authority addressing the same legal question or a different one?

Fail conditions:

- citing dicta as binding,
- citing a dissent like it's law,
- quoting a standard that was later rejected in the same opinion.

Deliverable: exact source voice + holding/dicta classification when applicable

- notes. Ambiguous or incorrect attribution fails closed.

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

For every claim, defendant, and challenged act, verify a separate fair-warning
record:

| Field              | Required content                                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Event              | Event date, stage, and challenged conduct                                                                                       |
| Rule               | The constitutional right or rule at the conduct-specific level                                                                  |
| Authority          | Case, court, publication and binding status, decision date, and pinpoint                                                        |
| Precedential force | Holding, alternative holding, implicit holding, dicta, silence or non-holding, appellate fact statement, or persuasive-only use |
| Comparison         | Material factual similarities and material differences                                                                          |
| Fair warning       | Why the authority made the alleged unlawfulness apparent on the event date                                                      |
| Status             | Verified, needs narrowing, or filing-critical GAP                                                                               |

Check actual probable cause separately from arguable probable cause. Do not use
a district-court decision, nonprecedential decision, or later-decided case as
the source of clearly established law. When several cases allegedly combine to
supply fair warning, verify the contribution and status of each case and explain
the combined rule. Apply the rule of orderliness and later-history checks before
approving the proposition.

### Stage 6 - Negative authority / undermining checks

For each key authority you rely on (and each adverse case you cite):

1. Does the decision contain limiting language that narrows the rule?
2. Does selected later-history documentation show it was criticized, limited,
   overruled, or abrogated?
3. Do selected later cases in your court change the test?
4. If your opponent cites the same case differently, who is right?

Deliverable: "Undermining risk: LOW/MED/HIGH" + recommended swap/additional
cite.

If the selected offline material is insufficient, return the gap. A distinct
authorized freshness-research invocation may gather candidate citator or
primary-source material, but a later offline audit must verify it before use.

### Stage 7 — Quote and parenthetical integrity

Quotes and parentheticals are common failure points — and parentheticals are the
#1 vector for AI hallucination. A fabricated parenthetical on a real case with a
correct citation is nearly undetectable without reading the source.

**Mandatory method**: For every parenthetical, you MUST:

1. Open the authority PDF (not your training data, not your memory of the case)
2. Read the actual holding and the text at the cited pinpoint
3. Verify that the parenthetical accurately describes what the court held or
   said
4. If the parenthetical describes a proposition that does not appear anywhere in
   the opinion: **MAJOR** (fabricated parenthetical)
5. If the parenthetical overstates, inverts, or materially mischaracterizes the
   holding: **MAJOR**

Additional rules for quoted text:

1. Quotes must preserve meaning; ellipses can't change substance.
2. If you paraphrase, you still must be faithful to qualifiers.

**Do not trust your own knowledge of what a case holds.** The entire point of
this stage is to catch propositions that sound right but aren't in the source.
Read the PDF.

Deliverable: "Quote integrity: PASS/FAIL" + corrected parenthetical + page in
PDF where verified (or "NOT FOUND IN SOURCE").

### Stage 8 - Record cite and inference audit (facts vs evidence)

For each factual claim, first classify it as a source observation, pleaded
allegation, party or court characterization, permitted inference, or GAP. Then:

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

### Stage 11 - Record correctness, groundedness, and provenance

For every atomic proposition:

1. Record correctness as `verified`, `incorrect`, or `unresolved`.
2. If correctness is `verified`, separately record groundedness as `grounded`,
   `misgrounded`, or `ungrounded`; otherwise use `not-applicable`.
3. Map every relied-on citation to the exact authority artifact, hash, domain
   YAML paths, pinpoint, source text, scope and qualifiers, jurisdiction,
   decision date, posture, precedential force, source voice, and support status.
4. Record the independent audit stage, exact input fingerprints, selected source
   IDs, execution time, and model or provider identity when available.
5. Render the machine-readable record under `proposition-audit.schema.json` and
   a human report with one section per proposition ID.

A real citation, working link, source list, snippet, or positive treatment
symbol does not establish proposition support. No aggregate pass may conceal an
incorrect, unresolved, misgrounded, or ungrounded proposition.
