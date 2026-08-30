# Retrospective

## What changed

Issue #63 now provides trusted-host operations for one fixed-role attack,
repeatable role-profile sweeps, and bounded role sequences joined only by
persisted ordinary files. Each run publishes through the existing explicit
output writer and documents its selected logical files and hashes in an ordinary
YAML receipt.

## What the review caught

The initial green sweep compared role policy but did not include the trusted
adapter class or exact task instructions in the invariant signature. Review
added those gates and exposed the single-run `attack` operation named by the
issue. Review also corrected an overlap check whose bounded error subclass could
have been swallowed by a broad `ValueError` handler.

## Result

Profiles remain untrusted data selected from declared folders. Each variant and
each sequence hop gets a fresh process and explicit output folder; only a
trusted-host-published file selected by path and hash may cross to a later role.
