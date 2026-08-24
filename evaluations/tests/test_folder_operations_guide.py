import json
import re
import unittest
from pathlib import Path, PurePosixPath


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPOSITORY_ROOT / "README.md"
GUIDE_PATH = REPOSITORY_ROOT / "FOLDER_OPERATIONS.md"
PINNED_INSTALL_SOURCE = re.compile(
    r"https://github\.com/PoliceConductUS/section-1983-skills/tree/"
    r"v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$"
)
CALLER_ROOTS = {
    "__RECORD_ROOT__": "/synthetic/inputs/record",
    "__AUTHORITIES_ROOT__": "/synthetic/inputs/authorities",
    "__OUTPUT_ROOT__": "/synthetic/output",
}
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
    "immutable QC report": "skills/filing-ci/SKILL.md",
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


def folder_operations_link_destinations(markdown):
    return [
        destination
        for _label, destination in markdown_links(markdown)
        if destination == "FOLDER_OPERATIONS.md"
        or "folder operation" in _label.lower()
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
        cls.normalized = " ".join(cls.guide.split())
        cls.normalized_lower = cls.normalized.lower()

    def test_readme_links_exactly_once_to_confined_install_local_guide(self):
        destinations = folder_operations_link_destinations(self.readme)
        self.assertEqual(destinations, ["FOLDER_OPERATIONS.md"])
        resolved = confined_repository_path(destinations[0])
        self.assertTrue(resolved.is_file())
        self.assertEqual(resolved, GUIDE_PATH.resolve())

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
        positions = [self.guide.find(heading) for heading in FIRST_HOUR_HEADINGS]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))

    def test_canonical_invocation_fixture_is_machine_parseable(self):
        blocks = version_one_json_blocks(self.guide)
        self.assertEqual(len(blocks), 1)
        fixture = blocks[0]
        for token, root in CALLER_ROOTS.items():
            fixture = fixture.replace(token, root)
        invocation = json.loads(fixture)

        self.assertEqual(invocation["version"], 1)
        self.assertEqual(
            [item["role"] for item in invocation["inputs"]],
            ["record", "authorities"],
        )
        self.assertEqual(
            [item["root"] for item in invocation["inputs"]],
            [CALLER_ROOTS["__RECORD_ROOT__"], CALLER_ROOTS["__AUTHORITIES_ROOT__"]],
        )
        self.assertEqual(invocation["output"], {"root": CALLER_ROOTS["__OUTPUT_ROOT__"]})
        self.assertEqual(invocation["internet"], "disabled")
        self.assertEqual(
            invocation["isolation"],
            {"inputs": "read-only", "output": "read-write", "undeclared": "none"},
        )

        target = invocation["target"]
        self.assertEqual(target["role"], "record")
        target_path = PurePosixPath(target["path"])
        self.assertFalse(target_path.is_absolute())
        self.assertNotIn("..", target_path.parts)

        runtime = invocation["runtime"]
        self.assertEqual(set(runtime), {"max_seconds", "max_input_bytes"})
        self.assertIsInstance(runtime["max_seconds"], int)
        self.assertGreater(runtime["max_seconds"], 0)
        self.assertLessEqual(runtime["max_seconds"], 3600)
        self.assertIsInstance(runtime["max_input_bytes"], int)
        self.assertGreater(runtime["max_input_bytes"], 0)
        self.assertLessEqual(runtime["max_input_bytes"], 1_073_741_824)

    def test_output_root_is_reused_for_terminal_receipt_verification(self):
        heading = FIRST_HOUR_HEADINGS[-1]
        self.assertIn(heading, self.guide)
        verification = self.guide.split(heading, 1)[1]
        self.assertIn("__OUTPUT_ROOT__", verification)
        self.assertIn(".skill-runs/<run-id>/manifest.json", verification)
        self.assertIn(".skill-runs/<run-id>/incomplete.json", verification)
        self.assertGreaterEqual(self.guide.count("__OUTPUT_ROOT__"), 2)

    def test_trusted_host_execution_and_input_hash_verification_are_explicit(self):
        execution = self.guide.split(FIRST_HOUR_HEADINGS[3], 1)
        self.assertEqual(len(execution), 2)
        self.assertIn("input-read-only", execution[1].lower())
        self.assertIn("trusted host", execution[1].lower())

        verification = self.guide.split(FIRST_HOUR_HEADINGS[4], 1)
        self.assertEqual(len(verification), 2)
        self.assertIn("__RECORD_ROOT__", verification[1])
        self.assertIn("__AUTHORITIES_ROOT__", verification[1])
        self.assertRegex(verification[1].lower(), r"\b(?:sha-256|hash(?:es)?)\b")
        self.assertRegex(verification[1].lower(), r"\bunchanged\b")

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

    def test_folder_backed_patterns_link_to_install_local_skill_owners(self):
        links = markdown_links(self.guide)
        skill_destinations = [
            destination
            for _label, destination in links
            if destination.startswith("skills/")
        ]
        self.assertEqual(len(skill_destinations), len(set(skill_destinations)))

        for operation, expected_owner in OPERATION_OWNERS.items():
            with self.subTest(operation=operation):
                matching_lines = [
                    line for line in self.guide.splitlines() if operation in line.lower()
                ]
                self.assertEqual(len(matching_lines), 1)
                self.assertIn(f"]({expected_owner})", matching_lines[0])

        for destination in skill_destinations:
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
            r"no adapter (?:is|becomes )?(?:part of|required by|required for)",
        )

    def test_examples_are_synthetic_and_machine_independent(self):
        self.assertIn("generic synthetic example", self.normalized_lower)
        for private_marker in (
            "/Users/",
            "/home/",
            "C:\\Users\\",
            "3-25-CV",
            "Lotts",
            "Irving",
            "Scholer",
            "dalelotts",
            "ECF No.",
        ):
            with self.subTest(private_marker=private_marker):
                self.assertNotIn(private_marker, self.guide)

    def test_current_onboarding_docs_reject_obsolete_runtime_terminology(self):
        current_onboarding = "\n".join((self.readme, self.guide))
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

    def test_legal_safety_obligations_reject_reversed_semantics(self):
        for obligation, pattern in SAFETY_OBLIGATIONS.items():
            with self.subTest(obligation=obligation):
                self.assertRegex(self.normalized_lower, pattern)
        mutations = {
            "source classification": "convert an allegation or inference into a fact",
            "human approval": (
                "no actual user approval is required to change a protected decision "
                "to `status: approved`"
            ),
            "immutable inputs": "overwrite immutable inputs",
            "configured validation": "run guessed validation commands",
            "not filing ready": "filing-ready",
        }
        for obligation, mutation in mutations.items():
            with self.subTest(inversion=obligation):
                self.assertNotRegex(mutation, SAFETY_OBLIGATIONS[obligation])

    def test_install_is_pinned_to_one_immutable_release(self):
        sources = remote_install_sources(self.guide)
        self.assertEqual(len(sources), 1)
        self.assertIsNotNone(PINNED_INSTALL_SOURCE.fullmatch(sources[0]))
        self.assertIn("npx skills add . --list", self.guide)
        self.assertIn("tag has not been published", self.normalized_lower)
        self.assertIn("do not substitute `main`", self.normalized_lower)

    def test_tag_guard_rejects_noncanonical_suffix(self):
        mutated = self.guide.replace("/tree/v0.1.0", "/tree/v0.1.0-main")
        sources = remote_install_sources(mutated)
        self.assertEqual(len(sources), 1)
        self.assertIsNone(PINNED_INSTALL_SOURCE.fullmatch(sources[0]))


if __name__ == "__main__":
    unittest.main()
