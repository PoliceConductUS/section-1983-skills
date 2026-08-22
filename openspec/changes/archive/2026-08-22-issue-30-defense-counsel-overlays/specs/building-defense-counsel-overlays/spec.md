## ADDED Requirements

### Requirement: Immutable public research snapshot

The skill SHALL consume one immutable versioned research snapshot containing
approved embedded source content, exact queries, retrieval dates, checked-
through date, deduplication method, declared coverage, known unavailable
records, actor and case identifiers, source roles, and SHA-256 fingerprints. It
MUST NOT browse during generation or validation, read an unlisted path or URL,
or incur PACER or another fee without separate explicit authorization.

Filed papers and official proceeding records MAY establish litigation behavior.
Bar directories, firm biographies, articles, CLE materials, and irrelevant
social media MUST NOT independently establish litigation behavior. Missing
public content and fee-gated records SHALL remain scoped gaps.

#### Scenario: Public docket coverage is incomplete

- **WHEN** the declared search identifies a fee-gated or unavailable record
- **THEN** the snapshot records the missingness and the overlay does not treat
  the visible records as a complete denominator

### Requirement: Separate identity and time-bounded counsel teams

The overlay SHALL maintain individual-attorney identity records separately from
counsel-team records. Identity records MAY contain verified professional name,
bar status, firms, appearances, represented parties, dates, and approved source
IDs. Team records MUST identify members, represented parties, effective dates,
litigation-alignment groups, and source IDs. Neither record type may contain a
historical argument, court treatment, current attack, pattern, or forecast.

#### Scenario: Counsel substitutes during the case

- **WHEN** a sourced withdrawal and appearance change the effective team
- **THEN** the prior team version remains immutable and a new time-bounded team
  version links to the applicable litigation-alignment groups

### Requirement: Exact professional attribution

Every behavior record SHALL use a supported attribution role distinguishing
signer, named author, oral advocate, appearance counsel, listed counsel, and
counsel team. Individual behavior requires direct source support for signer,
named-author, oral-advocate, or another equally direct attribution. Appearance
or listed status alone MUST NOT establish authorship or individual behavior. A
jointly filed paper SHALL default to counsel-team behavior absent direct
individual attribution.

#### Scenario: Attorney appears and is listed on a joint paper

- **WHEN** a source establishes only appearance and listed-counsel status
- **THEN** the validator permits identity and team membership but rejects an
  individual historical-argument attribution

### Requirement: Four separately attributable evidence layers

The four evidence layers SHALL remain separately keyed and fingerprinted. They
are historical arguments, judicial treatments, current-case attack links, and
forecasts. Historical arguments MUST preserve case, court, docket, posture,
represented party and alignment group, exact location and quotation, claim,
challenged act, element or defense, qualified-immunity prong when applicable,
requested relief, attribution, date, and source IDs.

Judicial treatment MUST link to one historical argument and identify the actual
court actor and source. It MUST NOT become counsel conduct. A current-attack
link MUST reference a canonical litigation-alignment attack ID and MUST NOT copy
the attack text. A forecast MUST remain a derived advisory record and MUST NOT
become historical fact.

#### Scenario: Court rejects a recurring defense argument

- **WHEN** an official order rejects a source-backed historical argument
- **THEN** the counsel assertion and court treatment remain distinct linked
  records and only the court actor receives the rejection conclusion

### Requirement: Complete pattern and forecast evidence

A recurring pattern, court-documented loss pattern, or next-move forecast SHALL
identify its declared comparable corpus, scope and selection method,
denominator, coded-record count, unresolved and unavailable missingness,
posture, supporting examples, contrary examples, confidence, source IDs, and
checked-through date. Every support and contrary record MUST belong to the
comparable set.

An incomplete denominator MAY support a bounded example but MUST NOT support an
`often`, `usually`, recurring-pattern, loss-rate, or forecast conclusion. A
forecast MUST describe only a professional litigation move, use calibrated
confidence, state limits, and MUST NOT use certainty, predict a case outcome, or
predict judicial behavior.

#### Scenario: Comparable public corpus is incomplete

- **WHEN** unresolved or unavailable records prevent a complete denominator
- **THEN** the overlay preserves bounded examples and gaps but emits no tendency
  or next-move forecast

#### Scenario: Complete comparable corpus contains contrary examples

- **WHEN** a bounded forecast is otherwise supported
- **THEN** the forecast identifies supporting and contrary examples, posture,
  denominator, missingness, confidence, sources, checked-through date, and
  limits

### Requirement: Comparative and privacy boundaries

Cross-case consistency records SHALL preserve the exact sourced positions being
compared. They MUST NOT assert concession, waiver, judicial estoppel,
misconduct, or bad faith unless a separately verified legal analysis establishes
that effect. The overlay MUST exclude family, politics, private life, protected
traits, rumors, personality assessments, irrelevant social media, threats,
deception, harassment, and instructions to manipulate an adversary or judge.

#### Scenario: Counsel takes different positions in two cases

- **WHEN** approved sources support a material difference
- **THEN** the overlay reports the bounded comparison and does not assign an
  automatic legal or moral consequence

### Requirement: Relevant review composition

Blind common-attack review jobs MUST receive no counsel identity, team,
behavior, treatment, pattern, or forecast data. Actual-adversary jobs MAY
receive only validated counsel-team records matching the target
litigation-alignment group, claim, defendants, challenged acts, posture, and
effective dates. A forecast MAY remain separately labeled advisory context but
MUST NOT be stated as an actual attack, remove a common attack, or suppress the
blind review.

#### Scenario: Two counsel teams represent different alignment groups

- **WHEN** one target is reviewed for the first group
- **THEN** its actual-adversary job excludes the other team's records and its
  blind job excludes all counsel records

### Requirement: Immutable counsel lifecycle and overrides

The repository SHALL publish a counsel-specific lifecycle guide defining source
hierarchy, attribution, research, creation, reuse, refresh, rebuild,
supersession, degradation, and filing consumption. Appearance, withdrawal,
substitution, changed team alignment, a new signed filing or oral argument,
verified identity or status change, new court treatment, material public
evidence, corrected attribution, or explicit user scope change MUST prompt a new
lifecycle decision.

Every superseded version SHALL remain immutable. A user override MAY change
research or review scope but MUST NOT rewrite source provenance, attribution,
checked dates, history, forecasts, or prior versions.

#### Scenario: User excludes an attorney from forecast research

- **WHEN** the user supplies a scoped exclusion
- **THEN** the effective research scope records the override while preserving
  the generated identity, attribution, prior forecast, and source history
