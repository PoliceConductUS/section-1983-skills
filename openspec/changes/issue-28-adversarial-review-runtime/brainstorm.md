# Brainstorm

## Problem

The public adversarial-review launcher validates a strong clean-room packet but
does not establish a clean-room reviewer. Its command path accepts a caller
Boolean claiming that empty capabilities exist. In actual use the orchestrator
could not prove that assertion, so it correctly emitted only an independent-
review-unavailable report. The contract is honest but not operational.

The repository also needs this runtime to become a reusable execution seam for
later litigation-alignment review plans. Those later stories must be able to
schedule fresh blind and actual-adversary reviews without granting the reviewer
filesystem, browser, repository, conversation, or provider-session access.

## Approved approach

- Add a built-in stateless OpenAI Responses adapter. The model receives only the
  already validated embedded packet. The request supplies no tools, selects no
  tool, stores no response, and includes no conversation or previous-response
  identifier.
- Require an explicit model and `OPENAI_API_KEY`; do not silently select a
  provider model or claim independence when provider configuration is absent.
- Use strict structured output for the five report categories and validate the
  response before rendering Markdown.
- Keep the existing argument-array command provider as a compatibility seam, but
  do not treat a bare caller assertion as proof of isolation. A command provider
  remains unavailable unless a separately trusted runtime adapter owns and
  proves that boundary.
- Resolve the project boundary and audited version folder outside the reviewer
  packet. Write one new report with exclusive-create semantics in the version's
  `audits/` folder. Never overwrite an existing report or modify the draft.
- Record a bounded receipt: runtime type, explicit model, local run identity,
  document family, packet/draft/source fingerprints, time, outcome, and stable
  failure class. Exclude credentials and provider/session continuation state.

## Rejected alternatives

### Continue accepting the Boolean assertion

This preserves the current failure. The launcher can prove that the Boolean is
true, but not that the runtime actually denies capabilities.

### Run an ordinary Codex or local agent subprocess

An ordinary agent process can inherit filesystem and tool access. Scrubbing its
environment and current directory is useful but does not establish the required
empty-capability boundary.

### Require Docker as the public runtime

A container can isolate a local command, but it adds an image and daemon
dependency and still does not define the model's provider-session behavior. The
stateless provider request is the narrower enforceable reviewer boundary. A
future command adapter may add a container-backed proof without changing the
review packet.

### Let the provider write the audit report

The provider must not receive a case path or filesystem capability. The host
validates the structured response and performs the single authorized exclusive
report write.

## Boundaries

- No adversary, judge, litigation-alignment, or counsel overlay is added here.
- No filing is edited and no recommendation is implemented.
- No private or case-specific fixture is committed.
- No new dependency, workflow, root `docs/`, or `.superpowers/` directory is
  added.

## Open questions

None. Paid docket retrieval, overlay construction, and multi-review planning
belong to the two approved child stories.
