# Publishing

The skills CLI uses GitHub as its registry. Publishing a skill means pushing
this repository to GitHub. There is no separate registry step.

## First-time setup

From the repository root:

The `PoliceConductUS` GitHub organization must exist first (create it at
github.com/organizations/plan if it does not).

```bash
git init
git add --all
git commit --message "Add section-1983-drafting skill"

gh repo create PoliceConductUS/section-1983-skills --public --source . --push
```

Without the GitHub CLI, create the repository in the GitHub web interface
instead, then:

```bash
git remote add origin git@github.com:PoliceConductUS/section-1983-skills.git
git push --set-upstream origin main
```

The repository must be public for `npx skills add` to reach it without
credentials.

## Releasing changes

Treat `main` as the stable release branch. Make and test changes on a feature
branch. Merge to `main` only when the release is complete and the verification
gates below pass. Tag the merged release so users and maintainers can identify
the exact contract version.

```bash
git switch -c feature/describe-the-change
git add --all
git commit --message "Describe the change"
git push --set-upstream origin feature/describe-the-change

# After review and merge to main
git switch main
git pull --ff-only
git tag --annotate vX.Y.Z --message "Release vX.Y.Z"
git push origin main vX.Y.Z
```

Users pick up the new version with `npx skills update`.

## Verifying before a push

```bash
# Run the test suite
python3 -m unittest discover skills/section-1983-drafting/scripts

# Confirm the CLI can discover the skills from the local checkout
npx skills add . --list
```

Before pushing, also run the `skill-creator` runtime's `quick_validate.py`
against every `skills/*/` directory that contains `SKILL.md`.
