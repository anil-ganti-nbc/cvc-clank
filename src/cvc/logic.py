from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import IngestionRecord, ReviewRecord, TriggerCheck
from .store import RULE_ID_RE, Workspace, append_jsonl, discover_rule_ids, now_iso, sha256_file


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "did", "do", "for", "from",
    "how", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was", "were", "what",
    "when", "where", "which", "with", "within", "would", "does", "has", "have", "into", "not",
}


def tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9][a-z0-9_-]{2,}", text.lower()) if token not in STOP_WORDS}


def _rule_texts(workspace: Workspace) -> dict[str, str]:
    path = workspace.path("corpus/rules/BASELINE_V0.1.md")
    texts: dict[str, str] = {}
    if not path.exists():
        return texts
    for line in path.read_text(encoding="utf-8").splitlines():
        if "STD-" not in line or not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        rule_match = next((cell for cell in cells if RULE_ID_RE.fullmatch(cell)), None)
        if rule_match:
            texts[rule_match] = " | ".join(cells)
    return texts


def _evidence_records(workspace: Workspace) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in [
        workspace.path("corpus/evidence/FLEET_EVIDENCE_REGISTER_V0.1.jsonl"),
        *sorted(workspace.path("corpus/acquisitions").glob("*.jsonl")),
    ]:
        if path.exists():
            try:
                from .store import load_jsonl

                records.extend(load_jsonl(path))
            except Exception:
                # Verify is the command for corpus integrity; query remains bounded if one optional
                # evidence view cannot be read.
                continue
    return records


def _trigger_matches(workspace: Workspace, affected: set[str], text: str = "") -> list[dict[str, Any]]:
    query_tokens = tokens(text)
    matches: list[dict[str, Any]] = []
    for trigger in workspace.triggers():
        rule_ids = set(trigger.get("rule_ids", []))
        trigger_text = " ".join(str(trigger.get(key, "")) for key in ("trigger_condition", "required_artifact", "minimum_sufficient_proof"))
        overlap = len(query_tokens & tokens(trigger_text))
        if rule_ids & affected or overlap >= 3:
            matches.append({"trigger": trigger, "match_tokens": overlap, "explicit_rule_match": bool(rule_ids & affected)})
    return matches


def status(workspace: Workspace) -> dict[str, Any]:
    board = workspace.board()
    matrix = workspace.matrix()
    triggers = workspace.triggers()
    ingest = workspace.state_jsonl("state/ingest/ingestions.jsonl")
    reviews = workspace.state_jsonl("state/reviews/reviews.jsonl")
    distribution = {grade: sum(row.get("recalculated_support") == grade for row in matrix.get("rules", [])) for grade in ("E0", "E1", "E2", "E3", "E4")}
    return {
        "workspace": str(workspace.root),
        "mission_state": board.get("closeout_decision", workspace.config.mission_state),
        "board_status": board.get("status"),
        "matrix_version": matrix.get("matrix_version"),
        "rule_count": len(matrix.get("rules", [])),
        "support_distribution": distribution,
        "open_future_evidence_triggers": sum(t.get("current_status") not in {"SATISFIED", "CLOSED"} for t in triggers),
        "ratified_e4_rules": sorted(row.get("rule_id") for row in matrix.get("rules", []) if row.get("recalculated_support") == "E4"),
        "pending_ratifications": 0,
        "last_ingestion": ingest[-1] if ingest else None,
        "last_review": reviews[-1] if reviews else None,
        "reasoning_provider": "disabled" if not workspace.config.reasoning_enabled else "configured-but-not-implemented",
    }


def board_rows(workspace: Workspace, grade: str | None = None, maturity: str | None = None, applicability: str | None = None, ratified: bool = False, blocked: bool = False) -> list[dict[str, Any]]:
    rows = []
    for row in workspace.board().get("rules", []):
        if grade and row.get("current_support_grade") != grade:
            continue
        if maturity and row.get("maturity") != maturity:
            continue
        if applicability and applicability.upper() not in str(row.get("applicability", "")).upper():
            continue
        if ratified and row.get("ratification_state") != "RATIFIED_E4":
            continue
        if blocked and "BLOCKED" not in str(row.get("evidence_availability_state", "")):
            continue
        rows.append(row)
    return rows


