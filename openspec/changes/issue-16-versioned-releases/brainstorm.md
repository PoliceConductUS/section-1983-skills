# Versioned Release Discipline Brainstorm

## Approved direction

Use immutable semantic-version tags as the only release identity. Do not create
a stable branch. Install examples pin an exact tag, and a manually dispatched
GitHub workflow validates the exact `main` commit before it creates an annotated
tag and GitHub release.

## Release boundary

- A push or merge to `main` is not publication.
- A tag-triggered workflow is insufficient because it validates after the tag
  already exists.
- The release workflow runs only from `main`, runs the complete repository gate,
  and creates the tag only after that gate succeeds.
- A released tag is never moved, reused, or deleted to disguise a bad release. A
  correction receives a new version.
- The initial documented release target is `v0.1.0`; it becomes installable only
  after the completed stack reaches `main` and the release workflow creates it.

## Rejected alternatives

- A movable stable branch is not reproducible and was expressly rejected.
- Bare repository install commands resolve a moving default branch.
- `npx skills update` does not express a deliberate upgrade between immutable
  tagged sources.
- A package-registry release would add an unapproved distribution system.
