# Folder-backed FilingPacket contract

A FilingPacket is an ordinary declared folder containing \`filing-packet.json\`
and every manifest-listed member. The ordered manifest fixes stable document
IDs, independent document kinds and packet roles, canonical relative paths, byte
sizes, hashes, and revision provenance. Exactly one member is \`main\`; every
other role requires express operation authorization.

Validate every member before work. The manifest targets the whole packet; a
document target is one exact listed member and never counts as whole-packet
coverage. Source packets remain recursively read-only. Drafting or revision
returns proposed members for trusted-host publication as a complete new packet
beneath the caller's explicit output folder.
