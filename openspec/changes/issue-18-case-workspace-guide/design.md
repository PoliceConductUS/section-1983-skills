## Context

Installed skills refer to artifact roles rather than fixed filenames, but a new
user may not know how to create the first approved-source list, chronology,
protected decision, gap record, or generated-output boundary. The repository
needs documentation that remains portable across project layouts.

## Goals / Non-Goals

**Goals:**

- Give a stranger a bounded first-hour sequence.
- Explain each artifact role and a generic example path.
- Make renaming/configuration portability explicit.
- Preserve missing evidence and unavailable tools as gaps.

**Non-Goals:**

- Create a workspace template, repository, skill, or script.
- Prescribe litigation strategy or case facts.
- Require one filesystem layout or case-management product.
- Claim that creating files establishes filing readiness.

## Decisions

### One install-local root guide

Use `CASE_WORKSPACE.md` at repository root. README links it with a relative link
so a tagged installation or source checkout resolves without an external site.

### Roles before filenames

The guide names immutable inputs, approved source registry, chronology,
protected decisions, verified authorities, gaps, working material, and generated
artifacts. An example layout makes the roles concrete, but every example path is
renameable when project configuration identifies the equivalent role.

### Explicit first-hour evidence boundary

The flow records one synthetic source ID and one source-bounded chronology entry
before a protected decision. Unknown facts, missing authorities, and absent
validation commands are recorded as gaps or unavailable; the guide never invents
them.

## Risks / Trade-offs

- **[Example paths look mandatory]** → State portability before and after the
  layout and label every path by role.
- **[A first-hour checklist looks filing-ready]** → State that it establishes
  workspace roles only and does not satisfy substantive filing gates.
- **[Guide drifts from release discipline]** → Test that its remote install uses
  an exact canonical semantic-version tag.

## Migration Plan

1. Add focused RED tests for the absent guide and README route.
2. Add the minimal guide and link.
3. Run focused and full verification, review, and archive.

## Open Questions

None.
