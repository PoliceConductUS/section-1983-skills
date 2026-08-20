import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
LAUNCHER = (
    REPOSITORY
    / "skills"
    / "adversarial-filing-review"
    / "scripts"
    / "launch_review.py"
)
QUALITY_CONTROL_SKILLS = {
    "adversarial-filing-review",
    "audit-authorities",
    "auditing-section-1983-discovery-responses",
    "auditing-section-1983-privilege-logs",
    "drafting-false-arrest-complaints",
    "drafting-for-judge-scholer",
    "drafting-section-1983-complaints",
    "drafting-section-1983-rule-59e",
    "filing-ci",
}
QUALITY_CONTROL_TRIGGER = re.compile(
    r"(?:\buse when\b.{0,120}\b(?:independently\s+)?(?:auditing|reviewing|"
    r"verifying|evaluating|checking|assessing|performing quality control|"
    r"performing an? assessment|conducting (?:an? )?(?:independent )?assessment)\b|"
    r"\bneeds (?:an )?independent.{0,60}\breview\b|"
    r"\bneeds to (?:independently )?(?:audit|review|verify|evaluate|check)\b|"
    r"\bneeds to determine.{0,80}\bor audit\b|\bdrafts and audits\b|"
    r"\bdrafting, revising, or auditing\b|\bchecker must run\b)",
    re.IGNORECASE,
)
QUALITY_CONTROL_RULES = (
    (
        "An independent quality-control stage is non-mutating.",
        "An independent quality-control stage may mutate an artifact under review.",
    ),
    (
        "It may read designated artifacts and write only its designated report or result.",
        "It may write changes to an artifact under review.",
    ),
    (
        "It must not edit, overwrite, correct, regenerate, or otherwise modify an artifact under review.",
        "It may edit, overwrite, correct, regenerate, or otherwise modify an artifact under review.",
    ),
    (
        "A combined instruction to audit and fix does not authorize same-stage mutation.",
        "A combined instruction to audit and fix authorizes same-stage mutation.",
    ),
    (
        "Recommendations, proposed language, corrections, and copy-ready replacements are advisory only and do not authorize implementation.",
        "Recommendations, proposed language, corrections, and copy-ready replacements authorize implementation.",
    ),
    (
        "Remediation requires a separately authorized drafting or revision stage.",
        "Remediation may occur during the independent quality-control stage.",
    ),
    (
        "Create a new version when versioning applies.",
        "Overwrite the current version when versioning applies.",
    ),
    (
        "A new read-only quality-control stage must verify the remediated artifact.",
        "The prior quality-control result transfers to the remediated artifact.",
    ),
    (
        "An internal self-check inside an explicitly authorized drafting or revision stage may guide edits within that stage, but it is not an independent quality-control result.",
        "An internal drafting self-check is an independent quality-control result.",
    ),
)


def normalized(text):
    return " ".join(text.casefold().split())


def frontmatter_description(text):
    parts = text.split("---", 2)
    if len(parts) != 3:
        return ""
    lines = parts[1].splitlines()
    description = []
    collecting = False
    for line in lines:
        if line.startswith("description:"):
            collecting = True
            value = line.partition(":")[2].strip()
            if value not in {"", ">", ">-", "|", "|-"}:
                description.append(value.strip('"\''))
            continue
        if collecting and line.startswith((" ", "\t")):
            description.append(line.strip().strip('"\''))
            continue
        if collecting:
            break
    return " ".join(description)


def discovered_quality_control_skills():
    discovered = set()
    for path in (REPOSITORY / "skills").glob("*/SKILL.md"):
        if QUALITY_CONTROL_TRIGGER.search(frontmatter_description(path.read_text())):
            discovered.add(path.parent.name)
    return discovered


def assert_contract(test, text):
    contract = normalized(text)
    for affirmative, inversion in QUALITY_CONTROL_RULES:
        with test.subTest(rule=affirmative):
            test.assertIn(normalized(affirmative), contract)
            test.assertNotIn(normalized(inversion), contract)


def launcher_module():
    specification = importlib.util.spec_from_file_location(
        "quality_control_adversarial_launcher",
        LAUNCHER,
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def sha256_bytes(content):
    return hashlib.sha256(content).hexdigest()


class NonMutatingQualityControlTest(unittest.TestCase):

    def test_current_quality_control_entrypoints_are_discovered_by_public_triggers(self):
        self.assertSetEqual(discovered_quality_control_skills(), QUALITY_CONTROL_SKILLS)

    def test_each_independently_installable_entrypoint_carries_the_complete_contract(self):
        for name in sorted(discovered_quality_control_skills()):
            with self.subTest(skill=name):
                skill = (REPOSITORY / "skills" / name / "SKILL.md").read_text()
                assert_contract(self, skill)

    def test_clean_room_review_rejects_attempted_artifact_and_extra_output_writes(self):
        launcher = launcher_module()
        with tempfile.TemporaryDirectory() as artifact_directory:
            artifact_root = Path(artifact_directory)
            artifact = artifact_root / "canonical-draft.md"
            draft = b"# Synthetic Filing\n\nCanonical allegation.\n"
            artifact.write_bytes(draft)
            before = sha256_bytes(artifact.read_bytes())
            with tempfile.TemporaryDirectory() as command_directory:
                reviewer = Path(command_directory) / "reviewer.py"
                reviewer.write_text(
                    textwrap.dedent(
                        """
                        import json
                        import pathlib
                        import sys

                        packet = json.load(sys.stdin)
                        pathlib.Path("canonical-draft.md").write_text(
                            packet["draft"]["content"] + "\nUnauthorized correction.\n"
                        )
                        pathlib.Path("extra-output.md").write_text("Unauthorized output.\n")
                        print(json.dumps({"report": "Synthetic read-only result."}))
                        """
                    )
                )
                packet = {
                    "draft": {
                        "content": draft.decode(),
                        "version": "synthetic-v1",
                        "sha256": sha256_bytes(draft),
                    },
                    "document_family": "complaint or amended complaint",
                    "sources": [
                        {
                            "id": "SRC-1",
                            "role": "record",
                            "content": "Synthetic source.\n",
                            "sha256": sha256_bytes(b"Synthetic source.\n"),
                        }
                    ],
                    "skill": {"content": "Synthetic public skill."},
                    "checklist": {"content": "Synthetic public checklist."},
                    "capabilities": [],
                }

                with self.assertRaises(launcher.ReviewLaunchError) as captured:
                    launcher.launch_review(
                        packet,
                        [sys.executable, str(reviewer)],
                        runtime_enforces_empty_capabilities=True,
                    )

            self.assertEqual(sha256_bytes(artifact.read_bytes()), before)
            self.assertEqual([path.name for path in artifact_root.iterdir()], [artifact.name])
            self.assertEqual(
                captured.exception.finding_id,
                "reviewer-output-boundary-violated",
            )


if __name__ == "__main__":
    unittest.main()
