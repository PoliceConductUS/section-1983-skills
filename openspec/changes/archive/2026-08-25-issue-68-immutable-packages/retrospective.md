# Retrospective

## What worked

- Separating the folder envelope from domain schemas preserved current counsel
  and alignment validators while creating one reusable integrity boundary.
- Frozen member bytes made the package/run boundary concrete without adding a
  case-management or repository dependency.
- Keeping canonical role-contract bytes separate from package bytes directly
  proved that instruction-shaped profile data cannot become behavior.
- RED and GREEN commits exposed every new public contract before its
  implementation and kept the draft PR synchronized throughout.

## Review correction

The first loader implementation enforced `max_bytes` only after reading the
manifest and all members. Fresh whole-story review identified that this did not
provide a bounded read. A new RED test prohibited reads of already-oversized
manifest/member paths; the loader now checks file sizes and uses bounded reads
before accepting bytes.

The first public README wording named an obsolete runtime while denying any
dependency on it. The existing onboarding regression test correctly rejected the
terminology. The README now describes the boundary as product- and
repository-runtime-independent.

## Deferred by contract

- Issue #33 owns the generic judicial-profile builder and removal of embedded
  judge-specific runtime assumptions.
- Issue #61 owns fresh-process launch of a static role with validated profile,
  target, context, and output packages.
- Issues #62 and #63 own concrete role packages and comparative sweeps.
