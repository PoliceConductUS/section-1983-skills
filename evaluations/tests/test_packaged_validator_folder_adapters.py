import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILLS = REPOSITORY / "skills"


def tree_hash(root):
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


class PackagedValidatorFolderAdapterTest(unittest.TestCase):
    def run_isolated(self, skill_name, script_name, arguments, stdin, inputs):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / skill_name
            shutil.copytree(SKILLS / skill_name, package)
            trap = root / "network-trap"
            trap.mkdir()
            (trap / "sitecustomize.py").write_text(
                "import socket\n"
                "def blocked(*args, **kwargs):\n"
                "    raise AssertionError('network access attempted')\n"
                "socket.socket = blocked\n",
                encoding="utf-8",
            )
            before = {name: tree_hash(path) for name, path in inputs.items()}
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(trap)
            command = [
                sys.executable,
                str(package / "scripts" / script_name),
                *arguments,
            ]
            first = subprocess.run(
                command,
                cwd=package,
                env=environment,
                input=stdin,
                capture_output=True,
                text=True,
                check=False,
            )
            second = subprocess.run(
                command,
                cwd=package,
                env=environment,
                input=stdin,
                capture_output=True,
                text=True,
                check=False,
            )
            after = {name: tree_hash(path) for name, path in inputs.items()}
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(after, before)

    def test_each_validator_runs_from_its_isolated_skill_with_network_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            litigation = root / "litigation"
            litigation.mkdir()
            litigation_fixtures = SKILLS / "building-litigation-alignment-overlays" / "references" / "fixtures"
            shutil.copy2(litigation_fixtures / "complete-snapshot.json", litigation / "snapshot.json")
            self.run_isolated(
                "building-litigation-alignment-overlays",
                "validate_overlays.py",
                [
                    "--docket-snapshot-root",
                    str(litigation),
                    "--docket-snapshot-target",
                    "snapshot.json",
                ],
                (litigation_fixtures / "complete-overlay.json").read_text(),
                {"docket-snapshot": litigation},
            )

            counsel = root / "counsel"
            counsel.mkdir()
            counsel_fixtures = SKILLS / "building-defense-counsel-overlays" / "references" / "fixtures"
            shutil.copy2(counsel_fixtures / "complete-research-snapshot.json", counsel / "snapshot.json")
            self.run_isolated(
                "building-defense-counsel-overlays",
                "validate_counsel_overlays.py",
                [
                    "--research-snapshot-root",
                    str(counsel),
                    "--research-snapshot-target",
                    "snapshot.json",
                ],
                (counsel_fixtures / "complete-counsel-overlay.json").read_text(),
                {"research-snapshot": counsel},
            )

            decisions = root / "decisions"
            decisions.mkdir()
            corpus_fixture = SKILLS / "studying-rule-59e-decisions" / "references" / "fixtures" / "valid-complete.json"
            shutil.copy2(corpus_fixture, decisions / "corpus.json")
            self.run_isolated(
                "studying-rule-59e-decisions",
                "validate_corpus.py",
                [
                    "--decisions-root",
                    str(decisions),
                    "--corpus-target",
                    "corpus.json",
                ],
                "",
                {"decisions": decisions},
            )

            filing = root / "filing"
            filing.mkdir()
            (filing / "draft.md").write_text(
                "Officer Doe struck the handcuffed plaintiff four times.\n",
                encoding="utf-8",
            )
            self.run_isolated(
                "section-1983-drafting",
                "draft_lint.py",
                [
                    "--filing-root",
                    str(filing),
                    "--filing-target",
                    "draft.md",
                ],
                "",
                {"filing": filing},
            )

    def test_helpers_expose_no_output_publication_or_command_dispatch_seam(self):
        helpers = (
            SKILLS / "building-litigation-alignment-overlays" / "scripts" / "validate_overlays.py",
            SKILLS / "building-defense-counsel-overlays" / "scripts" / "validate_counsel_overlays.py",
            SKILLS / "studying-rule-59e-decisions" / "scripts" / "validate_corpus.py",
            SKILLS / "section-1983-drafting" / "scripts" / "draft_lint.py",
        )
        forbidden = (
            "validate_folder_invocation",
            "skill_output_writer",
            "output_root",
            "subprocess",
            "os.system",
            "urllib",
            "requests",
            "socket",
        )
        for helper in helpers:
            source = helper.read_text(encoding="utf-8")
            with self.subTest(helper=helper.name):
                for token in forbidden:
                    self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
