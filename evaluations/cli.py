import argparse
import json
import math
import os
import sys
import tempfile
from pathlib import Path

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import FixtureValidationError, load_corpus
from evaluations.judgment import (
    CandidateProtocolError,
    JudgmentProtocolError,
    run_candidate,
    run_judgments,
)
from evaluations.reporting import (
    compare_baseline,
    render_json,
    render_markdown,
    report_exit_status,
)


class ConfigurationError(ValueError):
    pass


def _command(value):
    if value is None:
        return None
    try:
        command = json.loads(value)
    except json.JSONDecodeError as error:
        raise ConfigurationError("configured command must be JSON") from error
    if not isinstance(command, list) or not command or not all(
        isinstance(argument, str) and argument for argument in command
    ):
        raise ConfigurationError(
            "configured commands must be nonempty JSON argument arrays"
        )
    return command


def _same_existing_file(first, second):
    try:
        return first.exists() and second.exists() and first.samefile(second)
    except OSError:
        return False


def _output_destination(path, label):
    destination = Path(path)
    try:
        parent = destination.parent.resolve(strict=True)
    except OSError as error:
        raise ConfigurationError(f"{label} parent is unavailable: {error}") from error
    if not parent.is_dir() or not os.access(parent, os.W_OK):
        raise ConfigurationError(f"{label} parent is not a writable directory")
    if destination.exists() and not destination.is_file():
        raise ConfigurationError(f"{label} must not be a directory")
    try:
        resolved = destination.resolve(strict=False)
    except OSError as error:
        raise ConfigurationError(f"{label} cannot be resolved: {error}") from error
    return destination, resolved


def _inside(path, directory):
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def _preflight_outputs(corpus, baseline, json_output, markdown_output):
    try:
        corpus_path = Path(corpus).resolve(strict=True)
        baseline_path = Path(baseline).resolve(strict=True)
    except OSError as error:
        raise ConfigurationError(f"protected input is unavailable: {error}") from error
    if not corpus_path.is_dir() or not baseline_path.is_file():
        raise ConfigurationError("corpus and baseline must be valid inputs")

    json_path, json_resolved = _output_destination(json_output, "JSON output")
    markdown_path, markdown_resolved = _output_destination(
        markdown_output, "Markdown output"
    )
    outputs = (
        (json_path, json_resolved, "JSON output"),
        (markdown_path, markdown_resolved, "Markdown output"),
    )
    for path, resolved, label in outputs:
        if resolved == baseline_path or _same_existing_file(path, baseline_path):
            raise ConfigurationError(f"{label} aliases the baseline")
        if _inside(resolved, corpus_path):
            raise ConfigurationError(f"{label} resolves inside the fixture corpus")
    if (
        json_resolved == markdown_resolved
        or _same_existing_file(json_path, markdown_path)
    ):
        raise ConfigurationError("JSON and Markdown outputs must be distinct")
    return json_path, markdown_path


def _validate_baseline(baseline, fixtures):
    if not isinstance(baseline, dict):
        raise ConfigurationError("baseline root must be an object")
    minimums_by_fixture = baseline.get("fixtures")
    if not isinstance(minimums_by_fixture, dict):
        raise ConfigurationError("baseline fixtures must be an object")
    fixtures_by_id = {fixture["id"]: fixture for fixture in fixtures}
    for fixture_id, minimums in minimums_by_fixture.items():
        if fixture_id not in fixtures_by_id:
            raise ConfigurationError(f"baseline references unknown fixture {fixture_id}")
        if not isinstance(minimums, dict):
            raise ConfigurationError(f"baseline minimum for {fixture_id} must be an object")
        deterministic = minimums.get("minimum_deterministic_pass_count", 0)
        if type(deterministic) is not int or deterministic < 0:
            raise ConfigurationError(
                f"deterministic minimum for {fixture_id} must be a nonnegative integer"
            )
        judgment = minimums.get("minimum_judgment_pass_rates", {})
        if not isinstance(judgment, dict):
            raise ConfigurationError(
                f"judgment minimums for {fixture_id} must be an object"
            )
        rubric_ids = {criterion["id"] for criterion in fixtures_by_id[fixture_id]["rubric"]}
        for criterion_id, rate in judgment.items():
            if criterion_id not in rubric_ids:
                raise ConfigurationError(
                    f"baseline references unknown rubric {criterion_id} for {fixture_id}"
                )
            if (
                isinstance(rate, bool)
                or not isinstance(rate, (int, float))
                or not math.isfinite(rate)
                or not 0 <= rate <= 1
            ):
                raise ConfigurationError(
                    f"judgment minimum for {fixture_id}/{criterion_id} must be finite from zero through one"
                )


def _permanent_regressions(fixture):
    results = []
    for regression in fixture["regressions"]:
        result = grade_candidate(fixture, regression["candidate"])
        observed = sorted({finding["id"] for finding in result["findings"]})
        expected = set(regression["expected_findings"])
        results.append(
            {
                "id": regression["id"],
                "expected_findings": sorted(expected),
                "observed_findings": observed,
                "expectation_met": expected.issubset(observed),
            }
        )
    return results


