# Retrospective

## Outcome

Issue 29 turns an approved docket snapshot into an immutable, source-preserving
litigation-alignment overlay. The result determines which case-specific
adversary material may enter each fresh review without conflating the adversary,
plaintiff, magistrate judge, district judge, or appellate court.

## What RED established

The repository had no public contract for issue-scoped defendant grouping,
canonical attack/response/treatment ledgers, or blind-versus-actual review
slices. It also lacked a shared lifecycle for creating, refreshing, rebuilding,
superseding, and pinning case overlays.

## What worked

- One immutable embedded snapshot made source confinement and reproducibility
  testable without live docket access.
- Separate canonical ledgers prevented a response or judicial disposition from
  becoming an adversary status.
- Per-target, per-group review jobs made the two independent adversarial passes
  explicit and proved the leave motion and proposed amendment are distinct
  artifacts.
- A general lifecycle guide avoided duplicating common rules in judge and later
  counsel documentation.
- Naming the judge overlay a Judicial Reasoning Profile clarified its legitimate
  affirmative use while preserving the anti-gaming boundary.

## Review findings and corrections

The first full suite exposed the missing governance registry and runtime-source
provenance sentence. Whole-story review then found that locally valid fields
were not always linked to each other: source lists could disagree with quote
locations, dates could drift from filing dates, attacks could drift from group
dimensions, matrix links could cross attacks, judicial treatment could cite a
source issued by another actor, and target families could disagree with their
pinned sources. A second probe found malformed nested types could escape as
Python exceptions. Focused RED drove stable fail-closed findings for each case.

## Deviations

- Issue 29 deliberately does not research or profile defense attorneys. Issue 30
  owns attorney and counsel-team litigation-behavior profiles and their
  lifecycle documentation.
- The validator checks structure, provenance, linkage, grouping, and review
  slices. It does not determine whether a docket assertion is legally correct or
  whether an alignment rationale is persuasive.
- Judge reasoning research remains governed by the existing decision-corpus and
  transfer-card contracts; this story adds lifecycle integration and clearer
  profile scope rather than a second corpus format.

## Reusable lesson

Role separation requires more than different field names. Every role-specific
record must bind its source, date, actor, issue dimensions, and downstream links
to the same immutable evidence packet. A validator that checks each field in
isolation can still preserve a perfectly formatted misattribution.
