# Standards Baseline Evidence Pass 1

## Watch Clank conformance audit

Status: evidence pass complete; `STANDARD_V0.1` is **not frozen**.

Date: 2026-08-30

Audit mode: read-only, no remediation.

The first evidence pass applied the governing loop:

```text
failure / success
        ↓
lesson
        ↓
candidate invariant
        ↓
 evidence across Clanks
        ↓
standard
        ↓
machine-checkable conformance
```

The audit evaluates Watch Clank against the candidate baseline as it exists in
the evidence corpus. `PASS`, `FAIL`, `WARN`, `NOT_APPLICABLE`, `UNKNOWN`, and
`EXEMPT` are per-rule audit outcomes. The counts below are a report summary,
not an aggregate conformance score.

## 1. Evidence corpus and integrity boundary

### Diagnostic Clank

The locally available Diagnostic Clank bundle contains:

- the processed [Honor Pad X9 Max miss](C:/Users/anil/Desktop/diagnostic-clank-honor-miss-evidence/reports/processed/20260828-111746_codex_tablet-clank_honor-pad-x9-max-miss.md), a high-confidence `tablet-clank` source-gap incident whose first failed gate is `source_capability`;
- `state/diagnostic.db`, schema version `2`;
- one `agent_outputs` row for that handoff;
- zero rows in the normalized `incidents`, `report_ingestions`,
  `report_findings`, `report_lessons`, and related claim/disposition tables.

The database was inspected read-only. The processed report is usable evidence,
but the local database copy cannot independently replay the full Diagnostic
incident ledger. Watch's committed failure corpus states that its 12 Watch
lessons came from a Diagnostic database plus an ingested historical L register;
those lessons are treated as extracted, provenance-bearing evidence.

### Watch Clank

The audit used the committed Watch contracts and forensic material, including:

- `ZLM_5.3_FLASH_WATCH_CLANK_BRIEF.md`;
- `WATCH_EXPANSION_FAILURE_CORPUS.md`;
- `WATCH_EVENT_SEMANTICS.md`;
- `WATCH_SOAK_CONTRACT.md`;
- `WATCH_COLLECTOR_ARCHITECTURE_AUDIT.md`;
- `ARCHITECTURE_NOTES_QC_VOLUME.md`;
- the hostile architecture audit and correction;
- the incident/autopsy handoffs for freshness, baseline absorption, floods,
  silent delivery, regional coverage, deployment duplication, and QC.

The local `watch_clank.db` was inspected read-only and is an empty development
database: all Watch domain tables contain zero rows and only the Alembic
version row is present. The documented 2026-08-29 live-state counts in the
Watch brief are therefore cited as committed audit evidence, not re-verified
current database state.

### OEM Radar

OEM Radar contributes successful-pattern evidence for implementation-neutral
source descriptors, normalized product identity, raw snapshot retention,
per-source run accounting, and a notification outbox with deduplication and
retry. This is design/test evidence, not a claim of fleet-wide production
operation. The primary references are:

- `C:\Users\anil\Documents\oem_radar-full\oem_radar\docs\ARCHITECTURE.md`;
- `C:\Users\anil\Documents\oem_radar-full\oem_radar\docs\DATABASE.md`;
- `C:\Users\anil\Documents\oem_radar-full\oem_radar\tests\test_discord.py`;
- `C:\Users\anil\Documents\oem_radar-full\oem_radar\tests\test_runner.py`.

No local BANKAI/BANKAI II incident corpus, Great Clank Audit report, KTW
history, Smartphone/Smartwatch/Feature Phone migration history, or full
Motherclank ledger was found. Those remain evidence-pass inputs, not inferred
facts.

Primary input hashes captured at audit time:

| Input | SHA-256 |
|---|---|
| Diagnostic processed Honor report | `8022C1E15111D5F86B40A522D1FCA68FAFADFCD4819C1427B855C7F379F6C5D3` |
| Diagnostic database copy | `EE512F37AF1ACAE2416CC6AB5108C9C858CE94BFB8A82CCFF4568BC5EBF8D953` |
| Watch failure corpus | `8618678FF6E8979A342EE9F56542D6F388A027B31938A071485F0526582B4F25` |
| Watch operating brief | `E8EE1F8A43E132AA2A17A83AA3B3BFC83B76A4A1A36EB868E7AAFF6B971C6A44` |
| OEM Radar architecture | `69ACBE84E0FB245B9D19E9D7A8CA3A94027731A31D3482D494DF5AB2E4CFDE90` |
| OEM Radar database contract | `E08D22467367E1360995C0223457E5E2914C6991A5D7B3ECFA5B45278BAE2ACE` |

## 2. Support-grade result