def rule_detail(workspace: Workspace, rule_id: str) -> dict[str, Any] | None:
    rule_id = rule_id.upper()
    row = next((row for row in workspace.board().get("rules", []) if row.get("rule_id") == rule_id), None)
    if row is None:
        return None
    triggers = [trigger for trigger in workspace.triggers() if rule_id in trigger.get("rule_ids", [])]
    matrix_row = next((item for item in workspace.matrix().get("rules", []) if item.get("rule_id") == rule_id), {})
    artifacts = []
    for path in sorted(workspace.path("corpus").rglob("*")):
        if path.is_file() and rule_id in path.read_text(encoding="utf-8", errors="ignore"):
            artifacts.append(str(path.relative_to(workspace.root)))
    return {
        "rule": row,
        "rule_text_from_frozen_baseline": _rule_texts(workspace).get(rule_id),
        "support_matrix_record": matrix_row,
        "future_evidence_triggers": triggers,
        "strongest_evidence_references": row.get("strongest_evidence", ""),
        "matching_corpus_artifacts": artifacts[:40],
    }


def query(workspace: Workspace, question: str, limit: int = 8) -> dict[str, Any]:
    query_tokens = tokens(question)
    rules: list[dict[str, Any]] = []
    for rule_id, text in _rule_texts(workspace).items():
        score = len(query_tokens & tokens(text))
        if score:
            row = next((item for item in workspace.board().get("rules", []) if item.get("rule_id") == rule_id), {})
            rules.append({"score": score, "rule_id": rule_id, "rule_text": text, "support_grade": row.get("current_support_grade"), "maturity": row.get("maturity")})
    rules.sort(key=lambda item: (-item["score"], item["rule_id"]))
    evidence: list[dict[str, Any]] = []
    for record in _evidence_records(workspace):
        text = json.dumps(record, ensure_ascii=False)
        score = len(query_tokens & tokens(text))
        if score:
            evidence.append({"score": score, "evidence_id": record.get("evidence_id"), "source_system": record.get("source_system"), "historical_verdict": record.get("historical_verdict"), "incident_or_pattern": record.get("incident_or_success_pattern", record.get("incident_or_pattern")), "lesson": record.get("lesson"), "affected_rule_ids": record.get("affected_rule_ids", []), "evidence_role": record.get("evidence_role", record.get("provenance", {}).get("independence_role", "UNKNOWN"))})
    evidence.sort(key=lambda item: (-item["score"], str(item["evidence_id"])))
    affected = {item["rule_id"] for item in rules[:limit]}
    trigger_matches = _trigger_matches(workspace, affected, question)
    return {
        "question": question,
        "packet_limit": limit,
        "reasoning": {"enabled": False, "status": "DISABLED", "note": "No reasoning provider is configured; this is a bounded retrieval packet, not a generated conclusion."},
        "relevant_rules": rules[:limit],
        "preserved_evidence": evidence[:limit],
        "future_evidence_triggers": [item["trigger"] for item in trigger_matches[:limit]],
        "bounded_conclusion": "Evidence is presented with provenance and open blockers. No stronger conclusion is emitted when the packet does not establish one.",
    }


def _input_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def _input_classification(path: Path, text: str) -> str:
    name = path.name.lower()
    lowered = (name + " " + text[:4000]).lower()
    if "diagnostic" in lowered or "incident" in lowered or "lesson" in lowered:
        return "DIAGNOSTIC_OR_LEARNING_EVIDENCE"
    if "migration" in lowered or "restore" in lowered or "continuity" in lowered:
        return "CONTINUITY_OR_MIGRATION_EVIDENCE"
    if "delivery" in lowered or "outbox" in lowered or "ack" in lowered:
        return "DELIVERY_EVIDENCE"
    if "research" in lowered or "search" in lowered or "notebookcheck" in lowered:
        return "RESEARCH_EVIDENCE"
    return "UNCLASSIFIED_REVIEW_REQUIRED"


def preview_ingest(workspace: Workspace, input_path: Path) -> dict[str, Any]:
    input_path = input_path.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    digest = sha256_file(input_path)
    prior = workspace.state_jsonl("state/ingest/ingestions.jsonl")
    frozen_hashes = {str(item.get("destination_sha256", "")).upper() for item in workspace.migration_manifest().get("artifacts", [])}
    duplicate = digest in frozen_hashes or any(item.get("input_sha256") == digest for item in prior)
    text = _input_text(input_path)
    affected = discover_rule_ids(text, workspace.all_rule_ids())
    matches = _trigger_matches(workspace, set(affected), text)
    outcomes = ["DUPLICATE_EVIDENCE"] if duplicate else (["NEW_EVIDENCE"] if affected else ["INSUFFICIENT_TO_CLASSIFY"])
    if matches:
        outcomes.append("TRIGGER_CANDIDATE")
    return {
        "input_path": str(input_path),
        "filename": input_path.name,
        "input_sha256": digest,
        "classification": _input_classification(input_path, text),
        "affected_rule_ids": affected,
        "trigger_matches": [{"trigger_id": item["trigger"].get("trigger_id"), "rule_ids": item["trigger"].get("rule_ids", []), "status": item["trigger"].get("current_status")} for item in matches],
        "duplicate": duplicate,
        "proposed_outcomes": outcomes,
        "state_will_change": False,
        "notes": ["Preview is read-only; no state or corpus artifact is written.", "Support grades, ratification state, and frozen historical artifacts are immutable."],
    }


