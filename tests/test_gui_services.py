from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from cvc.gui import run_smoke_test
from cvc.services import CVCService
from cvc.store import sha256_file


ROOT = Path(__file__).resolve().parents[1]


def _copy_workspace() -> tuple[tempfile.TemporaryDirectory[str], CVCService]:
    holder = tempfile.TemporaryDirectory(prefix="cvc-gui-test-")
    destination = Path(holder.name) / "workspace"
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns(".pytest_cache", "__pycache__", ".git"),
    )
    return holder, CVCService(destination)


def test_gui_service_status_rules_e4_and_triggers() -> None:
    service = CVCService(ROOT)
    status = service.get_status()
    assert status["rule_count"] == 38
    assert status["ratified_e4_rules"] == ["STD-EPI-001", "STD-STD-002"]
    assert len(service.get_board()) == 38
    assert len(service.get_triggers()) == 12
    assert service.get_rule("STD-STD-002")["rule"]["current_support_grade"] == "E4"


def test_gui_smoke_service_checks_all_views_without_state_write() -> None:
    service = CVCService(ROOT)
    before = service.workspace.state_jsonl("state/ingest/ingestions.jsonl")
    result = run_smoke_test(ROOT)
    after = service.workspace.state_jsonl("state/ingest/ingestions.jsonl")
    assert all(result.values())
    assert before == after


def test_preview_is_read_only_and_ingest_is_append_only_without_grade_change() -> None:
    holder, service = _copy_workspace()
    try:
        input_path = Path(holder.name) / "evidence.md"
        input_path.write_text("STD-EPI-003 explicit terminal classification and no silent disappearance", encoding="utf-8")
        matrix = service.workspace.path("corpus/board/FLEET_SUPPORT_MATRIX_V0.2.json")
        before_hash = sha256_file(matrix)
        assert not service.workspace.path("state/ingest/ingestions.jsonl").exists()
        preview = service.preview_ingest(input_path)
        assert preview["state_will_change"] is False
        assert not service.workspace.path("state/ingest/ingestions.jsonl").exists()
        result = service.ingest_artifact(input_path)
        assert result["support_grade_change_applied"] is False
        assert sha256_file(matrix) == before_hash
        assert service.workspace.state_jsonl("state/ingest/ingestions.jsonl")
    finally:
        holder.cleanup()


def test_trigger_check_history_and_reasoning_fail_closed() -> None:
    holder, service = _copy_workspace()
    try:
        input_path = Path(holder.name) / "trigger.md"
        input_path.write_text("STD-DIA-001 incident lesson invariant regression conformance", encoding="utf-8")
        result = service.check_triggers(input_path)
        assert result["support_grade_change_applied"] is False
        assert service.workspace.state_jsonl("state/reviews/trigger_checks.jsonl")
        history = service.get_history()
        assert {row["provenance"] for row in history if row["type"] in {"CLOSEOUT", "RATIFICATION"}} == {"FROZEN_HISTORY"}
        assert any(row["type"] == "TRIGGER_CHECK" and row["provenance"] == "RUNTIME_STATE" for row in history)
        search = service.search("STD-DIA-001")
        assert search["RULES"]
        assert search["TRIGGERS"]
        assert service.query_corpus("diagnostic evidence")["reasoning"]["status"] == "DISABLED"
    finally:
        holder.cleanup()
