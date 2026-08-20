# Retrospective

## What worked

- Defining roles instead of mandatory filenames made the guide portable across
  existing case-workspace layouts.
- A single generic synthetic path from source registration through validation
  gave a stranger a concrete first hour without creating a template.
- Mutation tests made safety semantics and install-local link confinement
  observable instead of relying on keyword presence.

## What changed during implementation

The first draft named a future immutable tag as an unconditional prerequisite.
Independent review confirmed that the tag is intentionally unavailable until a
green release is published. The guide now states that condition, forbids a
moving-branch substitute, and gives source-checkout users a local discovery
command.

The initial tests accepted nearby tokens and link decoys. Review tightened them
to check affirmative duties, the operative Markdown destination outside fenced
examples, and the entire semantic-version tag.

## Future rule

Workspace onboarding documents define artifact roles and evidence boundaries,
not one mandatory directory tree. A published install must use an immutable tag.
Before that tag exists, document an explicit local-checkout path and never
replace the pin with `main` or another moving branch.
