## ADDED Requirements

### Requirement: CourtListener discovery preserves judge identity and candidate disposition

The acquisition operation MUST document a CourtListener REST API discovery path
that resolves the judge before searching cases, prefers a stable judge
identifier, and permits a documented name-query fallback. It MUST distinguish
opinion authorship from docket assignment and referral, and MUST narrow
candidates by applicable court, judicial tenure or date range, case category,
procedural posture, and the profile's research question. Nature-of-suit,
cause-of-action, Section 1983, and police or law-enforcement search terms MUST
remain discovery leads rather than proof that a candidate belongs in the profile
corpus.

Before inclusion, the acquisition operation MUST require primary docket material
to verify the judge relationship, Section 1983 basis, police or law- enforcement
involvement, and relevant posture. It MUST preserve sanitized query provenance,
stable result identity, pagination or cursor identity, selection or exclusion
status, and an inspectable reason for every reviewed candidate. It MUST NOT
persist API tokens, credentials, cookies, authorization headers, or other
secrets.

#### Scenario: Judge-name search returns mixed civil-rights cases

- **WHEN** CourtListener returns candidates that include non-police cases,
  agency-only matters, unresolved judge relationships, or non-Section 1983
  claims
- **THEN** acquisition retains each reviewed candidate's stable identity and
  exclusion reason and admits only candidates independently verified from
  primary docket material

### Requirement: PACER fallback requires separate access and fee authority

The acquisition operation MUST treat PACER or court-specific CM/ECF as an
optional official fallback for docket identity, assignment, status, and
completeness. It MUST require explicit authorization to use the access method
and separate approval before incurring any fee. Credentials MUST remain in the
authorized runtime and MUST NOT be written to the acquisition output, source
provenance, profile, receipt, or temporary files.

#### Scenario: CourtListener coverage is incomplete

- **WHEN** a candidate cannot be verified completely from public CourtListener
  and court materials
- **THEN** acquisition records the coverage gap and uses PACER or CM/ECF only
  after both access authorization and any required fee approval are present
