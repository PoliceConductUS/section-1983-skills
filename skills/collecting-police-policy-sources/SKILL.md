---
name: collecting-police-policy-sources
description: >-
  Use when bounded public research must collect police-policy source files and
  YAML provenance for later independent policy analysis.
---

# Collecting Police-Policy Sources

Collect ordinary policy-source files and document their provenance. Do not
interpret policy meaning or decide compliance, liability, admissibility, or
filing readiness.

## Folder inputs and output

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only. The
exact roles are:

- `department-identity` contains the approved department identity and aliases.
- `jurisdiction` contains the approved jurisdiction and relevant time scope.
- `approved-source-system` contains the approved official or public source
  systems and any access constraints.
- `research-scope` contains the bounded questions, checked-through date, query
  limits, access limits, and cost limits.

Target is none. Internet is `authorized` only for the bounded collection
described by those inputs. The caller supplies one exact full absolute output
folder or execution stops to ask for it. Writes occur only beneath the
caller-declared output folder. Only the trusted host may publish returned
artifacts beneath that folder. Every cache, download, staging file, working
file, process current directory, and `TMPDIR`, `TMP`, or `TEMP` location must
remain beneath `<output-folder>/temp`; no other temporary location is available.

Internet is used only when that skill expressly authorizes it. Execution stops
before reading case material if the host cannot enforce the filesystem and
network boundary.

Read the [source-documented folders](references/source-documented-folders.md)
contract and [policy-source YAML contract](references/policy-source-yaml.md)
before research.

## Research boundary

Use only approved source systems and the exact department, jurisdiction, date,
query, access, and cost scope supplied at invocation. Never incur a fee, use an
unapproved credential, broaden the jurisdiction, or follow an unapproved source
system without separate user authorization.

Preserve the exact query, filters, checked date, result identity, URL, and
coverage limitation. An empty result, incomplete index, unavailable archive,
paywall, ambiguous identity, or out-of-scope result is a gap. It can never
establish absence. Empty or incomplete searches never establish that a policy or
version does not exist.

## Classify without interpreting

Select exactly one source classification:

- `adopted_policy`
- `statute`
- `regulation`
- `collective_bargaining`
- `accreditation`
- `model_policy`
- `training_material`
- `form`
- `guidance`
- `comparison_source`

Record the proposed adoption relationship separately as `documented`,
`uncertain`, `rejected`, or `not_applicable`. A model policy, accreditation
standard, training document, form, or comparison source does not become
department policy without adoption evidence. Classification never establishes
policy meaning, compliance, or legal effect.

## Return ordinary files and domain YAML

For each retrieved ordinary file, return:

1. one canonical output-relative path beneath `sources/` and the exact bytes;
2. one adjacent canonical `<source-name>.SOURCE.yaml` path and deterministic
   bytes satisfying the policy-source YAML contract; and
3. one candidate-index entry identifying that source-documentation path.

Also return `policy-source-candidates.yaml` and `policy-source-gaps.yaml`. These
YAML files document proposed source files and research coverage. They do not
define folder membership, grant filesystem or network authority, or supply
commands. Return deterministic artifact plans; never open the output folder or
write files directly.

Only the trusted host publishes the proposed files append-immutably and records
the terminal run receipt. All proposed artifact paths are output relative;
`temp/`, `.skill-runs/`, absolute paths, traversal, symlinks, and undeclared
paths are unavailable.

## Keep collection separate from analysis

Do not invoke, emulate, or perform Issue #57 policy decomposition during this
collection. Newly acquired material remains candidate collection output. It may
be analyzed only in a later invocation after review, when the caller expressly
declares the resulting ordinary folder as a new recursive read-only input.

Do not add atomic requirements, duties, prohibitions, actor scope, compliance
status, constitutional analysis, Monell analysis, negligence analysis, or filing
conclusions to source documentation.

## Return contract

Return proposed ordinary bytes and deterministic YAML bytes under canonical
output-relative paths, plus every bounded gap. Preserve source provenance,
classification, adoption uncertainty, effective-date evidence or gap, review
state, limitations, duplicates, and SHA-256. Missing or invalid provenance,
changed bytes, unsupported fields, duplicate identities, or escaping paths are
invalid and ineligible for publication.

This skill does not research a real department in repository fixtures and does
not decide what the user should allege, argue, or file.
