# CVC Targeted Evidence Acquisition #4

## Second event / delivery implementation — acquisition report

**Acquisition ID:** `CVC-EVENT-DELIVERY-001`  
**Review date:** 2026-08-30  
**Status:** `CLOSED / RETAIN_E3_NO_GRADE_CHANGE`

## Executive result

This pass audited only `STD-EVT-001` and `STD-DEL-002`, using the frozen fleet corpus, frozen Patient #1 and Patient #2 audits, directly linked normalized records, Story implementation/tests, and previously frozen packages. No external provider was contacted, no live Discord send was attempted, no Clank was remediated, and no support grade was changed.

The corpus establishes a strong portable pattern for observation/classification/event separation. Story, Watch, and OEM express separately addressable layers, and preserved incidents show the cost of collapsing them. The corpus also establishes that delivery truth can be separate from event truth in OEM and that Watch send failure does not mutate event truth. However, durable event/outbox/attempt/ack separation remains concentrated in OEM. The exact second-independent-implementation proof for delivery is missing, and the exact replay proof for a non-OEM collector is missing.

**Recommendation for both rules:** `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE`.

## Scope and corpus boundary

The acquisition was additive and offline. It used the frozen Watch and OEM audits, the frozen fleet evidence register, the frozen E4 contract and wishlist, Diagnostic-linked records already in the register, Motherclank-derived indexes only for navigation, Story source and tests in the workspace, and the prior frozen acquisition packages. No new source or transport was contacted.

Raw Watch/OEM repositories and the referenced OEM `test_discord.py` artifact are not available in this workspace. The evidence package therefore preserves the claims and hashes recorded by the frozen audits and register; it does not convert those references into fresh live verification. Missing delivery attempts, acknowledgements, restart reads, database rows, timestamps, or implementation history were not inferred.

## Evidence counts

| Evidence role | Count | Treatment |
|---|---:|---|
| `PRIMARY` | 12 | Direct implementation, incident, replay, or profile-boundary evidence as preserved in the corpus |
| `DERIVED` | 3 | Motherclank/fleet synthesis or capability navigation; not independent implementation evidence |
| `EXECUTABLE_CONFORMANCE` | 1 | Eight selected offline Story tests, all passed |
| `MISSING_EXPECTED_EVIDENCE` | 2 | The exact frozen E3 blockers for the two scoped rules |
| **Total** | **18** | Additive register only |

## Event-layer separation — `STD-EVT-001`

The rule’s core distinction is well supported across materially different architectures:

* Story stores source evidence/observations, fact/classification state, events/timeline entries, and research/finalization links as separate objects. Its tests keep publication metadata, nested unrelated dates, and page presence from becoming unsupported product events.
* Watch separately models `SourceObservation`, leads, `Event`, and `EventReview`. Specialist leads do not mint official Events.
* OEM separately models listings, canonical products, immutable snapshots, change events, and notifications. Its event path follows normalization/validation rather than raw source presence.
* OEM Diagnostic case `DIA-DB-002` preserves a concrete violation: first-crawl baseline entities emitted ordinary novelty alerts and polluted analytics. The recorded repair separates baseline classification from novelty/event authority.
* OEM baseline migration and regional/PSREF runs preserve zero event/notification outcomes for known or baseline material instead of treating source presence as a new event.

The event-layer boundary is therefore independently observable in Story, Watch, and OEM. The missing part is the frozen minimum proof: a second independent non-OEM **collector** replay with durable observation, classification, and event records, explicit event criteria, and a page-presence negative that remains non-event after restart or reinspection. Watch’s local audit database was empty, and no equivalent non-OEM collector replay is accessible.

## Delivery truth versus event truth — `STD-DEL-002`

The positive OEM pattern is explicit:

`change_event` → durable notification/outbox row → deduplication key → attempt → transport result → `pending/sent/failed` state, with notification linked to the event by event ID.

OEM’s historical baseline, cutover, and replay records preserve distinct event, pending, sent, review-queue, and zero-result counts. The notification-noise incident shows why this matters: event candidates, filtering/review, alert population, and delivered output are separate observables. The dual-host Diagnostic case records notifications remaining queued while the non-authoritative NAS had Discord disabled; collection authority and delivery authority were not silently equated.

Watch supplies useful failure-boundary evidence: Discord failures are caught so they do not mutate event truth, and its silent-period audit distinguishes generated events from eligible delivery. But Watch uses a direct-send path with scattered delivery indicators rather than a durable outbox/attempt/ack workflow. This is protective partial separation, not complete durable conformance.

KTW has no alert integration by policy. That is a profile applicability boundary and is not evidence against the invariant. Story has no delivery layer; its absence is also not negative evidence.

The frozen minimum proof remains absent: one independent delivery-enabled Clank other than OEM with an injected delivery failure, immutable event truth, durable outbox/attempt/ack lineage, and a second read observing unchanged event truth.

## Implementation independence

