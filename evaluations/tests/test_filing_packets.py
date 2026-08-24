import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.filing_packet import (
    FilingPacketError,
    evaluate_filing_readiness,
    load_filing_packet,
    publish_filing_packet,
    resolve_filing_packet_target,
)
from scripts.validate_folder_invocation import validate_invocation


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "evaluations" / "fixtures" / "filing-packets"


class FilingPacketTest(unittest.TestCase):
    def test_four_packet_families_validate_with_stable_order_and_kind_role_split(self):
        cases = (
            ("complaint", {"main"}, ["complaint"]),
            ("motion-with-amended-complaint", {"main", "exhibit"}, ["motion", "amended-complaint"]),
            ("response", {"main"}, ["response"]),
            ("multi-exhibit", {"main", "exhibit"}, ["motion", "exhibit-a", "exhibit-b"]),
        )
        for name, roles, expected_order in cases:
            with self.subTest(name=name):
                packet = load_filing_packet(FIXTURES / name, authorized_roles=roles)
                self.assertEqual([document["id"] for document in packet.documents], expected_order)
                self.assertEqual(sum(document["role"] == "main" for document in packet.documents), 1)
        amended = load_filing_packet(
            FIXTURES / "motion-with-amended-complaint",
            authorized_roles={"main", "exhibit"},
        ).documents[1]
        self.assertEqual((amended["kind"], amended["role"]), ("amended-complaint", "exhibit"))

    def test_manifest_rejects_main_order_role_member_hash_and_path_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "packet"
            shutil.copytree(FIXTURES / "multi-exhibit", root)
            original = json.loads((root / "filing-packet.json").read_text())
            mutations = {
                "two-main": lambda value: value["documents"][1].update(role="main"),
                "duplicate-id": lambda value: value["documents"][1].update(id="motion"),
                "unauthorized-role": lambda value: value["documents"][1].update(role="appendix"),
                "missing-member": lambda value: value["documents"][1].update(path="missing.txt"),
                "wrong-hash": lambda value: value["documents"][1].update(sha256="f" * 64),
                "traversal": lambda value: value["documents"][1].update(path="../outside.txt"),
            }
            for label, mutate in mutations.items():
                value = copy.deepcopy(original)
                mutate(value)
                (root / "filing-packet.json").write_text(json.dumps(value))
                with self.subTest(label=label), self.assertRaises(FilingPacketError):
                    load_filing_packet(root, authorized_roles={"main", "exhibit"})

    def test_target_is_whole_packet_or_exact_manifest_member(self):
        packet = load_filing_packet(FIXTURES / "multi-exhibit", authorized_roles={"main", "exhibit"})
        self.assertEqual(resolve_filing_packet_target(packet, "filing-packet.json")["scope"], "packet")
        target = resolve_filing_packet_target(packet, "exhibit-b.txt")
        self.assertEqual((target["scope"], target["document_id"]), ("document", "exhibit-b"))
        for path in ("unlisted.txt", "../motion.md", ""):
            with self.subTest(path=path), self.assertRaises(FilingPacketError):
                resolve_filing_packet_target(packet, path)

    def test_revision_publishes_complete_new_packet_and_preserves_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            context = root / "context"
            output = root / "output"
            shutil.copytree(FIXTURES / "complaint", source)
            context.mkdir()
            output.mkdir()
            (context / "facts.txt").write_text("approved context\n")
            before = {path.relative_to(source): path.read_bytes() for path in source.rglob("*") if path.is_file()}
            invocation = validate_invocation({
                "version": 1,
                "skill": "synthetic-packet-drafter",
                "inputs": [{"role": "filing", "root": str(source)}, {"role": "record", "root": str(context)}],
                "output": {"root": str(output)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 1048576},
                "internet": "disabled",
                "isolation": {"inputs": "read-only", "output": "read-write", "undeclared": "none"},
            })
            source_packet = load_filing_packet(source, authorized_roles={"main"})
            receipt = publish_filing_packet(
                invocation,
                packet_id="revised-complaint",
                documents=[{
                    "id": "complaint",
                    "kind": "amended-complaint",
                    "role": "main",
                    "path": "amended-complaint.md",
                    "contents": "# Amended Complaint\n",
                }],
                authorized_roles={"main"},
                source_packet=source_packet,
                run_id="33333333-3333-4333-8333-333333333333",
                skill_version="1",
            )
            packet_root = output / "filing-packets" / "revised-complaint"
            revised = load_filing_packet(packet_root, authorized_roles={"main"})
            self.assertEqual(revised.provenance["source_packet_sha256"], source_packet.manifest_sha256)
            self.assertEqual(len(receipt["artifacts"]), 2)
            self.assertEqual(before, {path.relative_to(source): path.read_bytes() for path in source.rglob("*") if path.is_file()})

    def test_filing_readiness_requires_every_gate_to_cover_every_member(self):
        packet = load_filing_packet(FIXTURES / "multi-exhibit", authorized_roles={"main", "exhibit"})
        ready = evaluate_filing_readiness(packet, [
            {"gate": "authority-audit", "result": "pass", "scope": "packet"},
            {"gate": "filing-ci", "result": "pass", "document_ids": ["motion", "exhibit-a", "exhibit-b"]},
        ])
        self.assertTrue(ready["ready"])
        incomplete = evaluate_filing_readiness(packet, [
            {"gate": "filing-ci", "result": "pass", "document_ids": ["motion", "exhibit-a"]},
        ])
        self.assertFalse(incomplete["ready"])
        self.assertEqual(incomplete["missing_coverage"], {"filing-ci": ["exhibit-b"]})


if __name__ == "__main__":
    unittest.main()
