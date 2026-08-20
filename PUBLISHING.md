# Publishing

GitHub hosts this repository, but a push or merge to `main` does not publish a
skills release. `main` is integration history. Each published version is one
immutable annotated semantic-version tag in `vMAJOR.MINOR.PATCH` form.

Do not create a stable branch. Do not move, reuse, or delete a released tag to
replace its commit. Publish a correction under a new version.

## First-time repository setup

The `PoliceConductUS` GitHub organization and this public repository must exist
before the skills CLI can install a release without credentials. Creating or
pushing the repository does not create a release.

```bash
git init
git add --all
git commit --message "Add section-1983 skills"

gh repo create PoliceConductUS/section-1983-skills --public --source . --push
```

Without the GitHub CLI, create the repository in the GitHub web interface, then
add the remote and push `main`. That push remains unreleased until the release
workflow succeeds.

## Releasing a validated version

Merge the complete reviewed stack to `main` before starting a release. Choose a
new semantic version that does not already exist. The initial documented release
target is `v0.1.0`.

Dispatch the release workflow from `main`:

```bash
gh workflow run release.yml --ref main -f version=v0.1.0
```

The workflow, in order:

1. rejects a non-`main` dispatch;
2. rejects a malformed or existing remote tag;
3. installs the locked dependencies with `npm ci`;
4. runs the complete `npm run validate` gate on the dispatched commit;
5. creates and pushes an annotated tag for that exact commit; and
6. creates the GitHub release with generated notes.

A failed validation creates no tag. The GitHub Actions run records the commit
and validation result; the annotated tag records the released commit; and the
GitHub release records the notes.

If the tag push succeeds but GitHub release creation fails, preserve the tag and
create the missing release record for that same tag. Never retag another commit
under the same version.

## Updating the recommended install version

After the release exists, update every pinned README install source to the new
tag in one reviewed change. Consumers choose when to upgrade by replacing the
tag in the source URL and running the install command again. A generic update
against a moving branch is not a released-version upgrade.

## Verifying changes before merge

Run the same repository gate used by the release workflow:

```bash
npm ci
npm run validate
```

The release workflow reruns both commands on `main`; a prior feature-branch run
does not substitute for the release run.