| System/evidence | Independence classification | Counting treatment |
|---|---|---|
| Story Clank | `INDEPENDENT` | Separate research implementation; event-layer evidence only |
| Watch Clank | `INDEPENDENT` | Separate collector implementation; event and partial delivery evidence |
| OEM Radar | `INDEPENDENT` | Separate collector/delivery implementation; strongest positive delivery evidence |
| KTW | `INDEPENDENT` | Separate profile, delivery not applicable by policy |
| OEM Diagnostic cases and OEM replays | `PARTIALLY_SHARED` | Primary historical evidence, but same OEM implementation family; not additional implementations |
| Motherclank GIC/capability/fleet synthesis | `DERIVED_DOCUMENTATION_ONLY` | Navigation and conformance-target context; never counted as implementation evidence |

The package explicitly does not count OEM’s outbox, cutover, baseline, noise, and replay records as independent delivery implementations. It also does not count a report and its summary, a Diagnostic row and CVC normalization, or a derived capability matrix as independent evidence.

## Survivability

| System | Event-layer result | Delivery-layer result | Basis |
|---|---|---|---|
| Story | `UNVERIFIED` across restart | `NOT_APPLICABLE` | Offline tests validate model/finalization boundaries, not persistence across restart |
| Watch | `UNVERIFIED` | `UNVERIFIED` / partial failure protection | Frozen audit records event-preserving send failure, but local DB was empty and delivery state is scattered |
| OEM | `PARTIALLY_SURVIVES` | `PARTIALLY_SURVIVES` | Durable event/outbox design and historical migration/cutover/replay evidence exist; raw second-read failure trace is unavailable |
| KTW | `UNVERIFIED` for this rule | `NOT_APPLICABLE` | Delivery unsupported by policy |

No durability claim was inferred from code structure alone. Process restart, application restart, database reopen, and transport-outage evidence is incomplete outside the preserved OEM historical patterns.

## Executable conformance

Only relevant offline tests available in this workspace were run:

* `test_timeline_task_does_not_promote_publication_metadata_to_event`
* `test_sale_date_becomes_event_but_modified_metadata_does_not`
* `test_explicit_regional_event_keeps_region_and_target_binding`
* `test_event_without_date_is_retained_as_explicitly_unresolved`
* `test_nested_game_release_date_does_not_become_hardware_event`
* `test_chronology_uses_publication_for_explicit_announced_today_only`
* `test_available_now_uses_observed_at_as_explicit_availability_observation`
* `test_final_graph_validator_reports_unknown_references_and_found_without_hits`

Result: **8 passed** using `PYTHONPATH=src`, fixture-only execution, and no provider contact. These tests directly exercise event extraction, target binding, non-event metadata handling, and graph integrity. They do not exercise delivery truth, an outbox, a transport failure, retry, acknowledgement, or restart durability. The frozen OEM audit references `test_discord.py`, but that raw test artifact is unavailable and was not rerun.

## Bidirectional failure/success evidence

### `STD-EVT-001`

Success evidence includes Story’s separate canonical objects and tests, Watch’s observation/lead/Event/EventReview model, and OEM’s listing/product/snapshot/change-event model. Failure evidence includes OEM first-crawl baseline pollution and the historical risk of treating source presence as novelty/event truth. Both directions are present across the corpus.

### `STD-DEL-002`

Success evidence includes OEM durable event/outbox/attempt/status separation, baseline-silent migration, and explicit queue/delivery counts. Failure or boundary evidence includes Watch direct-send/scattered state, OEM notification noise, the dual-host queued-notification incident, and KTW’s policy absence. The failure/success pattern is real, but complete durable separation is not independently implemented beyond OEM in accessible primary evidence.

## E4 review

| Rule | Breadth | Independent implementations | Failure evidence | Success evidence | Observability | Survivability | Reproducibility | Profile stability | Evidence boundary | Recommendation |
|---|---|---|---|---|---|---|---|---|---|---|
| `STD-EVT-001` | PASS | PASS | PASS | PASS | PASS | PARTIAL | PARTIAL | PARTIAL | MATERIAL_OPEN | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |
| `STD-DEL-002` | PASS | PARTIAL | PASS | PASS | PARTIAL | PARTIAL | PARTIAL | PARTIAL | MATERIAL_OPEN | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |

### Exact retained blockers

`STD-EVT-001` frozen blocker:

> A second independent non-OEM collector with durable observation, classification, and event records plus a replay proving that page presence is not promoted to a product event.

Minimum sufficient proof:

> A replay with observation, classification, and event IDs, explicit event criteria, and a negative page-presence case that remains non-event after restart or reinspection.

`STD-DEL-002` frozen blocker:

> One independent delivery-enabled Clank with a durable event/outbox/attempt/ack trace proving that delivery failure cannot mutate event truth.

Minimum sufficient proof:

> An injected delivery failure where the event remains immutable, the outbox/attempt/ack lineage records the failure, and a second read observes unchanged event truth.

## Conclusion and stop conditions

Both rules remain E3. No support-grade overlay is prepared or applied. Ratification Decision #2 is **not justified**.

The frozen baseline, Patient #1 and Patient #2 audits, fleet register, E4 contract, Ratification #1 package, support matrices V0.1/V0.2, Diagnostic Acquisition #1, Motherclank Acquisition #2, and Research Scope Acquisition #3 must remain byte-identical in the final integrity check. This package is additive only.

No further acquisition cluster, remediation, live delivery test, support-grade change, maturity change, rule-text change, or Standards Clank work was started.

