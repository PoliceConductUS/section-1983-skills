import json
import re
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
NPM_RUN_PATTERN = re.compile(r"\bnpm\s+run\s+([A-Za-z0-9:_-]+)")


def package_scripts():
    package = json.loads((REPOSITORY / "package.json").read_text())
    return package["scripts"]


def referenced_scripts(command):
    return set(NPM_RUN_PATTERN.findall(command))


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


def command_discovers_evaluation_tests(command):
    tokens = shlex.split(command)
    required = {"python3", "-m", "unittest", "discover"}
    if not required.issubset(tokens):
        return False
    if "-s" not in tokens:
        return True
    start_directory = tokens[tokens.index("-s") + 1]
    return start_directory.removeprefix("./") in {".", "evaluations/tests"}


def corpus_wiring(scripts):
    for name, command in scripts.items():
        tokens = shlex.split(command)
        if not {"python3", "-m", "evaluations.cli"}.issubset(tokens):
            continue
        values = {}
        for flag in (
            "--corpus",
            "--baseline",
            "--json-output",
            "--markdown-output",
        ):
            if flag not in tokens or tokens.index(flag) + 1 >= len(tokens):
                break
            values[flag] = tokens[tokens.index(flag) + 1]
        if len(values) == 4:
            return {
                "name": name,
                "tokens": tokens,
                "corpus": Path(values["--corpus"]),
                "baseline": Path(values["--baseline"]),
                "json_report": Path(values["--json-output"]),
                "markdown_report": Path(values["--markdown-output"]),
            }
    raise AssertionError("package scripts require the canonical evaluation corpus command")


def workflow_triggers(workflow):
    lines = workflow.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^on:\s*(.*?)\s*$", line)
        if not match:
            continue
        inline = match.group(1).strip("[] ")
        if inline:
            return {
                item.strip().strip('"\'')
                for item in inline.split(",")
                if item.strip()
            }
        triggers = set()
        for nested in lines[index + 1 :]:
            if nested and not nested[0].isspace():
                break
            nested_match = re.match(
                r"^\s{2}[\"']?([A-Za-z0-9_-]+)[\"']?:",
                nested,
            )
            if nested_match:
                triggers.add(nested_match.group(1))
        return triggers
    return set()


def workflow_steps(workflow):
    lines = workflow.splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = re.match(r"^(\s*)-\s+(?:name|uses|run):", line)
        if match:
            starts.append((index, len(match.group(1))))
    steps = []
    for position, (start, indentation) in enumerate(starts):
        end = len(lines)
        for next_start, next_indentation in starts[position + 1 :]:
            if next_indentation == indentation:
                end = next_start
                break
        steps.append("\n".join(lines[start:end]))
    return steps


def yaml_scalar(lines, index, inline_value, field_indentation):
    value = inline_value.strip()
    if value not in {"|", "|-", "|+", ">", ">-", ">+"}:
        return value.strip('"\'')
    values = []
    for nested in lines[index + 1 :]:
        if nested.strip() and len(nested) - len(nested.lstrip()) <= field_indentation:
            break
        values.append(nested.strip())
    return "\n".join(values)


def step_field(step, field):
    lines = step.splitlines()
    pattern = re.compile(rf"^(\s*)(?:-\s+)?{re.escape(field)}:\s*(.*?)\s*$")
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            return yaml_scalar(lines, index, match.group(2), len(match.group(1)))
    return None


def step_with_path(step):
    lines = step.splitlines()
    for index, line in enumerate(lines):
        with_match = re.match(r"^(\s*)with:\s*$", line)
        if not with_match:
            continue
        with_indentation = len(with_match.group(1))
        for nested_index in range(index + 1, len(lines)):
            nested = lines[nested_index]
            indentation = len(nested) - len(nested.lstrip())
            if nested.strip() and indentation <= with_indentation:
                break
            path_match = re.match(r"^(\s*)path:\s*(.*?)\s*$", nested)
            if path_match:
                return yaml_scalar(
                    lines,
                    nested_index,
                    path_match.group(2),
                    len(path_match.group(1)),
                )
    return None


def run_invokes(step, expected):
    run_value = step_field(step, "run")
    if run_value is None:
        return False
    for command in re.split(r"(?:\r?\n|&&|\|\||;)", run_value):
        try:
            tokens = shlex.split(command)
        except ValueError:
            continue
        if tokens[: len(expected)] == expected:
            return True
    return False


