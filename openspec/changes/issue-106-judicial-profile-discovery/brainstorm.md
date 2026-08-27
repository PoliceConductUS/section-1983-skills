## Design Summary

Extend the existing Judicial Reasoning Profile acquisition operation with a
source-bounded CourtListener discovery recipe. Resolve the judge identity first,
preserve authorship, assignment, and referral as different relationships, then
narrow a declared candidate universe to Section 1983 cases involving police or
law-enforcement actors. Search metadata remains a lead until acquired primary
docket material verifies the judge relationship, claim, actor, and posture.

CourtListener and RECAP remain incomplete discovery/public-access sources.
PACER/CM-ECF is an optional official fallback when separately authorized; no
credential use or fee occurs without the trusted runtime and separate fee
approval. All sources remain ordinary files with `SOURCE.yaml` provenance under
the explicit output folder.

## Alternatives Considered

### CourtListener only

- **Approach:** Document judge-name discovery and stop when RECAP lacks a docket
  or document.
- **Advantages:** Smallest change and no paid-source boundary.
- **Disadvantages:** Leaves the profile corpus incomplete even when PACER can
  verify assignment, current status, or missing docket material.
- **Why not selected:** The approved design includes PACER as an optional
  official fallback without automatic credential or fee authority.

### Repository-owned CourtListener and PACER client

- **Approach:** Add executable API clients, credential handling, pagination,
  downloads, and PACER billing controls to this repository.
- **Advantages:** More automation.
- **Disadvantages:** Violates the thin-skill boundary, creates credential and
  billing risk, and exceeds the requested acquisition-contract change.
- **Why not selected:** General-purpose network tooling belongs in its owning
  repository and was not requested.

### Thin acquisition recipe with optional official fallback

- **Approach:** Update the existing skill, public guide, and OpenSpec contract
  with CourtListener query roles, candidate verification, provenance, exclusion,
  and PACER authorization rules. Add no client or credential storage.
- **Advantages:** Makes the supported path explicit, auditable, and install-local
  while preserving existing folder and network boundaries.
- **Disadvantages:** The trusted runtime or user must perform the actual API and
  PACER operations.
- **Why selected:** This is the narrowest design that supports the requested path
  without moving executable network functionality into the skills repository.

## Agreed Approach

Use the thin acquisition recipe with optional official fallback. The user
approved CourtListener discovery by judge followed by Section 1983 police-case
narrowing, with PACER supported only as an authorized fallback.

## Key Decisions

- Stable CourtListener judge IDs are preferred when supported; documented name
  queries remain available when an ID is unavailable.
- `author_id` or `judge`, `assigned_to_id` or `assignedTo`, and
  `referred_to_id` or `referredTo` represent different relationships and cannot
  substitute for one another.
- `suitNature`, `cause`, Section 1983 terms, and police terms retrieve candidates
  but do not establish corpus eligibility.
- Primary docket material must verify Section 1983, police involvement, judge
  relationship, and posture.
- Rejected and unresolved candidates retain inspectable reasons and source
  identity; search visibility is never the denominator.
- API tokens, PACER credentials, cookies, and authorization headers never enter
  durable outputs.
- PACER/CM-ECF use requires explicit access authorization and separate approval
  before any fee.

## Open Questions

None. Exact CourtListener parameters vary with the declared research scope and
current API, so the skill names supported search types and relationship fields
without hard-coding one universal query string.
