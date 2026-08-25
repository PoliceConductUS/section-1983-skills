# Issue #63 folder-scoped role orchestration plan

## Goal

Repeat fixed protected roles across explicit profile-file selections and connect
bounded role hops only through persisted ordinary files.

## Constraints

- Every input is selected from a caller-declared recursive read-only folder.
- Every invocation has one full absolute output folder.
- Every transient byte is under the applicable output folder's `temp/`.
- Roles, operations, adapters, and permissions remain trusted-host constants.
- No package, graph, repository, conversation, hidden context, or direct target
  mutation.
- Follow RED, minimal GREEN, immediate commit, and immediate push.

## Steps

1. RED-test variant validation, target equality, N fresh processes, distinct
   outputs, receipts, and stable failures.
2. Implement one-run publication and deterministic sweep comparison over the
   shared launcher and output writer.
3. RED-test artifact-only sequence linkage and prior-output immutability.
4. Implement bounded sequence validation without passing in-memory child state.
5. Run focused and full validation, archive OpenSpec, push, verify exact-head
   checks, and mark the PR ready while leaving the PR and issue open.
