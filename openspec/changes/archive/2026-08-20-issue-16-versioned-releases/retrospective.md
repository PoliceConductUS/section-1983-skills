# Retrospective

## What worked

- Requiring full validation before tag creation keeps the immutable artifact
  boundary simple and auditable.
- Keeping `main` as integration only avoids a second moving release channel.
- Mutation tests made destructive tag operations and incomplete cleanliness
  checks fail loudly instead of relying on command-name substring checks.

## What changed during implementation

The first workflow used a digit-only version expression and `git diff` as the
clean-tree gate. Review showed that canonical SemVer needs leading-zero rules
and that the gate must include staged and untracked files. The tests were also
tightened from permissive push matching to one exact non-destructive tag push.

## Future rule

Treat the release workflow as an executable safety contract. Any change to
version validation, repository cleanliness, tag creation, or tag push syntax
must add or update a mutation test before the workflow changes. Create releases
only from fully validated annotated tags; never create a stable branch or make
`main` an install target.
