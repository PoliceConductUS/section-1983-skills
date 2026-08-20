# Proposal: Close Filing CI Review Gaps

## Why

The original Issue #1 change implemented the approved skill behavior, but final
review found incomplete behavioral evidence and an underspecified durable
read-only contract. Leaving either gap would allow later changes to satisfy
structural validation while regressing behavior already shown unsafe.

## What Changes

- Record fresh-context GREEN evidence for absent configuration, an unavailable
  required verified-authority root, non-hard findings, and a current successful
  run.
- Strengthen the durable read-only requirement to preserve the tested separation
  between Filing CI reporting and later user-authorized drafting.
- Replace the durable capability's generated purpose placeholder.
- Update verification evidence without changing the public skill unless a
  scenario fails.

## Boundaries

- No checker implementation, evaluator framework, or new runtime dependency.
- No private case material.
- No change to issue or Project status.
- No `docs/` or `.superpowers/` directory.

## Impact

The public `filing-ci` skill should remain unchanged. OpenSpec gains a
corrective archive and a durable requirement that matches the already-tested
behavior.
