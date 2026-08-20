import json
import re
from pathlib import Path


class FixtureValidationError(ValueError):
    pass


REQUIRED_FIELDS = (
    "id",
    "target_skill",
    "prompt",
    "sources",
    "deterministic",
    "rubric",
    "passing_candidate",
    "regressions",
)


def _read_json(path, label):
    try:
        return json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FixtureValidationError(f"invalid {label}: {error}") from error


def _nonempty_string(value, label):
    if not isinstance(value, str) or not value:
        raise FixtureValidationError(f"{label} must be a nonempty string")
    return value


def _string_list(value, label, allow_empty=True):
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise FixtureValidationError(f"{label} must be a list of nonempty strings")
    if not allow_empty and not value:
        raise FixtureValidationError(f"{label} must not be empty")
    if len(value) != len(set(value)):
        raise FixtureValidationError(f"duplicate {label} entry")
    return value


def _confined_file(fixture_directory, reference, label):
    if not isinstance(reference, str) or not reference:
        raise FixtureValidationError(f"{label} must name a file in the fixture directory")
    relative = Path(reference)
    if relative.is_absolute() or ".." in relative.parts:
        raise FixtureValidationError(f"{label} must stay within the fixture directory")
    lexical_path = fixture_directory / relative
    try:
        lexical_path.relative_to(fixture_directory)
        resolved_path = lexical_path.resolve(strict=True)
        resolved_path.relative_to(fixture_directory.resolve(strict=True))
    except (OSError, ValueError) as error:
        raise FixtureValidationError(
            f"{label} must stay within the fixture directory"
        ) from error
    if not resolved_path.is_file():
        raise FixtureValidationError(f"{label} must name a file in the fixture directory")
    return resolved_path


def _unique_identifiers(items, label):
    identifiers = []
    for item in items:
        if not isinstance(item, dict):
            raise FixtureValidationError(f"every {label} must be an object")
        identifiers.append(_nonempty_string(item.get("id"), f"{label} id"))
    if len(identifiers) != len(set(identifiers)):
        duplicates = sorted(
            identifier
            for identifier in set(identifiers)
            if identifiers.count(identifier) > 1
        )
        raise FixtureValidationError(
            f"duplicate {label} identifier: {', '.join(duplicates)}"
        )
    return identifiers


def _validate_rules(contract):
    rules = []
    for field, value_field in (
        ("banned_terms", "term"),
        ("banned_patterns", "pattern"),
    ):
        configured = contract.get(field)
        if not isinstance(configured, list):
            raise FixtureValidationError(f"{field} must be a list")
        for rule in configured:
            if not isinstance(rule, dict):
                raise FixtureValidationError(f"every {field} rule must be an object")
            _nonempty_string(rule.get("id"), f"{field} rule id")
            value = _nonempty_string(rule.get(value_field), f"{field} {value_field}")
            if field == "banned_patterns":
                try:
                    re.compile(value)
                except re.error as error:
                    raise FixtureValidationError(
                        f"invalid banned pattern {rule['id']}: {error}"
                    ) from error
            rules.append(rule)
    _unique_identifiers(rules, "deterministic rule")


def _validate_contract(contract, source_ids):
    if not isinstance(contract, dict):
        raise FixtureValidationError("deterministic must be an object")
    _string_list(contract.get("required_fields"), "required field")
    _string_list(contract.get("ordered_headings"), "ordered heading")
    required_citations = _string_list(
        contract.get("required_citations"), "required citation"
    )
    _validate_rules(contract)
    unknown = sorted(set(required_citations) - set(source_ids))
    if unknown:
        raise FixtureValidationError(
            f"deterministic citation is absent from sources: {', '.join(unknown)}"
        )


