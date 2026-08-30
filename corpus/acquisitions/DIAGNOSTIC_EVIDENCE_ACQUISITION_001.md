# Targeted Evidence Acquisition 001: Diagnostic Ledger and Learning

Status: `COMPLETED_SCOPED_NO_GRADE_CHANGE`

This pass was limited to `STD-EPI-003`, `STD-CLS-001`, and `STD-DIA-001`. It used the exact frozen wishlist blockers and minimum-proof requirements. It did not change rule text, maturity, applicability, support grades, either support matrix, the fleet register, Ratification #1 artifacts, or any frozen audit.

## Executive result

The available evidence strengthens three narrow conclusions:

- DiagnosticBench preserves primary examples of explicit blocked/zero and scheduler/materialization distinctions.
- Diagnostic report-ingestion expectations preserve raw immutability, duplicate handling, contradiction retention, quarantine, and unresolved state/reason behavior.
- One previously completed Smartwatch learning-loop conformance result demonstrates the full workflow, but it is carried forward only and is not counted as a new independent Diagnostic primary incident.

The acquisition does not resolve the E4 blockers. No complete raw Diagnostic incident/lesson ledger is available in this environment, no complete cross-profile taxonomy mapping is available, no end-to-end per-unit terminal-accounting bundle is available, and no second independent complete learning loop is available.

## Evidence found

| Acquisition record | Role | What it establishes | Limit |
|---|---|---|---|
| `DIA-AQ1-DB-001` | `PRIMARY` | Unexpected zero is blocked/failure-classified; zero semantics are explicit. | Does not provide a complete per-unit stage ledger. |
| `DIA-AQ1-DB-004` | `PRIMARY` | Scheduler first fire is distinct from recurrence/materialization; the original overclaim is retained and partially superseded. | Scheduler boundary evidence is not full terminal accounting. |
| `DIA-AQ1-DB-009` | `PRIMARY` | `blocked_zero_result` is a first-class disposition rather than normal empty success. | One implementation and one failure pattern; no fleet taxonomy mapping. |
| `DIA-AQ1-REPORT-CORPUS` | `PRIMARY` | Raw report immutability, duplicate/contradiction retention, quarantine, and unresolved root-cause behavior are executable expectations. | Contract evidence is not production field-incident confirmation. |
| `DIA-AQ1-SEED-INDEX` | `DERIVED` | Indexes incident/lesson lineage and warns that lessons require originating records and status. | Not independent incidents; does not replace raw rows. |
| `DIA-AQ1-TRACEABILITY` | `DERIVED` | Maps Diagnostic ownership and adapter boundaries. | Architecture traceability is not live conformance. |
| `DIA-AQ1-LEARNING-LOOP-001` | `EXECUTABLE_CONFORMANCE` | One Smartwatch loop passed with preserved verdict and proposal-only revision. | Prior artifact only; not new evidence or an independent Diagnostic primary record. |

## Evidence missing and corpus boundary

The raw Diagnostic Clank repository and owner-supplied ledger paths referenced by the normalized records are not available in this workspace. The available corpus is therefore limited to the normalized rows and their recorded provenance. The pass does not infer missing incidents, lessons, timestamps, confidence, unresolved questions, or supersession state.

The following remain `MISSING_EXPECTED_EVIDENCE`:

- Complete raw Diagnostic incident/lesson ledger, including originating records, timestamps, confidence, dispositions, unresolved questions, and supersession history.
- One end-to-end production run bundle with per-unit terminal or pending disposition across scheduler, process, fetch, parse, persist, and evaluate stages, including explicit no-silent-drop reconciliation.
- A versioned cross-profile state/reason mapping covering the requested state families without collapsing `UNKNOWN` or profile exclusions.
- One additional independent real incident that completes incident → preserved verdict → lesson → candidate invariant → executable conformance → proposal-only revision.

Motherclank evidence was not acquired. Existing Motherclank references remain context only and were not promoted into new acquisition evidence.

## Role counts

| Evidence role | Count |
|---|---:|
| `PRIMARY` | 4 |
| `DERIVED` | 2 |
| `EXECUTABLE_CONFORMANCE` | 1 |
| `MISSING_EXPECTED_EVIDENCE` | 1 |
| Total acquisition records | 8 |

The four primary records are DiagnosticBench/report-corpus lineage records already present in the frozen normalized register. This pass creates an additive scoped view and does not claim a new independent primary corpus beyond that frozen register.

## Rule-specific findings

### `STD-EPI-003`

Frozen requirement: one independently implemented collector with durable per-unit terminal classification and a preserved production run demonstrating no silent candidate loss across scheduler, process, fetch, parse, persist, and evaluate stages.

