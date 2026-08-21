# Retrospective

## What worked

- Fresh-agent pressure separated three failure modes that a prose-presence test
  could not: overwriting a prior report, writing outside the version, and
  writing beside the filing.
- Extending the existing behavior classifier kept the contract tied to what a
  skill does rather than a permanent name registry.
- Repeating the compact rule in every affected public package preserved the
  boundary when a skill is installed without repository-root governance.
- Keeping failed findings separate from passing-but-suboptimal observations
  preserved both a truthful result and useful advisory improvement guidance.

## Misses and corrections

- The first deterministic RED expressed an out-of-bound failure but did not
  explicitly name traversal and symlink escapes. Review tightened the contract
  and its mutation test before implementation.
- The initial classifier matrix used synthetic descriptions only. Current live
  quality-control descriptions and stronger drafting-from-report negative
  controls were added before GREEN.
- The first live-description GREEN fixture copied the newly updated report
  contract along with the description. Removing one required clause from the
  copied fixture made the test exercise the intended classifier seam.

## Preserved boundary

The story adds no report-writing or remediation engine. It defines and validates
the install-local agent contract. Actual instruction-following behavior remains
covered by fresh-agent pressure tests, while deterministic CI checks the public
contract and rejects its tested inversions.

## Future rule

When a new public skill can run as an independent quality-control stage, give
its frontmatter an explicit behavioral trigger and include both the non-mutation
contract and this version-local immutable-report contract. A new report must
never become implicit review input for the next run.
