---
name: analyzing-police-policy-sources
description: >-
  Use when reviewed police-policy files must be decomposed into source-bounded
  atomic requirements without deciding compliance or legal liability.
---

# Analyzing Police-Policy Sources

Convert reviewed adopted-policy text into atomic requirement records. Preserve
the source's operative limits. Do not assess conduct or decide liability.

## Folder inputs and output

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only. The
exact roles are:

- `department-identity` contains the approved department identity and aliases.
- `jurisdiction` contains the approved jurisdiction and time scope.
- `policy-source` contains reviewed ordinary source files and adjacent domain
  `SOURCE.yaml`.
- `analysis-scope` selects source-documentation paths, approvals, dates, and
  bounded questions.

Target is none. Internet is `disabled`. The caller supplies one exact full
absolute output folder or execution stops to ask for it. Writes occur only
beneath the caller-declared output folder. Each proposed durable artifact uses
one canonical output-relative path in append-immutable mode. Only the trusted
host publishes it. Report every missing or ambiguous source fact as a bounded
gap.

Every extraction file, cache, staging file, working file, process current
directory, and `TMPDIR`, `TMP`, or `TEMP` location stays beneath
`<output-folder>/temp`; no other temporary location is available. Internet is
used only when that skill expressly authorizes it. Execution stops before
reading case material if the host cannot enforce the filesystem and network
boundary.

Read the [source-documented folders](references/source-documented-folders.md)
contract and
[policy requirement YAML contract](references/policy-requirement-yaml.md) before
analysis.

## Validate before decomposition

Resolve every selected `SOURCE.yaml` and ordinary artifact inside
`policy-source`. Require the documented relative path, SHA-256, source identity,
classification, adoption relationship, review approval, and effective-date
state to match before semantic work.

Only `adopted_policy` with `documented` adoption and separate
`approved_for_analysis` review may generate a department-policy requirement.
Statutes, regulations, collective-bargaining materials, accreditation
standards, model policies, training materials, forms, guidance, and comparison
sources remain distinct. They may identify a bounded gap or comparison question
but never become department policy without documented adoption.

Never apply a later policy retroactively. Preserve the source's effective date
or interval. If the effective date, supersession history, or applicable version
is uncertain, return a gap and do not generate a requirement for the uncertain
period.

## Decompose atomic operative units

One record contains one independently testable unit. Preserve:

- the exact quotation, pinpoint, source-relative path, and source hash;
- stable department, policy, source, and requirement identities;
- effective start, end, or explicit date gap;
- covered actor and triggering conditions;
- exactly one type: `mandatory`, `prohibited`, `permitted`, or `discretionary`;
- the required, prohibited, permitted, or discretionary action;
- every exception, definition, dependency, and cross-reference;
- every required documentation or review step; and
- every unresolved gap.

A condition never becomes an unconditional duty. A permission never becomes a
mandate. Discretion never becomes a duty or prohibition. An exception stays
attached to the same operative unit. If a referenced definition, exception,
dependency, page, or cross-reference cannot be resolved, return a gap instead
of completing the requirement by inference.

## Return artifacts without assessing conduct

Return deterministic output-relative bytes for:

- `policy-requirements.yaml`;
- `policy-analysis-gaps.yaml`;
- `policy-analysis.md`; and
- `policy-analysis-validation.json`.

The helper returns an artifact plan only and never opens an input or output
root. Only the trusted host publishes the plan and its terminal run receipt.
The caller may supply the resulting ordinary folder as a later read-only input
to a separately authorized policy-assessment invocation.

Do not decide whether an actor complied with a policy. Do not decide
constitutional or Monell liability, negligence, admissibility, governing legal
authority, litigation strategy, or filing readiness. Do not draft or edit a
filing.
