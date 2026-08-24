## 1. Folder invocation RED

- [ ] 1.1 Add public-seam tests for envelope validation, canonical roots,
      duplicate roles, root containment, target traversal, and symlink escape.
- [ ] 1.2 Add tests for deterministic logical manifests across different
      absolute roots and rejection of external symlink content.
- [ ] 1.3 Run and record focused RED caused only by the missing folder contract.

## 2. Minimal folder contract GREEN

- [ ] 2.1 Add the public JSON schema and standard-library conformance validator.
- [ ] 2.2 Add canonical documentation for the invocation, path, manifest, and
      trusted-host enforcement boundaries.
- [ ] 2.3 Run focused GREEN and refactor only while tests remain green.

## 3. Independently installable governance RED/GREEN

- [ ] 3.1 Add governance tests proving every public skill must carry the compact
      folder boundary and inverted permissions fail closed.
- [ ] 3.2 Extend governance validation and contribution review for the protected
      folder gate.
- [ ] 3.3 Add the compact boundary to every public `SKILL.md` and run focused
      GREEN, discovery, formatting, and governance validation.

## 4. Review and archive

- [ ] 4.1 Review schema, resolver, manifest, symlink, read-only declaration,
      network policy, and independently installable skill coverage; correct
      accepted Critical or Important findings test-first.
- [ ] 4.2 Complete verification and retrospective artifacts, archive the
      OpenSpec change on this branch, and validate the durable specs.
- [ ] 4.3 Run `npm run validate`, verify a clean worktree and origin parity,
      leave Issue #64 and its PR open, and mark the PR ready for review.
