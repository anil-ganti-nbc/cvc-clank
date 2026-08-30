from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CVCConfig:
    mission_state: str = "CVC_MISSION_COMPLETE_WITH_OPEN_EVIDENCE_BLOCKERS"
    board_path: str = "corpus/board/CVC_FINAL_BOARD_V0.1.json"
    matrix_path: str = "corpus/board/FLEET_SUPPORT_MATRIX_V0.2.json"
    triggers_path: str = "corpus/triggers/CVC_FUTURE_EVIDENCE_TRIGGERS_V0.1.jsonl"
    reasoning_enabled: bool = False


def load_config(root: Path) -> CVCConfig:
    """Read the small committed YAML-like config without requiring PyYAML."""
    path = root / "cvc.yaml"
    values: dict[str, str] = {}
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"\'')
    return CVCConfig(
        mission_state=values.get("mission_state", CVCConfig.mission_state),
        board_path=values.get("board_path", CVCConfig.board_path),
        matrix_path=values.get("matrix_path", CVCConfig.matrix_path),
        triggers_path=values.get("triggers_path", CVCConfig.triggers_path),
        reasoning_enabled=values.get("reasoning_enabled", "false").lower() == "true",
    )