The normalized register in [BASELINE_V0.1.md](./BASELINE_V0.1.md) now classifies
all 38 candidate rules:

| Support grade | Count | Interpretation in this pass |
|---|---:|---|
| `E0` | 1 | Proposal only: no direct local evidence. |
| `E1` | 1 | One direct system/contract evidence source. |
| `E2` | 8 | Repeated evidence within one Clank or one narrow system family. |
| `E3` | 28 | Same lesson evidenced across multiple Clanks or a Clank plus a separately sourced incident corpus. |
| `E4` | 0 | No fleet-wide evidence or broad demonstrated successful pattern has been established. |

This is a material improvement over the proposal-only baseline, but it is not
ratification. `E3` is the highest grade earned here; none of the rules may yet
be marked `VERIFIED` because the corpus lacks a complete fleet ledger and a
reviewed machine conformance run.

## 3. Cross-Clank generalization findings

| General lesson | Supporting systems | Baseline rules | Result |
|---|---|---|---|
| Local observation is not market/product novelty. | Story Clank, Watch Clank | `STD-EPI-001`, `STD-EVT-002` | `E3` support justified. |
| Discovery pointers and search leads are not claim evidence. | Story Clank, Watch Clank, OEM Radar source boundary | `STD-EPI-002`, `STD-SRC-001` | `E3` support justified. |
| Identity, region, source, and product scope must fail closed. | Story Clank, Watch Clank, Tablet Clank incident | `STD-SCP-001`, `STD-IDN-001`, `STD-COV-002` | `E3` support justified. |
| Observations, classifications, events, reviews, and delivery are distinct layers. | Story Clank, Watch Clank, OEM Radar | `STD-EVT-001`, `STD-EVI-002`, `STD-CLS-001` | `E3` support justified. |
| Blocked/empty/failed outcomes must remain visible and distinguishable. | Story Clank, Watch Clank, Tablet Clank diagnostic | `STD-SRC-002`, `STD-COV-001`, `STD-HLT-001` | `E3` support justified. |
| Run invocation, source health, and downstream materialization need provenance. | Story Clank, Watch Clank, OEM Radar, Tablet Clank diagnostic | `STD-PRO-001`, `STD-RUN-001`, `STD-RUN-002`, `STD-HLT-001` | `E3` support justified. |
| Delivery needs durable state separate from event truth. | Watch Clank, OEM Radar, Diagnostic missing-delivery accounting | `STD-DEL-001`, `STD-DEL-002` | `E3` support for the need; Watch does not yet conform fully. |
| Incident learning should become regression/conformance evidence. | Story Clank reports, Watch failure corpus, Diagnostic handoff | `STD-DIA-001` | `E3` support for the process; full ledger still missing. |

The pass answers the central question for the strongest rules: these are not
merely Story Intelligence lessons. It does **not** answer it for every
proposal-derived delivery, GUI, soak, lifecycle, and migration detail.

## 4. Watch Clank rule-by-rule audit

