# Table-of-Authorities Reconciliation

## Stage 11 — Regenerate Table of Authorities and Statutes/Rules

After completing the audit and any remediation, regenerate the TOA and
Statutes/Rules tables in the response document to reflect exactly what is cited
in the body.

### Process

1. **Extract all case citations from the body** (everything after the TOA,
   starting from INTRODUCTION or ARGUMENT). Parse each unique case with its full
   citation format (name, reporter, year).

2. **Extract all statute/rule citations from the body.** Include federal
   statutes (42 U.S.C. §), Federal Rules (Fed. R. Civ. P., Fed. R. Evid.), state
   statutes (Tex. Penal Code, Tex. Code Crim. Proc.), and local rules.

3. **Preserve existing page numbers.** If the document already has a TOA with
   page numbers filled in, carry those forward for any case that remains cited.
   New citations get empty page number fields. Removed citations are dropped.

4. **Sort cases alphabetically** by case name (ignore "In re", "Estate of", etc.
   for sort — sort on the substantive first word).

5. **Sort statutes/rules** by: federal statutes first (by title number), then
   Federal Rules (Civ. P., then Evid.), then state statutes (alphabetical by
   code name), then local rules.

6. **Replace the existing TOA and Statutes/Rules tables** in the document. Find
   the `### Cases` and `### Statutes and Rules` sections within the
   `## TABLE OF AUTHORITIES` block and replace their table contents entirely.

7. **Verify no orphans**: every case in the new TOA must appear in the body;
   every case in the body must appear in the TOA. Report any mismatches.

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

This stage ensures the TOA is always in sync with the body after edits,
additions, or removals during the audit.

### Recommended: Citation markup for reliable extraction

Regex-based citation extraction is inherently fragile due to format variations
(short-forms like `_Iqbal_`, signal words like `_See_`, split citations across
lines). For reliable automated TOA generation, consider wrapping citations in
semantic markup during drafting:

```markdown
<cite case="ashcroft-v-iqbal" reporter="556 U.S. 662" year="2009">_Ashcroft v.
Iqbal_, 556 U.S. 662, 678 (2009)</cite>
```

Or for statutes:

```markdown
<cite statute="42-usc-1983">42 U.S.C. § 1983</cite>
```

Benefits:

- TOA extraction becomes a simple DOM query, not a regex battle
- Short-form references (`_Iqbal_`) can use the same tag with a `short="true"`
  attribute
- Page numbers can be auto-populated from the rendered PDF
- Audit can verify every `<cite>` tag matches an authority on disk

This is a future enhancement — the manual/regex approach works for now but does
not scale.
