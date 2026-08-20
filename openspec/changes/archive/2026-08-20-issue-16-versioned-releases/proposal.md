## Why

The repository currently describes `main` as the stable release branch and shows
unpinned install commands. A consumer can therefore receive a moving tip,
including a partially integrated stack, even though the repository now has a
complete validation chain capable of gating releases.

## What Changes

- Make immutable semantic-version tags the only release identity.
- Add a manual release workflow that runs the complete validation chain on
  `main` before creating an annotated tag and GitHub release.
- Pin README installation examples to one exact published tag and explain
  deliberate upgrades.
- Rewrite publishing and contribution guidance so a push to `main` is not a
  release and a released tag is never moved or reused.
- Add repository integration tests for the executable release order and pinned
  install contract.

## Capabilities

### New Capabilities

- `repository-release-discipline`: Publish reproducible skill versions only from
  validated immutable tags.

### Modified Capabilities

None.

## Impact

The change updates repository release and install documentation, adds one GitHub
Actions workflow, and adds one standard-library integration test module. It
changes no skill, legal contract, dependency, package-registry artifact, or
runtime behavior.
