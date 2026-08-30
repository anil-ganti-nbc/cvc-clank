# Standards Baseline v0.1

Status: candidate-rule ledger; not yet the frozen normative specification.

Date: 2026-08-30

Scope: the shared contracts, invariants, and observable behavior expected of
Clanks across the ecosystem.

This baseline was created before Standards Clank implementation. It is a
ledger of candidate rules, not a conformance engine and not permission to
rewrite an existing Clank. Proposed levels are provisional:

- `MUST` means a safety or integrity candidate that should block conformance
  when violated.
- `SHOULD` means a fleet-wide reliability or operator-utility candidate that
  needs profile and deployment context.
- `MAY` means an implementation or presentation choice that should remain
  flexible.

## Evidence boundary

The current workspace contains a detailed Story Clank history from M0 through
M0.6, its contracts, source, regression tests, and frozen validation artifacts.
The local evidence pass also found a Watch Clank repository, its committed
failure corpus, a Watch database snapshot, an OEM Radar repository, and a
Diagnostic Clank database/report bundle. The Diagnostic database copy has
schema v2 but zero normalized incident/report/lesson rows; it contains one
agent-output handoff. Watch's committed failure corpus is therefore treated as
provenance-bearing extracted evidence, not as independently re-queryable raw
incident data. No Motherclank history or full fleet ledger was found locally.

Rules whose only support is the pasted ecosystem proposal are retained as
proposal-derived candidates and are explicitly marked as needing fleet
evidence. No rule is called empirically proven solely because it sounds
architecturally attractive.

Origin and support are separate dimensions. Origin records where a rule came
from (`FAILURE`, `SUCCESS`, `OPERATOR`, `ARCHITECTURE`, or `PROPOSAL`). Support
uses the following evidence scale:

- `E0` — unsupported proposal; no direct system or incident evidence is
  available.
- `E1` — one direct incident, system contract, or reproduced behavior proves a
  need for the rule.
- `E2` — the same lesson is evidenced repeatedly within one Clank.
- `E3` — the same invariant is evidenced across multiple Clanks.
- `E4` — fleet-wide evidence or a demonstrated successful pattern establishes
  the rule broadly.

`E3` and `E4` are intentionally absent from the current local corpus. A rule
must not be promoted to `VERIFIED` merely because it is repeated in Story
Clank.

Maturity is a separate dimension:

- `CANDIDATE` — proposed, but not yet sufficiently evidenced for trial as a
  shared rule.
- `PROVISIONAL` — locally evidenced and suitable for profile/conformance trial,
  but not fleet-verified.
- `VERIFIED` — evidence and successful conformance justify normative adoption.
- `DEPRECATED` — retained for history but no longer active.

Applicability is also separate: `CORE`, `COLLECTOR`, `RESEARCH`, `DELIVERY`,
`GUI`, `SPECIALIST_PROFILE`, or a documented combination. A rule can be
`MUST` within its applicable profile while still being only `CANDIDATE` or
`PROVISIONAL` in maturity.

Primary evidence corpus:

- [Story Clank README](../README.md)
- [M0 contract](../docs/M0_CONTRACT.md)
- [M0 field validation](../field-validation/M0_FIELD_VALIDATION_REPORT.md)
- [M0.1 field validation](../field-validation/M0_1_FIELD_VALIDATION_REPORT.md)
- [M0.2 blind validation](../field-validation/M0_2_BLIND_VALIDATION_REPORT.md)
- [M0.3 semantic binding validation](../field-validation/M0_3_SEMANTIC_BINDING_REPORT.md)
- [M0.5 entity-safe fact graph validation](../field-validation/M0_5_ENTITY_SAFE_FACT_GRAPH_REPORT.md)
- [M0.6 finalization validation](../field-validation/blind-m06/20260830T025123Z/M0_6_FINALIZATION_INTEGRITY_REPORT.md)
- [M0 regression suite](../tests/test_m0.py), [M0.1 regression suite](../tests/test_m01.py), [M0.2 regression suite](../tests/test_m02.py), [M0.3 regression suite](../tests/test_m03.py), [M0.4 regression suite](../tests/test_m04.py), [M0.5 regression suite](../tests/test_m05.py), and [M0.6 regression suite](../tests/test_m06.py)

