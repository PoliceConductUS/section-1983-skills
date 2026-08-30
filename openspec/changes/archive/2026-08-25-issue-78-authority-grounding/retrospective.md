# Retrospective

## What changed

Authority approval now uses an atomic proposition as its unit. The installed
JSON schema and human report contract keep proposition correctness separate from
citation groundedness and require exact source voice, support, legal context,
and provenance.

## What stayed separate

This story did not add retrieval behavior from Issue #79 or independent-stage
governance from Issue #80. It also did not convert substantive legal judgment
into deterministic software. The six fixtures test the Issue #78 failure
taxonomy without a live provider or network dependency.

## Evidence retained

The RED test commit precedes implementation, the focused and full validation
results are recorded in `verify.md`, and the implementation remains isolated in
the Issue #78 stacked branch and draft PR.
