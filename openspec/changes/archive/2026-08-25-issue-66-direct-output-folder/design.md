# Design: direct FilingPacket output

`publish_filing_packet()` keeps `fresh-regenerable` `OutputRun` publication but
removes the `filing-packets/<packet-id>/` prefix. The output root therefore
contains the packet manifest and its relative document paths directly, plus the
writer-owned `.skill-runs/` and `temp/` control namespaces.

The packet path grammar reserves `filing-packet.json`, `.skill-runs/`, and
`temp/`. Complete packet membership ignores the two trusted-host namespaces and
rejects every other unlisted file.
