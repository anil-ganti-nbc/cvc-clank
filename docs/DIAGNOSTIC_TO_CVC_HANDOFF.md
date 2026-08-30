# Diagnostic → CVC handoff

Diagnostic Clank may produce an evidence package suitable for explicit operator
ingestion into CVC. The boundary is:

```text
Diagnostic Clank: What failed and why?
CVC:             What does this teach the fleet?
```

The handoff is proposal/evidence input, not an automatic ingestion channel.
Diagnostic must not push every incident to CVC, and CVC must not infer a lesson
from a report that the operator has not deliberately supplied.

## Operator workflow

1. Diagnostic preserves the incident or success report and its provenance.
2. The operator reviews whether the report is appropriate CVC evidence.
3. The operator creates an explicit package with `diagnostic-clank handoff create`.
4. The operator reviews the package and, separately, runs `cvc ingest <artifact>`.
5. The operator may run `cvc check-triggers <artifact>` and, if warranted,
   `cvc review --affected`.

No scheduler, daemon, webhook, or cross-repository push is implied by this
contract. Existing historical verdicts, rule maturity, support grades, and
ratification state remain unchanged unless a separately justified governance
action is taken later.

## Minimum handoff fields

The machine-readable shape is
[`diagnostic-to-cvc-handoff.schema.json`](diagnostic-to-cvc-handoff.schema.json).
The minimum conceptual fields are:

| Field | Meaning |
| --- | --- |
| `source_clank` | Producing Clank identifier |
| `incident_id` | Stable source incident identifier |
| `incident_date` | Date of the historical incident |
| `historical_verdict` | Diagnostic's preserved verdict; do not rewrite it in CVC |
| `report_artifact_reference` | Stable report or artifact reference |
| `affected_components` | Components or Clanks affected |
| `root_cause` | Root cause, when supported by the source report |
| `first_failed_gate` | Earliest failed gate identified by Diagnostic |
| `remediation_evidence` | Evidence of remediation, if available; absence stays explicit |
| `candidate_lesson` | Proposed fleet-level lesson for CVC review |
| `provenance` | Source repository/revision and artifact hash |

The artifact hash supports replay and prevents a later mutable report from being
mistaken for the historical input. A handoff package never grants permission to
ingest itself; operator approval is a separate action. Positive evidence follows
the same path: a successful restore, migration, restart-survivability replay,
independent implementation, bounded replay, or durable-delivery result may be
packaged with an explicit success verdict. CVC is not incident-only.
