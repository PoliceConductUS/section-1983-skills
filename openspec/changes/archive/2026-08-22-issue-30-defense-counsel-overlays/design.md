# Design

## Context

Issue 29 supplies an immutable docket snapshot, issue-scoped litigation-
alignment groups, current adversary attacks, and blind-versus-actual review
plans. Issue 30 adds a different evidence layer: professional litigation
behavior attributable to identified defense attorneys or a time-bounded counsel
team across approved public matters. The new layer consumes immutable embedded
research, links rather than duplicates current attacks, and remains subordinate
to controlling law and the independent common-attack pass.

## Goals / Non-Goals

**Goals:**

- Reproduce every counsel conclusion from one immutable research snapshot.
- Separate identity, attribution, historical arguments, judicial treatment,
  current attacks, and forecasts.
- Preserve individual attorneys while treating unsupported joint conduct as team
  conduct only.
- Permit calibrated professional next-move forecasts with complete provenance,
  denominator, missingness, and contrary evidence.
- Integrate only relevant counsel-team material into actual-adversary review and
  filing manifests.
- Explain when counsel overlays may be reused and when a new immutable version
  is mandatory.

**Non-Goals:**

- Personal, political, family, personality, protected-trait, rumor, or
  irrelevant social-media profiling.
- Certainty about future conduct, case-outcome prediction, or judicial behavior
  prediction.
- Automatic concession, waiver, estoppel, bad-faith, or misconduct conclusions.
- Paid retrieval without separate explicit authorization.
- Editing a filing or replacing controlling-law analysis.

## Decisions

### One public skill and two new machine artifacts

Add `building-defense-counsel-overlays` with:

1. `counsel-research-snapshot.schema.json` for immutable approved public-source
   content, research queries, coverage, retrieval dates, actors, cases, and
   source fingerprints; and
2. `defense-counsel-overlay.schema.json` for separately fingerprinted identity,
   team, historical argument, judicial treatment, current-attack link, pattern,
   forecast, override, and gap ledgers.

One standard-library validator checks the public schema shape and cross-record
semantics. It accepts no path or URL inside the artifacts, performs no network
or fee-incurring call, emits stable findings with paths, and exits nonzero on
errors.

The existing filing-overlay manifest adds `counsel-identity` and `counsel-team`
pin kinds. The litigation-alignment validator continues to own the filing
manifest because it composes all case-overlay kinds for one filing version.

### Immutable research snapshot and source hierarchy

The snapshot embeds approved content and SHA-256 for each source. It records
exact search queries, retrieval date, checked-through date, deduplication
method, coverage declaration, known unavailable records, and fee-gated gaps.

Source roles are explicit:

1. current docket and filed papers;
2. official dockets, opinions, orders, hearing transcripts, and oral-argument
   records;
3. CourtListener or RECAP public records;
4. official bar directories for identity and status;
5. firm biographies only for identity, affiliation, and expressly claimed
   experience;
6. attorney-authored public articles and CLE material as bounded professional
   context; and
7. other approved public case artifacts with verified identity.

Only filed papers and official proceeding records may establish litigation
behavior. Identity, firm, article, or CLE sources cannot independently establish
that counsel made a litigation argument. Missing public coverage remains a gap;
the skill never purchases PACER content or treats the visible subset as a
complete denominator.

### Attribution and time-bounded counsel teams

Identity records contain stable attorney ID, verified professional name, bar
status and checked date, firm affiliations with effective dates, case
appearances, represented parties, and source IDs. They contain no litigation
behavior.

Team records identify stable team ID, member attorney IDs, effective date range,
represented parties, litigation-alignment group IDs, and source IDs. A team is
case- and time-bounded; appearance, withdrawal, substitution, or changed group
alignment produces a new version.

Every behavior record names one attribution role:

- `signer`;
- `named-author`;
- `oral-advocate`;
- `appearance-counsel`;
- `listed-counsel`; or
- `counsel-team`.

Only signer, named-author, oral-advocate, or another direct approved source may
support individual behavior. Appearance or listed counsel may establish identity
and team membership but not authorship. A jointly filed paper defaults to
`counsel-team` unless direct evidence supports an individual attribution.

### Four canonical evidence layers

Historical arguments preserve the case, court, docket, posture, represented
party/group, exact location and quotation, claim, challenged act, element or
defense, qualified-immunity prong when applicable, requested relief,
attribution, date, and source IDs.

Judicial treatments link to one historical argument, identify the actual court
actor and source, and preserve whether it was recommended, adopted, rejected,
modified, superseded, reversed, vacated, or unresolved. They do not rewrite the
counsel assertion or attribute a court conclusion to counsel.

