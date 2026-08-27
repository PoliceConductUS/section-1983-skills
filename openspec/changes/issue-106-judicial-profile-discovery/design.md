## Context

The existing profile builder separates internet-authorized acquisition from
offline compilation and already emits ordinary source bytes with `SOURCE.yaml`
provenance. It lacks a domain recipe for moving from an assigned judge to a
bounded Section 1983 police-case candidate universe. CourtListener exposes
separate search types and judge relationship fields, while its search and RECAP
coverage can be incomplete. PACER/CM-ECF can supply official docket information
but introduces credential and fee authority that the skill cannot infer.

## Goals / Non-Goals

**Goals:**

- Define CourtListener judge identity and case-discovery steps.
- Keep opinion authorship, docket assignment, and referral distinct.
- Require primary-source verification of Section 1983, police involvement,
  judge relationship, and posture.
- Preserve query provenance, candidate dispositions, exclusions, coverage, and
  gaps without secrets.
- Permit PACER/CM-ECF only through explicit access and fee gates.

**Non-Goals:**

- Build a CourtListener or PACER client.
- Hard-code one universal search query or infer API credentials.
- Add profile fields, network credentials, billing logic, CaseGraph, graph,
  package, repository, or persistence behavior.
- Treat discovery metadata as legal authority or corpus eligibility proof.

## Decisions

### Extend the existing acquisition operation

The skill already owns public source acquisition and the transition to later
read-only compilation. Keeping this path there avoids a second overlapping
profile-source skill.

### Use a positive acquisition recipe

The guidance states the ordered result shape: resolve identity, declare scope,
search each applicable relationship, narrow leads, verify primary materials,
record candidate dispositions, and persist source/provenance bytes. This
addresses an omitted workflow rather than a deliberate discipline violation.

### Preserve relationship and evidence boundaries

CourtListener opinion, docket, and RECAP searches have different judge fields.
The skill records which relationship was queried and which primary artifact
proved it. Search fields and police-related terms are leads only.

### Make PACER an authorized fallback

PACER/CM-ECF may verify official docket identity, assignment, status, and
completeness. The skill stops unless access is explicitly authorized and any fee
is separately approved. Credentials remain runtime-only.

### Test the public contract without adding network code

Focused tests exercise the install-local skill and guide contract: supported
search types/fields, verification and rejection boundaries, provenance and
secret exclusions, PACER authorization/fee requirements, and unchanged offline
compilation. No test calls an external service.

## Risks / Trade-offs

- **API fields can evolve** → Name the current supported relationships and
  require checked dates rather than embedding a client implementation.
- **Keyword filtering can omit or overinclude cases** → Treat every filter as a
  retrieval lead and require primary-source review plus explicit exclusions and
  missingness.
- **PACER can incur fees** → Require separate fee approval before retrieval and
  leave unavailable material as a gap.
- **Static contract tests cannot prove agent behavior** → Preserve the absence
  of newly authorized pressure agents in verification and cover the concrete
  install-local acquisition contract deterministically.

## Migration Plan

Publish the additive skill and guide changes in the existing stacked PR. No
stored profile or source folder requires migration. Reverting the commit restores
the prior generic acquisition guidance.

## Open Questions

None.
