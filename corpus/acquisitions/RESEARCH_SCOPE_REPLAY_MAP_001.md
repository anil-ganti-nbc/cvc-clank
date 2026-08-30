# Research Scope & Replay Evidence Map

**Acquisition:** `CVC-RESEARCH-SCOPE-REPLAY-001`  
**Purpose:** operator navigation and traceability only. This map is derived from preserved evidence and is not an independent evidence source.

## Operator objective → stage → lead → disposition → result → replay

| Operator/research objective | Search stage or source lane | Lead / observation | Admission or rejection | Bounded result | Replayability |
|---|---|---|---|---|---|
| Establish whether Notebookcheck covers Google Pixel 9 | Story M0.6 exact → relaxed → official → claim-specific → source-class → fallback → Notebookcheck | Search leads and category-only Google Store records were retained as leads; no direct NBC target hit | Category-only records were not evidence; no target-bound hit admitted | `NOT_FOUND_WITHIN_SEARCH_BUDGET`; 15 diagnostics; 0 coverage hits | `REPRODUCIBLE` offline from preserved investigation JSON |
| Test whether Samsung Galaxy S25 has direct NBC coverage | Story M0.6 exact/relaxed/official/comparison/claim/source/fallback/NBC | NBC leads included S26 FE and a S25 specs-leak article | Preserved output wrongly classified both as `PREDECESSOR`; no direct target hit | Structured `FOUND` state is unsafe; relation precision failure remains visible | `PARTIALLY_REPRODUCIBLE` from raw diagnostics/result records |
| Test staged, alias-aware search behavior | Story M0.6 alias/family/region/claim-specific stages | S25 and Xiaomi runs expose relaxed, alias/family, official-domain, and claim-specific purposes | Stage/task links are recorded; admission remains subject to target binding | Staged search is observable but not sufficient to prove recall or correctness | Local regression batch `5 passed`; selected plans replayable |
| Separate discovery from admitted evidence | Story source-class and evidence normalization | Search result pointers, snippets, category pages, and leads exist beside evidence items | Discovery-only, blocked, and non-target relations must not support target facts | Mechanics pass in local tests; wrong NBC relation proves the boundary is not fully safe | `REPRODUCIBLE` for selected executable tests |
| Benchmark lead vs admitted-evidence recall | OEM BANKAI-I recall path | 50 qualifying stories, recorded 0/50 recall; body/denominator incomplete | Cannot audit every lead’s fetch/admissibility/provenance/target binding | Bounded historical recall failure; E4 benchmark missing | `NOT_REPRODUCIBLE` without raw BANKAI body |
| Isolate official PSREF discovery from event evidence | OEM BANKAI-II PSREF | 1,545 official items; four review-only pass-1, zero pass-2 normal events/notifications | Review-only candidates remain distinct from normal event candidates | Baseline/review-only separation is visible | `NOT_REPRODUCIBLE` without full source artifacts |
| Test regional source coverage | OEM BANKAI-II regional path | 6,349 filtered URLs; no deltas/fetches/candidates | Regional/baseline isolation preserved | Result is bounded baseline-only / region coverage evidence, not broad absence | `NOT_REPRODUCIBLE` from summary alone |
| Test replay and gap accounting | OEM BANKAI-II replay | 0/50 initial; `region_gap=25`, `source_gap=19`, `schedule_latency=6`; later 238 alerts → 25 delivered + 63 review queue | Gaps and queue states retained instead of silently becoming no-hit | Bounded incomplete run; complete denominator and per-lead records absent | `NOT_REPRODUCIBLE` from unavailable raw replay bundle |
| Test bounded negative under provider failure | KTW source lane | Home/feed/robots/sitemap/API surfaces returned 403; residential path succeeded | `HOST-BLOCKED`/backoff recorded; not treated as universal absence | Provider/source failure is explicit and scope-bound | `PARTIALLY_REPRODUCIBLE` from preserved normalized outcome |
| Test source-universe declaration | Watch source matrix / region gap map / inventory | Official/news/specialist layers, authority tiers, freshness, permissions, explicit Citizen UK omission | Sources and gaps are declared, but raw versioned manifest is unavailable | `PARTIALLY_DECLARED`; common contract missing | `PARTIALLY_REPRODUCIBLE` |
| Test source-universe declaration | OEM descriptors and configured source path | Enabled sources/engines, cadence, manufacturer scope | Region/tier/exclusion/discovery-only fields not fully declared | `PARTIALLY_DECLARED`; common contract missing | `PARTIALLY_REPRODUCIBLE` |
| Test bounded negative/failure semantics | Diagnostic-linked BANKAI/Watch rows | Incomplete denominators, blocked states, and preserved unknown/gap outcomes | No inference from missing rows; failure remains bounded | Supports boundary discipline, not E4 completeness | `PARTIALLY_REPRODUCIBLE` |

## Stage vocabulary observed

The Story raw artifacts expose the following stages where applicable:

`STAGE_1_EXACT_IDENTITY` → `STAGE_2_RELAXED_IDENTITY` → `STAGE_3_OFFICIAL_DISCOVERY` → comparison/family and predecessor stages → `STAGE_5_CLAIM_SPECIFIC` → `STAGE_6_SOURCE_CLASS` → `STAGE_7_FALLBACK` → `STAGE_NOTEBOOKCHECK_COVERAGE`.

This is an observed implementation sequence, not a newly normative rule. OEM source-specific and regional paths use a different operational shape. That difference is one reason `STD-RES-002` and `STD-SRC-003` remain E3 pending a common replayable contract.

## Bounded result vocabulary observed

The preserved evidence distinguishes, among other states:

* `NOT_FOUND_WITHIN_SEARCH_BUDGET`
* `FOUND` with target-relation qualification
* `HOST-BLOCKED`
* `region_gap`
* `source_gap`
* `schedule_latency`
* review-only and baseline-suppressed outcomes
* unadmitted category-only or non-target leads

These state names are retained as evidence, not normalized into a new cross-fleet taxonomy in this acquisition.

## Evidence boundary

The map does not claim that an observed lead is evidence. Every row must be read with the admission/rejection column and the source record’s role. Derived audit summaries, report-plus-summary pairs, BANKAI syntheses, and CVC normalizations are navigation aids or traceability records and do not create independent support.

## Missing proof mapped to objective

| Rule | Missing proof that blocks E4 |
|---|---|
| `STD-EPI-002` | Complete frozen BANKAI lead/admission benchmark with denominator and every lead’s fetch, admissibility, provenance, target-binding, and final status, replayable without unavailable primary artifacts. |
| `STD-NEG-001` | Complete replayable bounded-negative benchmark preserving exact scope, all stages, budget, fetch outcomes, stopping reason, admitted evidence, unresolved gaps, final wording, and independent hit audit. |
| `STD-SRC-003` | Versioned machine-readable source/region/family/exclusion manifest tied to a coverage run, with authority tiers and discovery-only permissions. |
| `STD-RES-002` | Common replayable claim-scoped search-plan corpus preserving aliases, localization, stage purpose, provider, stopping reason, admission result, and bounded gaps. |

