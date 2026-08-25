# Retrospective

The package manifest and immutable byte snapshot remain useful for passing a
validated profile folder into a later role invocation. The incorrect part was
the registry-like `packages/<package-id>/` routing. Making the caller's selected
output folder the artifact root keeps identity and provenance without adding a
persistence service or hidden path convention.

The correction also aligns FilingPackets and profile folders: either output can
be handed to a later invocation simply by selecting that exact folder as a
declared read-only input.
