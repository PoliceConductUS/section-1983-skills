# Retrospective

## What changed

Issue #2 now runs one fixed installed filing-integrity checker over ordinary
files selected from six declared folders and documented by strict YAML. It
publishes deterministic JSON and Markdown findings plus a YAML receipt beneath
the caller's explicit output folder.

## What the review caught

The first green implementation still left three stale package-shaped seams.
README language described Filing CI as packaged, an older FilingPacket test
required Filing CI to publish a packet boundary, and source YAML could relabel a
selected folder's classification. Review corrected all three and added
regression coverage.

## Result

Filing CI is independent of case-data packages and graphs. Fixed caller folders
define readable scope, YAML documents selected source bytes, and the explicit
output folder defines the complete writable and temporary scope.