## Candidate rule ledger

### Epistemic safety and evidence

| ID | Proposed level | Candidate rule | Origin / grade | Evidence or trigger | Observable conformance | Disposition |
|---|---|---|---|---|---|---|
| `STD-EPI-001` | MUST | A first observation by a Clank is not proof of novelty. Publication, modification, fetch, discovery, sitemap, and similar metadata cannot become product events without event evidence. | Architectural invariant + repeated field failures / `E1`, `A` | M0 old-product/updated-page case; M0.2 metadata dates; M0.3 and M0.6 metadata-event gates; `test_m03.py`, `test_m06.py` | Date roles are explicit; novelty is unresolved or supported by event evidence; metadata-only events are rejected. | Retain as core candidate |
| `STD-EPI-002` | MUST | A search lead is a research pointer, not evidence. A URL, title, snippet, sitemap entry, or feed item must pass fetch, admissibility, provenance, and target-binding checks before supporting a claim. | Repeated field failure and current contract / `E1`, `A` | M0 anti-bot/error pages and M0.1 lead/evidence separation; `test_m01.py`, `test_m02.py` | Leads and admitted evidence are distinct types/collections; leads cannot close tasks or claims. | Retain as core candidate |
| `STD-EPI-003` | MUST | Every ingested unit must end in an explicit terminal or pending classification with a reason; no candidate may silently disappear between discovery, fetch, parsing, classification, persistence, and evaluation. | Proposal principle, reinforced by M0.2 task-status overclaim / `E1`, `P` | M0.2 broad `FOUND` statuses without usable output; M0.5 extraction rejection diagnostics | Each unit has a terminal/pending state, reason code, and provenance to the stage that made the decision. | Retain as core candidate; cross-Clank evidence pending |
| `STD-SCP-001` | MUST | Scope fails closed. Source, region, entity, product-family, and exclusion scope must be explicit; ambiguous ownership or target binding cannot silently become in-scope. | Proposal principle + repeated wrong-target outcomes / `E1`, `P` | M0.2 Anbernic RG 476H/RG 556 and wrong-source cases; M0.3 binding rules; M0.6 Notebookcheck false relations | The declared scope and exclusions are inspectable; unknown or ambiguous candidates are retained as unresolved/out-of-scope, not accepted by default. | Retain as core candidate |
| `STD-PRO-001` | MUST | Every admitted observation and material conclusion retains provenance sufficient to explain what was observed, when, where, by which collector/parser revision, and why it was admitted or rejected. | Current contract + repeated diagnostics requirement / `E1`, `A` | M0.1 provenance fields; M0.3 evidence relations; M0.5 fact provenance; `models.py` validation | An auditor can follow observation → source → parser/revision → classification → claim/event/task. | Retain as core candidate |
| `STD-EVI-001` | MUST | Evidence confidence, editorial utility, novelty confidence, and coverage confidence are separate propositions. No single score may silently stand in for all four. | Proposal-derived rating rule / `P` | No shared fleet scoring evidence in this repository; separation is consistent with the unresolved/unsupported M0 outcomes | Stored and rendered fields keep these dimensions separate, or the profile explicitly declares which dimensions it does not provide. | Retain as profile candidate; needs fleet evidence |
| `STD-EVI-002` | MUST | Supported, inferred, conflicting, and unresolved perspectives remain distinguishable. Inference cannot be promoted to supported status without direct evidence, and conflicts are retained rather than overwritten. | Current contract + regression coverage / `E1`, `A` | README invariants; M0.1 reasoning perspectives; M0.5 fact conflict resolution; `test_m05.py` | Every material claim/fact has a perspective/status and direct/conflicting evidence references as applicable. | Retain as core candidate |

### Identity, classification, and event integrity

