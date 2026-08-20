---
name: audit-authorities
description:
  "Use when auditing citations, authorities, quotations, pinpoints,
  procedural-posture fit, record support, distinguishing claims, or
  clearly-established-law analysis in a pleading, amendment proffer, motion,
  response, brief, RRD, or filing-ready legal document."
---

# SKILL: Audit Authorities, Citations, and Differentiators in a Legal Response

## Goal

Verify that every cited authority, factual assertion, and "differentiator"
(distinguishing fact/holding) is:

1. **Real and correctly identified**
2. **Accurately described** (holding vs dicta, standard, posture)
3. **Pinpoint-supported** (the cited page/paragraph actually says what is
   claimed)
4. **On-point** (relevant jurisdiction, procedural posture, materially similar
   facts)
5. **Not undermined** (distinguished, limited, overruled, abrogated, or
   factually inapplicable)
6. **Used honestly** (no "laundering" of a proposition through a quote or
   parenthetical)

This skill applies to complaints, amendment proffers, RRDs, motions, responses,
replies, briefs, declarations, and appendices.

## Project Integration

### Input files

Resolve the controlling draft, verified-authority root, source units, and
audit-output location from the repository instructions. If no repository schema
exists, ask for or identify explicit paths. A citation tracker is optional and
never replaces the document body or authority source.

### Output file

Write the audit where the repository requires. If no location is defined, return
the structured audit without inventing a source-tree path.

### Authority sourcing and verification

Resolve the canonical verified-case root from the project instructions, source
manifest, control file, or an explicit path supplied by the user. If none of
those identifies the root, ask for it and do not mark any case citation
verified. A public or installed skill must not assume a machine-specific path.

Every case citation must pass all three gates below before the citation or the
document can be marked verified:

1. **Verified-library gate.** Find the case's authority unit inside the resolved
   canonical verified-case root. Record the unit path, `SOURCE.yaml` path, and
   exact cited document. A downloaded PDF elsewhere, a web result, a citation
   tracker, or memory of the case does not pass. If the case is absent, mark the
   citation **FATAL / filing-critical GAP**. Do not silently add it to the
   verified library.
2. **Binding-status gate.** Open that unit's `SOURCE.yaml` and require an
   explicit `spec.binding: true` or `spec.binding: false`. Record the value and
   verify it against the deciding court, publication or precedential status,
   governing court, later history, and rule of orderliness. A case may be
   described as binding only when the metadata says `true` and the legal check
   agrees. A `false` case must be labeled nonbinding or persuasive. Missing or
   ambiguous binding metadata is a **FATAL / filing-critical GAP**.
3. **Exact-quotation gate.** For every direct quotation, open the exact opinion,
   order, concurrence, dissent, or other document cited from the verified unit.
   The quoted words must exist verbatim in that exact document at the stated
   pinpoint. A match in a different document, a summary, a representation, or a
   later opinion does not pass. If the exact quotation is not present, mark it
   **FATAL** and do not approve the filing text.

External retrieval may help investigate a gap, but it does not satisfy these
gates until the user-authorized verified authority unit and its metadata exist
under the canonical root.

After the three gates pass, complete the remaining authority audit:

1. Use the verified unit's source metadata and canonical document.
2. If later-history or identity confirmation requires another source, use
   primary sources where available:
   - **SCOTUS**: Library of Congress
     (`tile.loc.gov/storage-services/service/ll/usrep/`)
   - **Fifth Circuit**: `ca5.uscourts.gov/opinions/`
   - **General**: CourtListener RECAP archive
3. Preserve the source and retrieval provenance where repository rules require.
4. Do not mark an authority verified merely because a PDF was downloaded.
   Verification requires identity, court, publication and binding status,
   proposition and pinpoint, holding classification, procedural posture,
   pre-event timing when material, later history, and any rule-of-orderliness
   check.
5. If a load-bearing or filing-near authority cannot be verified, mark a
   filing-critical GAP. Do not treat the document as filing-ready.

### Audit depth by citation role

- **Plaintiff's affirmative authorities**: Full 10-stage audit (all stages)
- **Defendants' authorities cited only to distinguish**: Stages 2 (identity), 5
  (on-point / posture match), and 9 (differentiator validity) only - skip
  proposition-level pinpoint and context review when no proposition is being
  attributed. The verified-library gate, binding-status gate, and exact-
  quotation gate still apply to every cited case and every direct quote without
  exception.

### Direct quote verification (CRITICAL)

For every phrase in quotation marks attributed to an authority:

1. Locate the **exact text** in the exact cited document within the verified
   authority unit at the cited pinpoint
2. Compare **character-by-character** (watch for: missing qualifiers like
   "generally," "in this case," "under these facts"; changed verb tenses;
   omitted conditions)
