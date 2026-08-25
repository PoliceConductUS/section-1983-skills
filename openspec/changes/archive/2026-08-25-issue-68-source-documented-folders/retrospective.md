# Retrospective

## What changed

The first Issue #68 implementation duplicated the folder invocation boundary
with a second identity and membership abstraction. The correction removed that
entire layer rather than preserving it under different names.

## Result

The stack now has one generic persistence contract: declared recursive read-only
input folders and one explicit output folder. Domain YAML files carry the source
documentation each artifact type actually needs. Protected behavior remains
installed and input data remains data.

## Follow-through

Issues #33 and #61 must now be restacked and corrected to consume ordinary
folder files and domain YAML directly. Neither may import or recreate the
removed package helpers.
