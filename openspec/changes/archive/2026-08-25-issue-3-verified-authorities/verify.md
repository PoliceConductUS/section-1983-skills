# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_verified_authority_audit evaluations.tests.test_skill_folder_contracts evaluations.tests.test_filing_packets evaluations.tests.test_skill_folder_guidance evaluations.tests.test_skill_output_writer
```

Result: 94 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 573 evaluation tests passed.
- 24 installable skills were discovered.
- 31 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- Runtime inputs are only `filing-source` and `verified-authority`; ordinary
  `audit` disables internet.
- Corpus, authority, and source YAML select only relative ordinary files inside
  `verified-authority` and agree on their hashes.
- The skill uses no case-data package, package loader, FilingPacket, graph,
  CaseGraph, repository, Git, global datastore, or ambient corpus path.
- Eyecite extracts and resolves candidates but never supplies verified status.
- Persistent markup resolves to selected authority, source, and document paths;
  those paths remain logical and relative.
- Exact quotations must occur in the asserted page-delimited pinpoint segment.
  Unusable text requires visual review and cannot pass.
- Reports and receipts are deterministic, inputs remain byte-identical, and all
  staging stays beneath the explicit output folder's `temp/` directory.
