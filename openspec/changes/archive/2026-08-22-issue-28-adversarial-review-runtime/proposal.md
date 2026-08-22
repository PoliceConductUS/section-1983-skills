# Proposal: Trusted Adversarial Review Runtime

## Why

The adversarial-review contract currently fails closed in real use because its
launcher cannot establish the required empty-capability boundary. A trusted,
stateless runtime is needed so an independent review can actually occur while
the draft remains immutable and the reviewer sees only the approved packet.

## What Changes

**Reviewer runtime**

- From: a command launcher accepts a caller Boolean stating that the runtime
  enforces empty capabilities.
- To: a built-in stateless OpenAI Responses adapter constructs and exposes the
  enforceable no-tools, no-storage, no-session request boundary.
- Reason: independence must be established by the execution mechanism rather
  than asserted by its caller.
- Impact: additive public API/CLI behavior; the unsupported Boolean trust path
  no longer establishes independence.

**Review result**

- From: the launcher returns arbitrary JSON from a reviewer command.
- To: the trusted adapter requires and validates the complete categorized review
  response before rendering it.
- Reason: a successful runtime invocation must prove the existing public report
  contract occurred.
- Impact: trusted-runtime responses become protocol-bound.

**Immutable report**

- From: report placement is described by the skill but not owned by the public
  launcher.
- To: the execution path exclusively creates one version-specific audit report
  with a bounded receipt and refuses collisions or escaping paths.
- Reason: the usable public seam must preserve the repository's immutable audit
  contract.
- Impact: additive report-writing API/CLI behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `adversarial-filing-review`: establish and record a trusted clean-room
  runtime, validate its review protocol, and write one immutable
  version-specific report.

## Impact

The change affects the adversarial-review skill, its Python launcher/runtime,
public launcher tests, synthetic evaluation fixtures if behavioral pressure
requires them, README usage, and the durable adversarial-review specification.
It uses only the Python standard library and the existing OpenSpec/evaluation
toolchain.