| ID | Proposed level | Candidate rule | Origin / grade | Evidence or trigger | Observable conformance | Disposition |
|---|---|---|---|---|---|---|
| `STD-IDN-001` | MUST | Target identity is not established by a shared manufacturer, category, body mention, or approximate title. Exact model/SKU binding requires evidence; close variants remain separate until relatedness is evidenced. | Repeated blind-batch failures and contract invariant / `E1`, `A` | M0 query-only SKU crash; M0.2 RG 476H/RG 556; M0.5 wrong model/configuration binding; M0.6 mixed-family facts | Identity relation and identity status are explicit; non-direct evidence cannot support target-only facts, events, regions, or novelty. | Retain as core candidate |
| `STD-EVT-001` | MUST | Observation, classification, and event are separate records. An event is a defensible change or editorially relevant fact inferred from one or more observations, not a synonym for “page existed.” | Proposal principle + current schema / `A`, `P` | README/M0 contract model separation; M0.6 safe-but-empty chronology | The schema and audit views expose the three layers and their links; no collector writes events directly from raw presence. | Retain as core candidate; fleet evidence pending |
| `STD-EVT-002` | MUST | Date roles remain distinct. Announcement, release, availability, listing, leak, certification, benchmark, publication, modification, discovery, and fetch dates cannot be substituted for one another. | Repeated dates failures and current contract / `E1`, `A` | M0.1 date-role model; M0.3 modification-date regression; M0.6 chronology audit | Each date has a role, source/evidence basis, entity, region where applicable, and event status; undated events are explicitly unresolved. | Retain as core candidate |
| `STD-CLS-001` | MUST | Classifications have both a machine state and a reason. At minimum, a profile can represent known/baseline, new candidate, verified event, duplicate, irrelevant/out-of-scope, insufficient evidence, blocked, source failure, and unresolved. | Proposal taxonomy + M0 diagnostics / `E1`, `P` | M0.2 task status overclaim; M0.5 rejected candidates; `facts.py`, `models.py` | Every unit has one current classification, reason code, and relevant evidence/diagnostic references. | Retain as core candidate; exact taxonomy remains profile-extensible |
| `STD-FIN-001` | MUST | Finalization must validate the complete graph before publication: entity, evidence, fact, event, task, coverage, and delta references must resolve, and unsafe objects must be dropped or downgraded visibly. | Repeated finalization failures / `E1` | M0.5 three finalization crashes; M0.6 finalization integrity pass; `finalizer.py`, `test_m06.py` | Canonical output round-trips through validation; no dangling references or fallback that hides a product error. | Retain as core candidate |
| `STD-FIN-002` | MUST | A task in `FOUND`/success state must have the structured output required by its task contract. A coverage `FOUND` state requires at least one valid hit; a delta `FOUND` state requires semantically bound two-sided support. | Repeated M0.2–M0.6 failures / `E1` | M0.2 `FOUND` without useful delta; M0.5 empty `FOUND` coverage; M0.6 wrong-candidate deltas; `test_m04.py`, `test_m06.py` | Deterministic finalization checks state/output consistency and refuses or downgrades inconsistent results. | Retain as core candidate |
| `STD-NEG-001` | MUST | Negative conclusions are bounded statements about the executed search scope and budget, never broad claims of absence. They retain the diagnostics that justify the bounded result. | Repeated negative-recall failures / `E1`, `A` | M0 zero-result Notebookcheck cases contradicted by independent hits; M0.1 bounded states; `test_m02.py` | Negative states include scope, queries/stages, provider/fetch outcomes, timestamp, budget, and diagnostic IDs; `UNCLEAR` remains valid when evidence is insufficient. | Retain as core candidate |

### Sources, coverage, and research lanes

