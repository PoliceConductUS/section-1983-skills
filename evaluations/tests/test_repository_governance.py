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
CONTRIBUTION_RULES = (
    (
        "stacked story",
        "Use one story per stacked branch.",
        "Do not use one story per stacked branch.",
    ),
    (
        "RED before GREEN",
        "Write the RED failing test before GREEN implementation.",
        "Write GREEN implementation before the RED failing test.",
    ),
    (
        "green refactor",
        "Refactor only while the tests remain green.",
        "Refactor while the tests are failing.",
    ),
    (
        "OpenSpec lifecycle",
        "Complete OpenSpec design, tasks, verification, retrospective, and archive artifacts.",
        "Do not complete OpenSpec design, tasks, verification, retrospective, and archive artifacts.",
    ),
    (
        "human legal judgment",
        "Automation must not silently select plaintiff decisions, litigation strategy, or legal conclusions.",
        "Automation may silently select plaintiff decisions, litigation strategy, or legal conclusions.",
    ),
    (
        "measurement feedback",
        "Measurement is feedback, never a verdict.",
        "Measurement is a verdict.",
    ),
    (
        "measurement limits",
        "Score deltas and judgment-based evaluations prompt review and do not decide legal quality, filing readiness, or human judgment.",
        "Score deltas and judgment-based evaluations decide legal quality, filing readiness, and human judgment.",
    ),
    (
        "self-documenting code",
        "Prefer self-documenting code.",
        "Do not prefer self-documenting code.",
    ),
    (
        "refactor before comment",
        "Refactor before adding a comment.",
        "Do not refactor before adding a comment.",
    ),
    (
        "bounded comment",
        "A necessary comment is short and clear and references an ADR or recorded decision when practical.",
        "A necessary comment may be long and unclear and need not reference an ADR or recorded decision.",
    ),
    (
        "full validation",
        "Run `npm run validate` before release.",
        "Do not run `npm run validate` before release.",
    ),
    (
        "main is not publication",
        "A push to `main` is not publication.",
        "A push to `main` is publication.",
    ),
    (
        "immutable release",
        "Release only with immutable semantic-version tags.",
        "Do not use immutable semantic-version tags.",
    ),
    (
        "deterministic enforcement",
        "The validator checks deterministic boundaries, not subjective prose, comment, test, or legal quality.",
        "The validator checks subjective prose, comment, test, and legal quality.",
    ),
)
OWNER_LINKS = {
    "GOVERNANCE.md": "GOVERNANCE.md",
    "PUBLISHING.md": "PUBLISHING.md",
}
DUPLICATED_OWNER_MARKERS = (
    "## protected legal gates",
    "## releasing a validated version",
    "gh workflow run release.yml",
    "verification, factual and authority source, permission, filing-readiness",
)
QUALITY_CONTROL_RULES = (
    (
        "non-mutating stage",
        "An independent quality-control stage is non-mutating.",
        "An independent quality-control stage may mutate an artifact under review.",
    ),
    (
        "report-only output",
        "It may read designated artifacts and write only its designated report or result.",
        "It may write changes to an artifact under review.",
    ),
    (
        "reviewed artifact prohibition",
        "It must not edit, overwrite, correct, regenerate, or otherwise modify an artifact under review.",
        "It may edit, overwrite, correct, regenerate, or otherwise modify an artifact under review.",
    ),
    (
        "combined instruction boundary",
        "A combined instruction to audit and fix does not authorize same-stage mutation.",
        "A combined instruction to audit and fix authorizes same-stage mutation.",
    ),
    (
        "advisory output",
        "Recommendations, proposed language, corrections, and copy-ready replacements are advisory only and do not authorize implementation.",
        "Recommendations, proposed language, corrections, and copy-ready replacements authorize implementation.",
    ),
    (
        "separate remediation",
        "Remediation requires a separately authorized drafting or revision stage.",
        "Remediation may occur during the independent quality-control stage.",
    ),
    (
        "versioning",
        "Create a new version when versioning applies.",
        "Overwrite the current version when versioning applies.",
    ),
    (
        "fresh verification",
        "A new read-only quality-control stage must verify the remediated artifact.",
        "The prior quality-control result transfers to the remediated artifact.",
    ),
    (
        "drafting self-check distinction",
        "An internal self-check inside an explicitly authorized drafting or revision stage may guide edits within that stage, but it is not an independent quality-control result.",
        "An internal drafting self-check is an independent quality-control result.",
    ),
)


def read_public_file(path):
    if not path.is_file():
        raise AssertionError(f"required public file is missing: {path.relative_to(REPOSITORY)}")
    return path.read_text()


def assert_semantics(test, text, concepts):
    for label, patterns in concepts:
        with test.subTest(concept=label):
            alternatives = "|".join(f"(?:{pattern})" for pattern in patterns)
            test.assertRegex(text, rf"(?is){alternatives}")


def normalized(text):
    return " ".join(text.lower().split())


def replace_phrase(text, phrase, replacement):
    pattern = re.compile(r"\s+".join(re.escape(word) for word in phrase.split()))
    mutated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise AssertionError(f"fixture phrase not found exactly once: {phrase}")
    return mutated


