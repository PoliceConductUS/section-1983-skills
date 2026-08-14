# Publishing

The skills CLI uses GitHub as its registry. Publishing a skill means
pushing this repository to GitHub. There is no separate registry step.

## First-time setup

From `/Users/dalelotts/dev/PoliceConductUS/section-1983-skills`:

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

```bash
git add --all
git commit --message "Describe the change"
git push
```

Users pick up the new version with `npx skills update`.

## Verifying before a push

```bash
# Run the test suite
python -m unittest discover skills/section-1983-drafting/scripts

# Confirm the CLI can discover the skills from the local checkout
npx skills add . --list
```
