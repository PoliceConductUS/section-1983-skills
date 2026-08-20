import json
import re
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
VALIDATOR = REPOSITORY / "scripts" / "validate_governance.py"
VALID_DATE = "2026-08-20"


def read_public_file(path):
    if not path.is_file():
        raise AssertionError(f"required public file is missing: {path.relative_to(REPOSITORY)}")
    return path.read_text()


def assert_semantics(test, text, concepts):
    for label, patterns in concepts:
        with test.subTest(concept=label):
            alternatives = "|".join(f"(?:{pattern})" for pattern in patterns)
            test.assertRegex(text, rf"(?is){alternatives}")


def referenced_scripts(command):
    return set(re.findall(r"\bnpm\s+run\s+([A-Za-z0-9:_-]+)", command))


def reachable_scripts(scripts, start):
    pending = [start]
    reached = set()
    while pending:
        name = pending.pop()
        if name in reached or name not in scripts:
            continue
        reached.add(name)
        pending.extend(referenced_scripts(scripts[name]) - reached)
    return reached


def invokes_governance_validator(command):
    for part in re.split(r"(?:\r?\n|&&|\|\||;)", command):
        try:
            tokens = shlex.split(part)
        except ValueError:
            continue
        if len(tokens) < 2 or tokens[0] != "python3":
            continue
        if Path(tokens[1]).as_posix().removeprefix("./") == "scripts/validate_governance.py":
            return True
    return False


def valid_policy():
    return """# Governance

The user reserves litigation strategy, positions, concessions, requested relief,
and filing. When supported choices have different consequences, present each
choice and consequence, identify the user decision required, and select none.

Current jurisdiction-specific propositions belong only in a verified reference
that identifies the jurisdiction, authoritative source provenance, and checked
date. Public skills route to that reference without restating the proposition.

Verification, factual and authority source, permission, filing-readiness,
judgment-routing, rules-provenance, and tool-ownership are protected gates.
Any change that weakens a protected gate requires explicit human review.

This repository retains public skill instructions and repository-specific
validation or evaluation support. General-purpose executable tooling belongs in
its owning repository; this repository keeps only a thin skill wrapper.
"""


def valid_pull_request_template():
    return """## Protected legal gates

- Affected protected gate:
- Rationale:
- [ ] I request explicit human review of this protected-gate change.
"""


def valid_registry():
    return {
        "version": 1,
        "sources": [
            {
                "id": "federal-rules",
                "url": "https://www.uscourts.gov/rules-policies/current-rules-practice-procedure",
                "checked_on": VALID_DATE,
            }
        ],
        "skills": [
            {
                "name": "example-skill",
                "rules_mode": "bundled-rules-dependent",
                "reviewed_on": VALID_DATE,
                "rationale": "Contains current federal procedural rule content.",
                "source_ids": ["federal-rules"],
                "jurisdiction_reference": "skills/example-skill/references/jurisdiction.md",
            }
        ],
    }


def runtime_sourced_registry():
    registry = valid_registry()
    skill = registry["skills"][0]
    skill.update(
        {
            "rules_mode": "runtime-sourced",
            "rationale": "Uses an approved source supplied at runtime.",
            "output_provenance": {
                "source_identity": "actual approved source identity used",
                "checked_date": "actual checked date used",
            },
        }
    )
    skill.pop("source_ids")
    skill.pop("jurisdiction_reference")
    return registry


def write_temporary_repository(root, registry=None, policy=None, template=None):
    (root / "skills" / "example-skill" / "references").mkdir(parents=True)
    (root / "governance").mkdir()
    (root / ".github").mkdir()
    (root / "skills" / "example-skill" / "SKILL.md").write_text("# Example skill\n")
    (root / "skills" / "example-skill" / "references" / "jurisdiction.md").write_text(
        "Jurisdiction: Example District\n"
        "Authoritative source: https://www.uscourts.gov\n"
        f"Checked date: {VALID_DATE}\n"
    )
    (root / "GOVERNANCE.md").write_text(policy or valid_policy())
    (root / ".github" / "pull_request_template.md").write_text(
        template or valid_pull_request_template()
    )
    (root / "governance" / "rules-provenance.json").write_text(
        json.dumps(registry or valid_registry())
    )


def run_validator(repository_root):
    return subprocess.run(
        ["python3", "scripts/validate_governance.py", str(repository_root)],
        text=True,
        capture_output=True,
        check=False,
        cwd=REPOSITORY,
    )


