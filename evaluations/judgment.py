import json
import math
import os
import subprocess
import tempfile
import uuid


DEFAULT_TIMEOUT_SECONDS = 60
STREAM_LIMIT = 8192
TRUNCATION_MARKER = "[truncated]"


class CandidateProtocolError(RuntimeError):
    def __init__(self, finding_id, reason, stdout="", stderr=""):
        super().__init__(f"{finding_id}: {reason}")
        self.finding_id = finding_id
        self.reason = reason
        self.stdout = _bounded(stdout)
        self.stderr = _bounded(stderr)


class JudgmentProtocolError(RuntimeError):
    def __init__(self, finding_id, reason, stdout="", stderr=""):
        super().__init__(f"{finding_id}: {reason}")
        self.finding_id = finding_id
        self.reason = reason
        self.stdout = _bounded(stdout)
        self.stderr = _bounded(stderr)


def _text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return str(value)


def _bounded(value):
    text = _text(value)
    if len(text) <= STREAM_LIMIT:
        return text
    return text[: STREAM_LIMIT - len(TRUNCATION_MARKER)] + TRUNCATION_MARKER


def _positive_timeout(timeout_seconds):
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        raise ValueError("command timeout must be positive")
    return timeout_seconds


def _command(command):
    if not isinstance(command, list) or not command or not all(
        isinstance(argument, str) and argument for argument in command
    ):
        raise ValueError("command must be a nonempty argument array")
    return command


def _child_environment():
    return {
        key: value
        for key, value in os.environ.items()
        if key.casefold() not in {"pwd", "oldpwd"}
        and not any(
            context in key.casefold()
            for context in ("conversation", "session", "thread")
        )
    }


