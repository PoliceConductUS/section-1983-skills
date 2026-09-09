## Design Summary

Create one independently installable `validating-court-facing-assertions` skill
as the semantic owner of post-draft assertion validation. It reviews one
explicit court-facing target read-only, decomposes all text into propositions,
traces each proposition to original sources, checks required-content omissions,
applies assertion-level freshness rules, and returns one structured report for
trusted-host publication. Drafting skills perform any authorized correction in a
separate stage and send the revised document through targeted revalidation and
final whole-document and rendered-file review.

## Alternatives Considered

### Put the contract in `section-1983-drafting`

- **Approach:** Make the umbrella drafting skill own both drafting orchestration
  and the detailed validation report.
- **Advantages:** Adds no new public skill and keeps the main filing workflow in
  one package.
- **Disadvantages:** Standalone review and audit skills would depend on a broad
  drafting package, and the read-only validation role would be less distinct
  from the editing role.
- **Why not chosen:** The repository already treats independent quality control
  as a separate authority boundary.

### Copy the complete workflow into every affected skill

- **Approach:** Expand complaint, Rule 59(e), Monell, authority-audit,
  adversarial-review, and Filing CI instructions independently.
- **Advantages:** Every installed package would contain all wording locally.
- **Disadvantages:** Multiple semantic owners would drift and contradict the
  requested single shared contract.
- **Why not chosen:** It reproduces the exact duplication this change is meant
  to eliminate.

### Dedicated shared validation skill

- **Approach:** Add one public skill that owns the detailed semantic validation
  contract and have applicable skills reference it by name and responsibility.
- **Advantages:** One semantic owner, an explicit read-only role, independent
  installation, and narrow integration points for domain specialists.
- **Disadvantages:** Callers must load one additional skill and fail closed when
  it is unavailable.
- **Why chosen:** It preserves clear authority boundaries while giving the
  workflow one reusable source of truth.

## Agreed Approach

Use the dedicated shared validation skill. Preserve only the compact
install-local filesystem, immutable-report, and non-mutation safeguards already
required in independently installed QC-capable packages. Do not duplicate the
new assertion-validation semantics in consuming skills.

## Key Decisions

- `validating-court-facing-assertions` owns proposition decomposition, source
  tracing, substantive validation, omission coverage, report statuses,
  assertion-level freshness, the Mermaid summary, and validation stopping
  criteria.
- `section-1983-drafting` owns orchestration and sends findings to a separately
  authorized drafting or revision stage.
- Complaint, Rule 59(e), and Monell skills retain document-specific drafting
  requirements; authority auditing retains authority-specific verification;
  adversarial review remains a downstream defense attack; Filing CI remains
  deterministic.
- The skill has no CaseGraph dependency. A report may preserve an optional
  CaseGraph route only when that route is present in declared inputs.
- Independent run receipts remain append-immutable. A stable private current
  report, when a case project uses one, is maintained by the trusted case
  controller and may be proposed as new bytes by the skill; no input is
  overwritten.
- Behavioral fixtures exercise semantic failures. Deterministic checks verify
  contracts and status arithmetic but do not claim to decide support or legal
  sufficiency.

## Open Questions

None. The user approved the dedicated shared-skill design.
