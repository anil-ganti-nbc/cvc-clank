# CVC Clank ecosystem integration

This document records CVC's operational identity and the small set of stable
integration references. It is documentation only: it does not start a service,
alter a scheduler, or change the frozen CVC governance state.

## Canonical identity

| Field | Value |
| --- | --- |
| Name | CVC Clank |
| Role | Cross-Clank institutional evidence memory and learning/ratification support |
| Lifecycle | `OPERATIONAL` |
| Execution model | `OPERATOR_TRIGGERED` |
| Scheduling | `NONE` |
| Primary inputs | Diagnostic reports; incident artifacts; success-pattern evidence; migration/restore evidence; operator-supplied evidence packages |
| Primary outputs | Append-only evidence records; trigger checks; review recommendations; support-grade review packages; ratification references; corpus integrity results |
| Dependencies | Local frozen CVC corpus; operator-provided evidence; optional reasoning provider, disabled by default |

CVC must not be represented as a scheduled collector, production discovery
source, remediation agent, or Standards authority.

## Registry and documentation surfaces

The authoritative ecosystem inventory is the `clank-fleet` registry in
[Diagnostic Clank](https://github.com/anil-ganti-nbc/diagnostic-clank/blob/diagnostic-clank-2026-08/clank-fleet/inventories/fleet.yaml).
It records repository truth separately from deployment truth. CVC's registry
entry therefore identifies the repository with the schema's `NOT_APPLICABLE`
deployment state; it does not claim that CVC has a host deployment or a
scheduler.

The [Clank Systems Handbook](https://github.com/anil-ganti-nbc/clank-systems-handbook)
is a secondary learning/discoverability surface. Its CVC glossary entry links
back to this repository without becoming a second fleet registry. The governance
repository, [clank-architecture](https://github.com/anil-ganti-nbc/clank-architecture),
continues to own fleet laws and promotion policy; this integration does not
change those policies.

## Open future-evidence triggers

CVC has open future-evidence triggers in
`corpus/triggers/CVC_FUTURE_EVIDENCE_TRIGGERS_V0.1.jsonl`. A Clank that produces
relevant natural success/failure evidence should follow this operator workflow:

```text
new meaningful fleet evidence
  → cvc check-triggers <artifact>
  → operator review
  → cvc review --affected (if warranted)
```

This is discoverability and a manual workflow, not automatic monitoring.

## Observer-tier relationship

The observer-tier relationship is deliberately one-way:

```text
Collectors / operators
        ↓ evidence
Diagnostic Clank
        ↓ explicit handoff package (no auto-ingest)
CVC Clank
        ↓ evidence-backed lessons and open triggers
Motherclank synthesis (read-only summary)
```

Motherclank reads CVC through the fleet adapter contract. CVC's health means
corpus readability, frozen-manifest/hash integrity, manifest consistency, and
runtime-state readability; it is not collector freshness, source count, event
count, or delivery latency. CVC has no scheduler, owns its own corpus/state,
and grants no participant or enforcement authority.

`RATIFIED_E4`, `SUPPORTED_E3`, `OPEN_TRIGGER`, `BLOCKED_EVIDENCE`, and
`HISTORICAL_EVIDENCE` remain CVC evidence classifications. Motherclank may
summarize them, but cannot turn them into fleet mandates. A future Standards
Clank could consume CVC evidence to define normative contracts; Standards
Clank remains unstarted. The planned editorial CVC Workbench is also separate
and is not a fleet member.

## Standards boundary

CVC determines what the evidence supports. A future Standards Clank may consume
CVC's evidence corpus and ratified support state. CVC itself is not Standards
Clank and does not enforce fleet compliance. Standards Clank remains **NOT
STARTED**.

## Workbench boundary

Current CVC Clank is fleet institutional memory and evidence governance. The
planned Context + Verification + Coverage Workbench is a separate tool for
post-selection editorial research. No Workbench code is included here.
