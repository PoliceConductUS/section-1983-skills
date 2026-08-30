# Retrospective

## What changed

The prior implementation did not merely use a folder. It created a persistence
abstraction around that folder: one mandatory root JSON file, a schema, a
loader, a publisher, membership rules, stable packet identities, packet roles,
and packet-level gate semantics. This migration removes that entire layer
instead of renaming it.

## What remained valid

Recursive input non-mutation, explicit target selection, trusted-host output
publication, independent-review non-mutation, authority gates, complaint
fail-closed behavior, and user-owned litigation judgment remain unchanged.

## Review correction

One existing complaint-composition test depended on the formatter's exact line
wrapping around its fail-closed sentence. Rewording “canonical package” exposed
that brittleness. The test now recognizes semantically identical whitespace
without weakening the required “do not draft, revise, or audit” rule.

## Downstream rule

Future filing stories receive declared read-only folders and ordinary files.
They select a file by role-relative path, use domain-owned YAML only when that
domain requires source documentation, and write to the exact output folder. They
must not recreate folder membership or persistence through a new name.
