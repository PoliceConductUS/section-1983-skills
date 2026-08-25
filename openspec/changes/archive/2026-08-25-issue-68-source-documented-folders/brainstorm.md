# Brainstorm: source-documented folders without packages

## Accepted direction

The package abstraction is removed. A skill invocation already has the only
generic storage boundary it needs: named recursive read-only input folders and
one explicit output folder. Domain artifacts remain ordinary files. YAML files
owned by the applicable domain document source identity, provenance, dates,
hashes, classifications, validation, assumptions, and gaps.

There is no root package envelope, package identity, package kind, loader,
publisher, registry, graph, or compatibility layer. The trusted host may pin
declared input bytes using the existing logical input manifest, but that
host/run receipt does not turn an input folder into a package.
