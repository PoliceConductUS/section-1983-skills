# Design: output-root temporary confinement

## Namespace

The writer opens the validated output root and creates two sibling reserved
namespaces:

- `.skill-runs/<run-id>/` for durable incomplete, success, and failure receipts;
- `temp/<run-id>/` for transient staging files used by that run.

Both paths are created and opened relative to the retained output-root directory
descriptor without following symlinks. Public `write()` calls reject `temp/` and
`.skill-runs/` paths before filesystem resolution.

## Process configuration

An open run exposes a fresh value object containing:

- `cwd`: the canonical absolute `<output-folder>/temp` path;
- `environment.TMPDIR`: the same path;
- `environment.TMP`: the same path; and
- `environment.TEMP`: the same path.

The object supplies launch configuration only. It does not launch a process or
merge ambient environment values. A trusted host combines this configuration
with the Issue #64 operating-system isolation boundary so undeclared paths are
not writable or readable.

## Failure behavior

A missing, aliased, nondirectory, or colliding `temp` namespace fails before
artifact publication. Staging cleanup and sync semantics remain unchanged, but
operate against `temp/<run-id>/`. Failure receipts continue to record bounded
phases without absolute paths.
