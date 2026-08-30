# Retrospective

## What changed

The repository now exposes fixed `opposing-counsel` and `judicial-reviewer`
findings roles. Each role is conditioned on selected ordinary profile, filing,
source, and domain-YAML files without letting profile data change its operation,
permissions, or output authority.

## What the review caught

The first green implementation rejected a `disposition-emitted` field and
hostile profile capabilities, but the failure inputs existed only as inline test
data. Whole-story review added one checked-in disposition fixture and one
checked-in profile-override fixture for each role, matching the live issue's
behavioral-fixture requirement.

## Result

Both roles run through the shared folder-scoped launcher, preserve all selected
inputs, keep every transient byte beneath the explicit output folder, and return
only proposed source-backed findings for trusted-host publication.
