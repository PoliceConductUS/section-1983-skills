# Authority-Audit Record Schema

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
    text:
      "At the Rule 12(b)(6) stage, the court must accept pleaded facts as true
      and may deny qualified immunity when the complaint plausibly alleges
      violation of clearly established law."
    type: "legal_standard" # legal_standard | application | factual_claim | inference | procedural_claim
  citations:
    - raw_citation: "Case Name, 123 F.3d 456, 460 (5th Cir. 2019)."
      authority_type: "case" # case | statute | rule | regulation | secondary
      verified_unit_path: "/canonical/verified/cases/case-name"
      source_metadata_path: "/canonical/verified/cases/case-name/SOURCE.yaml"
      cited_document_path: "/canonical/verified/cases/case-name/documents/opinion.pdf"
      binding_level: "binding" # binding | persuasive | nonbinding
      binding_metadata: true # exact spec.binding value from SOURCE.yaml
      posture_in_authority: "appeal-from-12b6"
      pinpoint_claimed: "p. 460"
  verification:
    verified_library_check: "pass" # pass | fail
    binding_status_check: "pass" # pass | fail
    identity_check: "pass" # pass | fail
    pinpoint_check: "partial" # pass | fail | partial
    exact_quote_check: "not_applicable" # pass | fatal | not_applicable
    context_check:
      holding_or_dicta: "dicta"
      notes:
        "Statement appears in background discussion, not necessary to judgment."
    on_point_rating: "on-point-limited" # on-point-strong | on-point-limited | persuasive-only | distinguishable | inapplicable
    undermining_risk: "medium" # low | medium | high
  findings:
    - severity: "MAJOR" # FATAL | MAJOR | MODERATE | MINOR
      issue: "Quoted language exists but is dicta; posture differs."
      impact: "Overstates binding force; opponent can attack as misleading."
      fix:
        recommended_edit:
          "Rephrase as persuasive guidance and add a binding 12(b)(6) QI
          standard case."
        replacement_citations:
          - "Add binding circuit precedent directly addressing QI at 12(b)(6)."
  status: "needs-revision" # ok | needs-revision
```
