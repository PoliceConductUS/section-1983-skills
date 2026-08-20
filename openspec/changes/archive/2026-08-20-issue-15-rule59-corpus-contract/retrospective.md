# Retrospective: issue-15-rule59-corpus-contract

> Written: 2026-08-20 after clean whole-branch review. Pre-archive head:
> `6db98db`. Worktree:
> `/Users/dalelotts/dev/PoliceConductUS/section-1983-skills/.worktrees/issue-15-rule59-corpus`

## Evidence

- The focused public contract grew from 16 planned tests to 31 final tests.
- The full evaluation suite passes 181 tests.
- The implementation adds no dependency and keeps validation standard-library
  only and offline.
- All four checked-in fixtures are fictional Example District materials.
- A fresh synthetic public-package artifact validated without private material.

## Wins

- The public skill now has one canonical JSON publication seam while retaining
  CSV, YAML, and database working formats.
- Decision stages preserve recommendation, adoption, and independent reasoning
  authorship instead of collapsing them into a single judge outcome.
- Missing documents, candidate-only gaps, denominator completeness, and neutral
  transfer limits are linked and checked deterministically.
- Incomplete or convenience samples cannot validate a tendency or success-rate
  transfer.

## Misses

- The initial placement tests did not sufficiently prove that every public
  schema field was installed under the skill package. Review strengthened those
  tests before implementation.
- The first GREEN validator left legacy controlled fields and several
  cross-record invariants under-enforced. Corrective RED tests exposed each
  omission before archive.
- The second GREEN still treated some weak-source or incomplete records as
  eligible for strong transfers and did not fully constrain candidate inventory
  or adoption-only authorship. The final 31-test RED closed those boundaries.

## Plan deviations

| Plan area                    | What changed                                                                                                                                                                                                                   | Why                                                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| Public schema placement      | Tests were strengthened before implementation to prove canonical assets and fields live in the public skill package.                                                                                                           | The first test review found that the proposed assertions could pass without adequately protecting the installed package seam. |
| Integrity review             | Added controlled retrieval, confidence, and stated-reason fields; same-motion stage linkage; exact missing-document gap identity; denominator missingness equality; unique transfer row IDs; and candidate/document gap scope. | Whole-diff review found that valid shape alone did not preserve the intended coding and denominator contract.                 |
| Evidence completeness review | Added verified-source rules, complete-pair requirements for strong transfers, the candidate inventory formula, and required recommendation authorship on adoption-only orders.                                                 | A final whole-branch review found four remaining ways evidence strength or authorship could be overstated.                    |
| Sync workflow                | Some `git town sync` attempts were stopped by the permission gate; the parent agent retried and the next successful sync included the pending commits.                                                                         | This was workflow evidence for protected network mutation, not a product defect.                                              |

## Workflow compliance

The repository retains OpenSpec brainstorm, design, plan, delta specification,
tasks, verification, and retrospective artifacts. Tests preceded production in
the initial and both corrective cycles. Work occurred in the Issue #15 worktree,
and each commit was synced or included in the next successful
permission-authorized Git Town sync. The user-forbidden `.superpowers` directory
was not created; temporary workflow evidence stayed under `/private/tmp`.

## Surprises

- Candidate counts need a mechanically stated equation: coded motion IDs plus
  distinct unresolved candidate IDs. Record-linked document gaps do not create
  additional candidates.
- A complete denominator is not enough for a tendency if any coded source is
  less than a complete pair.
- An adoption-only row still needs its recommendation author even though it must
  not attribute that reasoning to the adopting judge.

## Long-term learning

No new repository feature is proposed. The durable schema, validator, tests, and
generated OpenSpec capability now carry these lessons directly.
