# Design

## Context

`launch_review.py` already validates exact embedded packet fields, verifies
SHA-256 fingerprints, uses argument arrays without a shell, creates a new empty
working directory, scrubs contextual environment values, bounds captured byte
streams, and rejects filesystem output by a command reviewer. Its trust defect
is singular but decisive: `runtime_enforces_empty_capabilities=True` is supplied
by the caller and proves nothing about the selected command.

The separately established quality-control contract permits the host to write
one immutable report under the audited version's `audits/` directory. It never
permits the reviewer to write there or to edit the artifact.

## Goals / Non-Goals

**Goals:**

- Execute an independent adversarial review through an enforceable stateless
  provider boundary.
- Validate the five-category review response and preserve current corrections
  and plaintiff-decision rules.
- Write one immutable report and receipt inside the audited version folder.
- Keep failure classifications bounded and deterministic.

**Non-Goals:**

- Infer adversary positions, defendant groups, judges, or counsel behavior.
- Browse for missing sources or retrieve docket material.
- Implement review recommendations or declare filing readiness.
- Build a general schema engine, provider framework, or container platform.

## Decisions

### One trusted built-in provider boundary

Add a focused standard-library OpenAI Responses adapter. It receives a validated
packet and explicit model, reads `OPENAI_API_KEY`, and sends one HTTPS request
to the Responses endpoint. The request contains the model, bounded instructions,
packet input, strict JSON-schema output, `tools: []`, `tool_choice: "none"`, and
`store: false`. It omits `conversation` and `previous_response_id` entirely.

The adapter is trusted because the reviewer is the stateless model invocation
whose capabilities are fully represented in that request. The API-client process
is transport and validation code, not the reviewer. It does not grant the model
a filesystem simply because the host process has one.

The model is always explicit. Missing credentials, transport failure, timeout,
non-success HTTP, invalid UTF-8/JSON, missing structured output, or schema
failure reports `independent-review-unavailable` or a narrower stable provider
failure and never becomes a successful review.

### Command seam remains, Boolean trust does not

Retain packet validation and command execution for compatibility and protocol
tests. Rename or route the legacy Boolean path so it cannot be selected as the
trusted public review mode. A custom provider may become trusted only through a
future adapter whose executable boundary is testable; an arbitrary command plus
a caller assertion remains unavailable.

### Structured response before Markdown

The provider returns an object with exactly the five canonical categories. Each
category is an array. Every finding carries the existing stable ID, attacked
quote, location, approved source IDs, concrete attack, consequence, status, and
an optional correction or plaintiff-decision object constrained by the current
skill rules. Empty arrays render as `None found`.

The host validates types, exact keys, source references, nonempty strings,
category exclusivity, complete `Replace`/`With` pairs, and no selected plaintiff
choice. Validation occurs before any success report is written.

### Exclusive version-specific report output

The CLI receives an exact project boundary and version folder. The host resolves
both canonical paths, requires the version inside the boundary, rejects
traversal and an escaping `audits/` symlink, and creates the canonical `audits/`
directory when absent. It verifies the audited draft fingerprint against the
packet before dispatch.

The host generates or accepts test-injected UTC time and UUID run identity,
constructs `adversarial-filing-review-<UTC timestamp>-<run-id>.md`, and opens
the new path exclusively. A collision fails closed without altering bytes. The
report includes the immutable receipt followed by the five canonical headings.
An unavailable execution may write an honest unavailable report through the same
exclusive path; its exit status remains nonzero and it cannot masquerade as a
completed review.

### Transport and time seams

Production uses `urllib.request` with the official HTTPS endpoint. Tests inject
or patch the transport and clock/run identity; no user-facing arbitrary endpoint
flag is added. This keeps credentials from being redirected while permitting
real request/response tests without network access.

## Data flow

1. Resolve boundary, version folder, and exact audited artifact.
2. Decode and validate the complete embedded packet and every fingerprint.
3. Verify the audited artifact bytes equal the packet draft fingerprint.
4. Construct the stateless no-tools/no-session request.
5. Execute one provider call with bounded timeout and response size.
6. Strictly decode and validate the categorized review object.
7. Render the receipt and review Markdown.
8. Exclusively create one report under `<version>/audits/`.
9. Return a machine-readable result naming the report and outcome.

No later step runs when an earlier step fails. The reviewer never receives a
path, URL, credential, environment value, prior review, or repository content.

## Testing

- Extend current public launcher tests rather than testing source strings.
- RED tests capture a provider spy request and prove the current launcher lacks
  a trusted mode.
- Validate exact packet-before-provider ordering, stateless request fields,
  absence of session/tool capabilities, model and key handling, response
  protocol, bounded transport failures, and invalid bytes.
- Use temporary version folders and immutable artifact hashes to prove the only
  write is a new audit report, collisions preserve bytes, symlink/traversal
  escapes fail, and unavailable results are not labeled complete.
- Add fresh synthetic behavior pressure showing a reviewer produces all five
  categories with supported corrections and reserved choices, without editing
  the draft.
- Run focused tests, the complete evaluation suite, corpus, governance, runtime
  skill validation, formatting, OpenSpec validation, and diff checks.

## Risks / Trade-offs

- Provider API drift could break the adapter. The request and response protocol
  is small, tested, and fails closed.
- Model output can be structurally valid but substantively poor. Existing
  deterministic and judgment fixtures plus fresh pressure tests evaluate the
  public behavior; the runtime does not claim a legal merits guarantee.
- A host with filesystem access could still be malicious. The public contract
  controls what this executable sends and writes; it does not claim to secure a
  compromised host operating system.
- The command seam is less convenient after removing unsupported trust. That is
  intentional: convenience cannot substitute for an established boundary.
