from __future__ import annotations

import json
import os
import shutil
import stat
import tempfile
from pathlib import Path

from cvc.logic import check_triggers, ingest, query, review, rule_detail, status
from cvc.store import Workspace, sha256_file


ROOT = Path(__file__).resolve().parents[1]


def _copy_workspace() -> tuple[tempfile.TemporaryDirectory[str], Workspace]:
    holder = tempfile.TemporaryDirectory(prefix="cvc-test-")
    destination = Path(holder.name) / "workspace"
    shutil.copytree(ROOT, destination)
    return holder, Workspace(destination)


def _make_writable(path: Path) -> None:
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def test_migration_hash_preservation_and_authoritative_distribution() -> None:
    workspace = Workspace(ROOT)
    result = workspace.verify()
    assert result.passed, result.failures
    manifest = workspace.migration_manifest()
    assert len(manifest["artifacts"]) == 42
    assert all(item["source_sha256"] == item["destination_sha256"] for item in manifest["artifacts"])
    matrix = workspace.matrix()
    assert matrix["matrix_version"] == "FLEET_SUPPORT_MATRIX_V0.2"
    assert matrix["support_grade_distribution"] == {"field": "recalculated_support", "semantic_name": "support_grade", "E0": 0, "E1": 1, "E2": 9, "E3": 26, "E4": 2, "total_rules": 38}


def test_rule_count_e4_set_and_ratification() -> None:
    workspace = Workspace(ROOT)
    rules = workspace.matrix()["rules"]
    assert len(rules) == 38
    assert {row["rule_id"] for row in rules if row["recalculated_support"] == "E4"} == {"STD-EPI-001", "STD-STD-002"}
    decision = json.loads((ROOT / "corpus/ratification/CVC_RATIFICATION_DECISION_001.json").read_text(encoding="utf-8"))
    assert decision["ratification_id"] == "CVC-RAT-001"
    assert {item["final_ratification"]["decision"] for item in decision["decisions"]} == {"RATIFIED_E4"}


def test_lookups_and_trigger_lookup() -> None:
    workspace = Workspace(ROOT)
    detail = rule_detail(workspace, "STD-EPI-001")
    assert detail is not None
    assert detail["rule"]["maturity"] == "PROVISIONAL"
    assert detail["support_matrix_record"]["recalculated_support"] == "E4"
    triggers = [row for row in workspace.triggers() if "STD-EPI-003" in row["rule_ids"]]
    assert triggers
    assert status(workspace)["open_future_evidence_triggers"] == 12


def test_mutation_detection_and_broken_json() -> None:
    holder, workspace = _copy_workspace()
    try:
        target = workspace.path("corpus/board/CVC_FINAL_BOARD_V0.1.json")
        _make_writable(target)
        target.write_text("{broken", encoding="utf-8")
        result = workspace.verify()
        assert not result.passed
        assert any("hash mismatch" in failure for failure in result.failures)
        assert any("invalid JSON" in failure for failure in result.failures)
    finally:
        holder.cleanup()


def test_broken_jsonl_detection() -> None:
    holder, workspace = _copy_workspace()
    try:
        target = workspace.path("corpus/triggers/CVC_FUTURE_EVIDENCE_TRIGGERS_V0.1.jsonl")
        _make_writable(target)
        with target.open("a", encoding="utf-8") as handle:
            handle.write("{broken\n")
        result = workspace.verify()
        assert not result.passed
        assert any("invalid JSONL" in failure for failure in result.failures)
    finally:
        holder.cleanup()


def test_append_only_ingest_duplicate_no_grade_change_and_historical_immutability() -> None:
    holder, workspace = _copy_workspace()
    try:
        input_path = Path(holder.name) / "candidate.json"
        input_path.write_text(json.dumps({"rule_id": "STD-EPI-003", "incident": "explicit terminal classification; no silent disappearance"}), encoding="utf-8")
        matrix_hash = sha256_file(workspace.path("corpus/board/FLEET_SUPPORT_MATRIX_V0.2.json"))
        original_hash = workspace.migration_manifest()["artifacts"][0]["source_sha256"]
        first = ingest(workspace, input_path)
        second = ingest(workspace, input_path)
        assert "NEW_EVIDENCE" in first["outcomes"]
        assert "DUPLICATE_EVIDENCE" in second["outcomes"]
        assert first["support_grade_change_applied"] is False
        assert second["historical_verdict_changed"] is False
        assert sha256_file(workspace.path("corpus/board/FLEET_SUPPORT_MATRIX_V0.2.json")) == matrix_hash
        assert workspace.migration_manifest()["artifacts"][0]["source_sha256"] == original_hash
        assert len(workspace.state_jsonl("state/ingest/ingestions.jsonl")) == 2
    finally:
        holder.cleanup()


def test_trigger_check_review_and_reasoning_fail_closed() -> None:
    holder, workspace = _copy_workspace()
    try:
        input_path = Path(holder.name) / "diagnostic-lesson.md"
        input_path.write_text("STD-DIA-001 incident lesson candidate invariant regression conformance preserved verdict", encoding="utf-8")
        trigger = check_triggers(workspace, input_path)
        assert trigger["check_id"].startswith("TRG-")
        assert trigger["support_grade_change_applied"] is False
        reviewed = review(workspace, ["STD-DIA-001"])
        assert reviewed["ratification_created"] is False
        assert reviewed["support_grade_changed"] is False
        packet = query(workspace, "what lesson and conformance evidence exists for diagnostic incidents?")
        assert packet["reasoning"]["status"] == "DISABLED"
        assert packet["bounded_conclusion"].startswith("Evidence is presented")
    finally:
        holder.cleanup()
