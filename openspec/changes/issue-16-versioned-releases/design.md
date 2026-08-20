## Context

The skills CLI accepts a GitHub tree ref and clones that ref. An install source
such as `https://github.com/PoliceConductUS/section-1983-skills/tree/v0.1.0`
therefore resolves an immutable release tag rather than the repository's moving
default branch.

The existing `npm run validate` command already runs formatting, drafting and
evaluation tests, skill discovery, OpenSpec validation, the canonical corpus,
and governance validation. Release work should reuse that command rather than
build a second gate.

## Goals / Non-Goals

**Goals:**

- Make every documented remote install resolve one exact semantic-version tag.
- Create tags only after the exact `main` commit passes `npm run validate`.
- Reject malformed or previously published version inputs before publication.
- Preserve a GitHub Actions run, annotated tag, commit, and generated release
  notes as release evidence.
- Make upgrades deliberate by changing the pinned source tag and reinstalling.

**Non-Goals:**

- Create or maintain a stable branch.
- Publish to npm, PyPI, skills.sh, or another registry.
- Automatically release every merge to `main`.
- Move, overwrite, or delete an existing tag.
- Change installed skill content or behavior.

## Decisions

### Manual release workflow

`.github/workflows/release.yml` uses `workflow_dispatch` with one version input.
The job has `contents: write`, rejects any ref other than `refs/heads/main`,
checks out the dispatched commit with full history, rejects versions outside
`vMAJOR.MINOR.PATCH`, and rejects an existing remote tag. It then runs `npm ci`
and `npm run validate`. Only after both succeed does it create and push an
annotated tag and create a GitHub release with generated notes.

This order makes validation a precondition to tag creation. The workflow does
not trigger on tag pushes because that would make validation retrospective.

### Pinned installation and deliberate upgrade

README commands use the full GitHub tree URL with the initial `v0.1.0` target.
The release workflow must create that tag after this stack reaches `main` before
the commands become usable. A later recommended release updates all displayed
install sources in one reviewed change. Consumers upgrade by choosing the new
tag and rerunning the install command; generic `skills update` is not presented
as a version-selection mechanism.

### Documentation consistency

`PUBLISHING.md`, README, and the release paragraph in `CONTRIBUTING.md` use the
same contract: `main` is integration history, the release workflow is the only
documented tag-creation path, and released tags are immutable.

### Behavioral repository tests

The focused tests inspect the public command and workflow seams. They require
all remote README install commands to use the same semantic-version tree ref,
reject generic update instructions, and verify workflow ordering from install
through tag and release creation. They also reject tag-push triggers and
documentation that calls `main` a stable release branch.

## Risks / Trade-offs

- **[The initial pinned command precedes the first tag]** → Publishing remains
  an explicit post-merge action; docs state the command becomes usable only
  after the release workflow creates `v0.1.0`.
- **[A release workflow can be dispatched from another branch]** → The job-level
  ref guard rejects every ref except `refs/heads/main`.
- **[Concurrent maintainers choose the same version]** → The workflow rejects an
  existing remote tag, and the tag remains immutable.
- **[The tag push succeeds but GitHub release creation fails]** → The green tag
  remains the release identity; maintainers create the missing release record
  for that exact tag and never retag another commit.

## Migration Plan

1. Add RED repository integration tests for pinned sources and release order.
2. Add the release workflow and reconcile README, publishing, and contribution
   guidance.
3. Run the full repository gate, archive this change, merge the complete stack
   to `main`, and manually dispatch the workflow for `v0.1.0`.

## Open Questions

None.
