# Approved Source Documentation

Each source selected from the declared `approved-sources` input folder must have
a selected domain-owned YAML record. The folder remains an ordinary input
folder; this record does not define folder membership or a generic container.

The adversarial reviewer accepts a strict flat YAML mapping with exactly these
fields:

```yaml
schema_version: 1
source_id: SRC-1
role: record
path: sources/SRC-1.txt
sha256: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
checked_through: 2026-08-25
```

- `source_id` is the stable identifier findings may cite.
- `role` is a lowercase domain role such as `record`, `authority`, or
  `operative-filing`.
- `path` is relative to the declared `approved-sources` root and must resolve to
  one ordinary file inside that root.
- `sha256` is the lowercase SHA-256 hash of the exact referenced bytes.
- `checked_through` is an ISO `YYYY-MM-DD` date and must satisfy the minimum
  date selected by the trusted host for the run.

The trusted host selects both the YAML and referenced source file. Missing,
duplicate, stale, escaping, malformed, or hash-mismatched records stop the run
before the role process starts.
