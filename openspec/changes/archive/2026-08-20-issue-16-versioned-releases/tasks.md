## 1. RED release contract

- [x] 1.1 Add focused repository tests for pinned README install sources,
      deliberate upgrades, and consistent release documentation.
- [x] 1.2 Add workflow tests requiring manual dispatch from `main`, semantic
      version and existing-tag rejection, full validation before tag creation,
      immutable tag push, and GitHub release notes.
- [x] 1.3 Run the focused module and confirm genuine failures against the
      current moving-main release contract.
- [x] 1.4 Commit the RED test and sync the child branch.

## 2. GREEN release workflow and documentation

- [x] 2.1 Add the manually dispatched release workflow with the approved
      validation-before-tag order.
- [x] 2.2 Pin every README install command to `v0.1.0` and document deliberate
      version upgrades.
- [x] 2.3 Rewrite publishing and contribution release guidance without a stable
      branch or push-to-main publication path.
- [x] 2.4 Run focused and full repository verification.
- [x] 2.5 Commit the GREEN implementation and sync the child branch.

## 3. Review, verification, and archive

- [x] 3.1 Review the complete Issue 16 diff for release-order, permission,
      documentation, and scope defects.
- [x] 3.2 Record verification and retrospective artifacts.
- [x] 3.3 Archive the OpenSpec change and validate the durable specification.
- [x] 3.4 Commit the archive, sync the stack, and preserve the worktree for the
      next child branch.
