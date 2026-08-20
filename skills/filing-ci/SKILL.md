---
name: filing-ci
description: >-
  Use when a project-configured deterministic filing-integrity checker must run
  after material legal-drafting changes, during filing-integrity checks, or
  before a filing-readiness statement.
---

# Filing CI

## Purpose

Run the project's configured deterministic filing-integrity checker and report
whether its filing gate is current and open or passed. This skill orchestrates
the checker; it does not reproduce the checker's determinations in prose.

## Resolve the configured inputs

Resolve the controlling draft and complete checker invocation from repository
instructions, project configuration, or explicit user input. Use a project's
verified-authority root when one is configured and the checker requires
authority verification.

- Run the exact configured invocation against the identified controlling draft.
- Do not invent an executable path, flag, source path, output location, or
  verified-authority root.
- If no complete invocation is configured, report **unavailable configuration**
  and leave the filing gate open.
- If the controlling draft, a required verified-authority root, or another
  required input is unreadable or unresolved, report that class and leave the
  filing gate open. When authority verification is required, do not substitute
  another authority directory or run an invocation that cannot receive the
  configured root.

## Run at the required workflow stages

Run Filing CI after every material change to the controlling draft and again
immediately before describing the document as filing-ready. A material change
invalidates any earlier successful result. A filing-readiness decision requires
a current successful run for the controlling draft.

Treat the checker's documented output contract as the boundary for interpreting
the result. If the configured checker cannot execute, report **unavailable
execution** and do not claim that a deterministic check ran. If promised output
is malformed or cannot be reliably interpreted, report **malformed promised
output** and leave the filing gate open.

## Return findings to drafting

Classify and report the result without changing the controlling filing:

- Preserve each checker-reported finding and its documented severity.
- Treat unresolved hard findings as an open filing gate.
- Present warnings and other documented non-hard findings without downgrading,
  dismissing, or correcting them.
- Return actionable findings, including the attacked location and required
  correction when supplied, to the drafting loop for correction and rerun.

Filing CI is read-only orchestration. While Filing CI is active, do not edit the
controlling filing, even when a broader user request asks to make it
filing-ready. Do not silently edit the filing, create project paths, rewrite
checker output, or claim that a correction is user-approved.

For a user-authorized correction, explicitly hand off to the applicable drafting
workflow outside Filing CI orchestration. That workflow must use a
checker-supplied correction or source-supported drafting; do not invent
corrective filing text. After the correction, return to Filing CI for a fresh
checker run.

## Filing gate and boundaries

Keep the filing gate open when configuration or execution is unavailable, a
required input is unresolved, promised output cannot be reliably interpreted, a
result is stale, or a hard finding remains unresolved. Describe Filing CI as
passed only after a current successful run for the controlling draft has no
unresolved hard findings; preserve documented warnings and independent filing
gates.

This skill does not own checker logic, verified-authority-store verification,
formatting, automatic correction, filing, or litigation judgment reserved to the
user.
