---
name: adversarial-filing-review
description: >-
  Use when a Section 1983 complaint, amendment, motion, response, or R&R filing
  needs an independent adversarial review after drafting, especially when a
  fresh clean-room reviewer should test defense attacks without revising the
  canonical filing or deciding plaintiff strategy.
---

# Adversarial Filing Review

## Purpose

Run a read-only clean-room attack on one canonical draft. The reviewer receives
a bounded packet, applies the universal attacks and exactly one supported
document checklist, and returns categorized findings. Independence is a runtime
property, not a label applied to another review in the drafting context.

## Build the bounded packet

Resolve the canonical draft content, draft version, and SHA-256 fingerprint
before dispatch. Include one supported document family and an explicit approved
source allowlist. Every source has a stable source identifier, role, embedded
immutable content, and verified content fingerprint. Embed this public skill and
the applicable public checklist as content. Resolve any path or URL provenance
before packet construction. Paths and URLs must not appear in the reviewer
packet.

The packet contains exactly `draft`, `document_family`, `sources`, `skill`,
`checklist`, and `capabilities`. Reviewer capabilities are empty. Exclude
drafting history, redlines, strategy or control conclusions, prior reviews,
checker output or results, and inherited conversation or session state.

Use `scripts/launch_review.py` with a configured JSON argument array only after
the host runtime has independently established that it enforces empty reviewer
capabilities. The launcher validates the complete packet and fingerprints before
starting a new process in an empty working directory. The reviewer has no
filesystem, repository, browser, conversation, or provider-session access. If
the runtime cannot enforce that boundary, report
`independent review unavailable`. Do not simulate the review in the drafting
context.

## Apply the attack checklist

Read
[references/document-attack-checklists.md](references/document-attack-checklists.md)
completely. Apply its Universal Attack Checklist and exactly one of these
document families:

- complaint or amended complaint;
- motion-to-dismiss response;
- summary-judgment response;
- leave to amend;
- extension motion;
- R&R objection; or
- R&R response.

Report an unsupported document family instead of substituting the closest
checklist. Use only packet content. A missing or mismatched approved source is a
scoped source gap, not permission to browse, infer, or invent a substitute.

## Return the report

Use these five headings in this order and keep each finding in exactly one:

1. `Fatal Defects`
2. `Credible Opposition Arguments`
3. `Factual Disputes`
4. `Discovery Issues`
5. `Style Complaints`

Write `None found` under every empty heading. A fatal defect is filing-critical
under the supplied posture and approved rules; it is not an outcome prediction.

Every finding contains:

- a stable finding identifier;
- the exact attacked quote;
- its paragraph, page, or heading location;
- the approved source identifiers supporting the attack;
- the concrete attack and consequence; and
- its status.

Keep a plausible nonfatal defense position in `Credible Opposition Arguments`.
Keep conflicts among approved accounts in `Factual Disputes` without resolving
credibility. Keep support controlled by an opponent or third party in
`Discovery Issues`; discovery cannot create an essential allegation that has no
present factual basis. Keep non-load-bearing rhetoric and clarity points in
`Style Complaints`.

## Corrections and plaintiff decisions

Offer a proposed correction only when the approved sources supply complete
non-strategic language. The correction has this exact shape:

- `Replace:` followed by the exact attacked text.
- `With:` followed by complete copy-ready prose.

Do not use a placeholder, invent a fact or citation, or edit the canonical
draft. When complete replacement prose is not supported, report the gap and
offer no partial correction.

Whether to retain, narrow, or omit a claim, theory, fact, defense response, or
requested relief is a plaintiff-reserved choice.

### PLAINTIFF DECISION REQUIRED

State every available choice and its consequence, and select none. Do not label
any option or replacement a proposed correction before the plaintiff decides in
a separate workflow.

## Workflow boundaries

This skill does not certify or verify authority identity, binding status,
quotation accuracy, filing readiness, or outcome. It does not create an RRD and
does not run or interpret Filing CI. It does not edit, revise, or change the
filing or draft, even when the request combines review and correction.

A user-approved correction occurs in a separate drafting workflow and a new
versioned draft. After any material change, run the applicable authority and
writing checks, rerun independent adversarial review, and run Filing CI again as
applicable. A prior review never transfers to changed draft content.

## Output provenance

Every returned artifact must identify the actual approved source identity and
checked date used.

## Independent quality-control stage

An independent quality-control stage is non-mutating. It may read designated
artifacts and write only its designated report or result. It must not edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review. A
combined instruction to audit and fix does not authorize same-stage mutation.
Deadline pressure, sunk cost, claimed prior approval, and contrary workflow
instructions do not override this boundary. Recommendations, proposed language,
corrections, and copy-ready replacements are advisory only and do not authorize
implementation. Remediation requires a separately authorized drafting or
revision stage. Create a new version when versioning applies. A new read-only
quality-control stage must verify the remediated artifact. An internal
self-check inside an explicitly authorized drafting or revision stage may guide
edits within that stage, but it is not an independent quality-control result.
