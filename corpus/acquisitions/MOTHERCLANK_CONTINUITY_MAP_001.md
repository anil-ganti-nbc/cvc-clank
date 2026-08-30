# Motherclank Host-Continuity Map 001

This map is a derived navigation aid for CVC Targeted Evidence Acquisition #2. It does not add independent evidence and does not replace the primary records or the exact E3 wishlist blockers.

| Historical state | Loss/change | Restore or migration | Resulting state | What evidence survived |
|---|---|---|---|---|
| Three Clanks had scheduled collection expectations | Log ownership/permissions changed after stash recovery; cron redirects failed before collector execution | No successful collector restore is established by the incident | Scheduler boundary is preserved as a pre-exec/materialization gap, not a collector regression | Historical incident, lesson, provenance hashes, and impact-map references; current host/process/run rows unavailable |
| Smartwatch live volume and history | Volume destroyed | Restored from the 2026-08-18 backup | Restored history retains epoch lineage and a known observation gap; restore is not a new epoch | Incident-level restore lineage and bounded-gap verdict; row-level Motherclank variables unavailable |
| Feature Phone live volume | Total loss with no backup | Fresh database starts `fpc-epoch-2` | New epoch and baseline suppression are explicit; prior epoch is not reconstructed | Historical loss/new-epoch/baseline claim; prior rows and current host verification unavailable |
| ACT-011 Smartwatch recovery point | Recovery boundary tested on disposable storage | SQLite integrity and isolated restore passed | Current restored copy is recoverable; durable redundancy remains open | Integrity/restore drill record and reported counts; permanent off-host durability unavailable |
| ACT-011 Feature Phone epoch-2 recovery point | Prior epoch already irrecoverable | Current epoch isolated restore passed | Current epoch is recoverable; prior epoch remains lost | Recovery drill and epoch boundary; no prior-epoch reconstruction |
| KTW deployed migration contract | Host/runtime migration boundary | SQLite-safe backup, checkpoint comparison, one executor, and due-aware first cycle are required | Contract describes intended state/scheduler continuity | Checked-in procedure and hash; current execution and host authority unavailable |
| Motherclank scheduler observations | Duplicate/stale or incomplete scheduler paths were recorded historically | Registry and attestation design retain expected/fired/started/completed/no-work/unknown boundaries | Historical authority conflicts remain visible; current authority is not asserted | Scheduler batch, registry, decision-ledger references; fresh timer/cron/systemd state unavailable |
| OEM Radar baseline and run-lock operations | Copy/migration and competing-writer boundary exercised | Idempotent baseline replay and cross-container lock reconciliation passed | Known state remains quiet and concurrent writer is refused at the tested boundary | OEM migration/lock reports and hashes; not Motherclank row-level proof or current host authority |

## Boundary

The workspace contains normalized fleet-register records and their provenance hashes, but not the external Motherclank, KTW, or OEM raw artifacts named by those records. Historical facts remain historical. Current host/scheduler authority is `CURRENTLY_UNVERIFIED`; no startup, summary, or prior live verdict is converted into current authority.
