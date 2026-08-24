# Folder-Scoped Skill Execution

`governance/folder-invocation.schema.json` defines version 1 of the
folder-native invocation envelope. A trusted host declares one or more named,
absolute input folders, exactly one absolute output folder, bounded runtime
limits, an `disabled` or `authorized` internet policy, and its isolation
declaration. A target, when needed, identifies one relative path in one input
role.

Every public skill treats only the declared input folders as available and
recursively read-only. It writes only below the declared output folder. It uses
the internet only when its own contract expressly authorizes it. If the host
cannot enforce read-only inputs, deny undeclared filesystem access, and enforce
the declared network policy, execution stops before reading case material.

## Conformance helper

`scripts/validate_folder_invocation.py` is a read-only standard-library helper.
It proves envelope shape, canonical-root and child-path confinement, target
selection, and deterministic logical input manifests. Its manifest includes only
each input role and its relative regular-file paths, byte sizes, and SHA-256
hashes; it contains no absolute source paths. The helper performs no writes, and
it can read a JSON envelope from standard input to emit that logical manifest or
a bounded JSON error.

The helper does not sandbox an agent. It cannot prove that an operating system
mounted inputs read-only, denied undeclared filesystem paths, or blocked the
network. Those filesystem and network capabilities must be enforced by the
trusted host; the isolation declaration and prompt text alone are not
enforcement.