| ID | Proposed level | Candidate rule | Origin / grade | Evidence or trigger | Observable conformance | Disposition |
|---|---|---|---|---|---|---|
| `STD-SRC-001` | MUST | Source class, authority/tier, and evidentiary permission are explicit. Discovery-only sources may discover work but cannot independently close a target event or fact. | M0 source-ranking failure and proposal tier model / `E1`, `P` | M0 anti-bot/secondary source mis-ranking; M0.1 actual-source tiering; M0.2 official-domain misclassification | A source inventory declares class/tier and allowed uses; claim finalization checks those permissions. | Retain as core candidate |
| `STD-SRC-002` | MUST | Source admissibility is evaluated before evidence admission. HTTP errors, anti-bot/CAPTCHA/login interstitials, empty/placeholder/JS-only shells, and unsupported content remain diagnostics, not evidence. | Repeated field failures and transport probes / `E1` | M0 blocked/error evidence; M0.1/M0.2 six transport probes; `test_m02.py` | Fetch disposition and body classification are persisted; non-admitted responses cannot support downstream claims. | Retain as core candidate |
| `STD-SRC-003` | SHOULD | A specialist Clank declares its source universe, region universe, product-family/entity scope, authority tiers, supplementary sources, discovery-only surfaces, and exclusions. | Proposal + repeated recall gaps / `E1`, `P` | M0/M0.3/M0.6 official and regional discovery gaps; M0.2 OEM source/region gaps | Coverage declarations are versioned, inspectable, and used to qualify both positive and negative results. | Retain as profile candidate; needs fleet evidence |
| `STD-SRC-004` | MUST | Official-source classification is based on actual host ownership, regional relationship, path/content semantics, and fetched content—not a small static registry or words in a title/body. | Repeated M0.2/M0.3 discovery failures / `E1` | M0.2 0/12 official classification despite official URLs; M0.3 dynamic three-letter manufacturer fix; M0.5 blocked official discovery | The audit can show why a host was classified as official, regional, store, secondary, or discovery-only. | Retain as core candidate |
| `STD-COV-001` | MUST | Coverage result states distinguish hit, bounded no-hit, incomplete/failed search, blocked, and not executed. A coverage `FOUND` result cannot contain zero admissible hits or only unrelated hits. | Repeated Notebookcheck failures / `E1` | M0.5/M0.6 stale/empty `FOUND`; nine wrong Notebookcheck relations in M0.6 | Coverage states are derived from final admissible hits and diagnostics, then cross-checked at finalization. | Retain as core candidate |
| `STD-COV-002` | MUST | Specialist coverage admission requires a target-bound identity relation appropriate to the lane. Manufacturer-only, category-only, unrelated, and ambiguous pages cannot count as valid target coverage. | Repeated Notebookcheck precision failures / `E1` | M0.5 5/18 visibly wrong relations; M0.6 0/9 manual precision; M0.6 direct recall 0/15 | Relations are independently auditable and conservative; direct target coverage is not conflated with loose family context. | Retain as core candidate |
| `STD-RES-001` | MUST | Compound operator requests are decomposed into atomic tasks such as identity, source, event/date, region, predecessor/sibling, delta, technical facts, and negative checks. Each task has its own support contract. | Repeated field failure / `E1` | M0 compound claims produced generic unresolved output; M0.1 atomic tasks; M0.5 comparison activation weakness | Task category, objective, allowed relations, required evidence semantics, diagnostics, and output references are explicit. | Retain as core candidate |
| `STD-RES-002` | SHOULD | Search planning is staged and claim-specific, with aliases, localized terms, official-domain paths, family/sibling terms, and bounded fallback; search quantity is not treated as coverage. | Repeated recall failures / `E1` | M0 exact/compound query failures; M0.1 staged search; M0.6 8/15 target evidence and 0/15 direct Notebookcheck recall | The run records stages, query purposes, providers, stopping reasons, and coverage gaps; profile sets the budget. | Retain as profile candidate |

### Run health, persistence, and epochs

| ID | Proposed level | Candidate rule | Origin / grade | Evidence or trigger | Observable conformance | Disposition |
|---|---|---|---|---|---|---|
| `STD-RUN-001` | SHOULD | Every collector run has an immutable run ID, start/end time, collector revision, source/region identity, fetch/parse outcomes, observed/persisted counts, classification totals, event totals, and delivery totals where delivery exists. | Proposal-derived collector contract / `P` | No scheduler/collector implementation exists in this repository; M0 run metrics demonstrate the need for separate facts | A run record is immutable after completion except for explicitly append-only diagnostics/acknowledgements. | Retain as fleet candidate; requires Diagnostic/Motherclank evidence |
| `STD-RUN-002` | SHOULD | Zero-event and zero-observation runs are first-class records with provenance; “ran successfully and found nothing” is not represented by missing data. | Proposal + negative evidence pattern / `E2`, `P` | M0/M0.6 empty research outcomes; no collector ledger in repository | A successful empty run is distinguishable from not-run, failed, blocked, and incomplete. | Retain as fleet candidate |
| `STD-HLT-001` | MUST | Scheduler health, process/run health, fetch health, parse health, classification health, persistence/materialization health, evaluation health, queue/outbox health, and delivery acknowledgement health are independently observable. | Proposal principle / `P` | No scheduler in Story Clank; proposal cites repeated fleet incidents | Each stage has an explicit state and transition evidence; upstream success cannot imply downstream success. | Retain as core candidate; requires fleet evidence |
| `STD-BAS-001` | SHOULD | Source expansion and soak precede baseline freeze; historical archive and expanded rebaseline precede novelty validation; delivery validation precedes production epoch. | Proposal-derived migration sequence / `P` | No baseline/epoch collector exists in repository | A Clank records its current baseline/epoch, migration step, freeze evidence, and whether novelty conclusions are valid for that epoch. | Retain as fleet candidate |
| `STD-HIS-001` | SHOULD | Collector/schema rewrites preserve entity identity, observations, events, evidence, health history, dedupe state, feedback, and outbox/delivery state, or record an explicit migration loss and exception. | Proposal-derived history rule / `P` | No persistence migration exists in repository | Migration reports enumerate preserved, transformed, lost, and unverifiable records. | Retain as fleet candidate |

