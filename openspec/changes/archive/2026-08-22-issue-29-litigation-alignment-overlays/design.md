# Design

## Context

The adversarial-review launcher accepts one bounded packet and can run a fresh
no-tools review. The judge-overlay guide defines evidence-coded judicial inputs.
Neither artifact decides which case-specific material should enter a reviewer
packet. Issue 29 supplies that orchestration contract without changing the
reviewer packet schema: relevant overlay records enter an actual-adversary job
as approved embedded sources, while blind jobs receive none.

## Goals / Non-Goals

**Goals:**

- Make every overlay reproducible from one immutable docket snapshot.
- Preserve individual defendants while deriving issue-specific alignment.
- Keep adversary, plaintiff, and judicial authorship structurally distinct.
- Generate independently reviewable blind and actual-adversary jobs.
- Explain when overlay versions may be reused and when a new version is
  mandatory.

**Non-Goals:**

- Research or profile individual defense attorneys.
- Fetch a live docket during overlay generation.
- Predict outcomes, infer personality, or optimize for a perceived preference.
- Decide legal truth, strategy, or filing readiness.
- Edit a target filing.

## Decisions

### One public skill and three machine artifacts

Add `building-litigation-alignment-overlays` with exactly three install-local
schemas:

1. `docket-snapshot.schema.json` for the immutable approved input;
2. `litigation-alignment-overlay.schema.json` for grouping, three ledgers, the
   derived matrix, and review plan; and
3. `filing-overlay-manifest.schema.json` for the overlays consumed by one filing
   version.

A standard-library validator checks schema-shaped structure plus linked-record
semantics that JSON Schema cannot express. It reports stable finding IDs and
paths as JSON and exits nonzero on errors. It does not infer a missing position.

### Canonical snapshot

The snapshot embeds each approved docket source's stable ID, docket entry,
filing date, document family, filing actors, exact content, and SHA-256. It also
identifies defendants and judicial actors with stable IDs. Overlay generation
accepts no path, URL, conversation history, or unlisted document. The overlay
records the canonical JSON fingerprint and `checked_through` date of the exact
snapshot.

Snapshot refresh is a separate authorized preflight. A new source, corrected
content, changed party/appearance data, or later checked-through date creates a
new snapshot version and invalidates any overlay that claims the old snapshot is
current.

### Issue-scoped litigation alignment

Each individual defendant has one alignment-dimension record per relevant issue:
capacity, challenged act, relevant-time knowledge position, qualified-immunity
position, requested relief, and other material defense. A group has one issue ID
and member list. Every member's alignment dimensions for that issue must match.
Every individual dimension belongs to exactly one effective group for that
issue.

A municipality remains separate from individual-capacity defendants unless a
record-supported mixed-alignment flag and source IDs establish alignment for the
particular issue. Generated groups remain immutable. User additions, exclusions,
or regrouping produce separate override records and an effective group set
without erasing the generated set or provenance.

### Three canonical ledgers

The adversary ledger contains only adversary positions. Each attack includes a
stable ID, exact source location and quote, date, group, claim, defendant,
challenged act, element or defense, qualified-immunity prong when applicable,
requested disposition, sources, and one adversary-prefixed status.

The plaintiff ledger links a response record to an attack and uses only
plaintiff-prefixed coverage states. The judicial ledger links treatment to the
actual magistrate judge, district judge, or appellate court. Recommendation,
adoption, rejection, modification, independent reasoning, affirmance, reversal,
vacatur, and remand remain actor-specific. An adopting treatment references the
recommendation it addresses; it never reattributes recommendation reasoning.

The derived matrix contains stable foreign keys and the exact union of linked
source IDs. It does not copy canonical position text. Empty response or
treatment links render explicit unavailable states; silence never becomes a
substantive disposition.

### Review plans

For each target artifact and effective group, an available actual profile
produces two distinct fresh jobs:

- `blind-common-attack`, with no adversary overlay IDs or content; and
- `actual-adversary`, with only attack IDs matching that target's group, claim,
  defendants, and challenged acts.

A leave-to-amend motion and its proposed amended complaint are two targets, so
the ordinary plan contains four jobs per group. When no responsive filing
exists, the plan records `actual-adversary-unavailable` and creates two distinct
blind common-attack jobs. It never invents an actual-adversary job.

Every job identifies a fresh run ID, target artifact ID and fingerprint, group,
review kind, included attack IDs, approved source IDs, and empty prior-review
IDs. The validator rejects adversary material in a blind job and cross-group
material in an actual job.

### Lifecycle and filing manifests

`OVERLAYS.md` owns the shared inventory and lifecycle:

- create when an overlay kind first becomes applicable;
- reuse only when the pinned snapshot, checked-through state, scope, and
  validator result remain current;
- refresh into a new immutable version when source checks advance without a
  substantive conclusion change;
- rebuild into a new immutable version after a material docket, party,
  alignment, attack, response, treatment, assignment, rule, or user-override
  event; and
- supersede without deleting the prior version.

A filing-version manifest pins every consumed overlay by kind, stable ID,
version, SHA-256, checked-through date, validator result, and source snapshot.
An overlay with a failing validator result or a snapshot/checked-through
mismatch produces no specialized drafting change.

The general guide includes one fictional complaint-to-motion-to-amend-to-
recommendation-to-order lifecycle. `JUDGE_OVERLAYS.md` links to the general
guide and owns assignment, official-procedure, corpus, and judicial-research
invalidation triggers. Issue 30 will own counsel-specific research triggers.

## Testing

- Structural tests require the public skill, metadata, local schemas, validator,
  README/router routes, general guide, judge-guide link, and corrected durable
  Purpose.
- Validator tests use synthetic snapshots and overlays to prove grouping,
  required splitting, municipality separation, individual preservation,
  overrides, source and hash integrity, exact role vocabularies, judicial-stage
  attribution, silence degradation, and manifest freshness.
- Review-plan tests prove blind isolation, exact actual slices, four jobs per
  group for a leave package, and two blind jobs when the actual profile is
  unavailable.
- Mutation tests reject `plaintiff-*` and judicial fields in attack records,
  recommendation/adoption conflation, copied derived text, and stale or failing
  manifest pins.
- The synthetic lifecycle and all artifacts remain generic and public-safe.

## Risks / Trade-offs

- The validator cannot decide whether a docket statement is legally correct. It
  checks declared role, provenance, linkage, and fail-closed states.
- Issue-scoped groups are more verbose than caption-wide groups. The extra rows
  are necessary to preserve material divergence.
- A single JSON overlay set contains three separately keyed and fingerprinted
  ledger objects rather than requiring three storage paths. This keeps
  installation portable while preserving canonical separation.
- A stale overlay may still be historically accurate. It remains immutable but
  cannot drive a current specialized drafting change.