| Rule | Result | Evidence | Gap / interpretation |
|---|---|---|---|
| `STD-EPI-001` | PASS | Watch explicitly states `FIRST_SEEN_BY_CLANK != NEW_REFERENCE`; event semantics and Timex/Casio freshness incidents enforce it. | Applies cleanly. |
| `STD-EPI-002` | PASS | Watch separates product observations, ReleaseLeads, SpecialistLeads, and official Events; Story Clank has the same lead/evidence boundary. | Applies cleanly. |
| `STD-EPI-003` | WARN | Watch has `PipelineLedger`, run outcomes, QC dispositions, and explicit source statuses. | Hostile audit still records silent/ambiguous paths and uncoupled enrichment outcomes; no fleet-wide proof of zero silent loss. |
| `STD-SCP-001` | PASS | Watch source/region map, Citizen UK `UK_PENDING` strategy, Casio/Seiko regional constraints, and Tablet source-capability diagnosis all fail closed. | Known blind spots are declared rather than relabeled as coverage. |
| `STD-PRO-001` | PASS | Watch retains `SnapshotFetch`, `SourceObservation`, `CollectorRun`, `PipelineLedger`, region, parser warnings, epoch, and baseline status. | Documentation is strong; live DB snapshot was empty here. |
| `STD-EVI-001` | WARN | Watch separates score, freshness, yield, QC, and novelty context in places. | No complete independent evidence/editorial/novelty/coverage confidence model is exposed. |
| `STD-EVI-002` | PASS | Watch contract explicitly distinguishes Event, SourceObservation, Watch, and EventReview; corrections preserve history. | Applies cleanly. |
| `STD-IDN-001` | WARN | Watch uses conservative reference normalization, URL/slug evidence, and explicit JDM suffix handling. | `TW4B20700`/`TW4B207009J` duplicate identity remains a documented live limitation. |
| `STD-EVT-001` | PASS | Watch model and brief separate observation, lead, Event, and review layers; OEM Radar separately models listing/product/change event. | Applies cleanly. |
| `STD-EVT-002` | PASS | Watch event semantics distinguish discovery, publication, lastmod, availability, baseline, and freshness; future timestamps are rejected/downgraded. | Applies cleanly. |
| `STD-CLS-001` | PASS | Watch uses acquisition and yield states, EventReview dispositions, lead states, baseline/freshness states, and explicit blocked/zero/unknown outcomes. | Full candidate-level accounting should be proven from a non-empty run ledger in a future audit. |
| `STD-FIN-001` | WARN | Watch has schema checks, transaction boundaries, migration checks, and Story Clank provides canonical graph validation. | No Watch-specific end-to-end conformance check proves every cross-layer reference is validated before publication. |
| `STD-FIN-002` | WARN | Watch makes Event/notification gates explicit and has run output counters. | The exact `FOUND`-requires-structured-output contract is not a Watch-native concept and is not universally machine-checked. |
| `STD-NEG-001` | PASS | Watch reports `UNKNOWN`, `BLOCKED`, `REGION_COVERAGE_GAP`, `NOT VERIFIED`, and “not guessed” outcomes; Diagnostic records missing evidence and first failed gate. | Applies cleanly; broad negative claims remain prohibited. |
| `STD-SRC-001` | PASS | Watch source matrix declares official/news/specialist layers, authority tiers, freshness, and Event permissions; specialist leads do not mint official Events. | Applies cleanly. |
| `STD-SRC-002` | PASS | Casio Akamai/Cloudflare denial, blocked/backoff states, failed fetch early return, and health tests keep invalid responses out of observations. | Applies cleanly. |
| `STD-SRC-003` | WARN | Watch has source matrix, regional gap map, source inventory, and explicit Citizen UK omission. | The declared universe still has structural gaps; this is a coverage warning, not a declaration failure. |
| `STD-SRC-004` | PASS | Watch source registry and source-specific classes distinguish OEM, regional, retailer, newsroom, and specialist surfaces. | Applies cleanly for current registered sources. |
| `STD-COV-001` | PASS | Watch distinguishes `SUCCESS`, `ZERO_ITEMS`, `BLOCKED`, `BACKED_OFF`, `FAILED`, `NEVER_RUN`, and separate acquisition/yield health. | Coverage/result state is visible and not inferred solely from output cardinality. |
| `STD-COV-002` | PASS | Watch forbids Notebookcheck as production discovery, keeps specialists as leads, and requires region-correct evidence for regional claims. | Applies cleanly. |
| `STD-RES-001` | NOT_APPLICABLE | Watch is primarily a scheduled collector, not a request-driven research dossier system. | Re-audit against a research Clank profile. |
| `STD-RES-002` | NOT_APPLICABLE | Watch source expansion is planned and staged, but it has no bounded web-research task lane equivalent to Story Clank. | Source-universe rules are covered by `STD-SRC-003`. |
| `STD-RUN-001` | PASS | Watch `CollectorRun` records invocation/outcome facts; soak contract requires fetch, parse, observed, persisted, event, QC, and error accounting. | Live values were documented but not re-read from the empty local DB. |
| `STD-RUN-002` | PASS | Watch treats baseline-silent and `ZERO_ITEMS` runs as explicit operational states, not missing rows. | Applies cleanly. |
| `STD-HLT-001` | WARN | Watch separates scheduler, collector, source component, acquisition, yield, event, QC, and delivery concerns. | Hostile audit documents fragmented scheduler authority and no alert if DB writing stops; independence is incomplete operationally. |
| `STD-BAS-001` | WARN | Watch has Epoch 1, force-baseline, source-scoped baseline, expansion/soak/promotion contracts, and explicit migration history. | Epoch creation is not automated; future-source onboarding still depends on operator memory. |
| `STD-HIS-001` | WARN | Watch preserves handoffs, migrations, raw snapshots, event reviews, and forensic history; OEM Radar preserves raw snapshots for replay. | No end-to-end Watch proof covers all identity, dedupe, health, feedback, and delivery state across a rewrite. |
| `STD-DEL-001` | FAIL | Watch sends directly through `DiscordNotifier._post`; notification state is documented as scattered (`Event.extra.alerted`, lead timestamps, config). OEM Radar has the desired outbox pattern. | Watch lacks the candidate outbox/attempt/ack workflow. This is a conformance failure, not a remediation request in this pass. |
| `STD-DEL-002` | WARN | Watch catches Discord failures so they do not mutate event truth, and the silent-period audit distinguishes generated events from eligible delivery. | Delivery state is not as durable/independent as the candidate rule requires. |
| `STD-DEL-003` | WARN | Timex/Citizen flood autopsies, burst context, QC tiers, and queue denominator rules make signal overload visible. | Burst annotation runs after inline sends; no complete signal-budget control exists. |
| `STD-GUI-001` | WARN | Watch exposes dashboard, runs, diagnostics, operations, intelligence, evidence, scheduler, and QC surfaces. | No shared Standards/Exceptions surface or cross-Clank vocabulary contract is yet implemented. |
| `STD-GUI-002` | PASS | Watch visibly renders blocked, warning, failed, zero, stale, unknown, degraded, and experimental states; webhook URLs are hidden. | Applies cleanly to current documented UI. |
| `STD-SOK-001` | WARN | Watch has a ten-item promotion gate, minimum four successful scheduled runs, QC yield, traversal progress, restart/health checks, and no-manual-surgery criteria. | The local empty DB prevents verifying a completed live soak record in this audit. |
| `STD-LIF-001` | PASS | Watch separates experimental maturity from acquisition/yield health and uses production-ready/promotion decisions alongside blocked/degraded/dormant states. | Applies cleanly. |
| `STD-DIA-001` | WARN | Watch’s failure corpus explicitly maps Diagnostic lessons to regression tests; Diagnostic’s Honor report records first failed gate and no-fix-before-reconstruction. | There is no live Standards revision/exception record linking an incident to a versioned universal rule yet. |
| `STD-SEC-001` | PASS | Watch has secret-safe notifier behavior, hidden webhook configuration, loopback dashboard controls, deployment prohibitions, and a gitleaks contract. | Applies cleanly for inspected surfaces. |
| `STD-STD-001` | WARN | Watch has versioned laws/contracts, Story Clank has schema versions, and OEM Radar has ADR/milestone records. | A shared rule registry, exception owner/expiry, and reproducible Standards version are not yet present. |
| `STD-STD-002` | PASS | Watch’s generic collector-family work and OEM Radar’s engine/provider protocols demonstrate contract-level reuse without prescribing one stack. | Applies cleanly. |

