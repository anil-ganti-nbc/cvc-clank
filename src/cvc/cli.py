from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from .services import CVCService
from .store import CorpusError


def _default_root() -> Path:
    configured = os.environ.get("CVC_ROOT")
    return Path(configured).resolve() if configured else Path(__file__).resolve().parents[2]


def _json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(prog="cvc", description="Operator-triggered runtime for the completed CVC corpus")
    command.add_argument("--root", type=Path, default=_default_root(), help="CVC workspace root (defaults to this workspace)")
    sub = command.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="show mission, board, matrix and local append-only state")
    board = sub.add_parser("board", help="list the authoritative board")
    board.add_argument("--grade", choices=["E0", "E1", "E2", "E3", "E4"])
    board.add_argument("--maturity")
    board.add_argument("--applicability")
    board.add_argument("--ratified", action="store_true")
    board.add_argument("--blocked", action="store_true")
    rule = sub.add_parser("rule", help="show one rule and its frozen references")
    rule.add_argument("rule_id")
    triggers = sub.add_parser("triggers", help="list future-evidence triggers")
    triggers.add_argument("--rule")
    triggers.add_argument("--status")
    sub.add_parser("verify", help="verify migration hashes and frozen corpus structure")
    ingest_cmd = sub.add_parser("ingest", help="preserve and classify one explicit input artifact")
    ingest_cmd.add_argument("input", type=Path)
    query_cmd = sub.add_parser("query", help="return a bounded provenance packet")
    query_cmd.add_argument("question", nargs="+")
    query_cmd.add_argument("--limit", type=int, default=8)
    trigger_cmd = sub.add_parser("check-triggers", help="check one input against frozen future triggers")
    trigger_cmd.add_argument("input", type=Path)
    review_cmd = sub.add_parser("review", help="write an operator-review package without ratification")
    review_cmd.add_argument("--affected", nargs="*", default=[])
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    service = CVCService(args.root)
    workspace = service.workspace
    try:
        if args.command == "status":
            _json(service.get_status())
        elif args.command == "board":
            _json({"matrix_version": workspace.matrix().get("matrix_version"), "rules": service.get_board(grade=args.grade, maturity=args.maturity, applicability=args.applicability, ratified=args.ratified, blocked=args.blocked)})
        elif args.command == "rule":
            result = service.get_rule(args.rule_id)
            if result is None:
                print(f"Unknown rule: {args.rule_id}")
                return 2
            _json(result)
        elif args.command == "triggers":
            rows = service.get_triggers(args.rule, args.status)
            _json({"triggers": rows})
        elif args.command == "verify":
            result = service.verify_corpus()
            _json(result.as_dict())
            return 0 if result.passed else 1
        elif args.command == "ingest":
            _json(service.ingest_artifact(args.input))
        elif args.command == "query":
            _json(service.query_corpus(" ".join(args.question), args.limit))
        elif args.command == "check-triggers":
            _json(service.check_triggers(args.input))
        elif args.command == "review":
            _json(service.create_review(args.affected))
        return 0
    except (CorpusError, OSError, ValueError) as exc:
        print(f"cvc: {exc}")
        return 2
