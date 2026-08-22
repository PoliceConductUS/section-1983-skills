# Retrospective

## Outcome

Issue 28 replaced an unprovable caller-asserted reviewer boundary with a
concrete stateless provider request. The launcher now owns both sides of the
trust contract: it constructs the no-tools/no-session request and writes one
immutable version-specific report after validating the response.

## What RED established

The original launcher could isolate an ordinary child process but could not
prove that the child lacked filesystem, browser, repository, or session
capabilities. A Boolean supplied beside an arbitrary command was only a claim.
RED also showed that packet correctness, provider protocol, and immutable report
placement needed one end-to-end public seam.

## What worked

- Keeping the existing exact packet schema preserved the clean-room input
  contract while replacing only the runtime boundary.
- A literal transport spy made the stateless request fields and absence of
  credential body leakage directly observable.
- Host-side artifact verification and exclusive report creation kept reviewer
  capabilities separate from permitted audit output.
- The real provider call found credential-fragment leakage that a full-secret
  assertion did not detect.
- Whole-story mutation pressure found packet echo, incomplete-status acceptance,
  and a write-time symlink race after the initial full suite was green.

## Review findings and corrections

The first live call exposed a masked API-key fragment in the 401 response body.
HTTP error bodies are no longer retained. The whole-story review then required a
top-level completed provider status, reduced the public success result to a
non-sensitive dispatch summary, and changed report creation to a directory-file-
descriptor boundary with no-follow and exclusive-open flags. Each correction was
captured by a failing test before production changed.

## Deviations

- The environment credential was invalid, so live dogfood verified endpoint
  reachability and unavailable-result behavior but not a completed real-model
  review. The complete success path remains covered by injected protocol tests.
- The command compatibility seam remains callable but can never produce an
  independent result. It was retained only to avoid silently changing the
  packet-validation API while removing unsupported trust.
- The public-route commit also removed retained HTTP bodies after the live call
  exposed their credential risk.

## Reusable lesson

An isolation claim is trustworthy only when the executable boundary makes the
capabilities observable. The same rule applies to output: preflight path checks
are insufficient unless the final write is anchored to the checked directory,
and a successful machine result should not duplicate the sensitive packet it
just processed.