def _invoke(command, request, error_type, agent, timeout_seconds):
    try:
        with tempfile.TemporaryDirectory(prefix="drafting-evaluation-") as directory:
            completed = subprocess.run(
                _command(command),
                input=json.dumps(request).encode("utf-8"),
                capture_output=True,
                cwd=directory,
                env=_child_environment(),
                timeout=_positive_timeout(timeout_seconds),
                check=False,
            )
    except FileNotFoundError as error:
        raise error_type(
            f"{agent}-command-unavailable",
            f"{agent} command unavailable: {error}",
        ) from error
    except OSError as error:
        raise error_type(
            f"{agent}-command-unavailable",
            f"{agent} command unavailable: {error}",
        ) from error
    except subprocess.TimeoutExpired as error:
        raise error_type(
            f"{agent}-command-timeout",
            f"{agent} command exceeded timeout of {timeout_seconds} seconds",
            stdout=error.stdout,
            stderr=error.stderr,
        ) from error

    stdout = _bounded(completed.stdout)
    stderr = _bounded(completed.stderr)
    if completed.returncode != 0:
        raise error_type(
            f"{agent}-command-nonzero",
            f"{agent} command exited {completed.returncode}",
            stdout=stdout,
            stderr=stderr,
        )
    try:
        response = json.loads(completed.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise error_type(
            f"{agent}-response-malformed-json",
            f"{agent} response was not valid JSON",
            stdout=stdout,
            stderr=stderr,
        ) from error
    if not isinstance(response, dict):
        raise error_type(
            f"{agent}-response-incomplete",
            f"{agent} response must be an object",
            stdout=stdout,
            stderr=stderr,
        )
    return response, stdout, stderr


def run_candidate(
    fixture,
    command,
    run_id,
    timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
):
    _positive_timeout(timeout_seconds)
    request = {
        "fixture_id": fixture["id"],
        "run_id": run_id,
        "prompt": fixture["prompt"],
        "sources": fixture["sources"],
    }
    response, stdout, stderr = _invoke(
        command,
        request,
        CandidateProtocolError,
        "candidate",
        timeout_seconds,
    )
    if "output" not in response or not isinstance(response["output"], (str, dict)):
        raise CandidateProtocolError(
            "candidate-response-incomplete",
            "candidate response requires output",
            stdout=stdout,
            stderr=stderr,
        )
    return response


def _validate_judgment_response(fixture, run_id, response, stdout, stderr):
    def incomplete(reason):
        raise JudgmentProtocolError(
            "judgment-response-incomplete",
            reason,
            stdout=stdout,
            stderr=stderr,
        )

    if response.get("fixture_id") != fixture["id"]:
        incomplete("judgment fixture id does not match request")
    if response.get("run_id") != run_id:
        incomplete("judgment run id does not match request")
    decisions = response.get("decisions")
    if not isinstance(decisions, list):
        incomplete("judgment response requires decisions")

    expected = [criterion["id"] for criterion in fixture["rubric"]]
    observed = []
    for decision in decisions:
        if not isinstance(decision, dict):
            incomplete("judgment decisions must be objects")
        criterion_id = decision.get("criterion_id")
        if not isinstance(criterion_id, str) or not criterion_id:
            incomplete("judgment criterion id must be a nonempty string")
        observed.append(criterion_id)
        if type(decision.get("passed")) is not bool:
            incomplete("judgment passed value must be boolean")
        if not isinstance(decision.get("reason"), str) or not decision["reason"].strip():
            incomplete("judgment decision requires a reason")
    if len(observed) != len(set(observed)) or set(observed) != set(expected):
        incomplete("judgment decisions must exactly cover the rubric")
    return response


def run_judgments(
    fixture,
    command,
    repetitions,
    timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
):
    _positive_timeout(timeout_seconds)
    if repetitions < 3:
        raise ValueError("judgment evaluation requires at least three repetitions")
    if command is None:
        return {
            "available": False,
            "id": "judgment-command-unavailable",
            "reason": "Judgment command unavailable: no command configured.",
            "runs": [],
        }

    runs = []
    for index in range(repetitions):
        run_id = f"{fixture['id']}-judgment-{index + 1}-{uuid.uuid4().hex}"
        request = {
            "fixture_id": fixture["id"],
            "run_id": run_id,
            "prompt": fixture["prompt"],
            "sources": fixture["sources"],
            "candidate": fixture["candidate"],
            "rubric": fixture["rubric"],
        }
        try:
            response, stdout, stderr = _invoke(
                command,
                request,
                JudgmentProtocolError,
                "judgment",
                timeout_seconds,
            )
        except JudgmentProtocolError as error:
            if error.finding_id == "judgment-command-unavailable" and not runs:
                return {
                    "available": False,
                    "id": error.finding_id,
                    "reason": error.reason,
                    "runs": [],
                    "stdout": error.stdout,
                    "stderr": error.stderr,
                }
            raise
        runs.append(
            _validate_judgment_response(fixture, run_id, response, stdout, stderr)
        )

    aggregate = aggregate_judgments(fixture["id"], fixture["rubric"], runs)
    aggregate["available"] = True
    return aggregate


def aggregate_judgments(fixture_id, rubric, runs):
    criteria = {}
    for criterion in rubric:
        criterion_id = criterion["id"]
        decisions = []
        for run in runs:
            decision = next(
                item
                for item in run["decisions"]
                if item["criterion_id"] == criterion_id
            )
            decisions.append(
                {
                    "run_id": run["run_id"],
                    "passed": decision["passed"],
                    "reason": decision["reason"],
                }
            )
        passes = sum(decision["passed"] for decision in decisions)
        run_count = len(decisions)
        pass_rate = passes / run_count if run_count else 0.0
        criteria[criterion_id] = {
            "passes": passes,
            "run_count": run_count,
            "pass_rate": pass_rate,
            "variance": pass_rate * (1 - pass_rate),
            "unstable": 0 < passes < run_count,
            "decisions": decisions,
        }
    return {"fixture_id": fixture_id, "runs": runs, "criteria": criteria}
