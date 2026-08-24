"""Trusted-host FilingPacket validation, publication, and gate coverage."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from scripts.skill_output_writer import OutputRun
from scripts.validate_folder_invocation import ValidatedInvocation, build_input_manifest


MANIFEST_NAME = "filing-packet.json"
PACKET_PREFIX = "filing-packets"
ROLES = frozenset({"main", "appendix", "exhibit", "proposed-order", "other"})
_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class FilingPacketError(ValueError):
    """A bounded FilingPacket contract failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class ValidatedFilingPacket:
    root: Path
    packet_id: str
    documents: tuple[dict[str, Any], ...]
    provenance: dict[str, str | None]
    manifest_sha256: str


def _fail(code: str) -> None:
    raise FilingPacketError(code)


def _canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        _fail("invalid-filing-packet-json")


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("invalid-filing-packet-json")
        result[key] = value
    return result


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _authorized_roles(value: Any) -> frozenset[str]:
    if not isinstance(value, (set, frozenset, tuple, list)):
        _fail("invalid-filing-packet-roles")
    selected = frozenset(value)
    if "main" not in selected or not selected <= ROLES or len(selected) != len(value):
        _fail("invalid-filing-packet-roles")
    return selected


def _relative_path(value: Any) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        _fail("invalid-filing-packet-path")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or path.as_posix() != value
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.parts[0] in {".skill-runs", PACKET_PREFIX}
        or value == MANIFEST_NAME
    ):
        _fail("invalid-filing-packet-path")
    return path


def _sha256(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def _manifest_value(root: Path) -> tuple[dict[str, Any], bytes]:
    try:
        selected_root = root.resolve(strict=True)
        if not selected_root.is_dir():
            _fail("invalid-filing-packet-root")
        manifest_bytes = (selected_root / MANIFEST_NAME).read_bytes()
        value = json.loads(
            manifest_bytes.decode("utf-8", errors="strict"),
            object_pairs_hook=_json_object,
        )
    except FilingPacketError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RuntimeError, ValueError):
        _fail("invalid-filing-packet-manifest")
    return value, manifest_bytes


def _validated_document(root: Path, value: Any, roles: frozenset[str]) -> dict[str, Any]:
    if type(value) is not dict or set(value) != {"id", "kind", "role", "path", "sha256", "size"}:
        _fail("invalid-filing-packet-document")
    if not _identifier(value["id"]) or not _identifier(value["kind"]):
        _fail("invalid-filing-packet-document")
    if value["role"] not in roles:
        _fail("unauthorized-filing-packet-role")
    relative = _relative_path(value["path"])
    if (
        not isinstance(value["sha256"], str)
        or _SHA256.fullmatch(value["sha256"]) is None
        or type(value["size"]) is not int
        or value["size"] < 0
    ):
        _fail("invalid-filing-packet-document")
    try:
        path = (root / Path(*relative.parts)).resolve(strict=True)
        path.relative_to(root)
        if not path.is_file():
            _fail("missing-filing-packet-member")
        contents = path.read_bytes()
    except FilingPacketError:
        raise
    except (OSError, RuntimeError, ValueError):
        _fail("missing-filing-packet-member")
    if len(contents) != value["size"] or _sha256(contents) != value["sha256"]:
        _fail("filing-packet-member-mismatch")
    return dict(value)


def load_filing_packet(packet_root, *, authorized_roles) -> ValidatedFilingPacket:
    """Load and verify one complete FilingPacket under a declared root."""
    roles = _authorized_roles(authorized_roles)
    root = Path(packet_root).resolve(strict=True)
    value, manifest_bytes = _manifest_value(root)
    if type(value) is not dict or set(value) != {"schema_version", "packet_id", "documents", "provenance"}:
        _fail("invalid-filing-packet-manifest")
    if value["schema_version"] != 1 or not _identifier(value["packet_id"]):
        _fail("invalid-filing-packet-manifest")
    provenance = value["provenance"]
    if type(provenance) is not dict or set(provenance) != {"input_manifest_sha256", "source_packet_sha256"}:
        _fail("invalid-filing-packet-provenance")
    if (
        not isinstance(provenance["input_manifest_sha256"], str)
        or _SHA256.fullmatch(provenance["input_manifest_sha256"]) is None
        or (
            provenance["source_packet_sha256"] is not None
            and (
                not isinstance(provenance["source_packet_sha256"], str)
                or _SHA256.fullmatch(provenance["source_packet_sha256"]) is None
            )
        )
    ):
        _fail("invalid-filing-packet-provenance")
    if type(value["documents"]) is not list or not value["documents"]:
        _fail("invalid-filing-packet-documents")
    documents = tuple(_validated_document(root, document, roles) for document in value["documents"])
    ids = [document["id"] for document in documents]
    paths = [document["path"] for document in documents]
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        _fail("duplicate-filing-packet-member")
    if sum(document["role"] == "main" for document in documents) != 1:
        _fail("invalid-filing-packet-main")
    return ValidatedFilingPacket(
        root=root,
        packet_id=value["packet_id"],
        documents=documents,
        provenance=dict(provenance),
        manifest_sha256=_sha256(manifest_bytes),
    )