3. If the quote does not appear verbatim in the authority: **FATAL**
4. If the quote appears but at a different pinpoint: **MODERATE** (fix the
   pinpoint)
5. If the quote is a paraphrase presented as a direct quote: **MAJOR**

This catches fabricated language attributed to real cases - a common AI-assisted
drafting failure.

## Attorney expectation model (how it's _supposed_ to work)

In competent practice, citation auditing is not "spot checking." It's a
**chain-of-support test**:

- **Every legal proposition** must be supported by authority that actually
  states it **in the context claimed**.
- **Every factual assertion** must be supported by record evidence (exhibits,
  declarations, transcripts).
- **Every key inference** must be tagged as inference and must be reasonable
  under the governing standard.
- **Every use of precedent** must respect:
  - jurisdiction (binding vs persuasive),
  - procedural posture (MTD vs SJ vs trial),
  - standard (plausibility vs summary judgment evidence),
  - and material similarity of facts.

Your audit should catch: wrong pinpoints, misleading parentheticals, overbroad
"stands for" claims, and "case name drop" citations that don't actually support
the sentence they're attached to.

## Definitions

- **Authority**: case, statute, rule, regulation, treatise, jury instruction,
  local rule, secondary source.
- **Proposition**: the legal claim _made in your text_ (the "why the court
  should rule for you" part).
- **Pinpoint**: the exact location the proposition appears
  (page/paragraph/Westlaw star page).
- **Differentiator**: a fact or legal feature that distinguishes your case from
  adverse authority (or aligns you with favorable authority).
- **Posture**: where you are procedurally (12(b)(6), 12(c), 56, preliminary
  injunction, etc.).
- **Holding vs dicta**:
  - **Holding** = necessary to the judgment.
  - **Dicta** = not necessary; may still be persuasive but should not be
    represented as binding.

## Output contract (what you produce)

For each citation (and each differentiator that matters), produce one structured
audit record with:

- what the brief claims,
- what the authority actually says,
- whether it supports the claim,
- and what to fix.

### Severity levels

- **FATAL**: authority does not exist, wrong case, wrong statute, or proposition
  not present; or citation contradicts statement.
- **MAJOR**: authority exists but posture/standard/facts mismatch makes it
  misleading as used.
- **MODERATE**: partially supported; needs narrowing, better phrasing, or better
  cite.
- **MINOR**: formatting/pinpoint/parenthetical cleanup; still basically correct.

## Detailed audit workflow

For a full authority audit, read
[references/full-audit-workflow.md](references/full-audit-workflow.md)
completely before beginning. It owns Stages 0 through 10, including the
clearly-established-law audit. For a deliberately limited adverse-authority
audit, use only the stages required by **Audit depth by citation role** above.
The verified-library, binding-status, and exact-quotation gates in this
entrypoint always control.

## Quality bar: "Would I sign this?"

Before finalizing:

- Every cited case exists under the canonical verified-case root, and the audit
  records its authority-unit path and exact cited document.
- Every case unit has an explicit, legally checked `spec.binding` value; the
  draft never calls a `false` or unresolved authority binding.
- Every direct quotation exists verbatim in the exact cited document at the
  cited pinpoint.
- Every paragraph with a legal conclusion has at least one authority that
  **directly supports** it.
- Every key authority is not only correct, but **not misleading** in posture and
  scope.
- Every adverse case is either:
  - fairly summarized and distinguished, or
  - acknowledged with limiting language (if it hurts you).

- Every record cite is accurate.

## Structured audit records

When the requested output is YAML or another machine-readable audit ledger, read
[references/audit-record-schema.md](references/audit-record-schema.md)
completely and use its fields and status vocabulary.

## Opinion (what matters most, practically)

If you do only three things, do these:

1. **Posture match** (MTD vs SJ) - this is the #1 way briefs accidentally become
   misleading.
2. **Holding vs dicta** - courts hate "case says X" when it's dicta.
3. **Material facts** - the "on-point" question is usually won or lost on 1-2
   decisive facts.

## Table-of-authorities reconciliation

When the deliverable contains a Table of Authorities or a Statutes and Rules
table, read [references/toa-reconciliation.md](references/toa-reconciliation.md)
completely after remediation and perform that reconciliation before approval.

## Optional upgrades

- Add a "**Key propositions list**" at the top (10-20 propositions that are
  load-bearing) and audit those first.
- Maintain a "**Known-good authority library**" for recurring standards (Rule
  12, QI, probable cause, etc.) so you're not re-auditing basics each time.
- Add a "**court-facing candor check**": if a case is adverse but central,
  acknowledge it and distinguish it cleanly.

If you want, paste one paragraph from your response (with its citations) and
I'll show what a **completed audit_item** looks like end-to-end, including a
court-safe rewrite.

## Output provenance

Every returned artifact must identify the actual approved source identity and
checked date used.
