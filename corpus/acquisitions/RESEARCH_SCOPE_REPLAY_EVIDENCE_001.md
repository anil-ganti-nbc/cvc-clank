# CVC Targeted Evidence Acquisition #3

## Research scope and replay — acquisition report

**Acquisition ID:** `CVC-RESEARCH-SCOPE-REPLAY-001`  
**Review date:** 2026-08-30  
**Status:** `CLOSED / RETAIN_E3_NO_GRADE_CHANGE`

## Executive result

This pass audited only `STD-EPI-002`, `STD-NEG-001`, `STD-SRC-003`, and `STD-RES-002`, using the frozen fleet corpus and directly linked workspace artifacts. No external provider was contacted, no new source was fetched, no support grade was changed, and no Ratification Decision #2 was created.

The corpus demonstrates useful separation between discovery leads and admitted evidence, bounded negative states, partial source-universe declarations, and staged claim-specific search behavior. It does not provide the complete replayable benchmarks required by the frozen E3 wishlist. In particular, the BANKAI denominator/body, a complete bounded-negative benchmark with independent hit audit, a common versioned source/region manifest, and a common claim-scoped search-plan corpus remain unavailable.

**Recommendation for all four rules:** `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE`.

## Run and corpus boundary

The acquisition was offline and additive. It used preserved Story M0–M0.6 artifacts, the frozen Watch and OEM audits, the frozen fleet evidence register, KTW host-block evidence, Diagnostic records already present in the register, the E4 contract, and the previously frozen packages. No new source contact occurred.

The raw external BANKAI, Watch, KTW, and linked Diagnostic source artifacts named by historical records are not all available in this workspace. The accessible material includes normalized rows, frozen reports, selected raw Story investigation artifacts, source hashes, and executable tests. Missing incidents, denominators, query outcomes, source rows, timestamps, supersession state, and coverage not present in those artifacts were not inferred.

Evidence roles are kept distinct:

| Role | Count | Treatment |
|---|---:|---|
| `PRIMARY` | 11 | Preserved implementation, run, incident, or source behavior |
| `DERIVED` | 3 | Navigation or audit synthesis; not independent evidence |
| `EXECUTABLE_CONFORMANCE` | 3 | Preserved replay or local regression result |
| `MISSING_EXPECTED_EVIDENCE` | 4 | Explicit record of a frozen blocker, not positive support |
| **Total** | **21** | Additive register only |

No prior evidence register or frozen artifact was edited.

## Lead versus evidence

The evidence boundary is present in more than one profile, but it is not yet safe enough for E4.

* Story M0.6 records staged leads, fetch/admission fields, target relation, source class, and task state. Pixel category-only Google Store results remain visible as non-evidence rather than facts.
* Story S25 preserves a failure in which Notebookcheck results were admitted with the wrong `PREDECESSOR` relation and no direct target hit. This is evidence that lead visibility alone does not guarantee safe target binding.
* OEM BANKAI-I records a 0/50 recall result with an incomplete body/denominator; OEM BANKAI-II preserves PSREF review-only candidates and regional/baseline isolation, but the complete lead-level benchmark is absent.
* The local regression `test_search_leads_and_blocked_pages_never_become_evidence` and related M0.1/M0.2 tests provide executable separation mechanics, not a cross-fleet recall benchmark.

The positive boundary is therefore reproducible in selected fixtures, while the negative evidence boundary and target-binding precision remain materially open.

## Bounded-negative findings

The preserved corpus shows the intended discipline:

* Pixel replay returns `NOT_FOUND_WITHIN_SEARCH_BUDGET` with 15 diagnostics, required stages, explicit provider/result fields, zero coverage hits, and negative diagnostics equal to the recorded coverage diagnostics.
* KTW preserves a host-block outcome across home/feed/robots/sitemap/API surfaces, with backoff and a residential-success distinction; this is a source failure, not a universal absence claim.
* OEM BANKAI-I and BANKAI-II preserve bounded zero/coverage-gap states, including incomplete denominators and `region_gap`, `source_gap`, and `schedule_latency` reasons.
* The local negative-conclusion regression passes and preserves diagnostics with the bounded state.

