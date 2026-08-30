## ADDED Requirements

### Requirement: Guide defines reproducible public case discovery

The judge-overlay authoring guide MUST define the CourtListener judge-first
case-discovery method, the distinction among opinion authorship, docket
assignment, and referral, the required court, tenure or date, case category,
posture, and research-question narrowing, and the primary-document verification
needed to establish Section 1983 and police or law-enforcement involvement. The
guide MUST require sanitized query provenance and an inspectable disposition for
each reviewed candidate, MUST explain that search metadata and search-result
counts do not establish a complete corpus, and MUST prohibit persisting access
secrets.

The guide MUST identify PACER or court-specific CM/ECF as the optional official
fallback for docket identity, assignment, status, or completeness. It MUST keep
access authorization separate from fee approval and MUST require an explicit gap
instead of implying that unavailable or unapproved official material was
checked.

#### Scenario: Maintainer builds a police Section 1983 judge corpus

- **WHEN** a maintainer follows the guide to find candidate cases by judge
- **THEN** the resulting acquisition record distinguishes discovery leads from
  primary-document verification, identifies included and excluded candidates,
  and preserves unresolved coverage gaps without exposing credentials
