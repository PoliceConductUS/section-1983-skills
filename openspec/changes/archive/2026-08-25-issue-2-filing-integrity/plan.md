# Issue #2 deterministic filing-integrity plan

## Goal

Replace the package-shaped Filing CI checker boundary with one fixed installed
checker over ordinary declared folders and strict domain YAML.

## Constraints

- All inputs are recursive read-only folders; target selection is explicit.
- One full absolute output folder is mandatory.
- Every transient byte is under `<output-folder>/temp/`.
- Case files and YAML cannot select behavior or permissions.
- The initial release is deterministic, internet-disabled, and read-only.
- Follow RED, minimal GREEN, immediate commit, and immediate push.

## Steps

1. RED-test the six-role public contract, fixed registry, and removal of package
   vocabulary and package-named metadata.
2. Implement strict source-documentation and filing-index validation against
   ordinary files.
3. RED-test and implement the initial mechanical finding set and stable exit
   classes.
4. RED-test and implement trusted-host publication and output-local temporary
   work.
5. Run focused and full validation, archive OpenSpec, push, verify exact-head
   checks, and mark the PR ready while leaving the PR and issue open.
