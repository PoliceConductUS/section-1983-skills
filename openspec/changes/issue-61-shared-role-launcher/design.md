# Design: Shared Static-Role Launcher

## Authority split

The trusted host owns folder invocation validation, package loading, static-role
selection, adapter selection, process isolation, time and byte limits, output
publication, and terminal receipts. The launcher receives validated host-owned
objects. A skill, task, profile, or child response never receives an output-root
path and cannot select an executable, adapter, role contract, network policy, or
output validator.

The selected `RoleLaunchDefinition` binds four trusted values:

- one validated static role contract and its canonical bytes;
- immutable public role-instruction bytes;
- one host-selected child-process adapter; and
- one role-specific output validator that returns proposed advisory artifacts.

Profile data remains ordinary immutable package bytes. It is never merged into
the role contract or role instructions.

## Static-role compatibility

The static-role contract adds exact operation identifiers, accepted target
package kinds, and an exact context-role-to-package-kind map. Existing profile
kind and freshness checks remain. The launcher rejects an unknown operation,
profile/target/context kind mismatch, missing or extra context role, stale
profile, failed package validation, or role internet mismatch before dispatch.

The assigned task selects one operation already authorized by the static role.
It cannot add capabilities or alter prohibitions, target mutation, internet, or
output authority.

## Canonical child request

The launcher constructs canonical UTF-8 JSON containing only:

- the static role contract and public role instructions;
- the assigned operation and bounded task text;
- selected profile, target, and context member identities, media types, hashes,
  and UTF-8 contents; and
- declared runtime/output protocol metadata without any local path.

Every package is fully loaded and pinned before request construction. Binary or
invalid UTF-8 child-facing members fail closed unless a future static role
defines a separate encoding contract.

## Process boundary

The trusted adapter is configured outside the invocation and profile. It must
attest that every launch creates one fresh process, starts with no conversation
or session state, exposes no undeclared filesystem path, and enforces the role's
network and capability policy. The launcher refuses an unavailable or false
attestation.

The launcher creates one run-scoped empty working directory beneath
`<output-folder>/temp/<run-id>/` and sets `cwd`, `TMPDIR`, `TMP`, and `TEMP` to
that same directory. The adapter receives canonical request bytes on standard
input and bounded runtime limits. Standard output and error are byte-bounded.
Timeout, nonzero exit, invalid UTF-8, malformed JSON, oversized streams, or
adapter failure become stable bounded failure artifacts without traceback or
case bytes.

## Output boundary

A role-specific validator accepts only its exact output schema and returns
canonical output-relative paths and bytes. The launcher verifies that all
artifacts are advisory and conform to the static role's output identifier. Only
the trusted host publishes returned artifacts beneath the explicit output
folder. Inputs and target bytes are fingerprinted before and after execution;
any change fails the run and no completed role result is published.

## Adversarial-review migration

The existing five-category packet and response validators remain the domain
owner. A protected adversarial-review role definition supplies its static public
instructions and output validator to the shared launcher. Its profile and
context packages replace embedded ambient source material. The shared launcher
does not reinterpret findings, select plaintiff strategy, or revise the filing.