class RepositoryGovernanceTest(unittest.TestCase):

    def assert_temporary_repository_error(self, mutate_registry, error_id):
        registry = valid_registry()
        mutate_registry(registry)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(error_id, result.stdout + result.stderr)

    def test_public_governance_reserves_user_judgment_and_protects_boundaries(self):
        policy = read_public_file(REPOSITORY / "GOVERNANCE.md")

        assert_semantics(
            self,
            policy,
            (
                ("strategy", (r"litigation.{0,40}strategy", r"strategy")),
                ("positions", (r"legal.{0,40}positions?", r"positions?")),
                ("concessions", (r"concessions?",)),
                ("requested relief", (r"requested.{0,40}relief", r"relief")),
                ("filing", (r"filing",)),
                (
                    "supported choices and consequences without selection",
                    (
                        r"supported.{0,80}choices?.{0,120}consequences?.{0,160}(?:select.{0,30}none|no.{0,30}selection)",
                        r"choices?.{0,120}consequences?.{0,160}(?:select.{0,30}none|no.{0,30}selection)",
                    ),
                ),
                (
                    "jurisdiction reference confinement",
                    (
                        r"jurisdiction.{0,80}proposition.{0,120}(?:only|must).{0,120}reference",
                    ),
                ),
                (
                    "sourced dated jurisdiction reference",
                    (
                        r"jurisdiction.{0,180}(?:authoritative|source).{0,180}(?:checked|date)",
                    ),
                ),
                ("verification gate", (r"verification",)),
                ("source gate", (r"(?:factual|authority).{0,30}source|source",)),
                ("permission gate", (r"permission",)),
                ("filing-readiness gate", (r"filing[- ]readiness",)),
                ("judgment-routing gate", (r"judgment[- ]routing",)),
                ("rules-provenance gate", (r"rules[- ]provenance",)),
                ("tool-ownership gate", (r"tool[- ]ownership",)),
                (
                    "thin wrapper ownership boundary",
                    (
                        r"thin.{0,30}(?:skill.{0,30})?wrapper.{0,180}owning.{0,60}repository",
                    ),
                ),
            ),
        )

    def test_pull_request_template_requires_protected_gate_review(self):
        template = read_public_file(REPOSITORY / ".github" / "pull_request_template.md")

        assert_semantics(
            self,
            template,
            (
                ("affected protected gate", (r"affected.{0,50}protected.{0,50}gate",)),
                ("rationale", (r"rationale",)),
                ("explicit human review", (r"explicit.{0,50}(?:human.{0,30})?review",)),
            ),
        )

    def test_validate_reaches_governance_validator(self):
        scripts = json.loads((REPOSITORY / "package.json").read_text())["scripts"]
        reached = reachable_scripts(scripts, "validate")

        self.assertTrue(
            any(invokes_governance_validator(scripts[name]) for name in reached),
            "validate must reach python3 scripts/validate_governance.py",
        )

    def test_live_repository_governance_validator_succeeds(self):
        result = run_validator(REPOSITORY)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_live_registry_classifies_exactly_the_public_skill_names(self):
        registry_path = REPOSITORY / "governance" / "rules-provenance.json"
        registry = json.loads(read_public_file(registry_path))
        discovered_names = [
            path.parent.name for path in (REPOSITORY / "skills").glob("*/SKILL.md")
        ]
        classified_names = [entry["name"] for entry in registry["skills"]]

        self.assertCountEqual(classified_names, discovered_names)

    def test_complete_temporary_repository_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root)
            result = run_validator(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_sourced_entry_with_output_provenance_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=runtime_sourced_registry())
            result = run_validator(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_sourced_entry_requires_actual_source_identity(self):
        registry = runtime_sourced_registry()
        registry["skills"][0]["output_provenance"].pop("source_identity")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("runtime-source-identity-required", result.stdout + result.stderr)

    def test_runtime_sourced_entry_requires_actual_checked_date(self):
        registry = runtime_sourced_registry()
        registry["skills"][0]["output_provenance"].pop("checked_date")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("runtime-source-date-required", result.stdout + result.stderr)

    def test_skill_entry_mismatch_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"].append(
                {
                    "name": "orphan-skill",
                    "rules_mode": "rules-independent",
                    "reviewed_on": VALID_DATE,
                    "rationale": "No current procedural rules are supplied.",
                }
            ),
            "skill-entry-mismatch",
        )

    def test_duplicate_skill_classification_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"].append(dict(registry["skills"][0])),
            "skill-entry-mismatch",
        )

    def test_invalid_rules_mode_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].update({"rules_mode": "invented-mode"}),
            "invalid-rules-mode",
        )

    def test_invalid_date_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].update({"reviewed_on": "20-08-2026"}),
            "invalid-date",
        )

    def test_bundled_rules_source_is_required(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].update({"source_ids": []}),
            "bundled-source-required",
        )

    def test_unknown_source_id_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].update({"source_ids": ["unknown-source"]}),
            "unknown-source-id",
        )

    def test_insecure_source_url_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["sources"][0].update({"url": "http://www.uscourts.gov"}),
            "insecure-source-url",
        )

    def test_jurisdiction_reference_is_required(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].pop("jurisdiction_reference"),
            "jurisdiction-reference-required",
        )

    def test_protected_review_language_is_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, template="# Pull request\n")
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("protected-review-language-missing", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
