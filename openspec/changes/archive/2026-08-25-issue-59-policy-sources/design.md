# Design: Folder-native police-policy source collection

## Invocation boundary

The installed skill contract has exactly four recursive read-only roles:
`department-identity`, `jurisdiction`, `approved-source-system`, and
`research-scope`. Target is none. Internet is `authorized`. One caller-supplied
full absolute output folder is the only writable root. The trusted host binds
the process working directory and temporary environment variables to
`<output-folder>/temp/`.

## Source acquisition

The agent follows only the bounded scope, source systems, access limits, cost
limits, and checked-through date provided by the declared inputs. A fee,
credential boundary, ambiguous identity, unavailable source, or out-of-scope
result remains a gap. Empty search results prove only the recorded search
coverage; they never prove that a policy or version does not exist.

The collector distinguishes adopted policy, statute, regulation,
collective-bargaining material, accreditation material, model policy, training
material, form, guidance, and comparison material. Classification and proposed
adoption relationship remain reviewable source facts, not policy meaning.

## Domain YAML

Every retrieved ordinary file has an adjacent `<name>.SOURCE.yaml`. The strict
record binds a stable source ID to one output-relative artifact path and its
SHA-256, URL, exact query and filters, retrieval and checked-through dates,
result identity, classification, proposed adoption relationship, review state,
retrieval result, effective-date evidence or gap, limitations, and duplicate
relationships.

`policy-source-candidates.yaml` contains an ordered list of source IDs and their
source-documentation paths. `policy-source-gaps.yaml` contains ordered bounded
search gaps. These YAML records document files and research results; they do not
define folder membership, filesystem authority, commands, or capabilities.

## Collector/analyzer separation

The collector returns output-relative artifact plans to the trusted host. The
host publishes them append-immutably and records the terminal run receipt. The
collector never calls Issue #57 or treats newly acquired bytes as approved
analysis input. A later invocation may declare the reviewed output folder as a
read-only policy-source input.

## Failure model

Malformed paths, duplicate IDs, duplicate documentation paths, unsupported
classifications or states, missing provenance, invalid dates or URLs, hash
mismatches, and undeclared capability fields are invalid. Inaccessible,
ambiguous, incomplete, or empty research results are valid only as explicit
gaps. Inputs remain byte-identical and no artifact is published outside the
explicit output boundary.
