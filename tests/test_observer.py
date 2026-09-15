from __future__ import annotations

import hashlib
import shutil
import stat
from pathlib import Path

from cvc.observer import observer_snapshot
from cvc.services import CVCService


ROOT = Path(__file__).resolve().parents[1]


def _state_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (root / "state").rglob("*")
        if path.is_file()
    }


def test_observer_exposes_authoritative_bounded_summary_without_writes() -> None:
    before = _state_hashes(ROOT)
    snapshot = observer_snapshot(ROOT)

    assert snapshot["identity"] == {
        "clank_id": "cvc-clank",
        "display_name": "CVC Clank",
        "repo": "https://github.com/anil-ganti-nbc/cvc-clank",
        "lifecycle": "OPERATIONAL",
        "execution_model": "OPERATOR_TRIGGERED",
    }
    assert snapshot["health"]["corpus_integrity"] == "PASS"
    assert snapshot["health"]["frozen_artifact_count"] == 42
    assert snapshot["health"]["hash_mismatch_count"] == 0
    assert snapshot["board"]["total_rules"] == 38
    assert snapshot["board"]["support_distribution"] == {
        "E0": 0, "E1": 1, "E2": 9, "E3": 26, "E4": 2,
    }
    assert snapshot["board"]["ratified_e4_count"] == 2
    assert snapshot["triggers"]["open_count"] == 12
    assert len(snapshot["triggers"]["items"]) == 12
    assert snapshot["activity"]["pending_reviews"] == 0
    assert _state_hashes(ROOT) == before


def test_service_observer_is_a_read_only_surface() -> None:
    service = CVCService(ROOT)
    before = _state_hashes(ROOT)
    result = service.get_observer_snapshot()
    assert result["summary"]["status"] == "OPERATIONAL"
    assert _state_hashes(ROOT) == before


def test_observer_propagates_frozen_hash_failure(tmp_path: Path) -> None:
    copy_root = tmp_path / "cvc"
    shutil.copytree(
        ROOT,
        copy_root,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
    )
    target = copy_root / "corpus" / "rules" / "BASELINE_V0.1.md"
    target.chmod(target.stat().st_mode | stat.S_IWRITE)
    target.write_text(target.read_text(encoding="utf-8") + "\ncorruption\n", encoding="utf-8")

    snapshot = observer_snapshot(copy_root)

    assert snapshot["health"]["corpus_integrity"] == "FAIL"
    assert snapshot["health"]["hash_mismatch_count"] >= 1
    assert snapshot["summary"]["status"] == "DEGRADED"


def test_observer_fails_soft_without_mutating_corrupt_runtime_state(tmp_path: Path) -> None:
    copy_root = tmp_path / "cvc"
    shutil.copytree(
        ROOT,
        copy_root,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
    )
    target = copy_root / "state" / "ingest" / "ingestions.jsonl"
    target.write_text('{"ingestion_id": "truncated"', encoding="utf-8")
    before = _state_hashes(copy_root)

    snapshot = observer_snapshot(copy_root)

    assert snapshot["summary"]["status"] == "DEGRADED"
    assert snapshot["health"]["runtime_state_readable"] is False
    assert snapshot["health"]["state_read_errors"]
    assert "state/ingest/ingestions.jsonl" in snapshot["health"]["state_read_errors"][0]
    assert len(snapshot["health"]["state_read_errors"][0]) <= 240
    assert snapshot["activity"]["latest_ingestion"] is None
    assert _state_hashes(copy_root) == before
