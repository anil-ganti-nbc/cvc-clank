# CVC Clank

CVC is the Clank ecosystem's evidence-backed institutional memory. It records
and evaluates lessons from incidents, successful architectural patterns,
migrations/restores, diagnostic findings, cross-Clank audits, evidence
triggers, and rule support/ratification history.

The canonical repository is <https://github.com/anil-ganti-nbc/cvc-clank>.

## Scope and identity

CVC is operational, operator-triggered, and unscheduled:

| Field | Value |
| --- | --- |
| Role | Cross-Clank institutional evidence memory and learning/ratification support |
| Lifecycle | `OPERATIONAL` |
| Execution model | `OPERATOR_TRIGGERED` |
| Scheduling | `NONE` |
| Primary inputs | Diagnostic reports; incident artifacts; success-pattern evidence; migration/restore evidence; operator-supplied evidence packages |
| Primary outputs | Append-only evidence records; trigger checks; review recommendations; support-grade review packages; ratification references; corpus integrity results |
| Dependencies | Local frozen CVC corpus; operator-provided evidence; optional reasoning provider, disabled by default |

CVC is **not** a collector, scheduler, remediation engine, Diagnostic Clank,
Standards Clank, or the daily Context/Verification/Coverage journalism
workbench. In particular, the planned CVC Workbench for post-selection editorial
research is a separate future tool and is not implemented here.

The normal learning loop is:

```text
Clank incident or success
  → Diagnostic or preserved evidence
  → explicit CVC ingest
  → trigger check
  → operator review where meaningful
  → support/ratification update only when justified
```

Operator approval is required. CVC does not automatically ingest every incident,
monitor the fleet, or send findings to another Clank.

## Mission boundary

CVC is closed as archaeology and governance preparation with the terminal state
`CVC_MISSION_COMPLETE_WITH_OPEN_EVIDENCE_BLOCKERS`. This repository consumes the
closeout corpus; it does not reopen archaeology, gather evidence, remediate a
Clank, change rule text/maturity/support grades, ingest new evidence during
publication, create another ratification decision, start Standards Clank, or
schedule background work.

The 42 migrated artifacts under `corpus/` are frozen historical input. Their
source and destination hashes are recorded in
`CVC_CORPUS_MIGRATION_MANIFEST_V0.1.json`. Frozen files are versioned and must
not be rewritten by normal runtime operations. Operator-generated records under
`state/` are mutable, append-only working state and remain local by default.
See [the handoff and boundary notes](docs/ECOSYSTEM_INTEGRATION.md) for the
Standards and Workbench boundaries.

## Operator commands

From this directory, use `cvc.cmd` on Windows or set `PYTHONPATH=src` and run
`python -m cvc`:

```text
cvc status
cvc board
cvc rule STD-HIS-001
cvc triggers
cvc verify
cvc ingest <artifact>
cvc check-triggers <artifact>
cvc review --affected
```

The longer forms below are also useful when narrowing a review:

```text
cvc board --grade E4
cvc triggers --status BLOCKED_ON_SPECIFIC_EVIDENCE
cvc query "what evidence exists for durable notification delivery?"
cvc review --affected STD-EPI-003 STD-DIA-001
```

`status`, `board`, `rule`, and `triggers` inspect frozen state. `verify` checks
the migration manifest, all migrated hashes, JSON/JSONL validity, rule counts,
the authoritative E0-E4 distribution, and the ratified E4 set. `query` returns
a bounded provenance packet. The default reasoning provider is disabled, so no
generated conclusion or private chain-of-thought is emitted.

`ingest` preserves a supplied artifact, hashes it, classifies it, maps explicit
rule IDs, and records possible future-trigger matches. `check-triggers` writes a
reviewable check artifact. `review` writes recommendations only. None of these
commands can modify the frozen corpus, support matrix, maturity, ratification,
or historical verdicts.

## Diagnostic handoff and future triggers

Diagnostic Clank answers **“what failed and why?”** CVC answers **“what does
this teach the fleet?”** Diagnostic may produce an evidence package suitable for
explicit operator ingestion, but it must not automatically push every incident
to CVC. The lightweight contract is documented in
[Diagnostic → CVC handoff](docs/DIAGNOSTIC_TO_CVC_HANDOFF.md), with a small
machine-readable schema for unambiguous packages.

When a new meaningful fleet success or failure appears, an operator can run:

```text
cvc check-triggers <artifact>
cvc review --affected
```

The open future-evidence trigger set is
`CVC_FUTURE_EVIDENCE_TRIGGERS_V0.1`. This is discoverable and operator-driven;
there is no automatic monitoring or scheduler.

## Layout

```text
corpus/   frozen CVC closeout, board, rules, evidence, audits, acquisitions
state/    local append-only operator ingest, trigger-check, and review artifacts
src/cvc/  stdlib runtime and CLI
tests/    runtime and integrity tests
scripts/  non-scheduled operator helpers/documentation
docs/     ecosystem identity and Diagnostic handoff contract
```

There is deliberately no daemon, scheduler, periodic scraper, Discord sender,
automatic ratifier, aggregate score, or M1/Standards Clank implementation here.

## Native desktop GUI

PySide6/PyQt6 are not present in the local runtime, so the GUI uses the native
stdlib Tkinter fallback. Launch it with `cvc-gui.cmd` or, from a configured
Python shell, `python -m cvc.gui`. The GUI is a thin front end over
`cvc.services.CVCService`; it does not shell out to the CLI.

The screens are Overview, Rules, Evidence Triggers, Ingest, History, and
Integrity. File ingestion always previews first and requires the explicit
`Preserve + Ingest` action. Search and Ask CVC remain deterministic; semantic
reasoning is visibly disabled unless a future provider is configured.
