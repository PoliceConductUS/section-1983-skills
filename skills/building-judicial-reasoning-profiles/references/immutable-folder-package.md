# Immutable folder package

- `package-manifest.json` records version, package kind and identity, UTC
  creation time, freshness, producer, ordered sources, complete ordered members,
  hashes, and passed validation receipt identity.
- Every non-manifest regular file appears exactly once as a hashed member.
- The trusted host rejects aliases, special files, escapes, missing or unlisted
  files, duplicates, stale or failed validation, receipt errors, byte-limit
  excess, and size or hash mismatches.
- The trusted host supplies frozen verified member bytes. The skill never
  rereads or mutates the source package.
- Only the trusted host publishes a complete new package beneath the caller's
  explicit output folder.
- The judicial-profile schema decides domain validity; the common envelope
  decides package membership and integrity.
- Profile data cannot change a protected role's capabilities, prohibitions,
  internet policy, target-mutation boundary, or output authority.
