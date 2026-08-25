# Tasks

## 1. Contract

- [x] 1.1 Record the clarified exclusive `<output-folder>/temp/` boundary.
- [x] 1.2 Design separate durable receipt and transient staging namespaces.

## 2. RED

- [x] 2.1 Add tests that require staging beneath `temp/<run-id>/` and reject
      public `temp/` artifact paths.
- [x] 2.2 Add tests for exact trusted-host working-directory and temporary
      environment configuration.

## 3. GREEN

- [x] 3.1 Move staging to the reserved temporary namespace without weakening
      stable-directory, atomicity, cleanup, or failure semantics.
- [x] 3.2 Expose bounded process configuration and update current guidance.

## 4. Verification

- [x] 4.1 Run focused and full validation and review the corrected boundary.
- [ ] 4.2 Write verification and retrospective evidence, archive this change,
      push, and mark PR #73 ready while leaving the PR and Issue #65 open.
