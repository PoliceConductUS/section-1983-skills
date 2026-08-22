# building-litigation-alignment-overlays Specification

## Purpose

Define an immutable, source-bounded method for deriving issue-scoped
litigation-alignment groups, separate adversary-attack, plaintiff-response, and
judicial-treatment ledgers, fresh blind and actual-adversary review plans, and
filing-version overlay pins from one approved docket snapshot.

## Requirements

### Requirement: Immutable docket snapshot input

The overlay skill SHALL consume exactly one immutable, versioned docket snapshot
containing approved embedded source content, stable source and actor
identifiers, filing metadata, checked-through date, and exact SHA-256
fingerprints. Overlay generation MUST NOT browse, read an unlisted path or URL,
or silently refresh the snapshot. The overlay MUST record the exact snapshot ID,
version, canonical fingerprint, and checked-through date.

#### Scenario: Docket changes after overlay generation

- **WHEN** a new or corrected docket source produces a different snapshot
- **THEN** the prior overlay remains immutable and is stale for current drafting
  until a new overlay version is generated and validated

### Requirement: Issue-scoped litigation-alignment groups

The overlay SHALL preserve every individual defendant and derive groups per
issue. Group members MUST share capacity, challenged act, relevant-time
knowledge position, qualified-immunity position, requested relief, and any other
material defense for that issue. A material divergence MUST split the members.
Every individual issue dimension MUST belong to exactly one effective group.

A municipality MUST remain separate from individual-capacity defendants unless
approved source IDs establish alignment for that particular issue. User
additions, exclusions, and regrouping MUST remain explicit overrides that
preserve the generated groups and provenance.

#### Scenario: Jointly represented officers diverge on qualified immunity

- **WHEN** two jointly represented officers assert materially different
  challenged acts or qualified-immunity positions for one claim
- **THEN** the effective overlay places them in separate groups for that issue
  while preserving both individual records

#### Scenario: User overrides a generated group

- **WHEN** the user directs a scoped regrouping
- **THEN** the overlay retains the generated group, records the instruction and
  consequence, and exposes a separate effective group result

### Requirement: Role-separated canonical ledgers

The overlay SHALL contain separately keyed and fingerprinted adversary-attack,
plaintiff-response, and judicial-treatment ledgers. An adversary attack MUST NOT
contain a `plaintiff-*`, magistrate-judge, district-judge, appellate-court,
`judge-*`, or `court-*` response or treatment field. Plaintiff coverage MUST use
plaintiff-prefixed states and remain outside the attack record. Judicial
treatment MUST identify the actual actor and stage.

#### Scenario: Plaintiff answers an attack later addressed by the court

- **WHEN** an adversary attack, plaintiff response, magistrate recommendation,
  and district order concern the same issue
- **THEN** four separately attributable records remain canonical and a derived
  row links them without reassigning any position

### Requirement: Judicial-stage attribution

The judicial ledger MUST distinguish magistrate-judge recommendations,
district-judge adoption, rejection, modification, and independent reasoning, and
appellate disposition. An adoption, rejection, or modification MUST link to the
recommendation it treats and MUST NOT convert the recommendation author's
reasoning into the district judge's independent reasoning. Uncertain authorship
or treatment MUST remain a scoped gap.

#### Scenario: District judge adopts a recommendation

- **WHEN** a district order adopts a magistrate recommendation without supplied
  independent reasoning
- **THEN** the ledger attributes the recommendation reasoning to the magistrate
  judge and records only the adoption disposition for the district judge

### Requirement: Source-preserving derived matrix

The derived issue matrix SHALL join attack, response, judicial treatment, and
current procedural status by stable foreign keys. Its source IDs MUST equal the
union of linked canonical records. It MUST NOT copy canonical position text or
treat silence as agreement, non-opposition, withdrawal, rejection, or adoption.
Missing response or treatment links MUST use explicit unavailable states.

#### Scenario: No plaintiff response is supplied

- **WHEN** the snapshot contains an attack but no approved plaintiff-response
  source
- **THEN** the matrix reports plaintiff response unavailable and does not infer
  that the attack was unanswered or conceded

### Requirement: Per-target and per-group independent review plan

The review plan SHALL contain distinct fresh `blind-common-attack` and
`actual-adversary` jobs. A blind job MUST receive no adversary attack, judge,
attorney, counsel-team, historical behavior, judicial treatment, pattern, or
forecast overlay ID or content. An actual job MUST receive only current attacks
and validated counsel-team material relevant to its group, claim, defendants,
challenged acts, posture, target, and effective date.

A bounded counsel forecast MUST remain separately labeled advisory context. It
MUST NOT become an actual attack, remove a common attack, suppress the blind
job, or displace controlling law. A motion and proposed amended complaint remain
separate targets and therefore produce distinct jobs.

When no adversary filing exists, the plan MUST report
`actual-adversary-unavailable`, create two distinct blind common-attack jobs,
and MUST NOT invent an actual-adversary or counsel forecast job.

#### Scenario: Relevant counsel profile exists

- **WHEN** one group has a validated effective counsel-team overlay
- **THEN** its actual-adversary job receives only that group's relevant counsel
  slice and its blind job receives no counsel material

#### Scenario: Counsel forecast omits a common attack

- **WHEN** the validated forecast does not identify one common attack
- **THEN** the blind common-attack job still tests that attack independently

### Requirement: Filing-version overlay manifest

Each filing version that consumes specialized overlays SHALL pin every consumed
overlay by kind, stable ID, version, fingerprint, checked-through date,
validator result, and source snapshot. Supported kinds SHALL include
litigation-alignment, judge, counsel-identity, and counsel-team overlays. The
manifest MUST keep the Judicial Reasoning Profile, controlling-law analysis,
litigation-alignment groups, individual-attorney identity, counsel-team
behavior, and user overrides separate.

A failing validator result, mismatched snapshot, stale checked-through date, or
irrelevant counsel-team scope MUST produce no specialized drafting change.

#### Scenario: Filing manifest pins counsel overlays

- **WHEN** a filing uses attorney identity and counsel-team behavior
- **THEN** it pins those immutable overlays separately from the judge and
  litigation-alignment overlays and preserves their distinct source snapshots

### Requirement: Public lifecycle and validation method

The repository SHALL publish a general overlay lifecycle guide and an
install-local validator. The guide MUST define inventory, prerequisites,
create/reuse/refresh/rebuild/supersede decisions, immutable versions,
event-driven invalidation, degradation, overrides, precedence, review routing,
and filing-manifest pins. It MUST include a generic complaint-to-motion-to-
amendment-to-recommendation-to-order lifecycle and MUST NOT contain private case
data or attorney research.

#### Scenario: Material docket event occurs

- **WHEN** a new filing, recommendation, order, assignment, party alignment, or
  explicit override changes overlay inputs
- **THEN** the method preserves the prior version and requires a new immutable
  overlay version before specialized drafting resumes
