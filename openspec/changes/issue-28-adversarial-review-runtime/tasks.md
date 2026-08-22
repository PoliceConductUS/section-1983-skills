## 1. Trusted-runtime RED

- [x] 1.1 Add public-seam tests for the trusted stateless provider request and
      prove the current launcher has no such entry point.
- [x] 1.2 Add protocol tests for categorized findings, supported corrections,
      reserved decisions, provider failures, invalid bytes, and bounded
      diagnostics.
- [x] 1.3 Add immutable-output tests for artifact hash verification, canonical
      version/audits confinement, exclusive creation, collision preservation,
      and unavailable-report honesty.
- [ ] 1.4 Run and record focused RED; independently review and correct the RED
      suite before production changes.

## 2. Minimal GREEN

- [ ] 2.1 Implement the stateless OpenAI Responses request/transport boundary
      with explicit model, no tools, no storage, and no session continuation.
- [ ] 2.2 Implement strict review-response validation and five-category Markdown
      rendering.
- [ ] 2.3 Implement canonical version resolution, artifact verification,
      exclusive immutable report creation, and bounded execution receipts.
- [ ] 2.4 Replace caller-asserted command trust with fail-closed behavior and
      preserve the command seam only as an untrusted/custom-provider boundary.
- [ ] 2.5 Update the public skill and README usage, then run focused GREEN,
      behavior pressure, and complete validation.

## 3. Review and archive

- [ ] 3.1 Review the whole story for clean-room leaks, output mutation,
      credential exposure, protocol false greens, and scope drift; correct
      accepted Critical or Important findings test-first.
- [ ] 3.2 Complete verification and retrospective artifacts, archive the
      OpenSpec change on this branch, and validate the durable spec.
- [ ] 3.3 Commit and `git town sync` after every commit; finish with
      local/origin parity, a clean worktree, Issue 28 open, and no PR.