### Delivery and operator experience

| ID | Proposed level | Candidate rule | Origin / grade | Evidence or trigger | Observable conformance | Disposition |
|---|---|---|---|---|---|---|
| `STD-DEL-001` | MUST | Notification delivery is an observable workflow: event → outbox record → attempt → transport result → acknowledged delivery state. Attempted enqueue or an HTTP call alone is not delivery. | Proposal-derived, explicitly motivated by notification incidents / `P` | No Discord/outbox implementation in repository | Each notification has an idempotency key, attempts, transport result, acknowledgement state, and retry/dead-letter path. | Retain as fleet candidate; Diagnostic ledger required |
| `STD-DEL-002` | MUST | Delivery truth is independent of event truth. A delivery failure cannot erase or alter the event; a delivered message cannot make an unsupported event true. | Proposal architectural invariant / `P` | No delivery path in repository | Event state and delivery state are separate records and can be audited independently. | Retain as fleet candidate |
| `STD-DEL-003` | SHOULD | Notification volume and signal budget are observable. Flooding, duplicate replay, and low-value alert storms are detectable and actionable. | Proposal-derived / `P` | No notification path in repository; proposal cites notification flood | Per-profile volume, dedupe, rate, and operator-signal health are measured; flood states are visible. | Retain as fleet candidate |
| `STD-GUI-001` | SHOULD | Operator-facing Clanks expose a shared vocabulary for overview/health, runs, candidates/observations, events, sources, coverage, delivery, feedback, and standards/exceptions, with specialist additions allowed. | Proposal-derived / `P` | No GUI in repository | A profile maps its operator surfaces to these concepts or documents why a surface is not applicable. | Retain as fleet candidate |
| `STD-GUI-002` | MUST | Blocked, unknown, failed, stale, degraded, dormant, and unresolved states are first-class and visible; the UI must not present only the happy path. | Proposal + M0 unresolved-state requirement / `A`, `P` | M0.1/M0.3/M0.6 bounded unresolved outputs; no GUI implementation | Ugly states have visible status, reason, age, and next action/exception where applicable. | Retain as core candidate; fleet evidence pending |
| `STD-SOK-001` | SHOULD | Tests passing is not soak completion. Graduation demonstrates natural execution, real source behavior, persistence, dedupe, classification, restart continuity, alert-volume health, and delivery behavior over an appropriate period. | Proposal-derived lifecycle rule / `P` | No daemon/soak implementation in repository | A soak record names duration, profile, inputs, source outcomes, restarts, alerts, failures, and graduation criteria. | Retain as fleet candidate |
| `STD-LIF-001` | SHOULD | Lifecycle and operational health are orthogonal. Experimental/development/soaking/production-ready/production must not replace independent failed, blocked, degraded, dormant, stale, or rework-required states. | Proposal + M0 decision history / `E2`, `P` | Repeated M0 “closed/rework required/do not begin M1” decisions; no lifecycle engine | State dimensions are separately queryable and rendered; transitions retain evidence and approvals. | Retain as fleet candidate |

### Governance, security, and conformance

