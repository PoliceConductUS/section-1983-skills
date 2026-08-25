# Issue #3 verified-authority plan

## Goal

Build the folder/YAML verified-authority citation gate without a package, graph,
repository, or ambient corpus dependency.

## Steps

1. Correct the live issue and public skill contract; remove FilingPacket and
   canonical-root assumptions.
2. RED-test strict corpus, authority, and source YAML binding to ordinary files.
3. Implement fixed-role loading and fail-closed authority selection.
4. RED-test eyecite candidate extraction, persistent citation mapping, exact
   quotation checks, and stable findings.
5. Implement deterministic audit and explicit output/temp publication.
6. Run focused and full validation, archive OpenSpec, verify the exact remote
   head, and mark the PR ready while leaving the PR and issue open.
