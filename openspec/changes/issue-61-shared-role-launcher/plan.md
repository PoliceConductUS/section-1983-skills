# Issue #61 Shared Static-Role Launcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans
> to implement this plan task-by-task.

**Goal:** Launch one protected static litigation role against validated
immutable folder packages in a fresh isolated process and return only bounded
advisory output.

**Architecture:** Repository trusted-host code loads and pins packages, binds a
static role, constructs a path-free canonical request, delegates exactly once to
a host-selected isolation adapter, validates the bounded response, and returns
proposed output artifacts. Skills and profile helpers remain install-local,
deterministic, and free of process or persistence authority.

**Tech stack:** Python standard library, immutable folder-package and output
writer APIs, JSON Schema Draft 2020-12, `unittest`, OpenSpec.

## Global constraints

- Full absolute output folder is mandatory.
- All transient work is under `<output-folder>/temp`; no system temp.
- No executable or adapter comes from task, profile, package, or child data.
- No child receives a local path, ambient environment, credential, session, or
  prior conversation.
- No input or target mutation; no direct child publication.
- No CaseGraph, Git, generated role, role sweep, or persistent agent process.
- Every behavior change follows RED, minimal GREEN, and immediate push.

### Task 1: Pre-dispatch model

- Create `scripts/static_role_launcher.py` and focused fictional fixtures/tests.
- Extend `governance/static-role-contract.schema.json` and
  `scripts/static_role_binding.py` only for exact operation/target/context
  compatibility.
- Validate all packages and canonical child-facing UTF-8 bytes before adapter
  selection or dispatch.

### Task 2: Isolation adapter

- Define a trusted adapter interface with immutable enforcement attestation.
- Create one run-scoped empty working directory under output `temp/` and pass
  only canonical stdin, scrubbed temp environment, timeout, and byte limits.
- Normalize every adapter/process failure into stable bounded result data.

### Task 3: Output and non-mutation

- Validate role-specific output through the trusted role definition.
- Return only canonical relative paths and bytes for trusted-host publication.
- Re-fingerprint all selected inputs after dispatch and fail on any change.

### Task 4: Adversarial review

- Preserve existing packet/response validators and report categories.
- Bind the reviewer to a static role definition and shared launcher request.
- Keep provider/network behavior expressly authorized and stateless.

### Task 5: Verification

- Run focused suites, copied-package checks, `npm run validate`, OpenSpec,
  governance, corpus, and fresh diff review.
- Archive on the owning branch, push, require exact-head CI, then mark ready.
