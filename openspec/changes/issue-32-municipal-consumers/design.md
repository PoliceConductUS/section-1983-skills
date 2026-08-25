# Design: Municipal profile consumers

## Exact folder roles

The following installed skills add `municipal-profile` to their existing exact
recursive read-only roles:

- `drafting-section-1983-complaints`;
- `rrd-rule12-city`;
- `drafting-section-1983-written-discovery`;
- `drafting-section-1983-deposition-outlines`; and
- `adversarial-filing-review`.

Each skill retains its current target policy and internet policy. Every durable
write remains beneath the one caller-declared output folder, and every temporary
byte and process temporary location remains beneath `<output-folder>/temp/`.

## Validation boundary

Before specialized work, each consumer requires `municipal-profile.yaml`,
`municipal-profile-gaps.yaml`, `municipal-profile.md`, and
`municipal-profile-validation.json` in the declared profile folder. The consumer
validates version 1, `valid: true`, one consistent profile identity, an ISO
checked-through date, selected-source hashes, upstream hashes, input-folder
fingerprints, and exact evidence, entity, event, chain, comparison,
contradiction, feature, and gap ID sets. Missing files, invalid syntax, changed
bytes, inconsistent identity, stale caller-rejected dates, failing validation,
or unresolved IDs stop specialized work.

The input-folder fingerprint comes from the trusted folder-boundary host and is
preserved in the consumer's output provenance. It does not create a new data
container.

## Consumer use

- Complaint drafting may map supported record facts and explicit gaps to one
  caller-selected municipal theory, candidate policymaker, notice path,
  causation mechanism, and challenged act. The profile cannot supply an
  allegation absent from the case record or select the theory.
- City Rule 12 planning may map the motion's actual attacks to profile domains,
  counterevidence, and gaps while preserving the pleading/record boundary and
  separately verified authority gate.
- Written discovery and deposition outlines may convert explicit profile gaps
  into bounded targets, requests, topics, and questions. A gap is not an
  expected fact.
- Adversarial review may attack the filing's municipal theory using only its
  declared profile, filing, and approved-source folders. It remains non-mutating
  and cannot select a disposition.

## Output boundary

Drafting consumers return proposed artifacts only beneath the explicit output
folder. Review output remains an immutable Issue #67 report. A later audit can
read a prior output only when the caller declares that folder as an input to a
new invocation.
