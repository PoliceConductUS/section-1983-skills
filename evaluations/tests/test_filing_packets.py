import copy
import json
import re
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
from scripts.validate_folder_invocation import (
    validate_installed_skill_invocation,
    validate_invocation,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "evaluations" / "filing-packet-fixtures"


class FilingPacketTest(unittest.TestCase):
    def test_schema_public_contract_and_relevant_skills_publish_packet_boundary(self):
        schema = json.loads(
            (ROOT / "governance" / "filing-packet.schema.json").read_text()
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            schema["properties"]["schema_version"],
            {"const": 1, "type": "integer"},
        )
        member_path_pattern = re.compile(
            schema["$defs"]["document"]["properties"]["path"]["pattern"]
        )
        for path in (
            "motion.md",
            "exhibits/exhibit-a.pdf",
            "exhibits/line\nbreak.txt",
        ):
            self.assertIsNotNone(member_path_pattern.fullmatch(path), path)
        for path in (
            "filing-packet.json",
            ".skill-runs/foreign/manifest.json",
            "temp/intermediate.tmp",
            "filing-packets/nested/document.md",
            "/absolute.md",
            ".",
            "./inside.md",
            "../outside.md",
            "inside/../outside.md",
            "inside//document.md",
            "inside/",
            "inside\\document.md",
            "inside\x00document.md",
        ):
            self.assertIsNone(member_path_pattern.fullmatch(path), path)
        for path in (
            ROOT / "README.md",
            ROOT / "GOVERNANCE.md",
            ROOT / "FILING_PACKETS.md",
        ):
            self.assertIn("FilingPacket", path.read_text())
        for skill in (
            "section-1983-drafting",
            "drafting-section-1983-complaints",
            "drafting-section-1983-rule-59e",
            "drafting-false-arrest-complaints",
            "adversarial-filing-review",
        ):
            text = (ROOT / "skills" / skill / "SKILL.md").read_text()
            self.assertIn("## FilingPacket boundary", text, skill)
            self.assertIn("never mutates the source packet", text, skill)
        filing_ci = (ROOT / "skills" / "filing-ci" / "SKILL.md").read_text()
        self.assertNotIn("## FilingPacket boundary", filing_ci)
        self.assertIn("## Folder inputs and output", filing_ci)
        authority_audit = (
            ROOT / "skills" / "audit-authorities" / "SKILL.md"
        ).read_text()
        self.assertNotIn("## FilingPacket boundary", authority_audit)
        self.assertIn("## Folder inputs and output", authority_audit)

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
                "boolean-version": lambda value: value.update(schema_version=True),
                "two-main": lambda value: value["documents"][1].update(role="main"),
                "duplicate-id": lambda value: value["documents"][1].update(id="motion"),
                "unauthorized-role": lambda value: value["documents"][1].update(role="appendix"),
                "missing-member": lambda value: value["documents"][1].update(path="missing.txt"),
                "wrong-hash": lambda value: value["documents"][1].update(sha256="f" * 64),
                "traversal": lambda value: value["documents"][1].update(path="../outside.txt"),
                "dot": lambda value: value["documents"][1].update(path="."),
                "manifest-member": lambda value: value["documents"][1].update(path="filing-packet.json"),
                "reserved-run": lambda value: value["documents"][1].update(path=".skill-runs/member.txt"),
                "reserved-temp": lambda value: value["documents"][1].update(path="temp/member.txt"),
                "reserved-packets": lambda value: value["documents"][1].update(path="filing-packets/member.txt"),
                "double-slash": lambda value: value["documents"][1].update(path="nested//member.txt"),
                "trailing-slash": lambda value: value["documents"][1].update(path="nested/"),
                "nul": lambda value: value["documents"][1].update(path="nested\x00member.txt"),
            }
            for label, mutate in mutations.items():
                value = copy.deepcopy(original)
                mutate(value)
                (root / "filing-packet.json").write_text(json.dumps(value))
                with self.subTest(label=label), self.assertRaises(FilingPacketError):
                    load_filing_packet(root, authorized_roles={"main", "exhibit"})

    def test_loader_rejects_symlinked_manifest_and_member_aliases(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = root / "external-manifest"
            shutil.copytree(FIXTURES / "complaint", packet)
            external_manifest = root / "external-filing-packet.json"
            (packet / "filing-packet.json").replace(external_manifest)
            (packet / "filing-packet.json").symlink_to(external_manifest)
            with self.assertRaises(FilingPacketError) as captured:
                load_filing_packet(packet, authorized_roles={"main"})
            self.assertEqual(
                captured.exception.code, "aliased-filing-packet-manifest"
            )

            packet = root / "internal-member"
            shutil.copytree(FIXTURES / "complaint", packet)
            manifest_path = packet / "filing-packet.json"
            manifest = json.loads(manifest_path.read_text())
            original_path = manifest["documents"][0]["path"]
            (packet / "member-alias.md").symlink_to(original_path)
            manifest["documents"][0]["path"] = "member-alias.md"
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(FilingPacketError) as captured:
                load_filing_packet(packet, authorized_roles={"main"})
            self.assertEqual(captured.exception.code, "aliased-filing-packet-member")

    def test_loader_excludes_host_control_namespaces_and_rejects_other_unlisted_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "packet"
            shutil.copytree(FIXTURES / "complaint", root)
            run_root = root / ".skill-runs" / "packet-run"
            run_root.mkdir(parents=True)
            (run_root / "manifest.json").write_text('{"status":"success"}\n')
            temp_root = root / "temp" / "packet-run"
            temp_root.mkdir(parents=True)
            (temp_root / "intermediate.tmp").write_bytes(b"transient\n")

            packet = load_filing_packet(root, authorized_roles={"main"})
            self.assertEqual(packet.root, root.resolve())

            (root / "unlisted.txt").write_bytes(b"not a packet member\n")
            with self.assertRaises(FilingPacketError) as captured:
                load_filing_packet(root, authorized_roles={"main"})
            self.assertEqual(captured.exception.code, "unlisted-filing-packet-member")

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
            authorities = root / "authorities"
            output = root / "output"
            shutil.copytree(FIXTURES / "complaint", source)
            context.mkdir()
            authorities.mkdir()
            output.mkdir()
            (context / "facts.txt").write_text("approved context\n")
            before = {path.relative_to(source): path.read_bytes() for path in source.rglob("*") if path.is_file()}
            envelope = {
                "version": 1,
                "skill": "drafting-section-1983-complaints",
                "inputs": [
                    {"role": "record", "root": str(context)},
                    {"role": "authorities", "root": str(authorities)},
                    {"role": "filing", "root": str(source)},
                ],
                "output": {"root": str(output)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 1048576},
                "internet": "disabled",
                "isolation": {"inputs": "read-only", "output": "read-write", "undeclared": "none"},
            }
            invocation = validate_installed_skill_invocation(
                envelope,
                ROOT / "skills" / "drafting-section-1983-complaints",
            )
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
            revised = load_filing_packet(output, authorized_roles={"main"})
            self.assertEqual(revised.provenance["source_packet_sha256"], source_packet.manifest_sha256)
            self.assertEqual(len(receipt["artifacts"]), 2)
            self.assertEqual(
                {artifact["path"] for artifact in receipt["artifacts"]},
                {"amended-complaint.md", "filing-packet.json"},
            )
            self.assertFalse((output / "filing-packets").exists())
            self.assertEqual(before, {path.relative_to(source): path.read_bytes() for path in source.rglob("*") if path.is_file()})

    def test_publication_rejects_an_invocation_not_bound_to_an_installed_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filing = root / "filing"
            output = root / "output"
            filing.mkdir()
            output.mkdir()
            invocation = validate_invocation({
                "version": 1,
                "skill": "synthetic-packet-drafter",
                "inputs": [{"role": "filing", "root": str(filing)}],
                "output": {"root": str(output)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 1048576},
                "internet": "disabled",
                "isolation": {"inputs": "read-only", "output": "read-write", "undeclared": "none"},
            })
            with self.assertRaises(FilingPacketError) as captured:
                publish_filing_packet(
                    invocation,
                    packet_id="unbound-packet",
                    documents=[{
                        "id": "motion",
                        "kind": "motion",
                        "role": "main",
                        "path": "motion.md",
                        "contents": "# Motion\n",
                    }],
                    authorized_roles={"main"},
                    source_packet=None,
                    run_id="44444444-4444-4444-8444-444444444444",
                    skill_version="1",
                )
            self.assertEqual(
                captured.exception.code, "unbound-filing-packet-invocation"
            )
            self.assertEqual(list(output.iterdir()), [])

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
