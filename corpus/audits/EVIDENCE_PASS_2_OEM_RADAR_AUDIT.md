# Standards Baseline Evidence Pass 2 — OEM Radar Conformance Audit

Status: second independent audit complete; `STANDARD_V0.1` is **not frozen**.

Date: 2026-08-30

Audit mode: read-only, no remediation.

Audit patient: OEM Radar, a boutique-PC OEM collector with a stateless
one-shot runtime, source/platform engines, normalized product identity,
SQLite snapshots, semantic diffs, and Discord delivery.

This is a separate scorecard from [Audit Patient #1 — Watch Clank](./EVIDENCE_PASS_1_WATCH_CLANK_AUDIT.md). The Watch scorecard was not edited,
re-scored, or improved during this audit and remains frozen historical
evidence of the 2026-08-30 assessment.

## 1. Audit question and method

The audit reused, without rewriting:

- all 38 rule IDs in [BASELINE_V0.1.md](./BASELINE_V0.1.md);
- the same normative levels, maturity labels, applicability labels, and
  `E0`–`E4` support-grade vocabulary;
- the same per-rule outcomes: `PASS`, `FAIL`, `WARN`, `NOT_APPLICABLE`,
  `UNKNOWN`, and `EXEMPT`;
- the same evidence boundary: contracts and documentation are not silently
  promoted to production evidence.

The audit examined OEM Radar documentation, implementation, configuration,
tests, and the available local runtime state. The test suite was run once;
no source, database, configuration, deployment, or notification remediation
was performed.

The governing learning loop remains:

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

## 2. Evidence boundary and integrity

### OEM Radar evidence available

The audited repository was:

`C:\Users\anil\Documents\oem_radar-full\oem_radar`

Evidence included:

- `docs/ARCHITECTURE.md`: ADRs, pipeline boundaries, source/engine/provider
  separation, error philosophy, and run telemetry;
- `docs/DATABASE.md`: normalized entity model, immutable snapshots, raw
  references, migration semantics, outbox schema, and crawler-run schema;
- `docs/DIFF_ENGINE.md`: semantic event taxonomy, identity-resolution
  boundary, deterministic diffing, and rule-driven severity;
- `docs/HANDOFF.md` and `README.md`: operational state, source coverage,
  baseline-quiet behavior, dashboard status, and known gaps;
- implementation in `src/`, including the injected fetcher, Shopify engine,
  normalized model, pipeline, SQLite provider, Discord provider, CLI, and
  dashboard;
- configuration descriptors for GMKtec, Minisforum, Beelink, AOOSTAR, and
  disabled/unverified sources;
- the 61-test offline suite, including fetch, engine, storage, migration,
  pipeline, diff, runner, and Discord outbox tests.

### Evidence limits

This repository copy has no `data/` runtime database and no Git metadata.
There was therefore no live product/event/run/outbox corpus and no commit
identity to inspect. The audit uses content hashes and the source snapshot
itself, not a claim of current production state. No live crawl, source probe,
or Discord webhook send was performed.

`python -m pytest -q` completed with **61 passed**. Pytest emitted one
environment warning because it could not create `.pytest_cache` under the
external repository; this is a runner/filesystem issue, not a product or
investigation failure.

The repository's own handoff warns that `start-radar.cmd` contains a literal
Discord webhook assignment. A non-secret pattern check confirmed that the
file contains a Discord webhook URL and a literal webhook assignment. The
secret value is intentionally not reproduced in this report.

### Primary input hashes

| Input | SHA-256 |
|---|---|
| OEM Radar `docs/ARCHITECTURE.md` | `69ACBE84E0FB245B9D19E9D7A8CA3A94027731A31D3482D494DF5AB2E4CFDE90` |
| OEM Radar `docs/DATABASE.md` | `E08D22467367E1360995C0223457E5E2914C6991A5D7B3ECFA5B45278BAE2ACE` |
| OEM Radar `docs/HANDOFF.md` | `EC4AB8D9718D6A0E5458F94ABD3FEA72FF3DA5A7D7F739A8BE4F90278D1DC220` |
| OEM Radar `docs/DIFF_ENGINE.md` | `147A6F1D1F50929FE034E2665F8A141DE3DF7C1223E8B90F18D39553E26EDC7B` |
| OEM Radar `tests/test_runner.py` | `D0F1CBEC61CE33EF248947F593B1215FD9CCEB5E9DC491E0CBA040F765FB2E6D` |
| OEM Radar `tests/test_sqlite_store.py` | `6C803652C54EFF83F4D353E49B17AD51131AFD2F925AA1B5477F411557C98F9B` |
| OEM Radar `tests/test_discord.py` | `BA1D753386CB7788A3432139B0C65C65DC3A7C7545C3AD2BF050DDCACD7AD69A` |
| OEM Radar `src/oem_radar/core/pipeline.py` | `4873E65E1D594A5DE1AA65E0F86EE511E8A2F9B82F158905F12410CA9612FFA2` |
| OEM Radar `src/oem_radar/core/runner.py` | `CB180977B6ED33EE9372CABF0D7E14644E51F63E6677D4807EA81B2992586C91` |
| OEM Radar `src/oem_radar/providers/sqlite/__init__.py` | `82C0B70AAEECA354E8B6187D57711B76A1BA84FAF9852423A412D9B8083283B9` |
| OEM Radar `src/oem_radar/providers/discord/__init__.py` | `14E2FAA72E8170B70FD317B6A768B67A768706710C8C6EB78DB8C02E239F43E3` |
| OEM Radar `start-radar.cmd` | `57CAD485F0EFEE066DD452C88047155472D33917E6FF21D2504C613027BF4D93` |
| Watch Audit Patient #1 report at audit start | `C62B973F1EF62EDC540D3CCFDFEADB122BDD29E119AB43A4D0F6982A5894B496` |

## 3. Support-grade result

These are OEM Radar's direct evidence contributions to the existing
candidate ledger. They do not replace or silently upgrade the baseline's
cross-Clank support grades. OEM Radar alone cannot produce `E3` or `E4`.

| Support grade | Count | Meaning in this audit |
|---|---:|---|
| `E0` | 3 | The OEM Radar profile does not exercise or support the proposed rule. |
| `E1` | 18 | One direct OEM Radar implementation, configuration, test, or artifact signal. |
| `E2` | 17 | Repeated support within OEM Radar through design plus implementation/tests. |
| `E3` | 0 | No new cross-Clank grade is claimed from this audit alone. |
| `E4` | 0 | No fleet-wide or broadly demonstrated production pattern is established. |

The audit therefore tests portability without pretending that one repository
is fleet evidence.

## 4. Rule-by-rule OEM Radar audit

Maturity and applicability below are the baseline values at audit start. The
audit does not change them.

| ID | Level | Maturity | Applicability | OEM grade | Result | Evidence and portability finding |
|---|---|---|---|---|---|---|
| `STD-EPI-001` | MUST | PROVISIONAL | CORE | E2 | PASS | `ProductRef`, listing/product separation, baseline-quiet first crawl, and detection-time wording keep first observation distinct from a claimed market launch. The rule travels cleanly. |
| `STD-EPI-002` | MUST | PROVISIONAL | CORE | E2 | PASS | Discovery yields pointers; fetch, parse, normalize, validate, and resolution precede downstream snapshots/events. A discovery pointer is not itself a normalized product fact. |
| `STD-EPI-003` | MUST | PROVISIONAL | CORE, COLLECTOR, RESEARCH | E1 | WARN | Per-product exceptions are retained in run error accounting, but there is no durable per-unit terminal/pending state with an explicit stage and reason for every candidate. |
| `STD-SCP-001` | MUST | PROVISIONAL | CORE, SPECIALIST_PROFILE | E2 | WARN | OEM identity, aliases, source IDs, and manufacturer country are explicit, but source-region scope, exclusions, and product-family boundaries are not a first-class declared contract. Coarse model keys can also create review risk. |
| `STD-PRO-001` | MUST | PROVISIONAL | CORE | E2 | WARN | Source URL, source ID, raw payload references, captured times, validation issues, and resolution fields exist. Collector/parser revision and a complete admission/rejection chain are not retained in each material record. |
| `STD-EVI-001` | MUST | CANDIDATE | RESEARCH, SPECIALIST_PROFILE | E0 | WARN | OEM Radar exposes parse confidence, resolution confidence, severity, and known-component state, but not separate evidence, editorial-utility, novelty, and coverage propositions. This is likely profile-dependent. |
| `STD-EVI-002` | MUST | PROVISIONAL | CORE, RESEARCH | E1 | WARN | Validation issues, low-confidence resolution, and event metadata are retained, but supported/inferred/conflicting/unresolved perspectives are not modeled as a complete fact-level vocabulary. |
| `STD-IDN-001` | MUST | PROVISIONAL | CORE, RESEARCH, SPECIALIST_PROFILE | E2 | WARN | The explicit resolve stage, canonical product/listing split, aliases, SKU fields, and rename/duplicate tests demonstrate the rule. The current coarse model-key resolver does not fully implement candidate-link review semantics promised by the ADR. |
| `STD-EVT-001` | MUST | PROVISIONAL | CORE, RESEARCH, COLLECTOR | E2 | PASS | Listings, canonical products, immutable snapshots, change events, and notifications are separate records/layers. The same invariant is expressed in a different domain without rewriting the rule. |
| `STD-EVT-002` | MUST | PROVISIONAL | CORE, RESEARCH, COLLECTOR | E1 | WARN | Detection, first-seen, captured, and vendor `published_at` values are distinct fields, but the collector does not provide a complete event-role model for announcement, release, availability, modification, and discovery dates. |
| `STD-CLS-001` | MUST | PROVISIONAL | CORE, COLLECTOR, RESEARCH | E2 | WARN | Product statuses, source/run statuses, validation issues, notification states, and removal grace exist. A single explicit classification plus reason code for every unit—including blocked, irrelevant, unresolved, and insufficient-evidence cases—is incomplete. |
| `STD-FIN-001` | MUST | PROVISIONAL | CORE | E2 | WARN | Pydantic validation, foreign keys, schema tests, and append-only references protect portions of the graph. There is no finalizer that validates the complete entity/evidence/fact/event/task/coverage/delta graph before publication. |
| `STD-FIN-002` | MUST | PROVISIONAL | CORE, RESEARCH, SPECIALIST_PROFILE | E0 | NOT_APPLICABLE | OEM Radar has no request/task `FOUND` contract or dossier coverage/delta tasks in this collector profile. Re-audit if those surfaces are added. |
| `STD-NEG-001` | MUST | PROVISIONAL | CORE, RESEARCH, SPECIALIST_PROFILE | E1 | WARN | Fetch and run failures are logged, and zero-product runs are represented. OEM Radar does not make bounded research-negative conclusions with query scope, budget, and diagnostic identifiers. |
| `STD-SRC-001` | MUST | PROVISIONAL | CORE, RESEARCH, SPECIALIST_PROFILE | E1 | WARN | YAML source descriptors declare engine and base URL, but no authority-tier/evidentiary-permission registry distinguishes discovery-only, official, retailer, or supplementary sources. |
| `STD-SRC-002` | MUST | PROVISIONAL | CORE, COLLECTOR, RESEARCH | E2 | WARN | HTTP errors, retry exhaustion, 4xx handling, and parser failures do not become snapshots. However, 200 anti-bot, login, placeholder, or JS-only bodies are not classified and persisted as explicit non-admitted source diagnostics. |
| `STD-SRC-003` | SHOULD | PROVISIONAL | SPECIALIST_PROFILE | E1 | WARN | OEM descriptors declare enabled sources, engines, cadence, and some manufacturer scope, but not a versioned region universe, authority tiers, exclusions, or discovery-only surfaces. |
| `STD-SRC-004` | MUST | PROVISIONAL | CORE, SPECIALIST_PROFILE | E1 | FAIL | The system identifies configured OEM/source descriptors, not actual official host ownership and regional/source relationship. It has no conformance path for official-vs-secondary classification based on fetched content. |
| `STD-COV-001` | MUST | PROVISIONAL | SPECIALIST_PROFILE, RESEARCH | E1 | WARN | `crawler_runs` records discovery/fetch/snapshot/event/error counts and baseline quiet preserves first-crawl history. Explicit bounded no-hit, blocked, incomplete, and not-executed coverage states are not a complete result model. |
| `STD-COV-002` | MUST | PROVISIONAL | SPECIALIST_PROFILE, RESEARCH | E1 | WARN | Entity resolution provides manufacturer/model binding for listings, but the coarse resolver and absent specialist relation vocabulary do not prove conservative target-bound coverage for every admitted source item. |
| `STD-RES-001` | MUST | PROVISIONAL | RESEARCH | E0 | NOT_APPLICABLE | OEM Radar is a configured collector, not a compound request-driven research dossier system. |
| `STD-RES-002` | SHOULD | PROVISIONAL | RESEARCH, SPECIALIST_PROFILE | E0 | NOT_APPLICABLE | There is no operator query/search-provider lane with aliases, localized terms, claim-specific stages, or bounded fallback. Source discovery strategy composition is a different profile capability. |
| `STD-RUN-001` | SHOULD | PROVISIONAL | COLLECTOR | E2 | WARN | Immutable-ish per-source `crawler_runs` include start/end, trigger, source, stats, errors, and status. Collector revision, region, parse/classification totals, and delivery totals are not all recorded as required fields. |
| `STD-RUN-002` | SHOULD | PROVISIONAL | COLLECTOR | E2 | PASS | A run row exists for successful zero-output and failed executions; baseline-quiet records history without alerts; missing execution is distinguishable from a completed empty run. |
| `STD-HLT-001` | MUST | PROVISIONAL | CORE, COLLECTOR, DELIVERY | E2 | WARN | Fetch, parse, validation, persistence, event, outbox, and delivery stages have separate code paths and some counters. Scheduler cadence, classification health, persistence health, and delivery acknowledgement are not independently observable end to end. |
| `STD-BAS-001` | SHOULD | PROVISIONAL | COLLECTOR, SPECIALIST_PROFILE | E2 | WARN | Source-scoped baseline quiet, first-run suppression, migration boundaries, and removal grace are implemented. There is no explicit epoch/soak/freeze record that qualifies novelty conclusions. |
| `STD-HIS-001` | SHOULD | PROVISIONAL | CORE, COLLECTOR | E1 | WARN | Content-hash snapshots, raw payload references, append-only history, and numbered migrations support replay. Migration reports do not enumerate all preserved, transformed, lost, and unverifiable identity, event, feedback, and delivery records. |
| `STD-DEL-001` | MUST | PROVISIONAL | DELIVERY | E2 | PASS | OEM Radar has the positive pattern: event record → durable notification outbox → dedup key → attempts → transport result → pending/sent/failed state. `test_discord.py` proves retry across a failed send and no duplicate enqueue. |
| `STD-DEL-002` | MUST | PROVISIONAL | DELIVERY, CORE | E2 | PASS | `change_events` and `notifications` are separate records linked by event ID. Failed delivery leaves event truth intact; a sent notification does not establish product truth. |
| `STD-DEL-003` | SHOULD | PROVISIONAL | DELIVERY | E1 | WARN | Deduplication, minimum severity, suppression, and planned digest behavior exist, but operational volume, rate, flood, and signal-budget health are not measured as a complete workflow. |
| `STD-GUI-001` | SHOULD | CANDIDATE | GUI | E1 | WARN | The dashboard shows overview, events, discovered components, and recent runs. It does not expose the full shared vocabulary of sources, coverage, delivery, feedback, standards, and exceptions. |
| `STD-GUI-002` | MUST | PROVISIONAL | GUI, CORE | E1 | WARN | Empty, failed, missing-webhook, and low-confidence states are rendered in some paths, but blocked, stale, degraded, dormant, unresolved, age, reason, and next-action rendering is not comprehensive. |
| `STD-SOK-001` | SHOULD | PROVISIONAL | COLLECTOR | E1 | WARN | Tests cover mocks, retries, migrations, dedupe, and two-run continuity, but no real-source soak record demonstrates natural execution, restart continuity, source behavior, alert-volume health, and delivery over time. |
| `STD-LIF-001` | SHOULD | PROVISIONAL | CORE, COLLECTOR | E1 | WARN | Baseline, active/removed product states, source status, and suppressed/pending/failed delivery states exist. Lifecycle maturity is not independently represented from operational health and approval evidence. |
| `STD-DIA-001` | MUST | PROVISIONAL | CORE | E1 | WARN | OEM Radar has ADRs, milestone gates, regression tests, and a handoff with explicit gaps. It has no versioned incident → lesson → invariant → conformance record that can feed the Standards baseline. |
| `STD-SEC-001` | MUST | PROVISIONAL | CORE, DELIVERY | E1 | FAIL | Environment-variable guidance exists, but `start-radar.cmd` contains a literal Discord webhook assignment and is part of the repository artifact. This directly violates the candidate secret-handling rule. The value is not reproduced here. |
| `STD-STD-001` | MUST | PROVISIONAL | CORE | E2 | WARN | ADRs, schema versions, milestone records, tests, and handoff dates provide local version history. There is no shared reproducible Standards version, exception owner/expiry, or per-result rule/profile identifier. |
| `STD-STD-002` | MUST | PROVISIONAL | CORE | E2 | PASS | Protocols, source engines, providers, YAML descriptors, and injected fetchers demonstrate implementation-neutral contracts. The audit did not need to reinterpret the rule for Python/SQLite/Shopify. |

## 5. Outcome summary

| Outcome | Count |
|---|---:|
| `PASS` | 7 |
| `WARN` | 26 |
| `FAIL` | 2 |
| `NOT_APPLICABLE` | 3 |
| `UNKNOWN` | 0 |
| `EXEMPT` | 0 |

The two failures are materially different:

1. `STD-SRC-004`: official-source classification is not implemented as an
   observable authority/host-ownership decision.
2. `STD-SEC-001`: a literal Discord webhook is present in the shipped
   `start-radar.cmd` artifact.

Neither failure was patched or re-audited.

## 6. Portability result

### What traveled cleanly

The following invariants retained the same meaning and produced direct
conformance evidence without special pleading:

- observation is not novelty;
- discovery pointers are not evidence;
- observation, product identity, snapshot, event, and delivery layers are
  distinct;
- completed empty runs are not missing runs;
- durable outbox state is separate from event truth;
- implementation-neutral boundaries can be audited from behavior/contracts,
  not stack choices.

### What required profile interpretation

`STD-FIN-002`, `STD-RES-001`, and `STD-RES-002` are not collector-native
concepts. Treating them as `NOT_APPLICABLE` preserved the rule text and
avoided inventing a research dossier interpretation for OEM Radar.

`STD-EVI-001`, `STD-COV-001`, `STD-COV-002`, `STD-GUI-001`, and `STD-SOK-001`
remain meaningful only after collector, specialist, research, and GUI
profiles define the minimum observable surfaces. This supports the requested
separation of normative level, maturity, and applicability.

### What the independent audit exposed

OEM Radar is stronger than Watch on the delivery invariant: its outbox,
deduplication, retry, suppression, and event/notification separation are
implemented and tested. It is weaker or incomplete on source authority
classification, evidence admission for hostile 200 bodies, per-unit terminal
classification, independent health dimensions, full operator vocabulary, and
secret-safe packaging.

No rule text was rewritten during this audit. The baseline language is
portable enough to expose these differences, but not yet mature enough to be
frozen as a universal standard.

## 7. Comparison with Watch Audit Patient #1

| Audit | PASS | WARN | FAIL | NOT_APPLICABLE | UNKNOWN | EXEMPT |
|---|---:|---:|---:|---:|---:|---:|
| Watch Clank — frozen 2026-08-30 scorecard | 20 | 15 | 1 | 2 | 0 | 0 |
| OEM Radar — this audit | 7 | 26 | 2 | 3 | 0 | 0 |

The counts are not a league table. OEM Radar was audited against a smaller
evidence boundary: no live database, no production run corpus, and no real
source crawl. The useful comparison is rule behavior:

- Watch passes more source, coverage, health, and operator-state rules because
  its evidence corpus contains regional incidents, forensic autopsies, soak
  contracts, and production-shaped operational history.
- OEM Radar passes the delivery rules that Watch fails or warns on because
  OEM Radar has a tested durable outbox and retry path.
- Both systems support the epistemic and layer-separation core, which is the
  strongest portability signal so far.
- OEM Radar's two failures are not evidence that the rules overfit; they are
  concrete missing capabilities the same rule language can name without
  rewriting.

## 8. No-remediation statement

No OEM Radar source, database, configuration, deployment, scheduler,
notification artifact, or test fixture was changed. No Watch artifact was
changed. The only intended write was this audit report. The existing Watch
report remains the immutable Audit Patient #1 reference.

## 9. Next evidence sequence

The requested order remains:

1. preserve this OEM Radar result as Audit Patient #2;
2. import the missing fleet evidence: BANKAI/BANKAI II, KTW, migration and
   restore incidents, scheduler authority, notification floods and silent
   delivery, Motherclank, and the complete Diagnostic ledger;
3. run one real incident through the full CVC loop, including a
   machine-checkable conformance result while preserving its original
   historical verdict;
4. only then review maturity and applicability, including whether the
   research, collector, delivery, GUI, and specialist profiles need explicit
   refinements;
5. re-review both frozen patient scorecards before any normative freeze.

Recommendation: **retain the candidate baseline, do not freeze
`STANDARD_V0.1`, and do not begin Standards Clank implementation yet.**