def ingest(workspace: Workspace, input_path: Path) -> dict[str, Any]:
    input_path = input_path.resolve()
    preview = preview_ingest(workspace, input_path)
    digest = preview["input_sha256"]
    duplicate = preview["duplicate"]
    affected = preview["affected_rule_ids"]
    matches = preview["trigger_matches"]
    ingestion_id = f"ING-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{digest[:12]}"
    preserved = workspace.path(f"state/ingest/sources/{ingestion_id}-{input_path.name}")
    preserved.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(input_path, preserved)
    outcomes = preview["proposed_outcomes"]
    record = IngestionRecord(
        ingestion_id=ingestion_id,
        input_path=str(input_path),
        preserved_path=str(preserved.relative_to(workspace.root)),
        input_sha256=digest,
        classification=preview["classification"],
        outcomes=outcomes,
        affected_rule_ids=affected,
        trigger_ids=[item["trigger_id"] for item in matches],
        support_grade_change_applied=False,
        historical_verdict_changed=False,
        created_at=now_iso(),
        notes=["Ingest is operator-triggered and append-only.", "No support grade or ratification state was changed."] + (["Input hash matches frozen or prior evidence."] if duplicate else []),
    )
    payload = {"schema_version": "cvc-ingestion-record.v0.1", **record.__dict__}
    workspace.append_state("state/ingest/ingestions.jsonl", payload)
    workspace.append_state(f"state/ingest/{ingestion_id}.jsonl", payload)
    return payload


def check_triggers(workspace: Workspace, input_path: Path) -> dict[str, Any]:
    input_path = input_path.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    digest = sha256_file(input_path)
    text = _input_text(input_path)
    affected = discover_rule_ids(text, workspace.all_rule_ids())
    matches = _trigger_matches(workspace, set(affected), text)
    dispositions = []
    for item in matches:
        trigger = item["trigger"]
        dispositions.append({"trigger_id": trigger.get("trigger_id"), "rule_ids": trigger.get("rule_ids", []), "disposition": "POTENTIAL_MATCH_REQUIRES_OPERATOR_REVIEW", "explicit_rule_match": item["explicit_rule_match"], "match_tokens": item["match_tokens"]})
    check_id = f"TRG-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{digest[:12]}"
    record = TriggerCheck(check_id, str(input_path), digest, [item["trigger"].get("trigger_id") for item in matches], dispositions, False, now_iso())
    payload = {"schema_version": "cvc-trigger-check.v0.1", **record.__dict__}
    workspace.append_state("state/reviews/trigger_checks.jsonl", payload)
    workspace.append_state(f"state/reviews/{check_id}.jsonl", payload)
    return payload


def review(workspace: Workspace, affected: list[str] | None = None) -> dict[str, Any]:
    rows = workspace.state_jsonl("state/ingest/ingestions.jsonl")
    valid = workspace.all_rule_ids()
    requested = sorted({item.upper() for item in (affected or []) if item.upper() in valid})
    if not requested and rows:
        requested = sorted({rule for row in rows[-10:] for rule in row.get("affected_rule_ids", []) if rule in valid})
    recommendations = []
    for rule_id in requested:
        recommendations.append({"rule_id": rule_id, "recommendation": "RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE", "basis": "Operator review package only; evidence and E4 contract must be reviewed before any recommendation changes.", "support_grade_change_applied": False})
    review_id = f"REV-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    record = ReviewRecord(review_id, requested, [row.get("ingestion_id") for row in rows[-10:]], recommendations, False, False, now_iso())
    payload = {"schema_version": "cvc-review-record.v0.1", **record.__dict__, "allowed_recommendations": ["PROMOTE_E4", "RETAIN_E3", "RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE", "DOWNGRADE_REVIEW_REQUIRED"]}
    workspace.append_state("state/reviews/reviews.jsonl", payload)
    workspace.append_state(f"state/reviews/{review_id}.jsonl", payload)
    return payload
