"""Bounded, read-only observer snapshot for the CVC fleet identity.

The observer reads the frozen corpus and append-only local state through the
same Workspace API used by the operator service. It never calls an operation
that writes state, and it intentionally reports integrity semantics rather
than collector freshness or source metrics.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .store import Workspace, now_iso

OBSERVER_SCHEMA_VERSION = "cvc-observer.v0.1"
_OPEN_STATUSES = {"SATISFIED", "CLOSED"}
_UNRESOLVED_OUTCOMES = {"INSUFFICIENT_TO_CLASSIFY", "UNMAPPED_REVIEW_REQUIRED"}
_RUNTIME_STATE_PATHS = (
    "state/ingest/ingestions.jsonl",
    "state/reviews/trigger_checks.jsonl",
    "state/reviews/reviews.jsonl",
)
_STATE_ERROR_MAX_CHARS = 240


def _activity(rows: list[dict[str, Any]], id_keys: tuple[str, ...]) -> dict[str, Any] | None:
    if not rows:
        return None
    row = rows[-1]
    return {
        "id": next((row.get(key) for key in id_keys if row.get(key)), None),
        "timestamp": row.get("created_at"),
    }


def _runtime_state(workspace: Workspace) -> tuple[dict[str, list[dict[str, Any]]], bool, list[str]]:
    rows: dict[str, list[dict[str, Any]]] = {}
    errors: list[str] = []
    for relative in _RUNTIME_STATE_PATHS:
        try:
            rows[relative] = workspace.state_jsonl(relative)
        except Exception as exc:  # noqa: BLE001 - surfaced as observer evidence
            rows[relative] = []
            detail = " ".join(str(exc).split())
            message = f"{relative}: {type(exc).__name__}: {detail}"
            if len(message) > _STATE_ERROR_MAX_CHARS:
                message = message[: _STATE_ERROR_MAX_CHARS - 3] + "..."
            errors.append(message)
    return rows, not errors, errors


def _trigger_view(trigger: dict[str, Any]) -> dict[str, Any]:
    return {
        "trigger_id": trigger.get("trigger_id"),
        "rule_ids": trigger.get("rule_ids", []),
        # The frozen trigger vocabulary calls this a trigger_class; expose it
        # as cluster as well so consumers need not infer a taxonomy.
        "cluster": trigger.get("trigger_class", "UNKNOWN"),
        "evidence_needed": {
            "required_artifact": trigger.get("required_artifact", "UNKNOWN"),
            "minimum_sufficient_proof": trigger.get("minimum_sufficient_proof", "UNKNOWN"),
        },
        "status": trigger.get("current_status", "UNKNOWN"),
    }


def observer_snapshot(root: Path | str) -> dict[str, Any]:
    """Return a bounded JSON-safe CVC snapshot without changing workspace state."""
    workspace = Workspace(root)
    observed_at = now_iso()
    integrity = workspace.verify()
    corpus = integrity.as_dict()
    manifest = workspace.migration_manifest()
    board = workspace.board()
    matrix = workspace.matrix()
    triggers = workspace.triggers()
    runtime_state, state_readable, state_errors = _runtime_state(workspace)
    ingestions = runtime_state["state/ingest/ingestions.jsonl"]
    reviews = runtime_state["state/reviews/reviews.jsonl"]
    open_triggers = [row for row in triggers if row.get("current_status") not in _OPEN_STATUSES]
    unresolved = [
        row for row in ingestions
        if _UNRESOLVED_OUTCOMES.intersection(row.get("outcomes", []))
    ]
    failures = corpus.get("failures", [])
    hash_mismatch_count = sum("hash mismatch" in str(item).lower() for item in failures)

    rules = matrix.get("rules", [])
    distribution = {
        grade: sum(row.get("recalculated_support") == grade for row in rules)
        for grade in ("E0", "E1", "E2", "E3", "E4")
    }
    ratified_e4 = sorted(
        row.get("rule_id") for row in rules if row.get("recalculated_support") == "E4"
    )
    return {
        "schema_version": OBSERVER_SCHEMA_VERSION,
        "observed_at_utc": observed_at,
        "identity": {
            "clank_id": "cvc-clank",
            "display_name": "CVC Clank",
            "repo": "https://github.com/anil-ganti-nbc/cvc-clank",
            "lifecycle": "OPERATIONAL",
            "execution_model": "OPERATOR_TRIGGERED",
        },
        "health": {
            "corpus_integrity": "PASS" if integrity.passed else "FAIL",
            "verification_timestamp_utc": observed_at,
            "frozen_artifact_count": len(manifest.get("artifacts", [])),
            "hash_mismatch_count": hash_mismatch_count,
            "manifest_consistent": not any("manifest" in str(item).lower() for item in failures),
            "runtime_state_readable": state_readable,
            "state_read_errors": state_errors,
            "failure_count": len(failures),
        },
        "board": {
            "total_rules": len(rules),
            "support_distribution": {grade: distribution.get(grade, 0) for grade in ("E0", "E1", "E2", "E3", "E4")},
            "ratified_e4_count": len(ratified_e4),
            "ratified_e4_ids": ratified_e4,
            "matrix_version": matrix.get("matrix_version"),
            "board_status": board.get("status"),
        },
        "activity": {
            "latest_ingestion": _activity(ingestions, ("ingestion_id",)),
            "latest_review": _activity(reviews, ("review_id",)),
            "pending_reviews": len(unresolved),
            "unresolved_ingestion_count": len(unresolved),
            "reasoning_provider": "disabled" if not workspace.config.reasoning_enabled else "configured-but-not-implemented",
        },
        "triggers": {
            "open_count": len(open_triggers),
            "open_trigger_ids": [row.get("trigger_id") for row in open_triggers],
            "items": [_trigger_view(row) for row in open_triggers],
        },
        "summary": {
            "status": "OPERATIONAL" if integrity.passed and state_readable else "DEGRADED",
            "integrity": "PASS" if integrity.passed else "FAIL",
            "rules": len(rules),
            "ratified_e4": len(ratified_e4),
            "open_triggers": len(open_triggers),
            "pending_reviews": len(unresolved),
        },
        "integrity_detail": corpus,
    }
