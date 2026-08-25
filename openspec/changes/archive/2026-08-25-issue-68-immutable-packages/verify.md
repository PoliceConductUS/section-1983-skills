# Verification

Verified on 2026-08-24 at branch head `d0754f5` against live GitHub Issue #68
and base branch `codex/issue-66-filing-packets`.

## Acceptance review

- The package contract uses ordinary input and output folders only. It has no
  CaseGraph, Git, registry, or version-directory dependency.
- The strict manifest records version, kind, stable identity, freshness,
  producer, logical sources, complete ordered members, hashes, classifications,
  and validation receipt identity.
- The loader rejects malformed, unsupported, stale-at-binding, aliased,
  escaping, special, duplicate, missing, unlisted, failed, mismatched, or
  oversized packages and returns only frozen verified member bytes.
- The publisher requires an installed-contract-bound invocation and writes one
  complete package through a fresh `OutputRun` beneath the explicit output
  folder without mutating inputs.
- Static role validation remains separate from profile bytes. The binder checks
  package kind and explicit-date freshness without merging profile data into
  capabilities, prohibitions, internet, target-mutation, or output authority.
- Fictional judicial, counsel-team, litigation-alignment, and municipal packages
  exercise the common envelope. Current counsel and alignment domain schemas
  remain authoritative for substantive artifacts.
- The actual isolated launcher remains owned by downstream Issue #61.

## Fresh commands

`npm run validate` completed with exit status 0:

- Prettier: all matched files formatted.
- Drafting tests: 27 passed.
- Evaluation tests: 517 passed.
- Skill discovery: 22 skills.
- OpenSpec: 25 passed, 0 failed.
- Evaluation corpus: completed.
- Governance validation: passed.

Additional checks completed with exit status 0:

- `python3 -m py_compile scripts/immutable_folder_package.py scripts/static_role_binding.py evaluations/tests/test_immutable_folder_packages.py`
- `git diff --check codex/issue-66-filing-packets...HEAD`

GitHub exact-head checks are recorded after the archived change is pushed.
