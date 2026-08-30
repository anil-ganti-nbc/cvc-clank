# E3 Specific Evidence Wishlist V0.1

This is an acquisition plan derived only from the frozen `E4_REVIEW_PASS_1` retained-E3 blockers. It is not newly gathered evidence, does not change any rule grade or maturity, and does not modify the frozen audits, evidence register, learning-loop test, E4 contract, or Pass 1 review.

There are 16 specific requests, one for each `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` rule. The smallest sufficient proof is stated for each item; a cluster may satisfy several requests with one coordinated acquisition package.

## Wishlist

| Rule | Blocking dimension | Specific missing evidence | Best candidate | Minimum sufficient proof | Priority |
|---|---|---|---|---|---|
| `STD-EPI-002` | evidence boundary / profile stability | Complete replayable lead-versus-admitted-evidence benchmark, including BANKAI denominator, scope, fetch/admissibility, and final task state. | OEM Radar / BANKAI-II | Every lead has fetch, admissibility, provenance, target-binding, and final-status fields; replay needs no unavailable artifact. | P1 |
| `STD-EPI-003` | survivability / profile stability | One independent collector with durable per-unit terminal classification and preserved production accounting across scheduler, process, fetch, parse, persist, and evaluate. | KTW or OEM Radar plus Motherclank | End-to-end bundle with stage IDs, terminal/pending reason, restart boundary, and no silent drops. | P0 |
| `STD-PRO-001` | survivability / evidence boundary | Current read-only host bundles for two lanes with revision, instance, datastore, source/run IDs, and decision provenance, paired with a preserved Motherclank batch. | Motherclank plus KTW/OEM/FPC | Two current bundles resolve every field and retain run/decision lineage on repeat inspection. | P0 |
| `STD-EVT-001` | profile stability / survivability | Second independent non-OEM collector with durable observation/classification/event records and a page-presence replay. | Feature Phone or Watch | Observation, classification, event IDs and explicit event criteria; page presence remains non-event after restart/reinspection. | P1 |
| `STD-CLS-001` | profile stability / evidence boundary | Versioned cross-profile taxonomy mapping covering known, baseline, new, duplicate, irrelevant, insufficient, blocked, source-failure, and unresolved. | Diagnostic plus Motherclank | Machine round-trip without collapsing `UNKNOWN` or profile exclusions. | P0 |
| `STD-NEG-001` | evidence boundary / profile stability | Complete bounded-negative case with scope, stages, budget, fetch outcomes, stopping reason, and independent hit audit. | OEM BANKAI-II or Watch Notebookcheck | One replayable benchmark with final bounded-negative wording and all gaps preserved. | P1 |
| `STD-SRC-003` | profile stability / evidence boundary | Machine-readable source/region/family/exclusion manifest tied to a replayable coverage run and discovery-only permissions. | OEM and Watch source matrices | Versioned manifest and run record every in-scope/excluded source and resulting gap. | P1 |
| `STD-RES-002` | profile stability / evidence boundary | Claim-scoped search-plan corpus with aliases, localized terms, stage purpose, provider, stopping reason, admission result, and gaps. | Story runner plus OEM BANKAI | Plan/replay pair yields stable stage/status accounting and distinguishes no-hit, blocked, unadmitted, and unresolved. | P1 |
| `STD-RUN-001` | survivability / profile stability | Cross-profile immutable run-record conformance bundle with identity, times, revision, source/lane, counts, and restart/migration provenance. | KTW plus OEM and Motherclank | Two implementations pass the same minimum fixture through restart or migration without lost counts/lineage. | P0 |
| `STD-RUN-002` | survivability / evidence boundary | Two-lane bundle with explicit empty, blocked, no-work-due, baseline-suppressed, and unknown records. | KTW and OEM | Fixture/live replay has status, reason, run ID, and zero-row accounting; no missing-run ambiguity. | P0 |
| `STD-HLT-001` | survivability / profile stability | Live health-plane trace joining scheduler, process, application, fetch, parse, persistence, evaluation, queue, and delivery. | Motherclank plus Smartphone or Feature Phone | One independent trace shows each plane and prevents upstream success from upgrading downstream failure/unobserved state. | P0 |
| `STD-BAS-001` | survivability / evidence boundary | Row-level restore/epoch evidence and current baseline IDs distinguishing restore, new epoch, and suppression after host restoration. | Smartwatch/FPC plus Motherclank | Exact hash, epoch, gap, baseline flag, suppression count, and no-novelty result reconcile. | P0 |
| `STD-HIS-001` | survivability / evidence boundary | Row-level second-lane restore/migration record preserving identity, observations, events, health, dedupe, feedback, outbox, and explicit losses. | Smartwatch/FPC plus Motherclank | Offline restore proof reconciles preserved/lost rows and retains original lineage. | P0 |
| `STD-DEL-002` | survivability / profile stability | Independent delivery-enabled Clank with durable event/outbox/attempt/ack trace under injected delivery failure. | Feature Phone or Smartphone | Event remains immutable while failure lineage is recorded and a second read confirms unchanged truth. | P1 |
| `STD-LIF-001` | survivability / profile stability | Live profile-transition matrix retaining health, capability, continuity, and soak independently across restart/restore. | Motherclank plus KTW or Smartwatch | Same lane can be production plus degraded or capability-limited plus continuous without state collapse. | P1 |
| `STD-DIA-001` | evidence boundary / profile stability | Complete raw Diagnostic ledger plus one additional independent incident through verdict, lesson, invariant, conformance, and proposal-only revision. | Diagnostic plus Motherclank | Original verdict retained by hash; second loop is executable, linked, proposal-only, and non-rewriting. | P0 |

