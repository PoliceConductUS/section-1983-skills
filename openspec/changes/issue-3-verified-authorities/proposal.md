# Proposal: Folder-native verified authority audits

## Why

The authority-audit skill still describes FilingPacket input, a canonical
verified-case root, and internet-authorized ordinary audits. Issue #3 requires a
deterministic citation gate over only caller-declared filing and authority
folders, with ordinary source-documentation YAML and no package or graph model.

## What changes

- Replace `filing` and `authorities` with exact `filing-source` and
  `verified-authority` roles.
- Require one explicit filing target and strict selected corpus, authority, and
  source YAML that bind ordinary authority document bytes.
- Integrate eyecite only for citation extraction and antecedent resolution;
  never treat extraction as legal verification.
- Add deterministic identity, hash, status, proposition, quotation, pinpoint,
  and missing-authority findings.
- Publish JSON and Markdown findings plus a YAML receipt beneath the explicit
  output folder, with all transient work under its `temp/` directory.
- Make ordinary audit internet-disabled and keep separately authorized freshness
  research non-certifying.

## Capability

- `verified-authority-audit`

## Non-goals

- No case-data package, package manifest or loader, FilingPacket, graph,
  CaseGraph, repository, Git, global datastore, ambient source discovery,
  substantive good-law certification by eyecite, or automatic filing edits.
