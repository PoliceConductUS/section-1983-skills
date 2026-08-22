## MODIFIED Requirements

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
