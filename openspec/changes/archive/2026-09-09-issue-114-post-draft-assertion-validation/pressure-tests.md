# Pressure-test evidence

## Baseline fresh-context test

The exact prompt and verbatim output are preserved in
[`pressure-tests/baseline.md`](pressure-tests/baseline.md).

A fresh-context reviewer received the seven original regression sources without
the new shared validation skill. The reviewer rejected the specific bad
conclusions, but could not reliably infer the reusable workflow:

- no formal report schema or complete per-assertion field set;
- no controlled classification and result vocabulary;
- no exact status roll-up or stopping rules;
- no complete freshness lifecycle, binding inventory, or dependency invalidation
  rule;
- no citation-granularity rule; and
- no way to determine whole-document completeness without the underlying
  court-facing target.

This established the baseline gap: common legal caution could catch obvious
examples, but it did not supply the stable, reusable, auditable contract.

## Initial guided fresh-context test

A separate reviewer received the implemented skill and the seven original
scenarios. It located an explicit rule for every regression and confirmed the
read-only correction boundary and deterministic-check limitation. It also found
these contract defects before delivery:

- target-hash binding literally made all findings stale after any target-byte
  change despite the intended unaffected-finding reuse rule;
- `Plaintiff submitted` did not have an unambiguous status under the source;
- the authority-audit handoff did not say how to handle an unavailable required
  specialist finding;
- the first reference candidate was shorthand rather than a complete report; and
- the described observation-review method was stronger than the supplied
  Markdown observation artifact.

The implementation now uses finding-level freshness bindings, a result list,
accurate method labels, a complete reference candidate, and fail-closed
specialist availability.

## Independent branch review

An independent code reviewer identified and the implementation addressed:

- corpus expected-finding IDs that disagreed with the canonical evaluator;
- semantic-owner governance running against generic temporary repositories;
- one-result records that could not preserve independent support and
  documentation statuses;
- a missing declared role for Filing CI results;
- a multi-document Rule 59 packet conflicting with one-target validation;
- missing declaration-skill routing;
- missing prior issue-register continuity; and
- missing Rule 59 and declaration OpenSpec deltas.

The user then approved an eighth behavioral rule: party-drafted advocacy cannot
independently support an underlying event or quotation, while a separate
identified Plaintiff-memory source may support an attributed memory claim. The
post-change fresh-context results are recorded below after their final run.

## Final guided fresh-context test

The exact prompt, correction, and verbatim corrected output are preserved in
[`pressure-tests/green.md`](pressure-tests/green.md).

The fresh-context invocation produced a complete proposed report without editing
the target. It independently applied all eight behavioral requirements,
preserved Plaintiff memory only as an attributed memory claim, refused to use a
party-drafted motion as event or quotation evidence, carried forward the prior
issue register, separated repository `HEAD` from reviewed working-tree bytes,
and bound findings to exact hashes. The first response exposed an exact-text
quotation defect; the corrected run preserved the target text byte-for-byte and
rechecked its status counts.