These are useful bounded states, but the frozen E3 requirement asks for one complete replayable negative benchmark containing exact scope, all stages, budget, fetch outcomes, stopping reason, admitted evidence, unresolved gaps, and an independent hit audit. That complete benchmark is not available. The S25 Notebookcheck relation failure further prevents treating a bounded result as safe merely because it is structured.

## Declared source universe

The source-universe contract is only partially portable and only partially machine-readable.

| System/profile | Assessment | Evidence |
|---|---|---|
| Watch | `PARTIALLY_DECLARED` | Source matrix, regional gap map, source inventory, authority tiers, freshness/permissions, and explicit omissions exist; raw versioned manifest and replayable coverage run are unavailable. |
| OEM Radar | `PARTIALLY_DECLARED` | Descriptors identify enabled sources/engines, cadence, and manufacturer scope; versioned region universe, tiers, exclusions, and discovery-only permissions are missing. |
| Story | `PARTIALLY_DECLARED` | Per-run region, source class, and search stages are observable; a durable declared source-universe manifest is absent. |
| KTW | `IMPLICIT`/`PARTIALLY_DECLARED` | Host/source block surfaces and migration/source behavior are preserved, not a complete research source contract. |

Across these systems there is no common primary manifest that enumerates every in-scope and excluded source, product/family category, region rationale, authority tier, discovery-only permission, effective version, and resulting gap. `STD-SRC-003` therefore remains E3.

## Staged, claim-specific search

Story M0.6 provides the clearest preserved staged plan: exact identity, relaxed identity, official discovery, comparison, claim-specific, source-class, fallback, and Notebookcheck coverage stages. The raw diagnostics retain purposes, queries, result counts, timestamps, regions, aliases/family intent where used, and a bounded stopping state. The S25 record demonstrates that a staged plan can still produce an unsafe relation classification.

OEM PSREF and regional runs demonstrate source isolation, review-only handling, baseline suppression, and bounded zero-result reasons. The local five-test regression batch passes the staged-search/task-link and bounded-negative checks. These are materially useful examples but not a common replayable plan schema across independent implementations. The required corpus preserving aliases, localized terms, provider, stopping reason, admission result, and bounded gaps is missing.

Staged query volume is consequently not treated as a proxy for recall, source coverage, or target-binding correctness.

## Replay results

| Replay | Status | Result |
|---|---|---|
| Story Pixel offline replay | `REPRODUCIBLE` | Same `NOT_FOUND_WITHIN_SEARCH_BUDGET`, 15 diagnostics, required stages, zero hits, and equal negative diagnostics; no providers contacted. |
| Local research regression batch | `REPRODUCIBLE` | Five selected M0.1/M0.2 tests passed; no providers contacted. |
| Story S25 preserved staged plan | `PARTIALLY_REPRODUCIBLE` | Raw diagnostics and stages are present, but the preserved result contains a wrong Notebookcheck relation and is not a clean positive benchmark. |
| OEM BANKAI-I/II | `NOT_REPRODUCIBLE` | Historical rows and hashes exist; the complete raw denominator/body and source artifacts are unavailable. |
| Watch source matrix / Hall of Shame | `PARTIALLY_REPRODUCIBLE` | Frozen summaries and source declarations exist; raw complete hit list and source-universe replay are unavailable. |
| KTW host-block | `PARTIALLY_REPRODUCIBLE` | Preserved outcomes and diagnostics exist; the complete source-universe/research replay does not. |

Replayability is therefore demonstrated for selected local artifacts, not for the minimum E4 benchmark for any of the four rules.

## Rule-by-rule E4 review

The review uses the frozen E4 contract without reinterpretation. The dimensions below are assessed against the available evidence; `PARTIAL` means the dimension is not fully established, not that the underlying behavior is absent.

