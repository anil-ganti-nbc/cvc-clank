# Fleet evidence ingestion — v0.1

Status: completed archaeology pass; review required. No Clank implementation,
frozen patient audit, or baseline rule text was changed.

## Result

- 41 normalized evidence records were ingested into
  `FLEET_EVIDENCE_REGISTER_V0.1.jsonl`.
- The register covers all 38 candidate rule IDs. It includes BANKAI/BANKAI II,
  KTW migration and reliability history, migration/restore incidents,
  scheduler authority and materialization gaps, notification flood/silent
  delivery evidence, Motherclank closeout/continuity/capability records, and
  the available DiagnosticBench/report-ingestion corpus.
- The support matrix recalculates record counts and primary/derived roles. It
  keeps the existing baseline grades frozen: no rule is promoted to E4.
- 18 rules are marked `APPROACHING_E4` for review, because their invariant has
  repeated cross-Clank evidence or a broad successful pattern. This is a
  review queue, not a maturity change.

## Evidence boundary

The available Diagnostic corpus is not the complete raw Diagnostic incident /
lesson ledger. It is the checked-in DiagnosticBench cases, report-ingestion
expectations, cross-references, and executable conformance material. The
register records this as `DIAG-CORPUS-BOUNDARY`; no missing historical verdict
was invented. Motherclank host `var/` batches are likewise not locally
available for row-level reconciliation, as recorded by the incident impact
map.

Derived closeout summaries, architecture syntheses, corpus indexes, and
capability matrices are linked for traceability but are excluded from the
primary-evidence count. A record can therefore support a rule's provenance
without pretending to be an independent incident.

## Rules approaching E4

`STD-EPI-001`, `STD-EPI-002`, `STD-EPI-003`, `STD-PRO-001`, `STD-EVT-001`,
`STD-CLS-001`, `STD-NEG-001`, `STD-SRC-003`, `STD-RES-002`, `STD-RUN-001`,
`STD-RUN-002`, `STD-HLT-001`, `STD-BAS-001`, `STD-HIS-001`, `STD-DEL-002`,
`STD-LIF-001`, `STD-DIA-001`, and `STD-STD-002`.

These remain E3 in the recalculated matrix. The principal blockers are fresh
host verification, common profile/conformance checks, the complete Diagnostic
ledger, row-level Motherclank artifact confirmation, and (for survivability)
durable off-host redundancy.

## Rules not advanced by this pass

No new fleet evidence is sufficient for `STD-FIN-001`, `STD-FIN-002`,
`STD-RES-001`, `STD-GUI-001`, or `STD-GUI-002`. `STD-EVI-001` now has direct
incident/benchmark evidence but remains E2 because the separate confidence,
utility, novelty, and coverage dimensions are not demonstrated across a
second operational scoring system. `STD-SRC-004` and `STD-SEC-001` retain
frozen OEM Patient #2 challenge findings and are not remediated.

## Learning-loop test

The Smartwatch restore incident was run through the full loop in
`FLEET_LEARNING_LOOP_TEST_V0.1.json`:

`historical incident → preserved verdict → lesson → candidate invariant →
cross-Clank evidence → executable conformance check → baseline revision
proposal`

The targeted Motherclank check passed with `122 passed, 1 warning`. The warning
was a non-product pytest/cache environment warning. The historical verdict was
not rewritten, the candidate revision is proposal-only, and the existing
baseline file remains unchanged.

## Frozen inputs

The two patient audits remain byte-identical:

| Artifact | SHA-256 |
|---|---|
| `standards/BASELINE_V0.1.md` | `F3FBFB0098193120DD3F9ADA83C65EC7952B9A2EB5483C78267CF2A8E170169F` |
| `standards/EVIDENCE_PASS_1_WATCH_CLANK_AUDIT.md` | `C62B973F1EF62EDC540D3CCFDFEADB122BDD29E119AB43A4D0F6982A5894B496` |
| `standards/EVIDENCE_PASS_2_OEM_RADAR_AUDIT.md` | `2341064C2664CDBAEDC56180EFB824EBAF647D0D80E95DB2DA1B7F92F68FC3BA` |

The machine-readable outputs are the JSONL register, support matrix, learning
loop record, and freeze manifest in this directory.

## Decision

This pass produces evidence for review. It does not freeze a normative
standard, change rule maturity, start M1, or authorize remediation of any
Clank finding.
