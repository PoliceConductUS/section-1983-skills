# Brainstorm: one immutable report contract for every QC stage

## Problem

Quality-control skills already promise non-mutation and explicit output, but a
promise alone cannot bind report content, filter prior reports from the reviewed
fingerprint, or prove that an output failure prevents completion.

## Approaches considered

### Keep report metadata as unvalidated prose

Rejected. The repository could only search for stock sentences and could not
prove that a concrete report identifies the reviewed bytes or its receipt.

### Write a Markdown report plus a separate metadata sidecar

Rejected. The quality-control contract requires exactly one report. A sidecar
would introduce a second artifact whose failure and identity need another
coordination rule.

### Make every skill call the output writer

Rejected. Installed skill processors must remain input-confined and must not
receive an output root or own persistence.

### Add a trusted-host Markdown envelope and publisher

Selected. A QC processor supplies bounded report content and finding lists. The
trusted host derives role manifests and the primary-target fingerprint, emits a
canonical JSON metadata block at the start of one Markdown report, then writes
and completes exactly one append-immutable `OutputRun`.

## Boundaries

- The report body and substantive finding schemas remain skill-owned.
- The host does not judge legal quality or select remediation.
- The existing generic folder validator and output writer remain the only
  filesystem boundary and persistence primitive.
- Only generated paths under `quality-control-reports/` are treated as QC
  reports for default fingerprint exclusion.
- Historical archived OpenSpec changes and prior reports are not rewritten.