## Acquisition clusters

### `DIAGNOSTIC_LEDGER_AND_LEARNING`

Rules: `STD-EPI-003`, `STD-CLS-001`, `STD-DIA-001`.

Package: complete raw Diagnostic ledger, its provenance/index boundary, and one additional real incident using the existing learning-loop contract. This package addresses terminal-accounting history, taxonomy/profile mapping, and repeatable historical learning without rewriting the original verdict.

### `MOTHERCLANK_HOST_CONTINUITY`

Rules: `STD-EPI-003`, `STD-PRO-001`, `STD-RUN-001`, `STD-RUN-002`, `STD-HLT-001`, `STD-BAS-001`, `STD-HIS-001`, `STD-LIF-001`.

Package: current read-only host/variable bundles, row-level restore and epoch records, and live run/health/lifecycle traces. The package is intentionally one continuity acquisition because the frozen blockers repeatedly identify missing host-level and row-level Motherclank evidence.

### `RESEARCH_SCOPE_AND_REPLAY`

Rules: `STD-EPI-002`, `STD-NEG-001`, `STD-SRC-003`, `STD-RES-002`.

Package: one complete research benchmark plus normalized scope, source, alias, staged-plan, admissibility, budget, and bounded-negative replay artifacts. The package targets the frozen BANKAI, Notebookcheck, source-scope, and common-plan-schema blockers.

### `SECOND_EVENT_DELIVERY_IMPLEMENTATION`

Rules: `STD-EVT-001`, `STD-DEL-002`.

Package: one independent non-OEM event/delivery implementation with durable observation-to-event and event-to-outbox/ack traces, including injected failure behavior. This directly addresses the frozen review’s lack of a second live implementation for these separations.

No GUI or second-scoring package is added because no GUI rule or second-scoring rule is in the 16-rule retained-E3 set for this pass.

## Provenance boundary

The blocking references for each JSONL record are the exact `blocking_evidence` values from `standards/E4_REVIEW_PASS_1.jsonl`. The wishlist is therefore a planning artifact, not an evidence acquisition result.