| Rule | Breadth | Independence | Failure/success | Observability | Reproducibility | Profile stability | Evidence boundary | Recommendation |
|---|---|---|---|---|---|---|---|---|
| `STD-EPI-002` | PASS | PASS | PASS | PASS | PARTIAL | PARTIAL | MATERIAL_OPEN | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |
| `STD-NEG-001` | PASS | PASS | PASS | PASS | PARTIAL | PARTIAL | MATERIAL_OPEN | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |
| `STD-SRC-003` | PASS | PASS | PASS | PASS | PARTIAL | PARTIAL | MATERIAL_OPEN | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |
| `STD-RES-002` | PASS | PASS | PASS | PARTIAL | PARTIAL | PARTIAL | MATERIAL_OPEN | `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE` |

The systems represented are Story, Watch, OEM Radar/BANKAI, KTW, and Diagnostic-linked evidence as applicable. Report-plus-summary pairs, BANKAI synthesis plus BANKAI rows, Watch incident plus handbook, and Diagnostic incident plus CVC normalization are not multiplied as independent systems. The shared-ancestry caveat remains recorded in each normalized evidence record.

### `STD-EPI-002` — discovery is not evidence

Positive separation is visible in Story’s lead/evidence fields, official/source-class stages, category-only records, OEM review-only PSREF handling, and executable regression coverage. Failure evidence includes the incomplete BANKAI recall denominator and the S25 wrong Notebookcheck relation. The exact frozen blocker remains:

> A complete, replayable lead-versus-admitted-evidence benchmark including the BANKAI denominator, source scope, fetch/admissibility outcomes, and final task state.

Minimum sufficient proof remains:

> One frozen benchmark in which every lead has fetch, admissibility, provenance, target-binding, and final-status fields and the run can be replayed without unavailable primary artifacts.

### `STD-NEG-001` — bounded negative

Pixel, KTW, OEM, and local regression artifacts preserve bounded states and diagnostics. The available negative examples have incomplete denominators, incomplete independent hit audits, or unavailable raw bodies. The exact frozen blocker remains:

> A complete bounded-negative research case with exact scope, query stages, budget, fetch outcomes, stopping reason, and an independent hit audit.

Minimum sufficient proof remains:

> One replayable negative benchmark whose scope, budget, all attempted stages, admitted evidence, unresolved gaps, and final bounded-negative wording are preserved together.

### `STD-SRC-003` — declared source universe

Watch and OEM provide useful partial declarations; Story supplies per-run source/search fields; KTW supplies source/block behavior. No common versioned source/region/family/exclusion manifest tied to a replayable run is present. The exact frozen blocker remains:

> A machine-readable source, region, family, and exclusion manifest tied to a replayable source-coverage run and explicit discovery-only permissions.

Minimum sufficient proof remains:

> A versioned manifest plus one run that records every in-scope and excluded source, region/category rationale, discovery-only limitation, and resulting coverage gap.

### `STD-RES-002` — staged claim-specific search

Story supplies the strongest observable staged search plan and local replay; OEM supplies bounded source-specific discovery behavior. The cross-system plan corpus and safe admission/relation outcome accounting are missing. The exact frozen blocker remains:

> A replayable claim-scoped search-plan corpus recording aliases, localized terms, stage purpose, provider, stopping reason, admission result, and bounded gaps.

Minimum sufficient proof remains:

> One plan and replay pair that produces the same stage/status accounting, preserves aliases and localization, and distinguishes no-hit, blocked, unadmitted, and unresolved outcomes.

## Acquisition conclusion

All four recommendations are `RETAIN_E3_NEEDS_SPECIFIC_EVIDENCE`. No support-grade overlay is prepared or applied. A further pass is justified only when one or more exact missing primary artifacts becomes available; repeating the same normalized subset would not resolve the blockers.

**Ratification Decision #2:** not justified. No rule reached a clean E4 recommendation, so no ratification package should be created.

## Integrity and stop conditions

The pre-write and post-write validation must confirm that the baseline, frozen patient audits, fleet register, E4 contract, Ratification #1 package, support matrices V0.1/V0.2, Diagnostic Acquisition #1, Motherclank Acquisition #2, and M0.6 artifacts remain byte-identical. The new artifacts are additive only.

No support-grade change, rule-text change, maturity change, applicability change, remediation, event/delivery acquisition, conformance audit, Standards Clank work, or evidence acquisition outside the four scoped rules was performed.

