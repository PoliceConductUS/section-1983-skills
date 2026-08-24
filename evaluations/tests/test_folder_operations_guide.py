import json
import re
import tempfile
import unittest
from pathlib import Path, PurePosixPath

from scripts.validate_folder_invocation import validate_invocation


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPOSITORY_ROOT / "README.md"
GUIDE_PATH = REPOSITORY_ROOT / "FOLDER_OPERATIONS.md"
OLD_GUIDE_PATH = REPOSITORY_ROOT / "CASE_WORKSPACE.md"
PINNED_INSTALL_SOURCE = re.compile(
    r"https://github\.com/PoliceConductUS/section-1983-skills/tree/"
    r"v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$"
)
CALLER_ROOT_TOKENS = (
    "__RECORD_ROOT__",
    "__AUTHORITIES_ROOT__",
    "__OUTPUT_ROOT__",
)
FIRST_HOUR_HEADINGS = (
    "## 1. Select input and output folders",
    "## 2. Create the invocation",
    "## 3. Validate the invocation",
    "## 4. Run the skill through a trusted host",
    "## 5. Verify inputs did not change",
    "## 6. Verify outputs and the terminal manifest",
)
OPERATION_OWNERS = {
    "folder-backed filing packet": "skills/section-1983-drafting/SKILL.md",
    "immutable qc report": "skills/filing-ci/SKILL.md",
    "profile package": "skills/building-defense-counsel-overlays/SKILL.md",
    "research corpus": "skills/studying-rule-59e-decisions/SKILL.md",
    "isolated role run": "skills/adversarial-filing-review/SKILL.md",
}
SAFETY_OBLIGATIONS = {
    "source classification": (
        r"without converting an allegation or inference into a fact"
    ),
    "human approval": (
        r"only an actual user approval changes a protected decision"
        r" to `status: approved`"
    ),
    "immutable inputs": r"never overwrite immutable inputs",
    "configured validation": r"run only validation commands configured by the project",
    "not filing ready": r"not filing-ready",
}
FORBIDDEN_SAFETY_CONTRADICTIONS = {
    "source classification": (
        r"\b(?:may|can|should|must|is allowed to) convert"
        r" an allegation or inference into a fact"
    ),
    "human approval": (
        r"(?:no actual user approval is required.{0,120}protected decision|"
        r"protected decision.{0,120}"
        r"(?:may|can|should|must|is allowed to) change.{0,120}"
        r"without actual user approval)"
    ),
    "immutable inputs": (
        r"\b(?:may|can|should|must|is allowed to) overwrite immutable inputs"
    ),
    "configured validation": (
        r"(?<!not )(?<!never )\brun"
        r" (?:any|guessed|unconfigured|arbitrary) validation commands"
    ),
    "filing ready": (
        r"\b(?:workspace|artifact|output|report|packet) (?:is|are) filing-ready\b"
    ),
}
OBSOLETE_TERMINOLOGY = {
    "CaseGraph": r"\bcasegraph\b",
    "CaseHome": r"\bcasehome\b",
    "ResourceHandle": r"\bresourcehandle\b",
    "resource UID": r"\bresource uid\b",
    "graph traversal": r"\bgraph traversal\b",
    "JSONL mutation": r"\bjsonl\b",
    "Git-history instruction": (
        r"\bgit(?:-backed)? history\b|"
        r"\bgit (?:log|commit|branch|checkout|merge|rebase)\b"
    ),
}


def prose_markdown(markdown):
    return re.sub(r"(?ms)^```.*?^```\s*", "", markdown)


def markdown_links(markdown):
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", prose_markdown(markdown))


def markdown_section(markdown, heading):
    match = re.search(rf"(?m)^{re.escape(heading)}\s*$", markdown)
    if match is None:
        return ""
    remainder = markdown[match.end() :]
    next_heading = re.search(r"(?m)^##\s+", remainder)
    return remainder[: next_heading.start()] if next_heading else remainder


def markdown_blocks(markdown):
    return [block for block in re.split(r"\n\s*\n", markdown) if block.strip()]


