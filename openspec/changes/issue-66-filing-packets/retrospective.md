# Retrospective

## Outcome

Issue #66 adds a folder-native FilingPacket lifecycle for complete filing sets.
Ordinary files and one strict manifest now carry membership, order, roles,
content identity, revision provenance, exact review targets, and mechanical gate
coverage while source folders remain read-only and output remains explicit.

## What worked

- Reusing `ValidatedInvocation`, logical input manifests, and `OutputRun` kept
  folder authority and publication in their existing trusted-host owners.
- Keeping document kind separate from packet role handles an amended complaint
  as either the main filing or an exhibit without changing its identity.
- Synthetic packet families made order, hashes, source preservation, target
  scope, and gate coverage executable rather than prose-only claims.
- Install-local contract copies preserve the FilingPacket boundary when a skill
  is installed without the repository around it.
- Draft-PR red commits made each review correction observable before its fix.

## Misses and corrections

- The first loader resolved manifest and member symlinks, which silently
  accepted external manifest bytes and in-root aliases. Canonical-path equality
  now rejects both before packet identity is assigned.
- The first publisher accepted a generic `ValidatedInvocation`; it now requires
  the installed-contract policy and role binding populated only by installed
  skill validation.
- Python boolean equality let `true` stand in for schema version `1`, and the
  public path regex described a looser language than the runtime. Type-exact
  version checks and one shared path language close that gap.
- The first public-skill list missed the existing Scholer overlay. Its package
  now carries and links its own FilingPacket contract.
- The first correction still exposed `.` as an unbounded empty-parts error and
  used a schema wildcard that disagreed with legal POSIX newline names. A final
  red-green pass bounded `.` and made every lookahead operate across the same
  character language as the runtime.

## Boundaries retained

This story does not perform electronic filing, define every court's role
catalog, mutate source packets, decide litigation strategy or legal quality,
provide a universal runner, or introduce CaseGraph resources. Public skills
remain thin processors; the trusted host owns validation and publication.

## Reusable lessons

Filesystem confinement is not the same as canonical identity: an in-root symlink
can stay confined while still giving the same bytes multiple logical names.
Public schemas and runtime validators also need mutation cases for host language
quirks such as Python's `bool` subclassing `int`, empty normalized paths, and
regex dot behavior across newline characters.
