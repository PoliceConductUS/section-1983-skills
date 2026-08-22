## Context

The repository already tells agents not to choose litigation strategy and
already contains verification, source, permission, and filing-readiness gates.
Those rules are distributed across `AGENTS.md`, `CONTRIBUTING.md`, and
individual skills. No public registry proves that every rules-dependent skill
identifies when and from where its rule content was checked. No repository test
fails when a new public skill omits that classification or when contribution
guidance drops the explicit-review boundary.

The repository owns public agent skills, not a general legal-rules retrieval
system, legal-advice engine, or filing toolchain. The design must therefore be
declarative, standard-library-only, install-neutral, and compatible with the
existing validation workflow.

## Goals / Non-Goals

**Goals:**

- State one public repository-wide judgment-routing and contribution policy.
- Classify every public skill's relationship to current procedural rules.
- Expose a concrete checked date and authoritative provenance for bundled rule
  content.
- Require runtime-sourced skills to return the source identity and checked date
  they actually used.
- Confine current jurisdiction-specific propositions to verified source
  references.
- Preserve explicit human review before protected legal gates can be weakened.
- Fail repository validation on incomplete or internally inconsistent governance
  data.

**Non-Goals:**

- Decide litigation strategy, filing, concessions, or legal positions.
- Certify the substantive correctness or continuing validity of every legal
  authority.
- Fetch, cache, or update rules automatically.
- Add branch protection, invent a reviewer identity, or make Git Town mandatory.
- Move general-purpose legal tooling into this repository.

## Decisions

### One public policy and one complete registry

`GOVERNANCE.md` owns the human-readable contract.
`governance/rules-provenance.json` owns machine-readable skill coverage and
source metadata. The registry discovers no skills implicitly: validation
compares its entries with the actual `skills/*/SKILL.md` directories so both
missing and stale entries fail.

Each skill entry uses one of three modes:

- `rules-independent`: the skill does not supply current procedural rule
  content.
- `runtime-sourced`: the skill consumes approved project or user sources and
  must expose the actual stable source identity and checked date in its output.
- `bundled-rules-dependent`: repository content supplies procedural rule
  propositions and the registry must identify one or more authoritative sources
  with checked dates.

Every entry has a nonempty rationale and `reviewed_on` ISO date. Shared
authoritative sources are normalized at the registry top level and referenced by
stable IDs.

### Jurisdiction-specific content lives in references

A public SKILL may route to a jurisdiction overlay and describe source-gated
workflow, but a current local rule, judge requirement, deadline, limit, or
judge-specific legal proposition belongs in a reference that identifies
jurisdiction, authoritative source, and checked date. The current Judge Scholer
overlay is normalized to that boundary.

### Repository-specific validation

`scripts/validate_governance.py` parses the JSON registry, enumerates public
skills, and validates modes, dates, source IDs, authoritative HTTPS URLs,
jurisdiction-reference paths, and required public policy/checklist phrases. It
does not retrieve sources or perform legal analysis. Focused standard-library
tests exercise valid and invalid temporary repositories, and `npm run validate`
invokes the validator.

### Explicit review remains human

The pull-request template requires an author to identify whether a change
affects verification, source, permission, filing-readiness, judgment routing,
rules provenance, or tool ownership, and to request explicit review when it
does. The validator ensures that this protected-gate inventory and review
instruction remain present. GitHub branch protection is an organization setting
and is not simulated in repository code.

### Alternatives

Policy-only prose is too weak because it cannot detect missing coverage.
Duplicating metadata in every SKILL is rejected because shared dates and URLs
would drift. A central registry with a narrow validator provides one public seam
and deterministic coverage.

## Risks / Trade-offs

- **[Registry dates can become old]** → The registry exposes staleness instead
  of hiding it; maintainers must refresh sources before claiming currency.
- **[A structural validator cannot prove legal accuracy]** → Governance
  expressly keeps the separate authority-verification gate and treats registry
  sources as provenance, not certification.
- **[Runtime sources differ by case]** → Runtime-sourced skills must return the
  actual source identity and checked date used; the repository does not invent a
  universal local-rule cache.
- **[Human review is not branch protection]** → The repository makes review
  obligations explicit and test-protected without fabricating external
  enforcement.

## Migration Plan

1. Add the policy, complete registry, pull-request checklist, validator tests,
   and RED validation wiring.
2. Normalize the Judge Scholer reference provenance and remove current
   jurisdiction-specific propositions from its SKILL surface.
3. Make the validator GREEN, run all public skill, evaluation, OpenSpec, corpus,
   and formatting gates, then archive the OpenSpec change on the owning branch.
4. Rollback is a normal revert of the Issue #14 commits; no external data or
   repository setting is mutated.

## Open Questions

None.
