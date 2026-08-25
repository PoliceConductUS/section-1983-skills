# Proposal: Shared Static-Role Launcher

## Why

Issue #61 must replace the one-off adversarial-review dispatch boundary with one
trusted launcher that composes protected static role behavior with immutable
profile, target, and context packages without exposing ambient filesystem,
session, command, or persistence authority.

## What changes

- Add a repository-owned trusted launcher for one fresh isolated role process.
- Extend static-role contracts with exact operations and compatible target and
  context package kinds while keeping profile data separate from behavior.
- Validate and pin every package and role reference before child dispatch.
- Send only canonical role instructions, assigned task, and selected immutable
  package-member bytes to the child; never send local paths.
- Route the child working directory and every temp environment variable beneath
  the caller-selected `<output-folder>/temp` tree.
- Require a trusted fixed adapter that proves fresh-process, filesystem,
  network, and capability enforcement; reject arbitrary child commands.
- Return bounded advisory artifacts or stable failure reports for trusted-host
  publication without mutating any input or target.
- Migrate `adversarial-filing-review` to the shared boundary while preserving
  its five categories, independence, read-only target, and plaintiff-decision
  rules.

## Capabilities

### New capability

- `static-role-launcher`

### Modified capabilities

- `immutable-folder-packages`
- `adversarial-filing-review`
- `explicit-skill-output-persistence`

## Non-goals

- No role sweep, multi-role sequence, persistent conversation, or persistent
  child process.
- No person-specific skill, generated role, profile-supplied instruction, or
  outcome prediction.
- No CaseGraph, Git, arbitrary command API, package mutation, or direct child
  filesystem access.
