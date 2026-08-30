# Event / Delivery Implementation Map

**Acquisition:** `CVC-EVENT-DELIVERY-001`  
**Purpose:** derived operator map for the two scoped rules. It is not an additional independent evidence source.

## Per-system flow

| System/profile | Source observation | Normalized / classified state | Event | Delivery / outbox | Attempt | Delivery state |
|---|---|---|---|---|---|---|
| Story Clank | Admitted source `Evidence` / source observation | Fact status, entity relation, task status, unresolved state | Qualified `Event` / `TimelineEntry` derived from facts | Not implemented in this research profile | Not applicable | Not applicable |
| Watch Clank | `SourceObservation` / product observation | ReleaseLead, SpecialistLead, EventReview disposition, baseline/freshness state | Official `Event` / change record | Direct Discord notifier; no durable outbox | Direct send through notifier | Scattered indicators; failure is caught, but no durable pending/sent/failed ledger |
| OEM Radar | Listing, raw payload, immutable snapshot | Canonical product, validation/resolution, baseline or change classification | Durable `change_events` record | Durable notification/outbox linked by event ID | Deduplicated attempts with transport result | `pending` / `sent` / `failed` |
| KTW | Research/source observation | Publication/profile policy state | No delivery-enabled event path in this profile | Not applicable by policy | Not applicable | Not applicable |
| Smartwatch / Feature Phone / Tablet | Preserved fleet summaries and incidents only | Capability or incident states where recorded | No accessible independent event-layer implementation replay in this pass | No accessible independent delivery trace | Not available | Unverified |

## Event truth versus delivery truth

```text
OEM:
source listing/snapshot
        ↓
product + validation/classification
        ↓
change_event (event truth)
        ↓ event_id
notification/outbox (delivery work)
        ↓
attempt + transport result
        ↓
pending / sent / failed (delivery truth)
```

The OEM path preserves event and delivery records separately. Historical baseline/cutover evidence records zero events, zero pending, and zero sent as distinct outcomes. The notification-noise and replay records retain filtering, review queue, and delivered counts without allowing transport output to create unsupported event truth.

```text
Watch:
source observation
        ↓
lead / EventReview
        ↓
Event
        ↓
direct notifier attempt
        ↓
scattered delivery indicators or caught failure
```

Watch demonstrates protective behavior—send failure does not mutate Event truth—but does not provide the durable outbox/attempt/ack state required by the candidate invariant.

```text
Story:
source Evidence
        ↓
fact / classification
        ↓
Event / TimelineEntry
        ↓
delivery not applicable to research profile
```

Story’s offline tests prove that metadata, unrelated nested dates, missing dates, and broken graph references do not become unsupported events. They do not provide delivery evidence.

## Failure and success map

| Rule | Failure / boundary | Successful behavior | What remains unproven |
|---|---|---|---|
| `STD-EVT-001` | OEM first-crawl baseline entities produced false novelty alerts; source presence was collapsed into event/alert truth | Story, Watch, and OEM expose separate observation/classification/event layers; baseline migration remains event-silent | A second independent non-OEM collector replay with durable IDs and a post-restart page-presence negative |
| `STD-DEL-002` | Watch has direct send/scattered state; OEM history contains notification noise and a dual-host queued-delivery incident | OEM persists event before outbox, links delivery by event ID, and records delivery outcomes separately; Watch catches send failures without mutating events | A second independent delivery-enabled implementation with injected failure, immutable event, durable attempt/ack lineage, and second-read proof |

## Independence map

* Story, Watch, and OEM are treated as separate implementation families for event-layer evidence.
* OEM’s baseline, cutover, noise, Diagnostic, and replay records share OEM ancestry and are not counted as separate delivery implementations.
* KTW is an independent profile but delivery is explicitly unsupported by policy, so it cannot satisfy the delivery implementation requirement.
* Motherclank capability, Golden Incident Corpus, and fleet archaeology records are derived navigation/conformance context only.

## Replay status

* Story: `REPRODUCIBLE` for the selected offline event tests; delivery `NOT_APPLICABLE`.
* Watch: `UNVERIFIED` for restart durability; direct-send failure behavior is preserved by the frozen audit.
* OEM: `PARTIALLY_REPRODUCIBLE`; frozen reports preserve implementation and historical replay claims, but raw repository/test/row artifacts are unavailable.
* KTW: `NOT_APPLICABLE` for delivery by policy.

