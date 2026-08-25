# Design: Declared-Folder Static-Role Launcher

## Authority split

The trusted host owns invocation validation, static-role selection, logical file
selection, adapter selection, process isolation, runtime and byte limits, output
validation, publication, and terminal receipts. Participant data, the assigned
task, and the child response cannot select an executable, adapter, role, network
policy, path, or output validator.

A `RoleLaunchDefinition` binds host-owned values:

- role identity, authorized operations, capabilities, and prohibitions;
- exact logical input purposes, allowed invocation roles, and cardinality;
- canonical public role-instruction bytes;
- internet, target-mutation, and output policy;
- one host-selected child adapter; and
- one role-specific advisory-output validator.

## Input selection

The launcher receives a validated #64 invocation and ordered logical selections.
Each selection names its purpose, declared input role, and safe input-relative
path. The host resolves and snapshots only those files, enforces the aggregate
input-byte limit, and requires UTF-8 for child-facing content. Domain YAML is
data and receives no behavior authority.

The canonical child request includes role-relative logical names, hashes, sizes,
and UTF-8 contents. It never includes an absolute root, local canonical path,
repository path, credential, environment, command, prior conversation, or
session identifier.

## Process boundary

The adapter is selected by trusted host code. Before dispatch it must attest to
one fresh process, scrubbed session state, undeclared-filesystem denial, fixed
network enforcement, capability enforcement, and no untrusted command surface.
False or unavailable attestation fails before launch.

The launcher creates an empty `<output-folder>/temp/<run-id>/` directory and
sets `cwd`, `TMPDIR`, `TMP`, and `TEMP` to it. The adapter receives only request
bytes and bounded limits. Timeout, nonzero exit, invalid UTF-8, malformed JSON,
oversized output, or adapter failure becomes a stable failure code without raw
streams, paths, credentials, case excerpts, or fabricated findings.

## Output and immutability

A role-specific validator accepts only its exact advisory schema and returns
canonical output-relative paths and bytes. The launcher never writes durable
artifacts; only the trusted host may publish them through #65. After dispatch,
the launcher rereads the selected logical inputs through the validated
invocation and compares hashes and sizes. Any change fails the run.

## Adversarial review

The existing five-category request and response validators remain domain owners.
The shared launcher supplies the fresh-process, selected-byte, temp, and bounded
failure boundary. It does not reinterpret findings, select plaintiff strategy,
or revise a filing.
