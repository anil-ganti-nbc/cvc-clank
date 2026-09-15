"""Shared application services used by both the CLI and the desktop GUI.

This module deliberately delegates all CVC behavior to the existing runtime
functions. It is an interface boundary, not a second implementation.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .logic import board_rows, check_triggers, ingest, preview_ingest, query, review, rule_detail, status
from .observer import observer_snapshot
from .store import CorpusIntegrityResult, Workspace, load_json, now_iso


class CVCService:
    def __init__(self, root: Path | str):
        self.workspace = Workspace(root)

    def get_status(self) -> dict[str, Any]:
        return status(self.workspace)

    def get_observer_snapshot(self) -> dict[str, Any]:
        """Return the bounded read-only fleet observer view."""
        return observer_snapshot(self.workspace.root)

    def get_board(self, **filters: Any) -> list[dict[str, Any]]:
        return board_rows(self.workspace, **filters)

    def get_rule(self, rule_id: str) -> dict[str, Any] | None:
        return rule_detail(self.workspace, rule_id)

    def get_triggers(self, rule_id: str | None = None, status_filter: str | None = None) -> list[dict[str, Any]]:
        rows = self.workspace.triggers()
        if rule_id:
            rows = [row for row in rows if rule_id.upper() in row.get("rule_ids", [])]
        if status_filter:
            rows = [row for row in rows if row.get("current_status") == status_filter]
        return rows

    def verify_corpus(self) -> CorpusIntegrityResult:
        return self.workspace.verify()

    def preview_ingest(self, input_path: Path | str) -> dict[str, Any]:
        return preview_ingest(self.workspace, Path(input_path))

    def ingest_artifact(self, input_path: Path | str) -> dict[str, Any]:
        integrity = self.verify_corpus()
        if not integrity.passed:
            raise RuntimeError("Corpus integrity failed; ingestion is blocked until an operator reviews the failure.")
        return ingest(self.workspace, Path(input_path))

    def check_triggers(self, input_path: Path | str) -> dict[str, Any]:
        return check_triggers(self.workspace, Path(input_path))

    def create_review(self, affected: list[str] | None = None) -> dict[str, Any]:
        return review(self.workspace, affected)

    def query_corpus(self, question: str, limit: int = 8) -> dict[str, Any]:
        return query(self.workspace, question, limit)

    def get_history(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        board = self.workspace.board()
        rows.append({
            "timestamp": board.get("board_date", "UNKNOWN"),
            "record_id": board.get("board_id", "CVC-FINAL-BOARD-001"),
            "type": "CLOSEOUT",
            "affected_rules": "38 rules",
            "outcome": board.get("closeout_decision", "UNKNOWN"),
            "artifact": "corpus/board/CVC_FINAL_BOARD_V0.1.json",
            "provenance": "FROZEN_HISTORY",
        })
        ratification_path = self.workspace.path("corpus/ratification/CVC_RATIFICATION_DECISION_001.json")
        if ratification_path.exists():
            ratification = load_json(ratification_path)
            rows.append({
                "timestamp": ratification.get("decision_date", "UNKNOWN"),
                "record_id": ratification.get("ratification_id", "CVC-RAT-001"),
                "type": "RATIFICATION",
                "affected_rules": ", ".join(ratification.get("scope", [])),
                "outcome": ratification.get("decision", "UNKNOWN"),
                "artifact": "corpus/ratification/CVC_RATIFICATION_DECISION_001.json",
                "provenance": "FROZEN_HISTORY",
            })
        matrix = self.workspace.matrix()
        rows.append({
            "timestamp": matrix.get("generated_at", "UNKNOWN"),
            "record_id": matrix.get("matrix_version", "FLEET_SUPPORT_MATRIX_V0.2"),
            "type": "SUPPORT_MATRIX",
            "affected_rules": "STD-EPI-001, STD-STD-002",
            "outcome": "APPEND_ONLY_SUPPORT_OVERLAY",
            "artifact": "corpus/board/FLEET_SUPPORT_MATRIX_V0.2.json",
            "provenance": "FROZEN_HISTORY",
        })
        for path, record_type in (("state/ingest/ingestions.jsonl", "INGESTION"), ("state/reviews/trigger_checks.jsonl", "TRIGGER_CHECK"), ("state/reviews/reviews.jsonl", "REVIEW")):
            for record in self.workspace.state_jsonl(path):
                rows.append({
                    "timestamp": record.get("created_at", "UNKNOWN"),
                    "record_id": record.get("ingestion_id") or record.get("check_id") or record.get("review_id", "UNKNOWN"),
                    "type": record_type,
                    "affected_rules": ", ".join(record.get("affected_rule_ids", [])),
                    "outcome": ", ".join(record.get("outcomes", record.get("matched_trigger_ids", []))) or record.get("recommendations", "RECORDED"),
                    "artifact": record.get("preserved_path") or f"state/{path}",
                    "provenance": "RUNTIME_STATE",
                    "detail": record,
                })
        return sorted(rows, key=lambda row: (str(row.get("timestamp")), str(row.get("record_id"))), reverse=True)

    def search(self, text: str, limit: int = 20) -> dict[str, list[dict[str, Any]]]:
        needle = text.strip().lower()
        if not needle:
            return {"RULES": [], "EVIDENCE": [], "TRIGGERS": [], "HISTORY": []}
        result: dict[str, list[dict[str, Any]]] = {"RULES": [], "EVIDENCE": [], "TRIGGERS": [], "HISTORY": []}
        for row in self.get_board():
            haystack = json.dumps(row, ensure_ascii=False).lower()
            if needle in haystack:
                result["RULES"].append({"label": row.get("rule_id"), "summary": row.get("strongest_evidence", row.get("remaining_blocker", "")), "rule_id": row.get("rule_id")})
        for record in self._evidence_records():
            haystack = json.dumps(record, ensure_ascii=False).lower()
            if needle in haystack:
                result["EVIDENCE"].append({"label": record.get("evidence_id"), "summary": record.get("incident_or_success_pattern", record.get("incident_or_pattern", "")), "artifact": record.get("artifact")})
        for trigger in self.get_triggers():
            haystack = json.dumps(trigger, ensure_ascii=False).lower()
            if needle in haystack:
                result["TRIGGERS"].append({"label": trigger.get("trigger_id"), "summary": trigger.get("trigger_condition", ""), "trigger_id": trigger.get("trigger_id")})
        for row in self.get_history():
            if needle in json.dumps(row, ensure_ascii=False).lower():
                result["HISTORY"].append({"label": row.get("record_id"), "summary": row.get("outcome", ""), "provenance": row.get("provenance")})
        return {key: values[:limit] for key, values in result.items()}

    def _evidence_records(self) -> list[dict[str, Any]]:
        paths = [self.workspace.path("corpus/evidence/FLEET_EVIDENCE_REGISTER_V0.1.jsonl"), *sorted(self.workspace.path("corpus/acquisitions").glob("*.jsonl"))]
        records: list[dict[str, Any]] = []
        from .store import load_jsonl

        for path in paths:
            if path.exists():
                records.extend(load_jsonl(path))
        return records

    def open_known_artifact(self, relative_path: str) -> bool:
        candidate = (self.workspace.root / relative_path).resolve()
        allowed = {((self.workspace.root / item.get("destination_path", "")).resolve()) for item in self.workspace.migration_manifest().get("artifacts", [])}
        allowed.update(path.resolve() for path in self.workspace.path("state").rglob("*") if path.is_file())
        if candidate not in allowed or not candidate.exists():
            return False
        os.startfile(candidate)  # type: ignore[attr-defined]
        return True

    def open_workspace_folder(self) -> None:
        os.startfile(self.workspace.root)  # type: ignore[attr-defined]