| ID | Proposed level | Candidate rule | Origin / grade | Evidence or trigger | Observable conformance | Disposition |
|---|---|---|---|---|---|---|
| `STD-DIA-001` | MUST | Standards evolve through a visible learning loop: failure or success → lesson → candidate invariant → evidence across Clanks → standard → machine-checkable conformance. A candidate invariant must not become a universal rule from one local incident alone. | Proposal-derived governance rule, refined by operator direction / `P` | No Diagnostic Clank ledger is present; Story reports already contain failure taxonomies and proposed fixes | A revision links the observation, lesson, candidate invariant, cross-Clank evidence set, normative decision, conformance check, and effective version. | Retain as core governance candidate; blocked on missing ledger |
| `STD-SEC-001` | MUST | Secrets, webhook credentials, and sensitive access material are never logged, committed, or included in evidence artifacts. | Proposal-derived security invariant / `P` | No Discord/secrets implementation in repository | Secret scanning and artifact review prove absence; redaction is tested at source and rendered layers. | Retain as core candidate; needs fleet evidence |
| `STD-STD-001` | MUST | The standard is versioned. Rules, profiles, exceptions, effective dates, and conformance results identify the standard version used; exceptions are explicit, scoped, justified, approved, and reviewable. | Proposal-derived governance contract / `P` | No Standards Clank exists yet | An audit can reproduce which rule/profile/version produced each result and distinguish pass, fail, warn, and exempt. | Retain as core candidate |
| `STD-STD-002` | MUST | Standards govern contracts, invariants, and observable behavior—not language, database, scheduler, framework, or internal implementation choices. | Architectural principle / `A`, `P` | M0 contract explicitly excludes implementation mandates; proposal states this principle | A conformance test uses observable artifacts and behavior; equivalent implementations can conform. | Retain as core candidate |

## Normalized maturity and applicability register

This register makes the three independent axes explicit. The rule table above
is the readable rationale ledger; this table is the normalized baseline view
to carry into a future machine-readable schema.