### Outcome summary

| Outcome | Count |
|---|---:|
| `PASS` | 20 |
| `WARN` | 15 |
| `FAIL` | 1 |
| `NOT_APPLICABLE` | 2 |
| `UNKNOWN` | 0 |
| `EXEMPT` | 0 |

The single concrete failure is `STD-DEL-001`: Watch’s delivery path is direct
send plus scattered state rather than a durable outbox/attempt/ack workflow.
This report does not remediate it.

## 5. What this audit proves

- The strongest epistemic, identity, provenance, source, coverage, and health
  rules generalize beyond Story Clank; they have `E3` support.
- Watch is a useful first patient because it contains real success paths,
  failure autopsies, source/region gaps, baseline/epoch history, QC, UI, and
  delivery behavior.
- Watch already embodies many candidate rules, especially observation/event
  separation, freshness, source typing, bounded failure states, run
  accounting, and operator-visible ugly states.
- OEM Radar demonstrates that the outbox rule is implementable without making
  it a stack mandate.

## 6. What this audit does not prove

- It does not prove fleet-wide `E4` support.
- It does not prove that Watch’s documented production counts are current in
  the local environment; the local Watch DB is empty.
- It does not establish full conformance for delivery, scheduler authority,
  migration preservation, soak completion, GUI standards, or exception
  governance.
- It does not justify freezing `STANDARD_V0.1`.

## 7. No-remediation statement

No Watch Clank or Story Clank source, database, deployment, scheduler,
notification path, or artifact was changed during this audit. The only writes
were this report and the candidate-baseline metadata in the current workspace.
No failing rule was patched, hidden, downgraded, or re-audited after a fix.

## 8. Ratification handoff

Before freezing `STANDARD_V0.1`:

1. restore/import the full Diagnostic Clank incident and lesson ledger, with
   its historical hashes and supersession state;
2. obtain Motherclank/fleet evidence, including the named BANKAI, KTW,
   migration, restore, scheduler, and notification histories;
3. review the 38-rule support matrix with Clank owners, especially the 28
   `E3` rules and the proposal-derived rules that have not reached `E3`;
4. preserve this Watch audit as the first no-remediation scorecard;
5. run a second independent Clank audit using the same rule IDs and evidence
   schema;
6. test one real incident through the complete learning loop, including a
   machine-checkable conformance result, without rewriting its historical
   verdict.

Recommendation: **keep the candidate baseline, do not freeze the normative
standard, and do not begin Standards Clank implementation yet.**