def _failure_finding(error, fixture_id):
    return {
        "id": error.finding_id,
        "fixture_id": fixture_id,
        "reason": error.reason,
        "stdout": error.stdout,
        "stderr": error.stderr,
    }


def _unavailable_judgment(identifier, reason, stdout="", stderr=""):
    return {
        "available": False,
        "id": identifier,
        "reason": reason,
        "runs": [],
        "stdout": stdout,
        "stderr": stderr,
    }


def _fixture_result(
    fixture,
    candidate_command,
    judgment_command,
    repetitions,
    timeout_seconds,
):
    permanent = _permanent_regressions(fixture)
    failures = []
    if candidate_command:
        try:
            candidate = run_candidate(
                fixture,
                candidate_command,
                run_id=f"{fixture['id']}-candidate",
                timeout_seconds=timeout_seconds,
            )["output"]
        except CandidateProtocolError as error:
            failures.append(_failure_finding(error, fixture["id"]))
            return (
                {
                    "fixture_id": fixture["id"],
                    "deterministic": {
                        "fixture_id": fixture["id"],
                        "passed": False,
                        "pass_count": 0,
                        "finding_count": 0,
                        "findings": [],
                    },
                    "permanent_regressions": permanent,
                    "judgment": _unavailable_judgment(
                        "judgment-skipped-candidate-failure",
                        "Judgment unavailable because candidate execution failed.",
                    ),
                },
                failures,
            )
    else:
        candidate = fixture["passing_candidate"]

    deterministic = grade_candidate(fixture, candidate)
    judgment_fixture = dict(fixture)
    judgment_fixture["candidate"] = candidate
    try:
        judgment = run_judgments(
            judgment_fixture,
            judgment_command,
            repetitions,
            timeout_seconds=timeout_seconds,
        )
    except JudgmentProtocolError as error:
        failures.append(_failure_finding(error, fixture["id"]))
        judgment = _unavailable_judgment(
            error.finding_id,
            error.reason,
            stdout=error.stdout,
            stderr=error.stderr,
        )
    return (
        {
            "fixture_id": fixture["id"],
            "deterministic": deterministic,
            "permanent_regressions": permanent,
            "judgment": judgment,
        },
        failures,
    )


def _atomic_write(destination, content):
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, destination)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--candidate-command-json")
    parser.add_argument("--judgment-command-json")
    parser.add_argument("--judgment-repetitions", type=int, default=3)
    parser.add_argument("--command-timeout-seconds", type=float, default=60)
    return parser


def main(argv=None):
    arguments = build_parser().parse_args(argv)
    try:
        candidate_command = _command(arguments.candidate_command_json)
        judgment_command = _command(arguments.judgment_command_json)
        if (
            not math.isfinite(arguments.command_timeout_seconds)
            or arguments.command_timeout_seconds <= 0
        ):
            raise ConfigurationError("command timeout must be positive")
        if arguments.judgment_repetitions < 3:
            raise ConfigurationError("judgment repetitions must be at least three")
        json_output, markdown_output = _preflight_outputs(
            arguments.corpus,
            arguments.baseline,
            arguments.json_output,
            arguments.markdown_output,
        )
        fixtures = load_corpus(arguments.corpus)
        baseline = json.loads(Path(arguments.baseline).read_text())
        _validate_baseline(baseline, fixtures)
    except (
        ConfigurationError,
        FixtureValidationError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        message = f"configuration: {error}"
        print(message[:4096], file=sys.stderr)
        return 2

    fixture_results = []
    regressions = []
    for fixture in fixtures:
        result, failures = _fixture_result(
            fixture,
            candidate_command,
            judgment_command,
            arguments.judgment_repetitions,
            arguments.command_timeout_seconds,
        )
        fixture_results.append(result)
        regressions.extend(failures)

    report = {"fixtures": fixture_results, "regressions": regressions}
    for fixture in fixture_results:
        if not fixture["deterministic"]["passed"] and not any(
            finding["fixture_id"] == fixture["fixture_id"]
            and finding["id"].startswith("candidate-")
            for finding in regressions
        ):
            report["regressions"].append(
                {
                    "id": "deterministic-candidate-failure",
                    "fixture_id": fixture["fixture_id"],
                }
            )
        for permanent in fixture["permanent_regressions"]:
            if not permanent["expectation_met"]:
                report["regressions"].append(
                    {
                        "id": "permanent-regression-mismatch",
                        "fixture_id": fixture["fixture_id"],
                        "regression_id": permanent["id"],
                    }
                )
    report["regressions"].extend(compare_baseline(report, baseline))

    try:
        _atomic_write(json_output, render_json(report))
        _atomic_write(markdown_output, render_markdown(report))
    except OSError as error:
        print(f"report write failed: {str(error)[:4000]}", file=sys.stderr)
        return 2
    return report_exit_status(report)


if __name__ == "__main__":
    raise SystemExit(main())
