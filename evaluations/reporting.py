import json


def compare_baseline(current, baseline):
    fixtures = {fixture["fixture_id"]: fixture for fixture in current.get("fixtures", [])}
    findings = []
    for fixture_id, minimums in baseline.get("fixtures", {}).items():
        fixture = fixtures.get(fixture_id, {})
        current_count = fixture.get("deterministic", {}).get("pass_count", 0)
        minimum_count = minimums.get("minimum_deterministic_pass_count", 0)
        if current_count < minimum_count:
            findings.append(
                {
                    "id": "baseline-deterministic-regression",
                    "fixture_id": fixture_id,
                    "metric": "deterministic_pass_count",
                    "minimum": minimum_count,
                    "current": current_count,
                }
            )
        judgment = fixture.get("judgment", {})
        minimum_rates = minimums.get("minimum_judgment_pass_rates", {})
        if minimum_rates and not judgment.get("available"):
            for criterion_id, minimum_rate in minimum_rates.items():
                findings.append(
                    {
                        "id": "baseline-judgment-unavailable",
                        "fixture_id": fixture_id,
                        "metric": f"{criterion_id}.pass_rate",
                        "minimum": minimum_rate,
                    }
                )
            continue
        criterion_results = judgment.get("criteria", {})
        for criterion_id, minimum_rate in minimum_rates.items():
            current_rate = criterion_results.get(criterion_id, {}).get("pass_rate", 0.0)
            if current_rate < minimum_rate:
                findings.append(
                    {
                        "id": "baseline-judgment-regression",
                        "fixture_id": fixture_id,
                        "metric": f"{criterion_id}.pass_rate",
                        "minimum": minimum_rate,
                        "current": current_rate,
                    }
                )
    return findings


def render_json(report):
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def render_markdown(report):
    lines = ["# Drafting-Skill Evaluation Report", ""]
    for fixture in report.get("fixtures", []):
        fixture_id = fixture["fixture_id"]
        deterministic = fixture["deterministic"]
        status = "passed" if deterministic["passed"] else "failed"
        lines.extend(
            [
                f"## {fixture_id}",
                "",
                f"Deterministic: {status}",
                "",
            ]
        )
        for finding in deterministic.get("findings", []):
            location = finding.get("location", "")
            lines.append(f"- {finding['id']}: {location}")
        if deterministic.get("findings"):
            lines.append("")

        permanent = fixture.get("permanent_regressions", [])
        if permanent:
            lines.extend(["Permanent regressions:", ""])
            for regression in permanent:
                status = "matched" if regression["expectation_met"] else "mismatched"
                lines.append(f"- {regression['id']}: {status}")
            lines.append("")

        judgment = fixture["judgment"]
        if not judgment.get("available"):
            identifier = judgment.get("id", "judgment-command-unavailable")
            lines.extend(
                [f"Judgment unavailable ({identifier}): {judgment['reason']}", ""]
            )
            for stream in ("stdout", "stderr"):
                if judgment.get(stream):
                    lines.extend([f"{stream}: {judgment[stream]}", ""])
        else:
            lines.extend(["Judgment results:", ""])
            for criterion_id, result in judgment.get("criteria", {}).items():
                stability = "unstable" if result["unstable"] else "stable"
                lines.append(
                    f"- {criterion_id}: pass rate {result['pass_rate']:.3f}; "
                    f"variance {result['variance']:.3f}; {stability}"
                )
            lines.append("")

    lines.extend(["## Regressions", ""])
    if report.get("regressions"):
        for finding in report["regressions"]:
            details = []
            if "metric" in finding:
                details.append(finding["metric"])
            if "minimum" in finding and "current" in finding:
                details.append(f"minimum {finding['minimum']}, current {finding['current']}")
            elif "minimum" in finding:
                details.append(f"minimum {finding['minimum']}; current unavailable")
            if finding.get("reason"):
                details.append(finding["reason"])
            suffix = f": {'; '.join(details)}" if details else ""
            lines.append(f"- {finding['id']} ({finding.get('fixture_id', 'corpus')}){suffix}")
            for stream in ("stdout", "stderr"):
                if finding.get(stream):
                    lines.append(f"  - {stream}: {finding[stream]}")
    else:
        lines.append("None.")
    lines.append("")
    return "\n".join(lines)


def report_exit_status(report):
    if report.get("regressions"):
        return 1
    for fixture in report.get("fixtures", []):
        if not fixture.get("deterministic", {}).get("passed", False):
            return 1
        if any(
            not regression.get("expectation_met", False)
            for regression in fixture.get("permanent_regressions", [])
        ):
            return 1
    return 0