| ID | Normative level | Maturity | Applicability | Support | Support basis |
|---|---|---|---|---|---|
| `STD-EPI-001` | MUST | PROVISIONAL | CORE | E3 | Story Clank M0–M0.6 plus Watch event laws and incidents independently repeat the boundary. |
| `STD-EPI-002` | MUST | PROVISIONAL | CORE | E3 | Story Clank lead/evidence separation plus Watch specialist-lead and event boundaries. |
| `STD-EPI-003` | MUST | PROVISIONAL | CORE, COLLECTOR, RESEARCH | E3 | Story task/rejection visibility, Watch pipeline/ledger gaps, and Diagnostic missing-stage accounting. |
| `STD-SCP-001` | MUST | PROVISIONAL | CORE, SPECIALIST_PROFILE | E3 | Story wrong-target outcomes, Watch regional/source gaps, and Tablet Clank source-capability miss. |
| `STD-PRO-001` | MUST | PROVISIONAL | CORE | E3 | Story provenance/cross-references and Watch SnapshotFetch/PipelineLedger/run provenance. |
| `STD-EVI-001` | MUST | CANDIDATE | RESEARCH, SPECIALIST_PROFILE | E0 | Pasted proposal only; no local multi-score system exists. |
| `STD-EVI-002` | MUST | PROVISIONAL | CORE, RESEARCH | E3 | Story perspectives/conflicts plus Watch Event/Observation/Review separation and QC states. |
| `STD-IDN-001` | MUST | PROVISIONAL | CORE, RESEARCH, SPECIALIST_PROFILE | E3 | Story binding failures, Watch conservative/JDM identity history, and OEM Radar resolver contract. |
| `STD-EVT-001` | MUST | PROVISIONAL | CORE, RESEARCH, COLLECTOR | E3 | Story schema plus Watch Watch/Observation/Event/Lead model and OEM Radar listing/product split. |
| `STD-EVT-002` | MUST | PROVISIONAL | CORE, RESEARCH, COLLECTOR | E3 | Story date-role tests plus Watch timestamp/event laws and freshness incidents. |
| `STD-CLS-001` | MUST | PROVISIONAL | CORE, COLLECTOR, RESEARCH | E3 | Story task/rejection states, Watch QC/source health states, and Diagnostic first-failed-gate classification. |
| `STD-FIN-001` | MUST | PROVISIONAL | CORE | E2 | M0.5 finalization crashes followed by M0.6 graph-integrity verification. |
| `STD-FIN-002` | MUST | PROVISIONAL | CORE, RESEARCH, SPECIALIST_PROFILE | E2 | Repeated `FOUND`/structured-output inconsistencies across blind batches. |
| `STD-NEG-001` | MUST | PROVISIONAL | CORE, RESEARCH, SPECIALIST_PROFILE | E3 | Story bounded negatives, Watch UNKNOWN/source-gap discipline, and Diagnostic missing-evidence accounting. |
| `STD-SRC-001` | MUST | PROVISIONAL | CORE, RESEARCH, SPECIALIST_PROFILE | E3 | Story source tiers plus Watch specialist-lead boundary and OEM Radar source descriptors. |
| `STD-SRC-002` | MUST | PROVISIONAL | CORE, COLLECTOR, RESEARCH | E3 | Story transport probes, Watch blocked/backoff semantics, and OEM Radar per-source degradation. |
| `STD-SRC-003` | SHOULD | PROVISIONAL | SPECIALIST_PROFILE | E3 | Story source gaps, Watch source/region matrices, and Tablet Clank source-capability miss. |
| `STD-SRC-004` | MUST | PROVISIONAL | CORE, SPECIALIST_PROFILE | E2 | Story official-host classification failures and Watch explicit source registry. |
| `STD-COV-001` | MUST | PROVISIONAL | SPECIALIST_PROFILE, RESEARCH | E3 | Story empty/wrong coverage states and Watch blocked/zero/unknown health semantics. |
| `STD-COV-002` | MUST | PROVISIONAL | SPECIALIST_PROFILE, RESEARCH | E3 | Story Notebookcheck relation failures and Watch specialist leads never becoming official Events. |
| `STD-RES-001` | MUST | PROVISIONAL | RESEARCH | E2 | Story compound-claim failures and atomic-task regression coverage; no equivalent Watch lane. |
| `STD-RES-002` | SHOULD | PROVISIONAL | RESEARCH, SPECIALIST_PROFILE | E3 | Story bounded-search recall, Watch staged source expansion, and Tablet source-capability miss. |
| `STD-RUN-001` | SHOULD | PROVISIONAL | COLLECTOR | E3 | Story run artifacts, Watch `collector_runs`, and OEM Radar `crawler_runs` all expose invocation accounting. |
| `STD-RUN-002` | SHOULD | PROVISIONAL | COLLECTOR | E3 | Story empty investigations, Watch ZERO_ITEMS/baseline runs, and OEM Radar baseline-quiet behavior. |
| `STD-HLT-001` | MUST | PROVISIONAL | CORE, COLLECTOR, DELIVERY | E3 | Story stage diagnostics, Watch scheduler/source/delivery separation, and Diagnostic `OPS_HEALTH_NOT_INTEL_HEALTH`. |
| `STD-BAS-001` | SHOULD | PROVISIONAL | COLLECTOR, SPECIALIST_PROFILE | E3 | Watch epoch/soak/baseline history plus OEM Radar fresh-source baseline behavior. |
| `STD-HIS-001` | SHOULD | PROVISIONAL | CORE, COLLECTOR | E3 | Watch migration/forensic preservation, Story frozen artifacts, and OEM Radar raw snapshot replay design. |
| `STD-DEL-001` | MUST | PROVISIONAL | DELIVERY | E3 | Watch direct-send/scattered delivery state plus OEM Radar outbox/retry/dedup design and tests. |
| `STD-DEL-002` | MUST | PROVISIONAL | DELIVERY, CORE | E3 | Watch silent-period event/delivery distinction plus OEM Radar separate event/notification records. |
| `STD-DEL-003` | SHOULD | PROVISIONAL | DELIVERY | E2 | Watch Timex/Citizen flood incidents and burst/QC telemetry; no second operational corpus. |
| `STD-GUI-001` | SHOULD | CANDIDATE | GUI | E1 | Watch has common operational surfaces; no cross-Clank GUI comparison is available. |
| `STD-GUI-002` | MUST | PROVISIONAL | GUI, CORE | E3 | Watch visible blocked/zero/stale/degraded states plus Story unresolved outputs. |
| `STD-SOK-001` | SHOULD | PROVISIONAL | COLLECTOR | E2 | Watch has a ten-gate soak contract and promotion controls; current local DB cannot verify live completion. |
| `STD-LIF-001` | SHOULD | PROVISIONAL | CORE, COLLECTOR | E2 | Watch maturity/health dimensions plus Story explicit M0 lifecycle decisions. |
| `STD-DIA-001` | MUST | PROVISIONAL | CORE | E3 | Watch failure corpus → tests, Diagnostic handoff → first failed gate, and Story validation → candidate rules. |
| `STD-SEC-001` | MUST | PROVISIONAL | CORE, DELIVERY | E2 | Watch secret-handling tests/docs and OEM Radar secret handling; no independent incident corpus. |
| `STD-STD-001` | MUST | PROVISIONAL | CORE | E3 | Watch FLEET_LAWS/versioned contracts, Story schema versions, and OEM Radar milestone/ADR records. |
| `STD-STD-002` | MUST | PROVISIONAL | CORE | E3 | Story implementation-neutral contract, Watch generic collector families, and OEM Radar protocol/engine boundary. |

