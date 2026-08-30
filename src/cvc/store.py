from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Iterable

from .config import CVCConfig, load_config
from .models import CorpusIntegrityResult


class CorpusError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CorpusError(f"invalid JSON: {path}: {exc}") from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise CorpusError(f"cannot read JSONL: {path}: {exc}") from exc
    for line_no, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CorpusError(f"invalid JSONL at {path}:{line_no}: {exc}") from exc
        if not isinstance(value, dict):
            raise CorpusError(f"JSONL row is not an object at {path}:{line_no}")
        rows.append(value)
    return rows


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(encoded + "\n")


class Workspace:
    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.config: CVCConfig = load_config(self.root)
        self.manifest_path = self.root / "CVC_CORPUS_MIGRATION_MANIFEST_V0.1.json"

    def path(self, relative: str) -> Path:
        return self.root / relative

    def board(self) -> dict[str, Any]:
        return load_json(self.path(self.config.board_path))

    def matrix(self) -> dict[str, Any]:
        return load_json(self.path(self.config.matrix_path))

    def triggers(self) -> list[dict[str, Any]]:
        return load_jsonl(self.path(self.config.triggers_path))

    def migration_manifest(self) -> dict[str, Any]:
        return load_json(self.manifest_path)

    def state_jsonl(self, relative: str) -> list[dict[str, Any]]:
        path = self.path(relative)
        return load_jsonl(path) if path.exists() else []

    def append_state(self, relative: str, value: dict[str, Any]) -> Path:
        path = self.path(relative)
        append_jsonl(path, value)
        return path

    def all_rule_ids(self) -> set[str]:
        return {row["rule_id"] for row in self.matrix().get("rules", [])}

    def verify(self) -> CorpusIntegrityResult:
        result = CorpusIntegrityResult(passed=True)
        try:
            manifest = self.migration_manifest()
        except CorpusError as exc:
            result.failures.append(str(exc))
            result.passed = False
            return result
        artifacts = manifest.get("artifacts", [])
        if not isinstance(artifacts, list) or len(artifacts) != 42:
            result.failures.append(f"migration manifest must contain 42 artifacts, found {len(artifacts) if isinstance(artifacts, list) else 'non-list'}")
        for artifact in artifacts:
            source = Path(str(artifact.get("source_path", "")))
            destination_value = str(artifact.get("destination_path", ""))
            destination = self.path(destination_value) if not Path(destination_value).is_absolute() else Path(destination_value)
            expected_source = str(artifact.get("source_sha256", "")).upper()
            expected_destination = str(artifact.get("destination_sha256", "")).upper()
            for label, path, expected in (("source", source, expected_source), ("destination", destination, expected_destination)):
                if not path.exists():
                    result.failures.append(f"{label} missing: {path}")
                    continue
                actual = sha256_file(path)
                if actual != expected:
                    result.failures.append(f"{label} hash mismatch: {path} expected {expected} got {actual}")
            result.checks.append({"destination": destination_value, "source_sha256": expected_source, "destination_sha256": expected_destination})
        for directory in ("corpus", "state", "src", "tests"):
            if not self.path(directory).exists():
                result.failures.append(f"required directory missing: {directory}")
        try:
            board = self.board()
            matrix = self.matrix()
            rules = matrix.get("rules", [])
            board_rules = board.get("rules", [])
            if len(rules) != 38 or len(board_rules) != 38:
                result.failures.append(f"authoritative rule count mismatch: matrix={len(rules)} board={len(board_rules)}")
            matrix_ids = {r.get("rule_id") for r in rules}
            board_ids = {r.get("rule_id") for r in board_rules}
            if matrix_ids != board_ids:
                result.failures.append("matrix and board rule IDs differ")
            distribution = {grade: sum(r.get("recalculated_support") == grade for r in rules) for grade in ("E0", "E1", "E2", "E3", "E4")}
            expected_distribution = matrix.get("support_grade_distribution", {})
            if any(distribution[g] != expected_distribution.get(g) for g in distribution):
                result.failures.append(f"support distribution mismatch: {distribution} vs {expected_distribution}")
            e4 = {r.get("rule_id") for r in rules if r.get("recalculated_support") == "E4"}
            if e4 != {"STD-EPI-001", "STD-STD-002"}:
                result.failures.append(f"unexpected E4 set: {sorted(e4)}")
            ratification = self.path("corpus/ratification/CVC_RATIFICATION_DECISION_001.json")
            rat_data = load_json(ratification)
            decisions = rat_data.get("decisions", rat_data.get("ratifications", []))
            result.checks.append({"rule_count": len(rules), "support_distribution": distribution, "e4_rules": sorted(e4), "ratification_present": ratification.exists(), "decision_count": len(decisions) if isinstance(decisions, list) else None})
        except CorpusError as exc:
            result.failures.append(str(exc))
        # Validate every migrated JSON/JSONL file, independently of its hash check.
        for artifact in artifacts:
            destination_value = str(artifact.get("destination_path", ""))
            destination = self.path(destination_value) if not Path(destination_value).is_absolute() else Path(destination_value)
            if destination.suffix.lower() == ".json":
                try:
                    load_json(destination)
                except CorpusError as exc:
                    result.failures.append(str(exc))
            elif destination.suffix.lower() == ".jsonl":
                try:
                    load_jsonl(destination)
                except CorpusError as exc:
                    result.failures.append(str(exc))
        result.passed = not result.failures
        return result


RULE_ID_RE = re.compile(r"STD-[A-Z0-9]+-[0-9]{3}")


def discover_rule_ids(value: Any, valid_ids: set[str]) -> list[str]:
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    return sorted(set(RULE_ID_RE.findall(text)) & valid_ids)


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
