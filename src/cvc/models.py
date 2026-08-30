from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CorpusArtifact:
    source_path: str
    destination_path: str
    source_sha256: str
    destination_sha256: str
    artifact_type: str
    artifact_role: str
    authoritative_state: str
    frozen_state: str


@dataclass(frozen=True)
class RuleRecord:
    rule_id: str
    normative_level: str
    maturity: str
    applicability: str
    support_grade: str
    ratification_state: str
    strongest_evidence: str = ""
    remaining_blocker: str = ""


@dataclass(frozen=True)
class EvidenceReference:
    evidence_id: str
    source_system: str
    artifact: str
    incident_or_pattern: str
    date: str
    historical_verdict: str
    lesson: str
    affected_rule_ids: tuple[str, ...]
    support_direction: str
    support_strength: str
    evidence_role: str
    provenance: str
    supersession_state: str
    notes: str = ""


@dataclass(frozen=True)
class FutureEvidenceTrigger:
    trigger_id: str
    trigger_class: str
    rule_ids: tuple[str, ...]
    trigger_condition: str
    required_artifact: str
    minimum_sufficient_proof: str
    current_status: str


@dataclass
class IngestionRecord:
    ingestion_id: str
    input_path: str
    preserved_path: str
    input_sha256: str
    classification: str
    outcomes: list[str]
    affected_rule_ids: list[str]
    trigger_ids: list[str]
    support_grade_change_applied: bool
    historical_verdict_changed: bool
    created_at: str
    notes: list[str] = field(default_factory=list)


@dataclass
class TriggerCheck:
    check_id: str
    input_path: str
    input_sha256: str
    matched_trigger_ids: list[str]
    dispositions: list[dict[str, Any]]
    support_grade_change_applied: bool
    created_at: str


@dataclass
class ReviewRecord:
    review_id: str
    affected_rule_ids: list[str]
    source_record_ids: list[str]
    recommendations: list[dict[str, Any]]
    ratification_created: bool
    support_grade_changed: bool
    created_at: str


@dataclass(frozen=True)
class RatificationReference:
    ratification_id: str
    decision: str
    source_path: str


@dataclass
class CorpusIntegrityResult:
    passed: bool
    checks: list[dict[str, Any]] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "checks": self.checks,
            "failures": self.failures,
            "warnings": self.warnings,
        }