## Consolidation and rejected overfit

The following distinctions were deliberately merged into the rules above:

- “Observation is not novelty” and “metadata dates are not events” are one
  epistemic boundary (`STD-EPI-001` plus the date-role detail in
  `STD-EVT-002`).
- “Search leads are not evidence,” “sitemap results are leads,” and “a URL
  discovered is not a supported claim” are one source/evidence boundary
  (`STD-EPI-002`).
- “No silent candidate death,” terminal classifications, and stage-specific
  outcomes are represented by `STD-EPI-003`, `STD-CLS-001`, and
  `STD-HLT-001`, rather than three competing lifecycle specifications.
- Notebookcheck-specific precision rules are generalized into target-bound
  specialist coverage (`STD-COV-001` and `STD-COV-002`); Notebookcheck remains
  a profile, not the ecosystem standard.
- Finalization graph integrity and task `FOUND` support are separate because
  M0.5 exposed dangling graph references while M0.2/M0.6 exposed semantic
  state/output mismatches.

The following were rejected as overfit or deliberately deferred:

- A required SQLite/Postgres/Python/Rust/cron/systemd implementation.
- A required universal sequence with fixed stage names; stage observability is
  required, but profiles may name equivalent stages.
- A universal Notebookcheck adapter or a static official-domain registry.
- A single aggregate “Clank score” or one magic confidence number.
- A requirement that every Clank implement every specialist lane, comparison,
  region, delivery channel, or GUI tab. Applicability and exceptions must be
  explicit instead.
- Novelty verdict optimization before source coverage, evidence integrity, and
  negative-search semantics are stable.

## Freeze blockers for the normative v0.1 specification

This baseline should not be called the frozen standard until:

1. The actual Diagnostic Clank incident ledger and Motherclank/fleet history
   are imported and each proposal-derived rule is traced to incidents,
   successful patterns, operator requirements, or architectural invariants.
2. Duplicate rules are reviewed with Clank owners and profile applicability is
   defined.
3. A machine-readable rule/exception schema is agreed, including rule ID,
   level, evidence origin, version, scope/profile, verification method,
   exception owner, expiry/review date, and remediation guidance.
4. At least one existing Clank is audited against the candidate core rules and
   the audit itself is reviewed.
5. The standard versioning and revision process is tested on one real incident
   without changing the historical verdict retroactively.

Until those blockers are cleared, `BASELINE_V0.1.md` is the source of
candidate rules and evidence links—not an authorization to start M1 or to
implement Standards Clank.

## Governing learning loop

Every future rule proposal should be processed in this order:

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

The arrows are decision gates, not merely documentation steps. A local failure
can justify a local fix before it justifies a fleet rule. Cross-Clank evidence
must establish that the lesson generalizes, or the rule remains a profile rule,
an experiment, or a documented exception. Once standardized, the rule needs a
repeatable conformance check that can produce evidence for `PASS`, `FAIL`,
`WARN`, or `EXEMPT` without relying on an opaque overall score.
