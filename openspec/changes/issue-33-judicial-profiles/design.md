# Design: Generic Judicial Reasoning Profile Builder

## Package surface

The public skill package contains:

- `SKILL.md` for operation routing and evidence boundaries;
- `agents/openai.yaml` for generic discovery;
- `references/folder-contract.json` with ordered roles `judge-identity`,
  `court-scope`, `approved-sources`, and `verified-authorities`, no target, and
  authorized internet policy;
- `references/judicial-reasoning-profile.schema.json` for the domain artifact;
- `references/immutable-folder-package.md` for the common envelope;
- fictional complete, thin, adoption-only, and hostile-profile fixtures;
- `scripts/validate_judicial_profiles.py` for deterministic domain validation.

The installed skill remains self-contained. Repository-level trusted-host code
loads and publishes the common package envelope; the skill owns only its domain
validator and instructions.

## Operations

### Acquisition

The invocation must expressly authorize internet access. The skill may return
proposed public-source bytes and a provenance record for trusted-host
publication as a complete source package. It must not return a judicial profile
and must not compile the newly acquired bytes. A later invocation must supply
that package in the read-only `approved-sources` role.

### Compilation

Internet must be disabled. All inputs are recursively read-only and validated
before use. The skill returns proposed domain members for trusted-host
publication as a complete `judicial-profile` package beneath the explicit fresh
output folder. No input is mutated or reread after validation.

## Judicial profile domain object

The version-1 object has exact top-level fields:

- `schema_version`, `profile_id`, `checked_through`;
- `judge_identity` and `court_scope` source-bound identities;
- ordered `records`;
- ordered `comparisons`;
- ordered `neutral_transfers`;
- `assumptions`, `gaps`, and `validation`.

Each record has stable identity, one source class, exact proposition, source
identity and date, issue, posture, attribution status, and permitted/prohibited
uses. Attribution status is one of `independent_reasoning`, `adoption_only`,
`recommendation`, or `outcome_only`.

`revealed_reasoning` does not itself prove independent attribution. Only a
record whose source class is `revealed_reasoning` and attribution status is
`independent_reasoning` may support a neutral transfer. Adoption-only,
recommendation, and outcome-only records remain visible at their actual class
and attribution but never become the assigned judge's reasoning.

Each comparison references two records and copies both exact propositions and
source dates. It also records issue, posture, similarities, differences, and one
state: `aligned`, `tension`, `divergent`, or `indeterminate`. References and
copied values must match. Comparison states are descriptions of record
relationships, not psychology, preference, hypocrisy, manipulation opportunity,
or prediction.

Each neutral transfer records issue, posture, one neutral drafting instruction,
and supporting record IDs. All supporting records must independently satisfy the
revealed-reasoning gate and match the transfer's issue and posture. Missing
support leaves transfers empty and records a gap.

## Protected role boundary

The profile schema rejects capabilities, prohibitions, internet policy,
target-mutation authority, output authority, system prompts, or role
instructions at any level intended to control a role. The generic static
`judicial-reviewer` contract and launcher remain downstream work. A profile is
evidence-bounded participant data only.

## Migration

Delete the complete `drafting-for-judge-scholer` package. Replace public routes
with the generic builder and remove every active test/spec dependency on the
real name or package. Generic receipt tests use a synthetic temporary installed
role contract rather than a public judge-specific skill.

Historical archived OpenSpec artifacts remain immutable history. Current
onboarding, public skills, active specifications, validators, and tests contain
no real-judge dependency.