def markdown_links(text):
    prose = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1\s*", "", text)
    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", prose)


def assert_contribution_contract(test, text, root):
    contract = normalized(text)
    for label, affirmative, inversion in CONTRIBUTION_RULES:
        with test.subTest(rule=label):
            test.assertIn(normalized(affirmative), contract)
            test.assertNotIn(normalized(inversion), contract)
    links = markdown_links(text)
    for label, destination in OWNER_LINKS.items():
        with test.subTest(owner=label):
            destinations = [target for link_label, target in links if link_label == label]
            test.assertTrue(destinations)
            for target in destinations:
                test.assertEqual(target, destination)
                resolved = (root / target).resolve()
                resolved.relative_to(root.resolve())
                test.assertTrue(resolved.is_file())
    for marker in DUPLICATED_OWNER_MARKERS:
        with test.subTest(duplicated_owner=marker):
            test.assertNotIn(marker, contract)


def assert_quality_control_contract(test, text):
    contract = normalized(text)
    for label, affirmative, inversion in QUALITY_CONTROL_RULES:
        with test.subTest(quality_control_rule=label):
            test.assertIn(normalized(affirmative), contract)
            test.assertNotIn(normalized(inversion), contract)


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

An independent quality-control stage is non-mutating. It may read designated
artifacts and write only its designated report or result. It must not edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review. A
combined instruction to audit and fix does not authorize same-stage mutation.
Recommendations, proposed language, corrections, and copy-ready replacements
are advisory only and do not authorize implementation. Remediation requires a
separately authorized drafting or revision stage. Create a new version when
versioning applies. A new read-only quality-control stage must verify the
remediated artifact. An internal self-check inside an explicitly authorized
drafting or revision stage may guide edits within that stage, but it is not an
independent quality-control result.
"""


def valid_pull_request_template():
    return """## Protected legal gates

- Affected protected gate:
- Rationale:
- [ ] I request explicit human review of this protected-gate change.
"""


def valid_contributing_contract():
    return """# Contributing

Use one story per stacked branch. Write the RED failing test before GREEN
implementation. Refactor only while the tests remain green. Complete OpenSpec
design, tasks, verification, retrospective, and archive artifacts.

Automation must not silently select plaintiff decisions, litigation strategy,
or legal conclusions. Follow [GOVERNANCE.md](GOVERNANCE.md).

Measurement is feedback, never a verdict. Score deltas and judgment-based
evaluations prompt review and do not decide legal quality, filing readiness, or
human judgment.

Prefer self-documenting code. Refactor before adding a comment. A necessary
comment is short and clear and references an ADR or recorded decision when
practical.

Run `npm run validate` before release. A push to `main` is not publication.
Release only with immutable semantic-version tags. Follow
[PUBLISHING.md](PUBLISHING.md).

The validator checks deterministic boundaries, not subjective prose, comment,
test, or legal quality.
"""


def valid_quality_control_skill(
    description="Use when independently auditing a synthetic artifact.",
):
    return f"""---
name: example-skill
description: {description}
---

# Example skill

An independent quality-control stage is non-mutating. It may read designated
artifacts and write only its designated report or result. It must not edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review. A
combined instruction to audit and fix does not authorize same-stage mutation.
Recommendations, proposed language, corrections, and copy-ready replacements
are advisory only and do not authorize implementation. Remediation requires a
separately authorized drafting or revision stage. Create a new version when
versioning applies. A new read-only quality-control stage must verify the
remediated artifact. An internal self-check inside an explicitly authorized
drafting or revision stage may guide edits within that stage, but it is not an
independent quality-control result.
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


