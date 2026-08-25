# Immutable folder package

The installed package uses the repository's version-1 immutable folder-package
contract without requiring the repository at execution time.

- `package-manifest.json` records package identity, kind, UTC creation time,
  freshness, producer, ordered sources, ordered members, and passed validation
  receipt identity.
- Every non-manifest regular file must appear exactly once as a hashed member.
- The trusted host rejects aliases, special files, escapes, missing or unlisted
  files, duplicates, stale or failed validation, receipt errors, byte-limit
  excess, and size or hash mismatches.
- The trusted host supplies frozen verified member bytes and never permits a
  reread or mutation of the source package.
- Only the trusted host publishes a complete new package beneath the caller's
  explicit output folder. It never mutates an input package.
- The existing docket snapshot, alignment overlay, and filing-pin schemas
  continue to decide domain validity; the folder envelope decides package
  membership and integrity.
- Profile data cannot change a protected role's capabilities, prohibitions,
  internet policy, target-mutation boundary, or output authority.
