# Issue #94 implementation plan

## Goal

Delete the implemented FilingPacket persistence abstraction and leave only
ordinary declared input folders, explicit target paths, domain-owned YAML source
records where applicable, the exact output folder, and its `temp/` subtree.

## Steps

1. Publish this design on a stacked branch and open a draft PR based on Issue
   #32's branch.
2. RED-test the exact obsolete implementation inventory, current skill guidance,
   active specifications, and replacement-abstraction prohibition.
3. Delete the FilingPacket implementation, schema, documentation, fixtures,
   specialized tests, and install-local references.
4. Update current skill guidance, governance, folder-operation guidance, and
   durable specifications to ordinary-folder and explicit-target behavior.
5. Run focused tests and full validation, perform whole-story review, record
   verification and retrospective evidence, and archive OpenSpec.
6. Verify exact local, origin, and PR heads plus GitHub checks, mark the PR
   ready, and leave both PR and Issue #94 open.
