# Design

## Context

The durable quality-control contract already separates read-only assessment from
later remediation. It permits a quality-control stage to write its own report or
result, but it does not identify the report root, protect earlier reports, or
distinguish generated reports from the artifacts under review.

## Decisions

### Resolve the audited version first

The stage must receive or resolve one existing version-specific directory before
the review begins. A missing, ambiguous, nonexistent, or out-of-bound version
directory makes report output unavailable. The stage does not invent a fallback
directory or write to a project root, shared temporary location, current working
directory, or neighboring version.

### One immutable report inside `audits/`

Each run writes exactly one new report below the canonical
`<version-folder>/audits/` directory. The filename uses
`<check-kind>-<UTC timestamp>-<run-id>.md`. The check kind is a stable lowercase
hyphenated identifier; the timestamp is UTC; and the run ID makes concurrent
runs distinct.

The report path must remain confined to the canonical `audits/` directory. The
stage must not follow a traversal or symlink outside it. Creation is exclusive:
if the selected path already exists, the run fails closed and preserves the
existing bytes. Reports are never edited, overwritten, replaced, renamed, or
deleted by a later quality-control run.

### Generated reports are not implicit review input

The `audits/` directory is excluded from the designated artifacts under review.
If an audit report itself needs review, the caller must expressly designate that
specific report. The reviewing stage then writes a different new report rather
than changing the report being reviewed.

### Report content remains advisory

Every report identifies the audited version, artifact paths and SHA-256
fingerprints, quality-control kind, UTC run time, run ID, scope, approved source
identities, and result. It separates failed findings from passing-but-suboptimal
observations. Either section may include concrete recommendations, proposed
language, or copy-ready replacements. A report must state that recommendations
are advisory and require separately authorized remediation. A passing result
does not convert an improvement into a required edit or authorize mutation.

### Independently installable coverage

The root governance policy owns the complete rule. The same compact conditional
contract is repeated in every public entrypoint identified by the existing
behavioral quality-control trigger. The current skill-name inventory remains a
test diagnostic, not the governing scope.

### Deterministic and behavioral enforcement

Extend the existing governance validator rather than add a report-writing
engine. Temporary-repository tests remove or invert each path, immutability,
scope, and advisory clause and require a stable skill-specific finding. Fresh
agents exercise actual filesystem behavior with original artifacts and prior
reports fingerprinted before and after.

## Risks

- **A report becomes review input on the next run:** exclude `audits/` unless a
  specific report is expressly designated.
- **A stable filename destroys history:** require timestamp plus run ID and
  refuse collisions.
- **A missing version root causes a convenient fallback:** fail closed and write
  nowhere else.
- **Copy-ready advice is mistaken for permission:** preserve the separate
  remediation and fresh-review stages.
- **Root-only policy disappears on installation:** repeat the compact contract
  in each behaviorally affected public skill.
