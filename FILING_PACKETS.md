# Folder-backed FilingPackets

A FilingPacket is an ordinary folder containing `filing-packet.json` and every
file listed by that manifest. The manifest fixes stable document identities,
deterministic order, document kinds, packet roles, relative paths, byte sizes,
hashes, and revision provenance. Document kind and packet role are independent:
an amended complaint can be `main` in one packet and an `exhibit` in another.

Exactly one member has role `main`. Other roles are accepted only when the
invoking operation expressly authorizes them. The trusted host validates every
listed file under the declared packet root before drafting or review. Missing,
unlisted, escaping, directory, size-mismatched, or hash-mismatched targets fail
closed.

The packet manifest is the whole-packet review target. A member target is the
exact relative path of one manifest-listed document. A member result never
silently counts as whole-packet coverage.

Drafting and revision read source packets and context folders as recursively
read-only inputs. The caller supplies the full absolute path of a fresh output
folder, or the skill asks for it before work begins. The trusted host publishes
every document and `filing-packet.json` directly in that folder through one
fresh-regenerable output run. It does not add a `filing-packets/<packet-id>/`
namespace. Revision provenance records the source manifest SHA-256 and every
output records the logical input-manifest SHA-256. Source packet bytes never
change. `.skill-runs/` contains trusted-host receipts, and `temp/` is the
invocation's only transient workspace; neither is a packet member.

Mechanical filing readiness requires every member to validate and every
configured packet-level gate to pass while covering the whole packet or every
member ID. It does not decide legal quality, strategy, filing authorization, or
whether the user should file.

The machine contract is
[`governance/filing-packet.schema.json`](governance/filing-packet.schema.json).
The trusted-host reference implementation is
[`scripts/filing_packet.py`](scripts/filing_packet.py).