Found: `DIA-AQ1-DB-001` and `DIA-AQ1-DB-009` preserve explicit blocked/zero failure dispositions. `DIA-AQ1-DB-004` preserves the scheduler first-fire/materialization boundary.

Not established: a complete per-unit terminal/pending accounting bundle, a successful end-to-end no-silent-drop reconciliation, or durable row-level evidence across every named stage. The raw Diagnostic ledger remains unavailable.

Recommendation: `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE`.

### `STD-CLS-001`

Frozen requirement: a versioned cross-profile state/reason mapping and corpus covering known/baseline, new candidate, verified event, duplicate, irrelevant/out-of-scope, insufficient evidence, blocked, source failure, and unresolved outcomes without collapsing profile distinctions.

Found: `DIA-AQ1-DB-001` and `DIA-AQ1-DB-009` show explicit blocked/zero semantics; `DIA-AQ1-REPORT-CORPUS` covers duplicate, contradiction, quarantine, and unresolved root-cause expectations; `DIA-AQ1-SEED-INDEX` and `DIA-AQ1-TRACEABILITY` preserve lineage and ownership context.

Not established: a machine-readable cross-profile mapping, full coverage of every requested state family, or a no-interpretation round-trip preserving `UNKNOWN` and profile-specific exclusions.

Recommendation: `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE`.

### `STD-DIA-001`

Frozen requirement: the complete raw Diagnostic ledger plus one additional independent real incident traversing incident, preserved verdict, lesson, candidate invariant, conformance check, and proposal-only baseline revision.

Found: `DIA-AQ1-REPORT-CORPUS` provides executable report-ingestion expectations; `DIA-AQ1-SEED-INDEX` and `DIA-AQ1-TRACEABILITY` preserve Diagnostic lineage/ownership context; `DIA-AQ1-LEARNING-LOOP-001` carries forward the prior Smartwatch loop, whose conformance result passed and whose historical verdict was preserved.

Not established: the complete raw Diagnostic ledger or a second independent complete learning loop. The Smartwatch loop is not double-counted as a new Diagnostic primary record.

Recommendation: `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE`.

## E4 dimension audit

Statuses below preserve the frozen Pass 1 dimensions and incorporate only the scoped acquisition findings. `N/A` is not used for any newly open dimension in this pass.

| Rule | Breadth | Independence | Failure/success support | Observability | Survivability | Reproducibility | Profile stability | Evidence boundary | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| `STD-EPI-003` | `PASS` carried from Pass 1 | `PASS` carried from Pass 1 | `PASS` carried from Pass 1 | `PASS` | `PARTIAL` | `PARTIAL` | `PARTIAL` | `MATERIAL_OPEN` | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |
| `STD-CLS-001` | `PASS` carried from Pass 1 | `PASS` carried from Pass 1 | `PASS` carried from Pass 1 | `PASS` | `PARTIAL` | `PARTIAL` | `PARTIAL` | `MATERIAL_OPEN` | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |
| `STD-DIA-001` | `PASS` carried from Pass 1 | `PASS` carried from Pass 1 | `PASS` carried from Pass 1 | `PASS` | `PARTIAL` | `PARTIAL` | `PARTIAL` | `MATERIAL_OPEN` | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |

The new records improve the factual basis for the existing `PASS` observability conclusions but do not close the `PARTIAL` survivability/profile/reproducibility dimensions or the material evidence boundaries.

## Exact remaining evidence requests

- `STD-EPI-003`: one independently implemented collector with durable per-unit terminal classification and a preserved production run demonstrating no silent candidate loss across scheduler, process, fetch, parse, persist, and evaluate stages; minimum proof is an end-to-end bundle with stage IDs, terminal/pending reason, restart/observer boundaries, and explicit no-silent-drop reconciliation.
- `STD-CLS-001`: a versioned cross-profile state/reason taxonomy mapping with a corpus covering known, baseline, new, duplicate, irrelevant, insufficient, blocked, source-failure, and unresolved outcomes; minimum proof is a machine-readable round trip that does not collapse `UNKNOWN` or profile exclusions.
- `STD-DIA-001`: the complete raw Diagnostic ledger plus one additional independent real incident through preserved verdict, lesson, candidate invariant, conformance check, and proposal-only revision; minimum proof retains the original verdict by hash and never rewrites it.

## Next acquisition decision

Another Diagnostic acquisition pass is justified only when the raw Diagnostic ledger/lesson corpus or an independently preserved second learning-loop incident becomes available. A repeat pass over the same normalized subset would not resolve the current P0 blockers.

No support-grade change, Ratification Decision #2, conformance audit, Motherclank acquisition, or Standards Clank work was started.
