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

For each sentence/paragraph with citations:

1. Write the proposition in plain English, scoped narrowly:

   - Bad: "Qualified immunity doesn't apply."
   - Good: "At the 12(b)(6) stage, the court must accept pleaded facts as true
     and may deny qualified immunity when the complaint plausibly alleges
     violation of clearly established law."

2. Identify whether the proposition is:

   - legal rule/standard,
   - application of rule to facts,
   - factual claim,
   - inference,
   - or procedural claim.

Deliverable: proposition statement + type.

### Stage 2 - Validate authority identity (existence + metadata)

For each cited authority:

1. Record and verify the canonical authority-unit path and its `SOURCE.yaml`.
2. Record `spec.binding` and confirm it is an explicit boolean whose value is
   legally correct for the governing court.
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

- case not found under the canonical verified-case root,
- missing or ambiguous `spec.binding`,
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
2. Is it criticized, limited, overruled, or abrogated?
3. Are there later cases in your court that changed the test?
4. If your opponent cites the same case differently, who is right?

Deliverable: "Undermining risk: LOW/MED/HIGH" + recommended swap/additional
cite.

_(If you have access to Shepard's/KeyCite, use it; if not, do a reasonable web
check for "overruled", "abrogated by", "limited by" and later circuit
authority.)_

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
