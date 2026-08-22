## Context

`studying-rule-59e-decisions` already defines study manifests, evidence-ledger
fields, controlled values, missingness limits, and finding cards. The contract
is human-readable but format-neutral, so it cannot be validated consistently.
Issue #15 asks to publish the schema and coding contract, separate different
judicial-authorship stages, preserve missing documents and denominator limits,
prohibit unsupported rates or tendencies, and provide validation fixtures and a
neutral transfer format.

The skill package must remain independently installable, standard-library-only,
public, and free of private case artifacts. General schema engines and corpus
databases are out of scope.

## Goals / Non-Goals

**Goals:**

- Publish a canonical corpus schema containing all required study and decision
  fields.
- Publish a separately reusable neutral transfer-card schema.
- Enforce decision-type/authorship consistency and denominator-strength rules.
- Validate canonical JSON without network access or third-party packages.
- Include synthetic valid and invalid fixtures with focused public-seam tests.
- Route the existing skill and corpus contract to the schemas and validator.

**Non-Goals:**

- Retrieve dockets, opinions, rules, or appellate history.
- Verify authority identity, quotations, pinpoints, later history, or legal
  correctness.
- Support arbitrary JSON Schema keywords or non-JSON working formats.
- Produce success predictions, judge psychology, or litigation strategy.
- Publish any private case corpus or research workspace path.

## Decisions

### Canonical corpus object

`references/decision-corpus.schema.json` describes one corpus object with
`schema_version`, `study`, `denominator`, `decision_records`, `retrieval_gaps`,
and `transfer_cards`. It uses JSON Schema Draft 2020-12 vocabulary for public
documentation, but the repository validator enforces the supported contract
directly and does not claim to implement a general JSON Schema engine.

### Separate neutral transfer-card schema

`references/transfer-card.schema.json` publishes the existing finding-card
fields under neutral names. Corpus cards embed that same object shape. Cards
convey evidence limits and permitted use; they do not choose a filing position
or drafting instruction.

### Semantic validation beyond shape

`scripts/validate_corpus.py` checks required object/list/string/integer/date
fields, controlled values, unique and referentially valid IDs, and these
cross-field invariants:

- recommendations use `recommendation-only` independence and identify a
  recommendation author;
- adoption-only orders use `adopts-without-additional-reasoning`, identify the
  adopting judge, and do not claim an independent reasoning author;
- independently reasoned final decisions use `independent` and identify the
  reasoning author;
- every missing-document reference has a visible gap-log entry;
- a card's row IDs resolve to corpus records;
- a `tendency` or `success-rate` card requires a complete denominator and zero
  unresolved relevant missingness.

The CLI accepts one corpus path, emits stable line-oriented errors, and exits
nonzero on invalid JSON or contract violations.

### Synthetic fixture matrix

Checked-in fixtures include a valid complete corpus containing all three core
decision types, a valid incomplete corpus limited to examples/cluster use, an
invalid incomplete tendency or rate claim, and an invalid authorship-stage
conflation. Tests execute the real CLI against copies of those files and also
mutate controlled inputs for narrow boundary cases.

### Existing contract remains the human guide

`references/corpus-contract.md` retains the research and coding explanations
while making canonical JSON the publication/transfer format. `SKILL.md` requires
reading the contract and running the validator before release or downstream
transfer.

## Risks / Trade-offs

- **[Schema and validator can drift]** → Tests compare public required fields
  and controlled values and execute every checked-in fixture.
- **[Canonical JSON adds an export step]** → Working CSV/YAML/database formats
  remain allowed, but publication uses one portable validation seam.
- **[A valid shape can still contain false coding]** → The skill continues to
  require primary-source verification and `audit-authorities`; the validator
  never certifies legal truth.
- **[Completeness can be overstated]** → The denominator object and gap log are
  explicit, and strong cards fail when their declared missingness contradicts
  completeness.

## Migration Plan

1. Add RED tests and synthetic fixtures that define the canonical public seam.
2. Publish both schemas, implement the validator, and route the skill/contract
   to them.
3. Run focused fixture/CLI tests, full repository validation, skill validation,
   and independent behavior checks.
4. Archive the OpenSpec change on the Issue #15 branch after review.

Existing prose-only studies are not silently converted. They remain prior
artifacts and must export a new versioned canonical JSON file before claiming
schema validation.

## Open Questions

None.
