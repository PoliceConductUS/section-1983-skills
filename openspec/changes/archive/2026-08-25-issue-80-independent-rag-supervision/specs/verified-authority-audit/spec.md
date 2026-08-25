## ADDED Requirements

### Requirement: Filing-near authority work has an independent audit stage

The skill MUST require a separate non-mutating `audit-authorities` invocation
for authority work performed by a stage that generated or materially revised a
filing-near legal proposition. The generating stage MUST NOT certify its own
authority work. The audit MUST read one exact target from a recursive read-only
`filing-source` folder, exact selected files from recursive read-only
`verified-authority` folders, and MUST use a new explicit output folder distinct
from the generation output folder. All audit temporary work MUST remain beneath
the audit output folder's `temp/` directory.

#### Scenario: Generator performs its own review

- **WHEN** generation and audit use the same stage or invocation identity
- **THEN** the result is `generator-self-review` and cannot pass supervision

### Requirement: Supervision binds both stages to immutable ordinary bytes

The supervision record MUST preserve generation-stage and audit-stage
identities, invocation identities, model or provider when available, exact
role/path/SHA-256 input fingerprints, selected source identities, UTC execution
times, and distinct output-folder fingerprints. Changed target or source bytes
MUST invalidate the prior audit. The record MUST NOT contain credentials,
provider continuation state, conversation IDs, or session IDs.

#### Scenario: Authority bytes change after audit

- **WHEN** a current selected authority fingerprint differs from the audit-stage
  fingerprint
- **THEN** the prior supervision result is `changed-input` and cannot pass

### Requirement: Independent execution and proposition outcomes remain distinct

The supervision contract MUST distinguish successful independent execution,
unavailable independent execution, malformed audit output, unresolved source
gaps, incorrect propositions, misgrounded propositions, ungrounded propositions,
and completed grounded propositions. Missing, unavailable, malformed, changed,
self-reviewed, failed, or unresolved states MUST NOT collapse into a pass.

#### Scenario: Independent provider is unavailable

- **WHEN** the required independent audit cannot execute
- **THEN** the record reports `independent-execution-unavailable` and cannot
  pass

### Requirement: Filing approval remains human reserved

AI MAY assemble research and audit records but MUST NOT decide litigation
strategy or filing approval. An AI-only supervision record MUST use
`human_approval: not-provided` and MUST NOT represent itself as human review or
approval.

#### Scenario: Every proposition is grounded

- **WHEN** a successful independent audit grounds every material proposition
- **THEN** supervision may report `passed`
- **AND** the record still does not represent human filing approval

### Requirement: Legal-RAG regression corpus is complete and deterministic

The repository MUST contain a versioned, network-independent synthetic YAML
corpus covering inverted holding, party voice, lower-court voice, superseded
panel, overruled authority, wrong jurisdiction, wrong statute, wrong date, wrong
posture, irrelevant citation, split support, uncited material proposition,
fictional judge, nonexistent rule, and corrected false premise. Every fixture
MUST preserve immutable source text and SHA-256, challenged text, expected
proposition correctness and groundedness, expected source voice, and the exact
reason a pass is allowed or forbidden.

#### Scenario: Fixture taxonomy is incomplete

- **WHEN** any required failure class or required expected field is absent
- **THEN** deterministic repository validation fails

### Requirement: Historical benchmarks remain dated and bounded

Any optional live-provider benchmark MUST remain separate from the synthetic
acceptance corpus and record provider, product, version, date, complete query
provenance, query distribution, sample size, and limitations. A historical
result MUST NOT be represented as a current vendor reliability rate.

#### Scenario: Prior benchmark is cited without version and dates

- **WHEN** a historical benchmark lacks its evaluated product version or dates
- **THEN** it cannot support a current reliability claim
