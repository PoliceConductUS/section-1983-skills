# Design: direct profile files and YAML source records

## Acquisition output

For each acquired source, write source bytes and a domain `SOURCE.yaml` record
directly beneath the explicit output folder. The YAML record identifies the
source, folder-relative artifact path, SHA-256, public retrieval identity,
retrieval and checked dates, source class, validation state, limitations, and
gaps. Internet provenance also remains in the shared output-run receipt.

Acquisition does not compile a profile. A later invocation may consume the
acquisition folder only after the caller declares it as `approved-sources`.

## Compilation output

Write these ordinary durable files through `OutputRun`:

- `judicial-profile.json`, validated by the existing profile schema and
  install-local validator;
- `judicial-profile-sources.yaml`, which maps each profile source ID to its
  declared input role, folder-relative `SOURCE.yaml`, referenced artifact,
  expected hash, applicable dates, classification, validation state, and gaps;
- `validation-receipt.json`.

No file lists every output member as folder membership. The shared terminal run
receipt remains trusted-host metadata, not a profile package envelope.

## Runtime boundary

All reads use declared input roots. All writes use the explicit output root.
Every transient byte stays under `<output-folder>/temp/`. Compilation disables
the internet. Acquisition requires explicit internet authorization. Input
folders remain unchanged and are not reread through a package snapshot.
