"""Contracts shared by the future MCP adapters, rules, agent, and API routes."""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class EvidenceKind(StrEnum):
    DAILIES = "dailies"
    FACT = "fact"
    CALL_SHEET = "call_sheet"


class RevisionRequest(BaseModel):
    scene_id: str
    fact_type: str
    old_value: str
    new_value: str

    @model_validator(mode="after")
    def is_supported_demo_revision(self) -> "RevisionRequest":
        if (self.scene_id, self.fact_type, self.old_value, self.new_value) != (
            "scene-12",
            "wardrobe",
            "blue jacket",
            "black jacket",
        ):
            raise ValueError("Only the prepared Scene 12 wardrobe revision is supported.")
        return self


class FollowupRequest(BaseModel):
    """Explicit human acknowledgement required before a durable follow-up."""

    reviewed_evidence: Literal[True]


class EvidenceRecord(BaseModel):
    evidence_id: str
    scene_id: str
    kind: EvidenceKind
    wardrobe_value: str | None = None
    shoot_status: str | None = None
    excerpt: str


class DependencyRecord(BaseModel):
    dependency_id: str
    source_scene_id: str
    target_scene_id: str
    shoot_date: date
    status: str
    evidence_id: str


class ImpactPulse(BaseModel):
    """A bounded, reader-derived summary of the active production window."""

    scope: str
    relevant_evidence_records: int = Field(ge=0)
    active_scene_records: int = Field(ge=0)
    affected_scenes: int = Field(ge=0)
    scheduled_dependencies: int = Field(ge=0)


class FindingType(StrEnum):
    CONTINUITY_CONFLICT = "continuity_conflict"
    SCHEDULE_DEPENDENCY = "schedule_dependency"


class ReadinessState(StrEnum):
    AT_RISK = "At risk"
    REVIEW_REQUIRED = "Review required"


class RuleFinding(BaseModel):
    finding_type: FindingType
    evidence_ids: tuple[str, ...]
    affected_scene_ids: tuple[str, ...]


class RuleEvaluation(BaseModel):
    readiness: ReadinessState
    findings: tuple[RuleFinding, ...] = ()
    review_evidence_ids: tuple[str, ...] = ()
    can_create_followup: bool
    reason: str = Field(min_length=1)