def run_appends_markdown_summary(step, markdown_report):
    run_value = step_field(step, "run")
    if run_value is None:
        return False
    has_append = ">>" in run_value or re.search(r"\btee\s+-a(?:\s|$)", run_value)
    return bool(
        has_append
        and markdown_report.as_posix() in run_value
        and "GITHUB_STEP_SUMMARY" in run_value
    )


def uploads_json_report(step, json_report):
    uses = step_field(step, "uses")
    if uses != "actions/upload-artifact@v7":
        return False
    configured_path = step_with_path(step)
    if configured_path is None:
        return False
    expected = json_report.as_posix().removeprefix("./")
    paths = {
        line.strip().strip('"\'').removeprefix("./")
        for line in configured_path.splitlines()
        if line.strip()
    }
    return expected in paths


def coherent_pull_request_workflows(wiring):
    matches = []
    for path in sorted((REPOSITORY / ".github" / "workflows").glob("*.y*ml")):
        workflow = path.read_text()
        if "pull_request" not in workflow_triggers(workflow):
            continue
        steps = workflow_steps(workflow)
        required = (
            any(run_invokes(step, ["npm", "ci"]) for step in steps),
            any(run_invokes(step, ["npm", "run", "validate"]) for step in steps),
            any(
                run_appends_markdown_summary(step, wiring["markdown_report"])
                for step in steps
            ),
            any(uploads_json_report(step, wiring["json_report"]) for step in steps),
        )
        if all(required):
            matches.append(path)
    return matches


class RepositoryIntegrationTest(unittest.TestCase):

    def test_validate_reaches_test_unit(self):
        scripts = package_scripts()

        self.assertIn("test:unit", reachable_scripts(scripts, "validate"))

    def test_test_unit_reaches_evaluation_test_discovery(self):
        scripts = package_scripts()
        reached = reachable_scripts(scripts, "test:unit")

        self.assertTrue(
            any(command_discovers_evaluation_tests(scripts[name]) for name in reached),
            "test:unit must reach evaluation unittest discovery",
        )

    def test_validate_reaches_the_canonical_corpus_gate(self):
        scripts = package_scripts()
        wiring = corpus_wiring(scripts)

        self.assertIn(wiring["name"], reachable_scripts(scripts, "validate"))

    def test_canonical_corpus_package_command_produces_portable_reports(self):
        wiring = corpus_wiring(package_scripts())
        self.assertNotIn("--candidate-command-json", wiring["tokens"])
        self.assertNotIn("--judgment-command-json", wiring["tokens"])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_report = root / "report.json"
            markdown_report = root / "report.md"
            command = list(wiring["tokens"])
            command[command.index("--json-output") + 1] = str(json_report)
            command[command.index("--markdown-output") + 1] = str(markdown_report)

            completed = subprocess.run(
                command,
                cwd=REPOSITORY,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(json_report.read_text())
            markdown = markdown_report.read_text()

        self.assertTrue(markdown.strip())
        self.assertTrue(report["fixtures"])
        for fixture in report["fixtures"]:
            self.assertFalse(fixture["judgment"]["available"])
            self.assertIn("unavailable", fixture["judgment"]["id"])
        self.assertIn("judgment unavailable", markdown.casefold())

    def test_canonical_report_outputs_are_ignored(self):
        wiring = corpus_wiring(package_scripts())
        reports = [wiring["json_report"], wiring["markdown_report"]]
        self.assertTrue(all(not path.is_absolute() for path in reports))
        completed = subprocess.run(
            ["git", "check-ignore", "--no-index", *map(str, reports)],
            cwd=REPOSITORY,
            text=True,
            capture_output=True,
            check=False,
        )

        ignored = {Path(line) for line in completed.stdout.splitlines()}
        self.assertEqual(ignored, set(reports), "both canonical reports must be ignored")

    def test_a_pull_request_workflow_has_coherent_evaluation_behavior(self):
        wiring = corpus_wiring(package_scripts())

        self.assertTrue(
            coherent_pull_request_workflows(wiring),
            "a pull_request workflow must run npm ci and validate, append the wired Markdown report, and upload the wired JSON report with actions/upload-artifact@v7",
        )


if __name__ == "__main__":
    unittest.main()
