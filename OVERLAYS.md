# Case Overlay Lifecycle

Case overlays are immutable, source-backed drafting inputs. They preserve
limited information about the assigned judge, litigation-alignment groups,
actual adversary attacks, plaintiff responses, judicial treatment, and counsel
roles without replacing governing law or the canonical docket record.

## Overlay inventory

Maintain one inventory entry for every judge overlay, litigation-alignment
overlay, individual-attorney identity overlay, counsel-team behavior overlay,
and filing-version manifest used in the case. The attorney and team overlay
research rules belong to their counsel-specific guide. This guide owns only the
shared lifecycle.

Each entry records a stable overlay ID, kind, immutable version, SHA-256,
checked-through date, validator result, source snapshot, scope, status, prior
version, and invalidation event. Preserve every superseded version.

## Creation prerequisites

Create an overlay only from an approved immutable source snapshot. A docket-
derived overlay uses one versioned docket snapshot with embedded content and
verified fingerprints. A judge overlay uses its validated corpus, neutral
transfer cards, and current official court-conduct sources. Resolve all sources
before generation; the overlay stage does not browse or silently update them.

Missing documents, uncertain authorship, uncertain grouping, stale research, and
failed validation are scoped gaps. They are not permission to infer a position
or reuse an old conclusion.

## Create, reuse, refresh, rebuild, or supersede

- **Create** the first version when an overlay kind becomes applicable.
- **Reuse** an immutable version only when its exact source snapshot,
  checked-through date, scope, prohibited inferences, and passing validator
  result remain current for the target.
- **Refresh** into a new immutable version when source checks advance but the
  supported content does not materially change.
- **Rebuild** into a new immutable version when an input, actor, group, attack,
  response, treatment, assignment, official requirement, or approved override
  materially changes.
- **Supersede** the prior version without editing, renaming, moving, or deleting
  it. State why reuse ended and link the replacement.

A validator pass proves the published structural and linkage contract. It does
not prove factual truth, legal sufficiency, authority strength, strategy, or
filing readiness.

## Event-driven invalidation

Reevaluate the inventory after every complaint or amended complaint, responsive
motion, opposition or response, reply, leave motion, proposed pleading,
recommendation, objection, district order, appellate disposition, appearance,
withdrawal, substitution, reassignment, official-rule change, source correction,
or explicit user override.

A new event does not always change a conclusion, but it always requires a
create/reuse/refresh/rebuild decision. Reuse is unavailable when the pinned
source snapshot or checked-through state no longer matches the current approved
input.

## User overrides and precedence

An explicit user instruction may add, exclude, or regroup a scope. Preserve the
generated result and record the override separately with its instruction ID,
rationale, affected records, and consequence. An override controls scope; it
does not rewrite source provenance or turn an unsupported position into fact.

Apply governing law and current official court requirements before overlays.
Then apply current validated docket positions and judicial treatment, bounded
neutral judge transfer cards, and user-approved scope. An overlay never
authorizes concealment, record distortion, assignment manipulation, personality
inference, or outcome prediction.

## Review routing

For each target artifact and litigation-alignment group, retain a blind common-
attack review even when an actual adversary profile exists. The blind reviewer
receives no adversary attack, response, judicial-treatment, judge, attorney, or
counsel-team overlay.

The actual-adversary reviewer receives only the validated attack slice matching
the group, claim, defendants, challenged acts, and target. Plaintiff response
and judicial treatment remain separate context and are never relabeled as an
adversary position. Silence must not become agreement, withdrawal, rejection, or
adoption.

If no responsive filing exists, report the actual profile unavailable and run
two fresh blind common-attack reviews per target and group. Do not invent a
future defense. A leave motion and proposed amended complaint are separate
targets and ordinarily require four reviews per group when the actual profile
exists.

## Filing-version manifest

Before specialized drafting, create a manifest for the exact filing version. Pin
each consumed overlay by stable ID, kind, version, fingerprint, checked- through
date, validator result, and source snapshot. Pin the target artifact fingerprint
as well.

A stale source snapshot, earlier checked-through state, mismatched fingerprint,
or validator result other than `passed` produces no specialized drafting change.
The prior overlay may remain historically useful, but it cannot be silently
transferred to the current filing.

## Synthetic end-to-end lifecycle

1. An **initial complaint** exists before a responsive filing. Create the first
   docket snapshot and litigation-alignment groups. The actual attack profile is
   unavailable, so two blind reviews run for each group.
2. A **responsive motion** identifies three distinct positions for two officers
   and a municipality. Rebuild from the new snapshot, split materially different
   groups, create adversary attack records, and run one blind plus one actual
   review for each target and group.
3. A leave motion and proposed **amended complaint** become separate targets.
   Reuse the attack ledger only if the pinned motion and grouping remain
   current; otherwise rebuild. Each group receives four jobs across the two
   targets.
4. A **magistrate** judge issues a recommendation. Add a magistrate-judge-
   recommended treatment record and rebuild the derived matrix without
   attributing that reasoning to another actor.
5. A **district** judge adopts, rejects, modifies, or independently addresses
   the recommendation. Add a distinct district-judge record linked to the
   recommendation, supersede the prior overlay version, and pin the new version
   before any specialized drafting change.

At every stage, the adversary attack, plaintiff response, and judicial treatment
ledgers remain separate. A later source can change the derived current status;
it cannot silently rewrite the earlier actor's canonical record.