def operation_units(markdown):
    units = []
    for block in markdown_blocks(markdown):
        lines = block.splitlines()
        if any(line.lstrip().startswith("|") for line in lines):
            units.extend(line for line in lines if line.lstrip().startswith("|"))
            continue
        bullet_units = []
        current = []
        for line in lines:
            if re.match(r"^\s*[-*]\s+", line):
                if current:
                    bullet_units.append("\n".join(current))
                current = [line]
            elif current:
                current.append(line)
        if current:
            bullet_units.append("\n".join(current))
        units.extend(bullet_units or [block])
    return units


def folder_operations_link_destinations(markdown):
    return [
        destination
        for label, destination in markdown_links(markdown)
        if destination == "FOLDER_OPERATIONS.md"
        or "folder operation" in label.lower()
    ]


def remote_install_sources(markdown):
    return [
        match.group(1)
        for match in re.finditer(r"(?m)^npx skills add (https://\S+)(?:\s|$)", markdown)
    ]


def version_one_json_blocks(markdown):
    candidates = []
    for body in re.findall(r"(?ms)^```json\s*$(.*?)^```\s*$", markdown):
        if '"version"' in body:
            candidates.append(body.strip())
    return candidates


def confined_repository_path(destination):
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination):
        raise ValueError("link must be repository-relative")
    if destination.startswith(("/", "\\")) or "#" in destination:
        raise ValueError("link must be a plain repository-relative path")
    resolved = (REPOSITORY_ROOT / destination).resolve()
    resolved.relative_to(REPOSITORY_ROOT.resolve())
    return resolved


class FolderOperationsGuideTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.guide = GUIDE_PATH.read_text(encoding="utf-8") if GUIDE_PATH.exists() else ""
        cls.prose = prose_markdown(cls.guide)
        cls.normalized = " ".join(cls.prose.split())
        cls.normalized_lower = cls.normalized.lower()

    def test_readme_links_exactly_once_to_confined_install_local_guide(self):
        destinations = folder_operations_link_destinations(self.readme)
        self.assertEqual(destinations, ["FOLDER_OPERATIONS.md"])
        resolved = confined_repository_path(destinations[0])
        self.assertTrue(resolved.is_file())
        self.assertEqual(resolved, GUIDE_PATH.resolve())

    def test_replaced_workspace_guide_and_link_are_absent(self):
        with self.subTest(artifact="old guide"):
            self.assertFalse(OLD_GUIDE_PATH.exists())
        with self.subTest(artifact="old README link"):
            destinations = [destination for _label, destination in markdown_links(self.readme)]
            self.assertNotIn("CASE_WORKSPACE.md", destinations)

    def test_readme_link_guard_rejects_traversal_and_fenced_decoy(self):
        mutated = self.readme + (
            "\n[Folder operations](../outside/FOLDER_OPERATIONS.md)\n"
            "```markdown\n[Folder operations](FOLDER_OPERATIONS.md)\n```\n"
        )
        self.assertNotEqual(
            folder_operations_link_destinations(mutated), ["FOLDER_OPERATIONS.md"]
        )
        with self.assertRaises(ValueError):
            confined_repository_path("../outside/FOLDER_OPERATIONS.md")

    def test_first_hour_flow_is_complete_and_ordered(self):
        positions = [self.prose.find(heading) for heading in FIRST_HOUR_HEADINGS]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))
        for heading in FIRST_HOUR_HEADINGS:
            with self.subTest(heading=heading):
                self.assertTrue(markdown_section(self.prose, heading).strip())

    def test_fenced_markdown_decoys_cannot_supply_headings_or_prose(self):
        decoy = "```markdown\n" + "\n".join(FIRST_HOUR_HEADINGS) + "\n"
        decoy += "trusted host hashes manifests folder-backed filing packet\n```\n"
        prose = prose_markdown(decoy)
        for heading in FIRST_HOUR_HEADINGS:
            with self.subTest(heading=heading):
                self.assertEqual(markdown_section(prose, heading), "")
        self.assertNotIn("trusted host", prose)
        self.assertEqual(operation_units(prose), [])

    def test_each_first_hour_step_contains_its_own_required_actions(self):
        requirements = {
            FIRST_HOUR_HEADINGS[0]: (
                r"recursiv(?:e|ely).{0,40}read-only input",
                r"exactly one.{0,40}output",
                r"\brecord\b",
                r"\bauthorities\b",
            ),
            FIRST_HOUR_HEADINGS[1]: (
                r"\bcanonical\b",
                r"\bversion 1\b",
                r"\binvocation\b",
            ),
            FIRST_HOUR_HEADINGS[2]: (
                re.escape("scripts/validate_folder_invocation.py"),
            ),
            FIRST_HOUR_HEADINGS[3]: (
                r"trusted host",
                r"input-read-only",
                r"host.{0,100}(?:owns|enforces).{0,100}(?:execution|sandbox|isolation)",
                r"(?:no universal (?:skill )?runner|does not (?:provide|invent).{0,40}universal)",
            ),
            FIRST_HOUR_HEADINGS[4]: (
                r"\brecord\b",
                r"\bauthorities\b",
                r"\b(?:sha-256|hash(?:es)?)\b",
                r"\bunchanged\b",
            ),
            FIRST_HOUR_HEADINGS[5]: (
                re.escape(CALLER_ROOT_TOKENS[2]),
                r"\bartifact",
                re.escape(".skill-runs/<run-id>/manifest.json"),
                re.escape(".skill-runs/<run-id>/incomplete.json"),
            ),
        }
        for heading, patterns in requirements.items():
            section = " ".join(markdown_section(self.prose, heading).split()).lower()
            for pattern in patterns:
                with self.subTest(heading=heading, pattern=pattern):
                    self.assertRegex(section, pattern.lower())

    def test_terminal_verification_uses_affirmative_success_semantics(self):
        section = " ".join(
            markdown_section(self.prose, FIRST_HOUR_HEADINGS[5]).split()
        ).lower()
        self.assertRegex(section, r"manifest\.json`? (?:validates\b|is valid\b)")
        self.assertNotRegex(
            section,
            r"manifest\.json.{0,40}\b(?:not valid|invalid)\b|"
            r"\b(?:not valid|invalid)\b.{0,40}manifest\.json",
        )
        self.assertRegex(section, r"incomplete\.json`? is absent\b")
        self.assertNotRegex(
            section,
            r"incomplete\.json.{0,40}\b(?:not absent|present)\b|"
            r"\b(?:not absent|present)\b.{0,40}incomplete\.json",
        )

    def test_canonical_invocation_fixture_conforms_to_the_real_validator(self):
        blocks = version_one_json_blocks(self.guide)
        self.assertEqual(len(blocks), 1)

        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            record_root = temporary_root / "pleading-material"
            authorities_root = temporary_root / "verified-law"
            output_root = temporary_root / "generated-review"
            for root in (record_root, authorities_root, output_root):
                root.mkdir()
            replacements = {
                "__RECORD_ROOT__": str(record_root),
                "__AUTHORITIES_ROOT__": str(authorities_root),
                "__OUTPUT_ROOT__": str(output_root),
            }
            fixture = blocks[0]
            for token, root in replacements.items():
                fixture = fixture.replace(token, root)
            invocation = json.loads(fixture)

            target = invocation.get("target")
            self.assertIsInstance(target, dict)
            self.assertIsInstance(target.get("path"), str)
            target_path = PurePosixPath(target["path"])
            self.assertFalse(target_path.is_absolute())
            self.assertTrue(target_path.parts)
            self.assertNotIn("..", target_path.parts)
            declared_target = record_root.joinpath(*target_path.parts)
            declared_target.parent.mkdir(parents=True, exist_ok=True)
            declared_target.write_text("synthetic record\n", encoding="utf-8")

            validated = validate_invocation(invocation)

            self.assertEqual(validated.skill, invocation["skill"])
            self.assertEqual(
                validated.inputs,
                (
                    ("record", record_root.resolve()),
                    ("authorities", authorities_root.resolve()),
                ),
            )
            self.assertEqual(validated.output_root, output_root.resolve())
            self.assertEqual(validated.internet, "disabled")
            self.assertEqual(validated.target, ("record", declared_target.resolve()))
            self.assertEqual(
                validated.runtime,
                {
                    "max_seconds": invocation["runtime"]["max_seconds"],
                    "max_input_bytes": invocation["runtime"]["max_input_bytes"],
                },
            )
            self.assertLessEqual(validated.runtime["max_seconds"], 3600)
            self.assertLessEqual(validated.runtime["max_input_bytes"], 1_073_741_824)

    def test_logical_roles_are_stable_while_caller_folders_are_configurable(self):
        selection = " ".join(
            markdown_section(self.prose, FIRST_HOUR_HEADINGS[0]).split()
        ).lower()
        self.assertIn("record", selection)
        self.assertIn("authorities", selection)
        self.assertRegex(
            selection,
            r"(?:(?:logical )?roles.{0,120}(?:remain|stay) stable|"
            r"(?:remain|stay) stable.{0,120}(?:logical )?roles)",
        )
        self.assertRegex(selection, r"(?:caller|user).{0,120}(?:select|choose|configure)")
        self.assertIn("folder names", selection)
        self.assertIn("absolute locations", selection)

    def test_inaccessible_capabilities_are_denied_explicitly(self):
        denials = {
            "undeclared folders": r"cannot access undeclared folders",
            "input mutation": r"cannot mutate (?:the )?input folders",
            "parent or sibling traversal": (
                r"cannot traverse to parent or sibling paths"
            ),
            "ambient repository": r"cannot read ambient repository contents",
            "unauthorized internet": r"cannot use the internet unless authorized",
        }
        for capability, pattern in denials.items():
            with self.subTest(capability=capability):
                self.assertRegex(self.normalized_lower, pattern)

    def test_guide_states_the_incremental_folder_native_migration_boundary(self):
        self.assertRegex(
            self.normalized_lower,
            r"(?:(?:does not|do not) (?:claim|mean|make).{0,120}"
            r"every installed skill.{0,100}(?:already )?folder-native|"
            r"not every installed skill.{0,100}(?:already )?folder-native)",
        )
        self.assertNotRegex(self.normalized_lower, r"\bissue\s*#?71\b|\#71\b")

    def test_folder_backed_patterns_link_to_install_local_skill_owners(self):
        links = markdown_links(self.guide)
        skill_destinations = [
            destination
            for _label, destination in links
            if destination.startswith("skills/")
        ]

        units = operation_units(self.prose)
        for operation, expected_owner in OPERATION_OWNERS.items():
            with self.subTest(operation=operation):
                matching_units = [
                    unit for unit in units if operation in unit.lower()
                ]
                self.assertGreaterEqual(len(matching_units), 1)
                for unit in matching_units:
                    self.assertIn(f"]({expected_owner})", unit)

        for destination in set(skill_destinations):
            with self.subTest(destination=destination):
                resolved = confined_repository_path(destination)
                self.assertTrue(resolved.is_file())
                self.assertEqual(resolved.name, "SKILL.md")

    def test_reproducibility_is_folder_native_and_does_not_require_git(self):
        for term in (
            "hashes",
            "manifests",
            "checked-through dates",
            "retrieval provenance",
        ):
            with self.subTest(term=term):
                self.assertIn(term, self.normalized_lower)
        self.assertRegex(
            self.normalized_lower,
            r"(?:does not|do not|without) require git(?: at runtime| runtime)?",
        )

    def test_separate_product_boundary_requires_no_adapter(self):
        self.assertRegex(
            self.normalized_lower,
            r"separate product.{0,200}export.{0,200}folders.{0,200}import.{0,200}outputs",
        )
        self.assertRegex(
            self.normalized_lower,
            r"no adapter (?:is |becomes )?(?:part of|required by|required for)",
        )

    def test_examples_are_synthetic_and_machine_independent(self):
        self.assertIn("generic synthetic example", self.normalized_lower)
        for private_marker in (
            "/users/",
            "/home/",
            "c:\\users\\",
            "3-25-cv",
            "lotts",
            "irving",
            "scholer",
            "dalelotts",
            "ecf no.",
        ):
            with self.subTest(private_marker=private_marker):
                self.assertNotIn(private_marker, self.guide.lower())

    def test_current_onboarding_docs_reject_obsolete_runtime_terminology(self):
        current_onboarding = "\n".join(
            (prose_markdown(self.readme), self.prose)
        )
        for term, pattern in OBSOLETE_TERMINOLOGY.items():
            with self.subTest(term=term):
                self.assertNotRegex(current_onboarding.lower(), pattern)

    def test_missing_material_and_tools_never_masquerade_as_ready(self):
        for phrase in (
            "do not invent",
            "validation unavailable",
            "record a gap",
            "not filing-ready",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.normalized_lower)

    def test_legal_safety_obligations_and_contradictions(self):
        for obligation, pattern in SAFETY_OBLIGATIONS.items():
            with self.subTest(obligation=obligation):
                self.assertRegex(self.normalized_lower, pattern)
        for contradiction, pattern in FORBIDDEN_SAFETY_CONTRADICTIONS.items():
            with self.subTest(contradiction=contradiction):
                self.assertNotRegex(self.normalized_lower, pattern)

    def test_every_safety_contradiction_pattern_distinguishes_prohibition_from_reversal(self):
        pattern_cases = {
            "source classification": (
                ("do not convert an allegation or inference into a fact",),
                ("may convert an allegation or inference into a fact",),
            ),
            "human approval": (
                (
                    "without actual user approval, a protected decision cannot change "
                    "to `status: approved`",
                ),
                (
                    "no actual user approval is required before a protected decision "
                    "changes to `status: approved`",
                ),
            ),
            "immutable inputs": (
                ("cannot overwrite immutable inputs",),
                ("is allowed to overwrite immutable inputs",),
            ),
            "configured validation": (
                (
                    "do not run any validation commands",
                    "must not run any validation commands",
                    "cannot run any validation commands",
                    "never run any validation commands",
                ),
                (
                    "run any validation commands",
                    "run guessed validation commands",
                    "run unconfigured validation commands",
                    "may run arbitrary validation commands",
                ),
            ),
            "filing ready": (
                ("the artifact is not filing-ready",),
                ("the artifact is filing-ready",),
            ),
        }
        for obligation, (safe_statements, unsafe_statements) in pattern_cases.items():
            pattern = FORBIDDEN_SAFETY_CONTRADICTIONS[obligation]
            for safe in safe_statements:
                with self.subTest(obligation=obligation, statement=safe):
                    self.assertNotRegex(safe, pattern)
            for unsafe in unsafe_statements:
                with self.subTest(obligation=obligation, statement=unsafe):
                    self.assertRegex(unsafe, pattern)

    def test_install_is_pinned_to_one_immutable_release(self):
        sources = remote_install_sources(self.guide)
        self.assertEqual(len(sources), 1)
        self.assertIsNotNone(PINNED_INSTALL_SOURCE.fullmatch(sources[0]))
        self.assertIn("npx skills add . --list", self.guide)
        self.assertIn("tag has not been published", self.normalized_lower)
        self.assertIn("do not substitute `main`", self.normalized_lower)

    def test_tag_guard_rejects_suffix_on_the_detected_pinned_version(self):
        sources = remote_install_sources(self.guide)
        self.assertEqual(len(sources), 1)
        source = sources[0]
        self.assertIsNotNone(PINNED_INSTALL_SOURCE.fullmatch(source))
        mutated_source = re.sub(r"(v\d+\.\d+\.\d+)$", r"\1-main", source)
        self.assertNotEqual(mutated_source, source)
        mutated = self.guide.replace(source, mutated_source, 1)
        mutated_sources = remote_install_sources(mutated)
        self.assertEqual(len(mutated_sources), 1)
        self.assertIsNone(PINNED_INSTALL_SOURCE.fullmatch(mutated_sources[0]))


if __name__ == "__main__":
    unittest.main()
