import hashlib
import json
import shutil
import tempfile
import unittest
import uuid
from pathlib import Path

from scripts.adversarial_review_role import load_approved_source_records
from scripts.profile_conditioned_roles import (
    build_judicial_reviewer_definition,
    build_opposing_counsel_definition,
    load_judicial_reviewer_profile,
    load_opposing_counsel_profile,
)
from scripts.static_role_launcher import (
    AdapterAttestation,
    AdapterResult,
    InputSelection,
    RoleLaunchError,
    bind_role_launch,
    launch_static_role,
    validate_role_task,
)
from scripts.validate_folder_invocation import validate_invocation


REPOSITORY = Path(__file__).resolve().parents[2]
COUNSEL_FIXTURES = (
    REPOSITORY
    / "skills"
    / "building-defense-counsel-overlays"
    / "references"
    / "fixtures"
)
JUDICIAL_FIXTURES = (
    REPOSITORY
    / "skills"
    / "building-judicial-reasoning-profiles"
    / "references"
    / "fixtures"
)


class FakeAdapter:
    def __init__(self, value):
        self.value = value
        self.calls = []

    def attest(self):
        return AdapterAttestation(
            fixed_adapter=True,
            fresh_process=True,
            scrubbed_session=True,
            undeclared_filesystem_denied=True,
            network_enforced=True,
            capabilities_enforced=True,
        )

    def launch(self, **kwargs):
        self.calls.append(kwargs)
        return AdapterResult(
            stdout=json.dumps(self.value, sort_keys=True).encode("utf-8"),
            stderr=b"",
            exit_code=0,
            timed_out=False,
        )


def finding(category, source_id):
    return {
        "id": "finding-1",
        "category": category,
        "attacked_quote": "Bounded allegation.",
        "location": "motion.md, paragraph 1",
        "source_ids": [source_id],
        "analysis": "The selected source identifies a bounded presentation gap.",
        "limitation": "This is simulated findings work, not a disposition.",
    }


class ProfileConditionedRoleTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.counsel_profile = self.root / "counsel-profile"
        self.judicial_profile = self.root / "judicial-profile"
        self.filing = self.root / "filing"
        self.sources = self.root / "approved-sources"
        self.counsel_output = self.root / "counsel-output"
        self.judicial_output = self.root / "judicial-output"
        for path in (
            self.counsel_profile,
            self.judicial_profile,
            self.filing,
            self.sources,
            self.counsel_output,
            self.judicial_output,
        ):
            path.mkdir()
        shutil.copyfile(
            COUNSEL_FIXTURES / "complete-counsel-overlay.json",
            self.counsel_profile / "defense-counsel-overlay.json",
        )
        shutil.copyfile(
            COUNSEL_FIXTURES / "complete-research-snapshot.json",
            self.counsel_profile / "counsel-research-snapshot.json",
        )
        shutil.copyfile(
            JUDICIAL_FIXTURES / "complete-profile.json",
            self.judicial_profile / "judicial-profile.json",
        )
        judicial_profile = json.loads(
            (self.judicial_profile / "judicial-profile.json").read_text()
        )
        judicial_source_ids = sorted(
            {
                judicial_profile["judge_identity"]["source_id"],
                judicial_profile["court_scope"]["source_id"],
                *(record["source_id"] for record in judicial_profile["records"]),
            }
        )
        source_index = [
            "schema_version: 1",
            f"profile_id: {judicial_profile['profile_id']}",
            "sources:",
        ]
        for source_id in judicial_source_ids:
            source_index.append(f"  - source_id: {source_id}")
        (self.judicial_profile / "judicial-profile-sources.yaml").write_text(
            "\n".join(source_index) + "\n", encoding="utf-8"
        )
        (self.filing / "motion.md").write_text(
            "# Synthetic motion\n\nBounded allegation.\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def invocation(self, profile, output):
        return validate_invocation(
            {
                "version": 1,
                "skill": "synthetic-profile-role",
                "inputs": [
                    {"role": "profile", "root": str(profile)},
                    {"role": "filing", "root": str(self.filing)},
                    {"role": "approved-sources", "root": str(self.sources)},
                ],
                "output": {"root": str(output)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 2_000_000},
                "internet": "disabled",
                "isolation": {
                    "inputs": "read-only",
                    "output": "read-write",
                    "undeclared": "none",
                },
            }
        )

    def approved_source(self, invocation, source_id):
        content = f"Approved source for {source_id}.\n".encode()
        artifact = self.sources / f"{source_id}.txt"
        artifact.write_bytes(content)
        digest = hashlib.sha256(content).hexdigest()
        metadata = self.sources / f"{source_id}.SOURCE.yaml"
        metadata.write_text(
            "schema_version: 1\n"
            f"source_id: {source_id}\n"
            "role: record\n"
            f"path: {source_id}.txt\n"
            f"sha256: {digest}\n"
            "checked_through: 2026-08-25\n",
            encoding="utf-8",
        )
        return load_approved_source_records(
            invocation=invocation,
            documentation_paths=(metadata.name,),
            minimum_checked_through="2026-08-01",
        )

    @staticmethod
    def task(operation):
        return validate_role_task(
            {
                "operation": operation,
                "instructions": "Review the selected filing and return findings only.",
            }
        )

    def test_opposing_counsel_uses_validated_profile_and_returns_findings_only(self):
        invocation = self.invocation(self.counsel_profile, self.counsel_output)
        profile = load_opposing_counsel_profile(
            invocation=invocation,
            overlay_path="defense-counsel-overlay.json",
            snapshot_path="counsel-research-snapshot.json",
        )
        approved = self.approved_source(invocation, "SRC-MOTION-CURRENT")
        adapter = FakeAdapter(
            {
                "output_kind": "opposing-counsel-findings",
                "findings": [finding("source-backed-attack", "SRC-MOTION-CURRENT")],
            }
        )
        selections = (
            InputSelection("profile", "profile", "defense-counsel-overlay.json"),
            InputSelection("profile", "profile", "counsel-research-snapshot.json"),
            InputSelection("filing-target", "filing", "motion.md"),
            InputSelection(
                "approved-source", "approved-sources", "SRC-MOTION-CURRENT.txt"
            ),
            InputSelection(
                "source-documentation",
                "approved-sources",
                "SRC-MOTION-CURRENT.SOURCE.yaml",
            ),
        )
        binding = bind_role_launch(
            build_opposing_counsel_definition(
                adapter=adapter,
                profile=profile,
                approved_sources=approved,
            ),
            invocation=invocation,
            task=self.task("opposing-counsel-simulation"),
            selections=selections,
        )

        result = launch_static_role(binding, run_id=str(uuid.uuid4()))

        self.assertTrue(result.success)
        self.assertEqual(result.artifacts[0].path, "reports/opposing-counsel-findings.json")
        output = json.loads(result.artifacts[0].contents)
        self.assertEqual(output["role"], "opposing-counsel")
        self.assertEqual(output["findings"][0]["category"], "source-backed-attack")
        self.assertEqual(binding.definition.internet, "disabled")
        self.assertEqual(binding.definition.target_mutation, "forbidden")

    def test_judicial_reviewer_uses_validated_profile_and_bounded_categories(self):
        invocation = self.invocation(self.judicial_profile, self.judicial_output)
        profile = load_judicial_reviewer_profile(
            invocation=invocation,
            profile_path="judicial-profile.json",
            source_index_path="judicial-profile-sources.yaml",
        )
        approved = self.approved_source(invocation, "opinion-source")
        adapter = FakeAdapter(
            {
                "output_kind": "judicial-review-findings",
                "findings": [finding("authority-presentation", "opinion-source")],
            }
        )
        binding = bind_role_launch(
            build_judicial_reviewer_definition(
                adapter=adapter,
                profile=profile,
                approved_sources=approved,
            ),
            invocation=invocation,
            task=self.task("judicial-review"),
            selections=(
                InputSelection("profile", "profile", "judicial-profile.json"),
                InputSelection(
                    "profile", "profile", "judicial-profile-sources.yaml"
                ),
                InputSelection("filing-target", "filing", "motion.md"),
                InputSelection(
                    "approved-source", "approved-sources", "opinion-source.txt"
                ),
                InputSelection(
                    "source-documentation",
                    "approved-sources",
                    "opinion-source.SOURCE.yaml",
                ),
            ),
        )

        result = launch_static_role(binding, run_id=str(uuid.uuid4()))

        self.assertTrue(result.success)
        self.assertEqual(result.artifacts[0].path, "reports/judicial-review-findings.json")
        output = json.loads(result.artifacts[0].contents)
        self.assertEqual(output["role"], "judicial-reviewer")
        self.assertEqual(output["findings"][0]["category"], "authority-presentation")
        self.assertEqual(binding.definition.capabilities, ())

    def test_disposition_emitted_is_rejected_for_each_role(self):
        cases = (
            (
                "opposing-counsel-findings",
                "source-backed-attack",
                "SRC-MOTION-CURRENT",
                self.counsel_profile,
                self.counsel_output,
                load_opposing_counsel_profile,
                {
                    "overlay_path": "defense-counsel-overlay.json",
                    "snapshot_path": "counsel-research-snapshot.json",
                },
                build_opposing_counsel_definition,
                "opposing-counsel-simulation",
            ),
            (
                "judicial-review-findings",
                "comprehension",
                "opinion-source",
                self.judicial_profile,
                self.judicial_output,
                load_judicial_reviewer_profile,
                {
                    "profile_path": "judicial-profile.json",
                    "source_index_path": "judicial-profile-sources.yaml",
                },
                build_judicial_reviewer_definition,
                "judicial-review",
            ),
        )
        for (
            output_kind,
            category,
            source_id,
            profile_root,
            output_root,
            load_profile,
            load_arguments,
            build_definition,
            operation,
        ) in cases:
            with self.subTest(output_kind=output_kind):
                invocation = self.invocation(profile_root, output_root)
                profile = load_profile(invocation=invocation, **load_arguments)
                approved = self.approved_source(invocation, source_id)
                response = {
                    "output_kind": output_kind,
                    "findings": [finding(category, source_id)],
                    "disposition-emitted": "dismiss",
                }
                definition = build_definition(
                    adapter=FakeAdapter(response),
                    profile=profile,
                    approved_sources=approved,
                )
                with self.assertRaises(RoleLaunchError):
                    definition.output_validator(response)

    def test_profile_behavior_override_fails_before_role_launch(self):
        hostile = json.loads(
            (self.judicial_profile / "judicial-profile.json").read_text()
        )
        hostile["capabilities"] = ["emit-disposition", "write-target"]
        (self.judicial_profile / "judicial-profile.json").write_text(
            json.dumps(hostile), encoding="utf-8"
        )
        invocation = self.invocation(self.judicial_profile, self.judicial_output)

        with self.assertRaises(RoleLaunchError) as captured:
            load_judicial_reviewer_profile(
                invocation=invocation,
                profile_path="judicial-profile.json",
                source_index_path="judicial-profile-sources.yaml",
            )

        self.assertEqual(captured.exception.code, "invalid-judicial-profile")


class PublicRoleSkillStructureTest(unittest.TestCase):
    def test_public_role_skills_are_fixed_folder_scoped_findings_roles(self):
        expected = {
            "SKILL.md",
            "agents/openai.yaml",
            "references/finding-schema.json",
            "references/folder-contract.json",
            "references/static-role-instructions.md",
        }
        for name, operation in (
            ("opposing-counsel", "opposing-counsel-simulation"),
            ("judicial-reviewer", "judicial-review"),
        ):
            with self.subTest(skill=name):
                root = REPOSITORY / "skills" / name
                actual = {
                    path.relative_to(root).as_posix()
                    for path in root.rglob("*")
                    if path.is_file() and "__pycache__" not in path.parts
                }
                self.assertEqual(actual, expected)
                contract = json.loads(
                    (root / "references" / "folder-contract.json").read_text()
                )
                self.assertEqual(
                    contract,
                    {
                        "version": 1,
                        "skill": name,
                        "input_roles": ["profile", "filing", "approved-sources"],
                        "target": {"policy": "required", "roles": ["filing"]},
                        "internet": "disabled",
                        "output": {"mode": "append-immutable"},
                    },
                )
                text = "\n".join(
                    path.read_text()
                    for path in (
                        root / "SKILL.md",
                        root / "references" / "static-role-instructions.md",
                    )
                ).casefold()
                self.assertIn(operation, text)
                self.assertIn("findings only", text)
                self.assertIn("<output-folder>/temp", text)
                self.assertNotIn("casegraph", text)
                self.assertNotIn("package manifest", text)


if __name__ == "__main__":
    unittest.main()
