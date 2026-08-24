## 1. Folder invocation RED

- [x] 1.1 Add public-seam tests for envelope validation, canonical roots,
      duplicate roles, root containment, target traversal, and symlink escape.
- [x] 1.2 Add tests for deterministic logical manifests across different
      absolute roots and rejection of external symlink content.
- [x] 1.3 Run and record focused RED caused only by the missing folder contract.

## 2. Minimal folder contract GREEN

- [x] 2.1 Add the public JSON schema and standard-library conformance validator.
- [x] 2.2 Add canonical documentation for the invocation, path, manifest, and
      trusted-host enforcement boundaries.
- [x] 2.3 Run focused GREEN and refactor only while tests remain green.

## 3. Independently installable governance RED/GREEN

- [x] 3.1 Add governance tests proving every public skill must carry the compact
      folder boundary and inverted permissions fail closed.
- [x] 3.2 Extend governance validation and contribution review for the protected
      folder gate.
- [x] 3.3 Add the compact boundary to every public `SKILL.md` and run focused
      GREEN, discovery, formatting, and governance validation.

## 4. Review and archive

- [x] 4.1 Review schema, resolver, manifest, symlink, read-only declaration,
      network policy, and independently installable skill coverage; correct
      accepted Critical or Important findings test-first.
- [x] 4.2 Complete verification and retrospective artifacts, archive the
      OpenSpec change on this branch, and validate the durable specs.
- [x] 4.3 Run `npm run validate`, verify a clean worktree and origin parity,
      leave Issue #64 and its PR open, and mark the PR ready for review.