Current-attack links refer to canonical Issue 29 attack IDs and relevant counsel
team IDs. They do not copy the current attack text or convert plaintiff/court
statuses into counsel behavior.

Forecasts are separately keyed derived records. They never become historical
facts. Patterns and forecasts link to their exact historical arguments and
judicial treatments.

### Pattern and forecast strength

A recurring pattern or next-move forecast requires a declared comparable set,
scope, selection method, denominator, coded-record count, unresolved and
unavailable missingness, posture, supporting examples, contrary examples, source
IDs, checked-through date, and calibrated confidence. Every cited support or
contrary record must belong to the declared comparable set.

An incomplete denominator may support a bounded example, not an `often`,
`usually`, recurring-pattern, loss-rate, or forecast conclusion. A forecast must
describe a professional litigation move, use `low`, `moderate`, or `high`
confidence, state reasons and limits, and never use certainty words such as
`will`, `always`, or `never`. It cannot predict the case outcome or a judge's
behavior.

Cross-case inconsistency remains a comparison between exact sourced positions.
It never becomes waiver, concession, estoppel, misconduct, or bad faith unless a
separate verified legal analysis supplies that legal effect. Court-documented
loss patterns use only linked judicial-treatment records and remain separate
from counsel assertions.

### Review composition

Blind common-attack jobs contain no counsel identity, team, behavior, treatment,
pattern, or forecast data. Actual-adversary jobs may contain only counsel-team
records that match the target litigation-alignment group, claims, defendants,
challenged acts, posture, and effective dates. Individual identity data enters
only as necessary to resolve attribution; irrelevant attorney records remain
excluded.

The actual review may receive a validated bounded forecast as advisory context.
It remains separately labeled, cannot be stated as an actual attack, cannot
remove a common attack, and cannot displace the blind job. The Judicial
Reasoning Profile, controlling law, current attacks, and counsel profile remain
separate source layers in the filing manifest.

### Lifecycle and documentation ownership

`COUNSEL_OVERLAYS.md` owns counsel-specific creation, research, attribution,
forecast, refresh, rebuild, and supersession rules. Create identity overlays
after counsel identity is verified. Create a team overlay only after a sourced
appearance or filing establishes the team. Create behavior and forecast records
only after the required public corpus exists.

Reuse requires the same identity/status, team membership, alignment scope,
source snapshot, checked-through date, corpus coverage, and passing validator.
An appearance, withdrawal, substitution, changed representation or alignment,
new signed filing or oral argument, verified status change, new judicial
treatment, material public evidence, corrected attribution, or explicit user
scope override triggers a refresh or rebuild into a new immutable version.

User overrides may add or exclude research and review scope. They cannot rewrite
sources, attribution, checked dates, history, forecasts, or earlier versions.
`OVERLAYS.md` continues to own shared inventory, precedence, manifests, and
immutable-version rules and links to the counsel guide.

## Testing

- Structural tests require the exact public skill package, two install-local
  schemas, validator, generic fixtures, README/router/governance routes, counsel
  guide, general-guide link, and modified manifest kinds.
- Validator tests use synthetic public-source snapshots and overlays to prove
  source/hash integrity, exact attribution roles, individual/team separation,
  team date/alignment linkage, ledger separation, cross-case comparison limits,
  court-treatment attribution, denominator/missingness, forecast calibration,
  paid-source gaps, immutable overrides, and malformed-input fail-closed output.
- Review-composition tests prove no counsel content reaches blind jobs, actual
  jobs receive only the relevant team slice, and forecasts cannot suppress
  common attacks.
- Mutation tests reject joint-filing authorship assigned to a merely listed
  lawyer, behavior supported only by a biography or article, denominator-free
  tendencies, unsupported certainty, case-outcome predictions, personal data,
  court treatment copied into counsel history, and overrides that rewrite
  provenance.
- All committed examples remain fictional, generic, and public-safe.

## Risks / Trade-offs

- Public docket coverage is often incomplete. The contract favors explicit
  missingness and bounded examples over broad conclusions.
- Team-level attribution is less personalized than assigning every joint paper
  to every lawyer, but it is the strongest supported inference from the public
  record.
- A professional forecast can be useful and still be wrong. The separate
  forecast ledger and required contrary evidence prevent it from becoming a fact
  or certainty.
- The validator proves structure, provenance, linkage, and declared evidence
  strength. It does not determine legal correctness, persuasive value, or filing
  readiness.