def resolve_filing_packet_target(packet: ValidatedFilingPacket, relative_path: str) -> dict[str, Any]:
    """Resolve either the whole manifest or one exact listed member."""
    if not isinstance(packet, ValidatedFilingPacket):
        _fail("invalid-filing-packet")
    if relative_path == MANIFEST_NAME:
        return {"scope": "packet", "packet_id": packet.packet_id, "path": MANIFEST_NAME}
    selected = _relative_path(relative_path)
    for document in packet.documents:
        if document["path"] == selected.as_posix():
            return {"scope": "document", "packet_id": packet.packet_id, "document_id": document["id"], "path": document["path"]}
    _fail("unlisted-filing-packet-target")


def _proposed_documents(documents: Any, roles: frozenset[str]) -> tuple[tuple[dict[str, Any], bytes], ...]:
    if type(documents) is not list or not documents:
        _fail("invalid-filing-packet-documents")
    result = []
    for value in documents:
        if type(value) is not dict or set(value) != {"id", "kind", "role", "path", "contents"}:
            _fail("invalid-filing-packet-document")
        if not _identifier(value["id"]) or not _identifier(value["kind"]) or value["role"] not in roles:
            _fail("invalid-filing-packet-document")
        relative = _relative_path(value["path"]).as_posix()
        contents = value["contents"]
        if isinstance(contents, str):
            contents = contents.encode("utf-8")
        if not isinstance(contents, bytes):
            _fail("invalid-filing-packet-contents")
        result.append(({
            "id": value["id"], "kind": value["kind"], "role": value["role"],
            "path": relative, "sha256": _sha256(contents), "size": len(contents),
        }, contents))
    ids = [record[0]["id"] for record in result]
    paths = [record[0]["path"] for record in result]
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        _fail("duplicate-filing-packet-member")
    if sum(record[0]["role"] == "main" for record in result) != 1:
        _fail("invalid-filing-packet-main")
    return tuple(result)


def publish_filing_packet(
    invocation: ValidatedInvocation,
    *,
    packet_id: str,
    documents: list[dict[str, Any]],
    authorized_roles,
    source_packet: ValidatedFilingPacket | None,
    run_id: str,
    skill_version: str,
) -> dict[str, Any]:
    """Publish one complete proposed packet through the shared output writer."""
    if not isinstance(invocation, ValidatedInvocation) or not _identifier(packet_id):
        _fail("invalid-filing-packet-invocation")
    roles = _authorized_roles(authorized_roles)
    proposed = _proposed_documents(documents, roles)
    if source_packet is not None:
        if not isinstance(source_packet, ValidatedFilingPacket) or source_packet.root not in {root for _, root in invocation.inputs}:
            _fail("unbound-source-filing-packet")
        source_sha256 = source_packet.manifest_sha256
    else:
        source_sha256 = None
    input_manifest = build_input_manifest(invocation)
    provenance = {
        "input_manifest_sha256": _sha256(_canonical_bytes(input_manifest)),
        "source_packet_sha256": source_sha256,
    }
    manifest = {
        "documents": [record for record, _ in proposed],
        "packet_id": packet_id,
        "provenance": provenance,
        "schema_version": 1,
    }
    prefix = f"{PACKET_PREFIX}/{packet_id}"
    run = OutputRun.start(
        invocation,
        run_id=run_id,
        skill_version=skill_version,
        mode="append-immutable",
        input_manifest=input_manifest,
    )
    try:
        for document, contents in proposed:
            run.write(f"{prefix}/{document['path']}", contents)
        run.write(f"{prefix}/{MANIFEST_NAME}", _canonical_bytes(manifest))
        return run.complete()
    except Exception:
        try:
            run.fail("filing-packet-publication", "publish")
        except Exception:
            pass
        raise


def evaluate_filing_readiness(packet: ValidatedFilingPacket, gates: Any) -> dict[str, Any]:
    """Evaluate mechanical packet-member coverage for configured QC gates."""
    if not isinstance(packet, ValidatedFilingPacket) or type(gates) is not list or not gates:
        _fail("invalid-filing-packet-gates")
    document_ids = [document["id"] for document in packet.documents]
    expected = set(document_ids)
    missing_coverage = {}
    failed_gates = []
    seen = set()
    for gate in gates:
        if type(gate) is not dict or not _identifier(gate.get("gate")) or gate["gate"] in seen:
            _fail("invalid-filing-packet-gate")
        seen.add(gate["gate"])
        if gate.get("result") != "pass":
            failed_gates.append(gate["gate"])
        if gate.get("scope") == "packet" and set(gate) == {"gate", "result", "scope"}:
            covered = expected
        elif set(gate) == {"gate", "result", "document_ids"} and type(gate["document_ids"]) is list:
            covered = set(gate["document_ids"])
            if len(covered) != len(gate["document_ids"]) or not covered <= expected:
                _fail("invalid-filing-packet-gate")
        else:
            _fail("invalid-filing-packet-gate")
        missing = [document_id for document_id in document_ids if document_id not in covered]
        if missing:
            missing_coverage[gate["gate"]] = missing
    return {
        "ready": not failed_gates and not missing_coverage,
        "failed_gates": failed_gates,
        "missing_coverage": missing_coverage,
    }
