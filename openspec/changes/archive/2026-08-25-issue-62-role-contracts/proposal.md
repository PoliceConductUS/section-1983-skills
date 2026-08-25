# Proposal: Source-documented opposing-counsel and judicial-review roles

## Why

Issue #62 needs two protected findings-only roles that consume the profile files
produced by the existing counsel and judicial profile skills. The rejected
package design must not return under a different name.

## What changes

- Add public `opposing-counsel` and `judicial-reviewer` skills.
- Add fixed launcher role definitions for `opposing-counsel-simulation` and
  `judicial-review`.
- Reuse the existing defense-counsel overlay and Judicial Reasoning Profile
  domain validators against selected ordinary files.
- Require selected profile source documentation, filing target, and approved
  source files from declared recursive read-only folders.
- Disable internet and return only exact findings schemas for trusted-host
  publication beneath the caller's explicit output folder.
- Add behavioral fixtures that reject dispositions and profile attempts to
  modify protected role behavior.

## Non-goals

- No package, manifest, graph, CaseGraph, repository, or ambient workspace.
- No person-specific skill, generated role, role sweep, persistent conversation,
  drafting, remediation, disposition, or outcome prediction.