def write_temporary_repository(
    root,
    registry=None,
    policy=None,
    template=None,
    contributing=None,
    skill_text=None,
):
    (root / "skills" / "example-skill" / "references").mkdir(parents=True)
    (root / "governance").mkdir()
    (root / ".github").mkdir()
    (root / "skills" / "example-skill" / "SKILL.md").write_text(
        skill_text or "# Example skill\n"
    )
    (root / "skills" / "example-skill" / "references" / "jurisdiction.md").write_text(
        "Jurisdiction: Example District\n"
        "Authoritative source: https://www.uscourts.gov\n"
        f"Checked date: {VALID_DATE}\n"
    )
    (root / "GOVERNANCE.md").write_text(policy or valid_policy())
    (root / "PUBLISHING.md").write_text(
        "# Publishing\n\nUse immutable semantic-version tags after validation.\n"
    )
    (root / "CONTRIBUTING.md").write_text(
        contributing if contributing is not None else valid_contributing_contract()
    )
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
        assert_quality_control_contract(self, policy)

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

    def test_public_contribution_contract_preserves_repository_norms(self):
        contract = read_public_file(REPOSITORY / "CONTRIBUTING.md")
        assert_contribution_contract(self, contract, REPOSITORY)

    def test_governance_validator_rejects_missing_or_inverted_contract(self):
        valid = valid_contributing_contract()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, contributing=valid)
            assert_contribution_contract(self, valid, root)

        mutations = [("missing contract", "# Contributing\n")]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in CONTRIBUTION_RULES
        )
        for label, destination in OWNER_LINKS.items():
            source = f"[{label}]({destination})"
            mutations.extend(
                (
                    (f"missing {label}", valid.replace(source, label)),
                    (
                        f"external {label}",
                        valid.replace(source, f"[{label}](https://example.com/{label})"),
                    ),
                    (
                        f"traversal {label}",
                        valid.replace(source, f"[{label}](../{label})"),
                    ),
                )
            )
        mutations.extend(
            (f"duplicated owner {marker}", f"{valid}\n{marker}\n")
            for marker in DUPLICATED_OWNER_MARKERS
        )
        for label, contract in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, contributing=contract)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "contribution-contract-language-missing",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_rejects_missing_or_inverted_quality_control_contract(self):
        valid = valid_quality_control_skill()
        mutations = [("missing contract", """---
name: example-skill
description: Use when independently auditing a synthetic artifact.
---

# Example skill
""")]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in QUALITY_CONTROL_RULES
        )
        for label, skill_text in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill_text)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-contract-language-missing: example-skill",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_classifies_quality_control_by_behavior(self):
        descriptions = (
            "Use when auditing a synthetic artifact.",
            "Use when independently auditing a synthetic artifact.",
            "Use when reviewing a synthetic artifact.",
            "Use when independently reviewing a synthetic artifact.",
            "Use when verifying a synthetic artifact.",
            "Use when evaluating a synthetic artifact.",
            "Use when checking a synthetic artifact.",
            "Use when performing quality control on a synthetic artifact.",
            "Use when assessing quality of a synthetic artifact.",
            "Use when assessing a synthetic artifact.",
            "Use when performing an assessment of a synthetic artifact.",
            "Use when conducting an independent assessment of a synthetic artifact.",
            "Use when a project-configured checker must run on a synthetic artifact.",
        )
        for description in descriptions:
            with self.subTest(description=description):
                skill = valid_quality_control_skill(description).partition(
                    "\nAn independent quality-control stage"
                )[0]
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-contract-language-missing: example-skill",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_rejects_missing_or_inverted_quality_control_policy(self):
        valid = valid_policy()
        mutations = [
            (
                "missing contract",
                valid.partition("\nAn independent quality-control stage")[0],
            )
        ]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in QUALITY_CONTROL_RULES
        )
        for label, policy in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, policy=policy)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-contract-language-missing: GOVERNANCE.md",
                    result.stdout + result.stderr,
                )

    def test_non_quality_control_trigger_does_not_require_the_contract(self):
        descriptions = (
            "Use when drafting correspondence from a completed audit report.",
            "Use when revising a draft with an internal self-check.",
        )
        for description in descriptions:
            with self.subTest(description=description):
                skill = f"""---
name: example-skill
description: {description}
---

# Example skill
"""
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill)
                    result = run_validator(root)

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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

    def test_every_live_runtime_sourced_skill_requires_output_provenance(self):
        registry = json.loads(
            read_public_file(REPOSITORY / "governance" / "rules-provenance.json")
        )
        runtime_skills = [
            entry["name"]
            for entry in registry["skills"]
            if entry["rules_mode"] == "runtime-sourced"
        ]

        for name in runtime_skills:
            with self.subTest(skill=name):
                skill = read_public_file(REPOSITORY / "skills" / name / "SKILL.md")
                self.assertRegex(
                    skill,
                    r"(?is)returned.{0,80}artifact.{0,200}actual.{0,100}approved.{0,100}source.{0,30}identity.{0,180}checked.{0,30}date.{0,100}used",
                )

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

    def test_non_string_rules_modes_are_rejected_without_traceback(self):
        for value in ([], {}, 7):
            with self.subTest(rules_mode=value):
                registry = valid_registry()
                registry["skills"][0]["rules_mode"] = value
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, registry=registry)
                    result = run_validator(root)

                output = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("invalid-rules-mode", output)
                self.assertNotIn("Traceback", output)

    def test_invalid_date_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].update({"reviewed_on": "20-08-2026"}),
            "invalid-date",
        )

    def test_bundled_rules_source_is_required(self):
        registry = valid_registry()
        registry["skills"][0]["source_ids"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bundled-source-required: example-skill", result.stdout + result.stderr)

    def test_unknown_source_id_is_rejected(self):
        registry = valid_registry()
        registry["skills"][0]["source_ids"] = ["unknown-source"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown-source-id: example-skill", result.stdout + result.stderr)

    def test_insecure_source_url_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["sources"][0].update({"url": "http://www.uscourts.gov"}),
            "insecure-source-url",
        )

    def test_malformed_source_urls_are_rejected_without_traceback(self):
        for url in ("https://[", "https://white space.example"):
            with self.subTest(url=url):
                registry = valid_registry()
                registry["sources"][0]["url"] = url
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, registry=registry)
                    result = run_validator(root)

                output = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("insecure-source-url", output)
                self.assertNotIn("Traceback", output)

    def test_duplicate_source_id_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["sources"].append(dict(registry["sources"][0])),
            "duplicate-source-id",
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