def load_fixture(directory):
    try:
        fixture_directory = Path(directory).resolve(strict=True)
    except OSError as error:
        raise FixtureValidationError(f"fixture directory is unavailable: {error}") from error
    if not fixture_directory.is_dir():
        raise FixtureValidationError("fixture directory must be a directory")

    manifest = _read_json(fixture_directory / "fixture.json", "fixture manifest")
    if not isinstance(manifest, dict):
        raise FixtureValidationError("fixture manifest must be an object")
    for field in REQUIRED_FIELDS:
        if field not in manifest:
            raise FixtureValidationError(f"fixture manifest is missing {field}")
    if manifest.get("synthetic") is not True:
        raise FixtureValidationError("fixture must explicitly set synthetic to true")
    fixture_id = _nonempty_string(manifest["id"], "fixture id")
    target_skill = _nonempty_string(manifest["target_skill"], "target skill")

    prompt_path = _confined_file(fixture_directory, manifest["prompt"], "prompt")
    source_manifest_path = _confined_file(
        fixture_directory, manifest["sources"], "source manifest"
    )
    passing_path = _confined_file(
        fixture_directory, manifest["passing_candidate"], "passing candidate"
    )

    source_manifest = _read_json(source_manifest_path, "source manifest")
    if not isinstance(source_manifest, list) or not source_manifest:
        raise FixtureValidationError("source manifest must be a nonempty list")
    source_ids = _unique_identifiers(source_manifest, "source")
    sources = []
    for source in source_manifest:
        source_path = _confined_file(
            fixture_directory, source.get("path"), f"source {source['id']}"
        )
        sources.append({"id": source["id"], "content": source_path.read_text()})

    regressions = manifest["regressions"]
    if not isinstance(regressions, list) or not regressions:
        raise FixtureValidationError("fixture requires at least one permanent regression")
    _unique_identifiers(regressions, "regression")
    loaded_regressions = []
    for regression in regressions:
        candidate_path = _confined_file(
            fixture_directory,
            regression.get("candidate"),
            f"regression {regression['id']} candidate",
        )
        expected = _string_list(
            regression.get("expected_findings"),
            f"regression {regression['id']} expected findings",
            allow_empty=False,
        )
        loaded_regressions.append(
            {
                "id": regression["id"],
                "candidate": candidate_path.read_text(),
                "expected_findings": list(expected),
            }
        )

    rubric = manifest["rubric"]
    if not isinstance(rubric, list) or not rubric:
        raise FixtureValidationError("rubric must be a nonempty list")
    _unique_identifiers(rubric, "rubric")
    for criterion in rubric:
        _nonempty_string(criterion.get("description"), "rubric description")
    _validate_contract(manifest["deterministic"], source_ids)

    return {
        "id": fixture_id,
        "synthetic": True,
        "target_skill": target_skill,
        "prompt": prompt_path.read_text(),
        "sources": sources,
        "source_ids": source_ids,
        "passing_candidate": passing_path.read_text(),
        "regressions": loaded_regressions,
        "deterministic": manifest["deterministic"],
        "rubric": rubric,
    }


def load_corpus(directory):
    try:
        corpus_directory = Path(directory).resolve(strict=True)
        children = sorted(path for path in corpus_directory.iterdir() if path.is_dir())
    except OSError as error:
        raise FixtureValidationError(f"corpus directory is unavailable: {error}") from error
    if not children:
        raise FixtureValidationError("corpus requires at least one fixture")
    missing = [path.name for path in children if not (path / "fixture.json").is_file()]
    if missing:
        raise FixtureValidationError(
            f"fixture directory is missing fixture.json: {', '.join(missing)}"
        )
    for child in children:
        try:
            child.resolve(strict=True).relative_to(corpus_directory)
        except (OSError, ValueError) as error:
            raise FixtureValidationError(
                f"fixture directory must resolve within the corpus: {child.name}"
            ) from error
    fixtures = [load_fixture(path) for path in children]
    identifiers = [fixture["id"] for fixture in fixtures]
    if len(identifiers) != len(set(identifiers)):
        duplicates = sorted(
            identifier
            for identifier in set(identifiers)
            if identifiers.count(identifier) > 1
        )
        raise FixtureValidationError(
            f"duplicate fixture identifier: {', '.join(duplicates)}"
        )
    return fixtures
